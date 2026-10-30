"""Configuración común y rutas de archivos."""
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
DATOS = BASE / 'data' / 'datos_puerto.csv'
LOGO = BASE / 'assets' / 'logo.png'
TITULO = 'CIPAS DDJ | Logística Portuaria'
