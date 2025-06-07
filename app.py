import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
import os

# Cargar datos
df = pd.read_csv("Mision_TIC_2020_100_mil_programadores.csv")
df['FECHA_CORTE'] = pd.to_datetime(df['FECHA_CORTE'])

# Inicializar app con Bootstrap tema oscuro
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Dashboard Ejecutivo - Misión TIC 2020"
server = app.server  

# Paleta de colores ejecutiva
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

# Estilos personalizados para tema oscuro ejecutivo
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
    'dropdown': {
        'z-index': '1000',
        'background-color': colors['card_bg']
    },
    'page': {
        'background-color': colors['background'],
        'min-height': '100vh',
        'padding': '20px 0'
    }
}

# Estilos CSS personalizados para el dropdown
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Estilos para el dropdown */
            .Select-control, .Select-menu-outer {
                background-color: #343a40 !important;
                color: white !important;
            }
            
            .Select-value-label {
                color: white !important;
            }
            
            .Select-menu-outer .VirtualizedSelectOption {
                background-color: #343a40 !important;
                color: white !important;
            }
            
            .Select-menu-outer .VirtualizedSelectFocusedOption {
                background-color: #212529 !important;
                color: white !important;
            }
            
            .Select-arrow {
                border-color: white transparent transparent !important;
            }
            
            .Select-placeholder, .Select--single > .Select-control .Select-value {
                color: white !important;
            }
            
            .is-open > .Select-control {
                background-color: #343a40 !important;
                color: white !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Layout con Bootstrap
app.layout = html.Div([
    dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Dashboard Misión TIC 2020", className="display-4"),
                    html.P("Análisis estratégico de los programadores", className="lead")
                ], style=custom_styles['header'], className="text-center")
            ], width=12)
        ]),
        
        # Filtros y Resumen en la misma fila
        dbc.Row([
            # Filtros
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filtros de datos"),
                    dbc.CardBody([
                        html.Label("Selecciona un departamento:", className="form-label fw-bold"),
                        html.Div([
                            dcc.Dropdown(
                                id='departamento-dropdown',
                                options=[{'label': d, 'value': d} for d in sorted(df['DEPARTAME_NOMBRE'].unique())],
                                value='ANTIOQUIA',
                                clearable=False
                            )
                        ], style={'position': 'relative', 'zIndex': 999})
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=3),
            
            # Resumen de datos
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Resumen del departamento"),
                    dbc.CardBody([
                        html.Div(id='resumen-datos', className="d-flex justify-content-around flex-wrap")
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=9)
        ], className="mb-4"),
        
        # Gráficos en filas y columnas responsivas
        dbc.Row([
            # Primera fila de gráficos
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Estado de formación"),
                    dbc.CardBody([
                        dcc.Graph(id='estado-formacion-bar')
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=6, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución por ruta y género"),
                    dbc.CardBody([
                        dcc.Graph(id='genero-ruta-bar')
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=6, className="mb-4"),
        ]),
        
        dbc.Row([
            # Segunda fila de gráficos
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Edad promedio por estrato social"),
                    dbc.CardBody([
                        dcc.Graph(id='edad-estrato-bar')
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=6, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Evolución temporal de registros"),
                    dbc.CardBody([
                        dcc.Graph(id='evolucion-temporal-line')
                    ])
                ], style=custom_styles['card'])
            ], md=12, lg=6, className="mb-4"),
        ]),
        
        # Footer
        dbc.Row([
            dbc.Col([
                html.Footer([
                    html.P("Creado por Duvan Esteban Metaute Garcia", 
                           className="text-center text-muted")
                ], className="py-3 mt-4 border-top")
            ], width=12)
        ])
    ], fluid=True, className="px-4")
], style=custom_styles['page'])

