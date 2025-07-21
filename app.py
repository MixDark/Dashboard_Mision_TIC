import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
import os
import requests
from io import StringIO

FILE_ID = "1sEcYdeZ5f3JlQwIfn2JtXuD_VaaEiD-7"

def load_csv_from_drive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text))

try:
    df = load_csv_from_drive(FILE_ID)
    df['FECHA_CORTE'] = pd.to_datetime(df['FECHA_CORTE'])
except Exception as e:
    print(f"Error al cargar el CSV: {e}")
    df = pd.DataFrame()

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Dashboard Ejecutivo - Misión TIC 2020"
server = app.server

colors = {
    'background': '#1E1E1E',
    'card_bg': '#2A2A2A',
    'header_bg': '#121212',
    'text': '#FFFFFF',
    'accent': '#007BFF',
    'accent2': '#17a2b8',
    'accent3': '#dc3545',
    'accent4': '#28a745',
    'chart_bg': '#2E2E2E',
    'grid': '#333333'
}

custom_styles = {
    'header': {
        'background-color': colors['header_bg'],
        'color': colors['text'],
        'padding': '2rem 1rem',
        'margin-bottom': '1.5rem',
        'border-radius': '0.3rem',
        'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
    },
    'card': {
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
        'margin-bottom': '20px',
        'border-radius': '0.5rem',
        'background-color': colors['card_bg'],
        'border': 'none'
    },
    'card-header': {
        'background-color': 'rgba(0, 0, 0, 0.2)',
        'border-bottom': '1px solid #444',
        'font-weight': 'bold',
        'color': colors['text']
    },
    'dropdown-container': {
        'padding': '15px',
        'background-color': 'rgba(0, 0, 0, 0.2)',
        'border-radius': '0.5rem',
        'margin-bottom': '20px'
    },
    'page': {
        'background-color': colors['background'],
        'min-height': '100vh',
        'padding': '20px 0'
    } 
}

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Dashboard Misión TIC 2020", className="display-4"),
                    html.P("Análisis estratégico de los programadores", className="lead")
                ], style=custom_styles['header'], className="text-center")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filtros de datos"),
                    dbc.CardBody([
                        html.Label("Selecciona un departamento:", className="form-label fw-bold"),
                        dcc.Dropdown(
                            id='departamento-dropdown',
                            options=[{'label': d, 'value': d} for d in sorted(df['DEPARTAME_NOMBRE'].unique())],
                            value='ANTIOQUIA',
                            clearable=False
                        )
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Resumen del departamento"),
                    dbc.CardBody([
                        html.Div(id='resumen-datos', className="d-flex justify-content-around flex-wrap")
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=9)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Estado de formación"),
                    dbc.CardBody([
                        dcc.Graph(id='estado-formacion-bar')
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución por ruta y género"),
                    dbc.CardBody([
                        dcc.Graph(id='genero-ruta-bar')
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=6),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Edad promedio por estrato social"),
                    dbc.CardBody([
                        dcc.Graph(id='edad-estrato-bar')
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Evolución temporal de registros"),
                    dbc.CardBody([
                        dcc.Graph(id='evolucion-temporal-line')
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=6),
        ]),
        dbc.Row([
            dbc.Col([
                html.Footer([
                    html.P("Creado por Duvan Esteban Metaute Garcia", className="text-center text-muted")
                ], className="py-3 mt-4 border-top")
            ])
        ])
    ], fluid=True)
], style=custom_styles['page'])

@app.callback(
    Output('resumen-datos', 'children'),
    Output('estado-formacion-bar', 'figure'),
    Output('genero-ruta-bar', 'figure'),
    Output('edad-estrato-bar', 'figure'),
    Output('evolucion-temporal-line', 'figure'),
    Input('departamento-dropdown', 'value')
)
def update_graphs(departamento):
    dff = df[df['DEPARTAME_NOMBRE'] == departamento].copy()
    dff['ESTRATO_SOCIAL'] = pd.to_numeric(dff['ESTRATO_SOCIAL'], errors='coerce')
    dff['ESTADO_FORMACION'] = dff['ESTADO_FORMACION'].str.strip().str.upper()
    dff = dff[dff['EDAD'] > 0]
    dff_unique = dff.drop_duplicates(subset=["DEPARTAME_NOMBRE", "MUNICIPIO_NOMBRE", "GENERO", "EDAD", "RUTA", "ESTADO_FORMACION"])

    total_aspirantes = len(dff_unique)
    total_hombres = len(dff_unique[dff_unique['GENERO'] == 'MASCULINO'])
    total_mujeres = len(dff_unique[dff_unique['GENERO'] == 'FEMENINO'])
    total_no_registra = len(dff_unique[~dff_unique['GENERO'].isin(['MASCULINO', 'FEMENINO'])])
    edad_promedio = round(dff_unique['EDAD'].mean(), 1)

    card_style = {
        'background-color': 'rgba(0, 0, 0, 0.2)',
        'border': '1px solid #444',
        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.2)'
    }

    resumen_cards = [
        dbc.Card([dbc.CardBody([html.H4(f"{total_aspirantes:,}", className="card-title text-center", style={'color': colors['accent']}), html.P("Total Aspirantes", className="card-text text-center")])], className="m-2", style={**card_style}),
        dbc.Card([dbc.CardBody([html.H4(f"{total_hombres:,}", className="card-title text-center", style={'color': colors['accent2']}), html.P("Hombres", className="card-text text-center")])], className="m-2", style={**card_style}),
        dbc.Card([dbc.CardBody([html.H4(f"{total_mujeres:,}", className="card-title text-center", style={'color': colors['accent3']}), html.P("Mujeres", className="card-text text-center")])], className="m-2", style={**card_style}),
        dbc.Card([dbc.CardBody([html.H4(f"{total_no_registra:,}", className="card-title text-center", style={'color': "#ffc107"}), html.P("No Registra", className="card-text text-center")])], className="m-2", style={**card_style}),
        dbc.Card([dbc.CardBody([html.H4(f"{edad_promedio}", className="card-title text-center", style={'color': colors['accent4']}), html.P("Edad Promedio", className="card-text text-center")])], className="m-2", style={**card_style})
    ]

    template = "plotly_dark"
    color_seq = px.colors.qualitative.Bold
    layout = {'paper_bgcolor': colors['chart_bg'], 'plot_bgcolor': colors['chart_bg'], 'font': {'color': colors['text']}, 'margin': dict(l=20, r=20, t=30, b=20), 'height': 350, 'legend': {'font': {'color': colors['text']}}, 'xaxis': {'gridcolor': colors['grid']}, 'yaxis': {'gridcolor': colors['grid']}}

    estado_counts = dff_unique['ESTADO_FORMACION'].value_counts().reset_index()
    estado_counts.columns = ['ESTADO_FORMACION', 'count']
    fig1 = px.bar(estado_counts, x='ESTADO_FORMACION', y='count', color='ESTADO_FORMACION', template=template, color_discrete_sequence=color_seq, text='count')
    fig1.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig1.update_layout(**layout, xaxis_title="", yaxis_title="Cantidad de Aspirantes")

    ruta_genero = dff_unique.groupby(['RUTA', 'GENERO']).size().reset_index(name='count')
    fig2 = px.bar(ruta_genero, x='RUTA', y='count', color='GENERO', barmode='group', template=template, color_discrete_sequence=color_seq, text='count')
    fig2.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig2.update_layout(**layout, xaxis_title="", yaxis_title="Cantidad de Aspirantes")

    edad_prom = dff_unique.groupby('ESTRATO_SOCIAL')['EDAD'].mean().reset_index()
    fig3 = px.bar(edad_prom, x='ESTRATO_SOCIAL', y='EDAD', template=template, color_discrete_sequence=color_seq, text=np.round(edad_prom['EDAD'], 1))
    fig3.update_traces(texttemplate='%{text}', textposition='outside')
    fig3.update_layout(**layout, xaxis_title="Estrato Social", yaxis_title="Edad Promedio")

    evol = dff_unique.groupby('FECHA_CORTE').size().reset_index(name='Cantidad')
    fig4 = px.line(evol, x='FECHA_CORTE', y='Cantidad', template=template, line_shape='spline', markers=True)
    if len(evol) > 10:
        indices = np.linspace(0, len(evol)-1, 5, dtype=int)
        text = [''] * len(evol)
        for i in indices:
            text[i] = evol['Cantidad'].iloc[i]
        fig4.update_traces(text=text, textposition='top center')
    else:
        fig4.update_traces(text=evol['Cantidad'], textposition='top center')
    fig4.update_layout(**layout, xaxis_title="Fecha", yaxis_title="Cantidad de Registros")

    return resumen_cards, fig1, fig2, fig3, fig4

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
