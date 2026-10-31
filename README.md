# CIPAS DDJ — Analítica Logística Portuaria

Proyecto modular en Python usando como entorno Visual Studio Code. Datos académicos simulados; no son estadísticas oficiales del Puerto de Cartagena.

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

## Criterios de cálculo y limitaciones

- Espera: diferencia entre hora de atraque y llegada, excluyendo fechas inválidas.
- Permanencia: tiempo en muelle positivo.
- Productividad aproximada de contenedores: suma de TEUs dividida entre horas válidas para contenedores; no equivale a tasa real de operación de grúas.
- Alerta: tiempo de espera superior a umbral configurable; valor inicial 3 h con fines académicos.
- **No es posible calcular ocupación física real**: el archivo carece de ID de muelle y capacidad/ventanas de disponibilidad. No inventar datos.
- Los registros incompletos se conservan y se omiten solo de cálculos afectados; auditoría disponible en el tablero.
- Las correlaciones entre clima y demoras no establecen causalidad.

## Ciencias de Datos I

- **Cipas DDJ**
- **Integrantes:**
- **Danis Daniel Barrero Romero**
- **Daniela Ramos Escudero**
- **Jaime Alberto Rodelo Ramirez**
- **V Semestre Ingenieria de Sotfware**
- **Universidad de Cartagena**
- **Centro Tutorial El Carmen de Bolivar**
- **Octubre 2026**
- **Periodo 2026-2**
