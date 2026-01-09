# Dashboard ejecutivo - Misión TIC 2020

Dashboard interactivo construido con Dash y Plotly para visualizar y analizar datos de la iniciativa Misión TIC 2020.

## 📋 Descripción

Este proyecto es una aplicación web que presenta un dashboard ejecutivo con visualizaciones dinámicas e interactivas. La aplicación obtiene datos en tiempo real desde Google Drive y los presenta mediante gráficos y tablas interactivas con un tema oscuro moderno.

## 🎯 Características

- **Visualizaciones interactivas**: Gráficos dinámicos con Plotly y Dash
- **Tema oscuro moderno**: Interfaz elegante con Bootstrap Dark theme (CYBORG)
- **Datos en la nube**: Integración con Google Drive para cargar datos CSV
- **Diseño responsivo**: Adaptable a diferentes tamaños de pantalla
- **Componentes bootstrap**: Estilización profesional con Dash Bootstrap Components

## 🛠️ Requisitos

- Python 3.13.1
- Las dependencias listadas en `requirements.txt`

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd dashboard
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

**En Windows:**
```bash
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🚀 Uso

Para ejecutar la aplicación:

```bash
python app.py
```

Luego abre tu navegador en: `http://localhost:8080`

## 📁 Estructura del proyecto

```
dashboard/
├── app.py              # Aplicación principal Dash con servidor WSGI
├── requirements.txt    # Dependencias del proyecto
├── runtime.txt         # Versión de Python
└── README.md          # Este archivo
```

## 🔑 Configuración

El archivo `app.py` contiene un `FILE_ID` que hace referencia a un archivo CSV en Google Drive:

```python
FILE_ID = "1sEcYdeZ5f3JlQwIfn2JtXuD_VaaEiD-7"
```

Si deseas usar tus propios datos, reemplaza este ID con el de tu archivo de Google Drive.

## 🎨 Paleta de colores

El dashboard utiliza la siguiente paleta de colores:

- **Fondo principal**: `#1E1E1E` (Gris oscuro)
- **Tarjetas**: `#2A2A2A` (Gris más claro)
- **Encabezado**: `#121212` (Casi negro)
- **Texto principal**: `#FFFFFF` (Blanco)
- **Acentos**: Azul, Cyan, Rojo y Verde

## 🌐 Despliegue en producción

La aplicación incluye un servidor WSGI integrado que es compatible con servicios como Heroku, Railway, Render, AWS, Google Cloud, Azure, etc.

## 🐛 Solución de problemas

### Error al cargar datos de Google Drive
- Verifica que el `FILE_ID` sea correcto
- Asegúrate de que el archivo sea público o compartido correctamente
- Revisa tu conexión a internet

### Error de conexión
- Verifica que estés usando la dirección correcta `http://localhost:8080`
- Asegúrate de que el puerto 8080 no esté en uso por otra aplicación

## 📝 Licencia

Este proyecto es privado. Para uso público, especifica la licencia deseada.

## ✉️ Contacto

Para preguntas o sugerencias, contacta al desarrollador del proyecto.