# Callbacks actualizados
@app.callback(
    Output('resumen-datos', 'children'),
    Output('estado-formacion-bar', 'figure'),
    Output('genero-ruta-bar', 'figure'),
    Output('edad-estrato-bar', 'figure'),
    Output('evolucion-temporal-line', 'figure'),
    Input('departamento-dropdown', 'value')
)
def update_graphs(departamento):
    dff = df[df['DEPARTAME_NOMBRE'] == departamento]
    
    # Crear tarjetas de resumen
    total_aspirantes = len(dff)
    total_hombres = len(dff[dff['GENERO'] == 'MASCULINO'])
    total_mujeres = len(dff[dff['GENERO'] == 'FEMENINO'])
    edad_promedio = round(dff['EDAD'].mean(), 1)
    
    card_style = {
        'background-color': 'rgba(0, 0, 0, 0.2)',
        'border': '1px solid #444',
        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.2)'
    }
    
    resumen_cards = [
        dbc.Card([
            dbc.CardBody([
                html.H4(f"{total_aspirantes:,}", className="card-title text-center", style={'color': colors['accent']}),
                html.P("Total Aspirantes", className="card-text text-center")
            ])
        ], className="m-2", style={**card_style, "min-width": "150px"}),
        
        dbc.Card([
            dbc.CardBody([
                html.H4(f"{total_hombres:,}", className="card-title text-center", style={'color': colors['accent2']}),
                html.P("Hombres", className="card-text text-center")
            ])
        ], className="m-2", style={**card_style, "min-width": "150px"}),
        
        dbc.Card([
            dbc.CardBody([
                html.H4(f"{total_mujeres:,}", className="card-title text-center", style={'color': colors['accent3']}),
                html.P("Mujeres", className="card-text text-center")
            ])
        ], className="m-2", style={**card_style, "min-width": "150px"}),
        
        dbc.Card([
            dbc.CardBody([
                html.H4(f"{edad_promedio}", className="card-title text-center", style={'color': colors['accent4']}),
                html.P("Edad Promedio", className="card-text text-center")
            ])
        ], className="m-2", style={**card_style, "min-width": "150px"}),
    ]
    
    # Tema y colores para gráficas en modo oscuro
    template = "plotly_dark"
    color_discrete_sequence = px.colors.qualitative.Bold

    # Configuración común para todos los gráficos
    layout_config = {
        'paper_bgcolor': colors['chart_bg'],
        'plot_bgcolor': colors['chart_bg'],
        'font': {'color': colors['text']},
        'margin': dict(l=20, r=20, t=30, b=20),
        'height': 350,
        'legend': {'font': {'color': colors['text']}},
        'xaxis': {'gridcolor': colors['grid']},
        'yaxis': {'gridcolor': colors['grid']}
    }

    # Gráfico 1: Estado de Formación con etiquetas
    estado_counts = dff['ESTADO_FORMACION'].value_counts().reset_index()
    estado_counts.columns = ['ESTADO_FORMACION', 'count']
    
    fig1 = px.bar(estado_counts, x='ESTADO_FORMACION', y='count', 
                  color='ESTADO_FORMACION',
                  template=template, 
                  color_discrete_sequence=color_discrete_sequence,
                  text='count')
    
    fig1.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig1.update_layout(
        **layout_config,
        xaxis_title="",
        yaxis_title="Cantidad de Aspirantes"
    )

    # Gráfico 2: Distribución por Ruta y Género con etiquetas
    ruta_genero = dff.groupby(['RUTA', 'GENERO']).size().reset_index(name='count')
    
    fig2 = px.bar(ruta_genero, x='RUTA', y='count', color='GENERO',
                  barmode='group', template=template, 
                  color_discrete_sequence=color_discrete_sequence,
                  text='count')
    
    fig2.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig2.update_layout(
        **layout_config,
        xaxis_title="",
        yaxis_title="Cantidad de Aspirantes"
    )

    # Gráfico 3: Edad Promedio por Estrato Social con etiquetas
    edad_prom = dff.groupby('ESTRATO_SOCIAL')['EDAD'].mean().reset_index()
    
    fig3 = px.bar(edad_prom, x='ESTRATO_SOCIAL', y='EDAD',
                  template=template, 
                  color_discrete_sequence=color_discrete_sequence,
                  text=np.round(edad_prom['EDAD'], 1))
    
    fig3.update_traces(texttemplate='%{text}', textposition='outside')
    fig3.update_layout(
        **layout_config,
        xaxis_title="Estrato Social",
        yaxis_title="Edad Promedio"
    )

    # Gráfico 4: Evolución Temporal de Registros con etiquetas
    evol = dff.groupby('FECHA_CORTE').size().reset_index(name='Cantidad')
    
    fig4 = px.line(evol, x='FECHA_CORTE', y='Cantidad',
                   template=template, 
                   line_shape='spline',
                   markers=True)
    
    # Solo mostrar etiquetas en algunos puntos para evitar sobrecarga
    if len(evol) > 10:
        indices = np.linspace(0, len(evol)-1, 5, dtype=int)
        text = [''] * len(evol)
        for i in indices:
            text[i] = evol['Cantidad'].iloc[i]
        fig4.update_traces(text=text, textposition='top center')
    else:
        fig4.update_traces(text=evol['Cantidad'], textposition='top center')
    
    fig4.update_layout(
        **layout_config,
        xaxis_title="Fecha",
        yaxis_title="Cantidad de Registros"
    )

    return resumen_cards, fig1, fig2, fig3, fig4

# Ejecutar
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run_server(debug=False, host='0.0.0.0', port=port)