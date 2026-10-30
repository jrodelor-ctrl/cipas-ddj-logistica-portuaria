# CIPAS DDJ — Analítica Logística Portuaria

Proyecto modular en Python para **Visual Studio Code**. Datos académicos simulados; no son estadísticas oficiales del Puerto de Cartagena.

## Estructura del proyecto

- `app.py`: punto de entrada Streamlit; une todos los módulos.
- `modulos/config.py`: rutas y configuración.
- `modulos/etl.py`: limpieza y auditoría de datos con Pandas.
- `modulos/indicadores.py`: cálculos de KPIs.
- `modulos/graficos.py`: gráficas con Plotly.
- `data/datos_puerto.csv`: datos suministrados.
- `assets/logo.png`: logotipo CIPAS DDJ.
- `diagramas/`: diagramas PNG, SVG y DOT con marca institucional.
- `tests/`: pruebas automáticas.
- `.vscode/`: configuración y extensiones sugeridas.

## Cómo ejecutar en VS Code (Windows/PowerShell)

1. Descomprimir el ZIP y abrir **la carpeta CIPAS_DDJ_Puerto** desde VS Code (Archivo → Abrir carpeta).
2. Instalar la extensión **Python** de Microsoft; Pylance y Python Debugger pueden instalarse automáticamente. Extensiones adicionales recomendadas: Ruff; Jupyter es opcional.
3. Abrir Terminal → Nueva terminal. Ejecutar:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

4. Abrir la URL local indicada por Streamlit (generalmente http://localhost:8501).
5. Para pruebas: `.\.venv\Scripts\python.exe -m pytest -q`.

Si `py` no existe, comprobar la instalación de Python con `python --version` y sustituir `py` por `python`.

## Criterios de cálculo y limitaciones

- Espera: diferencia entre hora de atraque y llegada, excluyendo fechas inválidas.
- Permanencia: tiempo en muelle positivo.
- Productividad aproximada de contenedores: suma de TEUs dividida entre horas válidas para contenedores; no equivale a tasa real de operación de grúas.
- Alerta: tiempo de espera superior a umbral configurable; valor inicial 3 h con fines académicos.
- **No es posible calcular ocupación física real**: el archivo carece de ID de muelle y capacidad/ventanas de disponibilidad. No inventar datos.
- Los registros incompletos se conservan y se omiten solo de cálculos afectados; auditoría disponible en el tablero.
- Las correlaciones entre clima y demoras no establecen causalidad.

## Publicación y traducción

Consulte `DESPLIEGUE.md` para publicar en Streamlit Community Cloud. Los rótulos creados por la aplicación están en español; elementos nativos de Streamlit pueden depender de idioma/versión.
