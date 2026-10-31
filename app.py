
"""
CIPAS DDJ
Sistema de Análisis y Optimización Logística Portuaria

Dashboard interactivo desarrollado con Python,
Streamlit, Pandas y Plotly.

Universidad de Cartagena
"""

import pandas as pd
import streamlit as st

from modulos.config import DATOS, LOGO, TITULO
from modulos.etl import limpiar_datos
from modulos.graficos import (
    esperas_por_carga,
    esperas_por_clima,
    llegadas_diarias,
    llegadas_por_hora,
)
from modulos.indicadores import indicadores


# =========================================================
# 1. CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title=TITULO,
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. DISEÑO VISUAL
# =========================================================

CSS = """
<style>

:root {
    --azul-oscuro: #153650;
    --azul-medio: #276079;
    --turquesa: #198083;
    --dorado: #d7a446;
    --texto: #1c354a;
    --fondo: #f4f7fa;
}

/* FONDO PRINCIPAL */

.stApp {
    background: #f4f7fa;
    color: #1c354a;
}

[data-testid="stAppViewContainer"] {
    background: #f4f7fa;
}

.block-container {
    max-width: 1480px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* BARRA LATERAL */

[data-testid="stSidebar"] {
    background: #eaf3f5 !important;
    border-right: 1px solid #cedfe5;
}

[data-testid="stSidebarContent"] {
    background: #eaf3f5 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #153650 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #c2d8df;
}

/* CUADROS DE SELECCIÓN */

[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #ffffff;
    border-radius: 10px;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #ffffff;
    border-radius: 10px;
}

/* ETIQUETAS SELECCIONADAS */

[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #176d86 !important;
    border-radius: 6px;
}

[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #ffffff !important;
}

/* CAMPO NUMÉRICO */

[data-testid="stSidebar"] input {
    background: #ffffff !important;
    color: #18364c !important;
    border-radius: 8px;
}

/* CARGA DE ARCHIVOS */

[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #ffffff;
    border: 1px solid #b5d1d9;
    border-radius: 14px;
    padding: 10px;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background: #e6f4f3 !important;
    color: #075b61 !important;
    border: 1px solid #9cc9ca !important;
    border-radius: 9px;
}

/* ENCABEZADO */

.hero {
    border-radius: 22px;
    padding: 34px 36px;

    background: linear-gradient(
        110deg,
        #17384e 0%,
        #276079 65%,
        #198083 100%
    );

    color: #ffffff;
    position: relative;
    overflow: hidden;

    box-shadow: 0 10px 35px #15324a20;
}

.hero::after {
    content: "◌";
    position: absolute;
    right: 35px;
    top: -85px;
    font-size: 245px;
    color: #ffffff12;
    pointer-events: none;
}

.hero .eyebrow {
    color: #7be2d7;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.hero h1 {
    color: #ffffff !important;
    font-size: clamp(27px, 3vw, 42px);
    font-weight: 800;
    margin: 0 0 14px 0;
    line-height: 1.2;
}

.hero p {
    color: #deebf3 !important;
    font-size: 15px;
    line-height: 1.7;
    margin: 0;
    max-width: 850px;
}

.tagline {
    display: inline-block;
    margin-top: 20px;
    padding: 8px 12px;

    background: #ffffff20;
    border: 1px solid #ffffff30;
    border-radius: 8px;

    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
}

/* TÍTULOS DE SECCIÓN */

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #153650;
    margin-top: 25px;
    margin-bottom: 8px;
}

.section-sub {
    color: #62788b;
    font-size: 13px;
    margin-bottom: 17px;
}

/* TARJETAS KPI */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e0e9f0;
    border-radius: 16px;

    padding: 18px 16px;
    min-height: 135px;

    box-shadow: 0 4px 14px #132d4710;
}

[data-testid="stMetricLabel"] p {
    color: #536e85 !important;
    font-size: 12px;
    font-weight: 650;
}

[data-testid="stMetricValue"] {
    color: #153650 !important;
    font-size: clamp(19px, 2vw, 29px);
    font-weight: 800;
}

/* PESTAÑAS */

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 9px;
}

[data-testid="stTabs"] button[role="tab"] {
    background: #ffffff;
    border: 1px solid #e0eaf1;
    border-radius: 10px;
    padding: 10px 15px;
    color: #214d69;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    background: #146d74;
    color: #ffffff;
    border-color: #146d74;
}

/* TABLAS */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* DESCARGAS */

.stDownloadButton button {
    background: #ffffff;
    border: 1px solid #a9c9d2;
    color: #124366;
    border-radius: 11px;
    font-weight: 700;
}

.stDownloadButton button:hover {
    background: #e6f4f3;
    color: #08726e;
    border-color: #18a69c;
}

/* MENSAJES */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* PIE DE PÁGINA */

.footer {
    text-align: center;
    margin-top: 32px;
    padding: 18px;

    border-top: 1px solid #dbe5ec;

    color: #70879a;
    font-size: 12px;
}

/* DISPOSITIVOS MÓVILES */

@media (max-width: 768px) {

    .hero {
        padding: 22px;
    }

    .hero h1 {
        font-size: 27px;
    }

    .block-container {
        padding-top: 1rem;
    }

}

</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# =========================================================
# 3. FUNCIONES AUXILIARES
# =========================================================

def mostrar_numero(valor, decimales=2):
    """Convierte valores numéricos en texto legible."""

    if pd.isna(valor):
        return "N/D"

    return f"{valor:,.{decimales}f}"


def mostrar_grafico(figura, identificador):
    """Personaliza los gráficos originales de Plotly."""

    figura.update_layout(
        template="plotly_white",

        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",

        font=dict(
            family="Arial",
            color="#19344a",
            size=12,
        ),

        title=dict(
            font=dict(
                size=16,
                color="#153650",
            ),
            x=0.03,
        ),

        colorway=[
            "#198083",
            "#276079",
            "#d7a446",
            "#78a8bb",
        ],

        margin=dict(
            l=30,
            r=25,
            t=75,
            b=40,
        ),

        height=370,
    )

    figura.update_xaxes(
        showgrid=False,
        linecolor="#e5ecf3",
    )

    figura.update_yaxes(
        gridcolor="#ecf1f5",
        zeroline=False,
    )

    st.plotly_chart(
        figura,
        use_container_width=True,
        key=identificador,
        config={
            "displaylogo": False,
            "responsive": True,
        },
    )


# =========================================================
# 4. BARRA LATERAL — LOGOTIPO Y CARGA
# =========================================================

with st.sidebar:

    if LOGO.exists():
        st.image(
            str(LOGO),
            use_container_width=True,
        )

    st.markdown("### ⚓ CENTRO DE CONTROL")

    st.caption(
        "CIPAS DDJ · Analítica portuaria"
    )

    st.divider()

    st.markdown("#### ① Archivo de datos")

    st.caption(
        "El tablero utiliza inicialmente el archivo de ejemplo. "
        "Puedes cargar otro archivo CSV para realizar un nuevo análisis."
    )

    archivo = st.file_uploader(
        "Seleccionar archivo CSV",
        type=["csv"],
        help="Carga un archivo con las nueve columnas requeridas.",
    )

    with st.expander(
        "¿Qué debe contener el archivo?"
    ):

        st.markdown(
            """
El archivo CSV debe contener:

- ID de registro.
- Buque.
- Tipo de carga.
- Hora de llegada.
- Hora de atraque.
- Tiempo de espera.
- Tiempo en muelle.
- TEU registrados.
- Condición climática.
"""
        )


# =========================================================
# 5. CARGA Y PROCESAMIENTO ETL
# =========================================================

try:

    if archivo is not None:
        fuente = pd.read_csv(archivo)
    else:
        fuente = pd.read_csv(DATOS)

    completo, auditoria = limpiar_datos(fuente)

except (
    ValueError,
    OSError,
    UnicodeError,
    pd.errors.ParserError,
) as error:

    st.error(
        f"No fue posible procesar el archivo CSV: {error}"
    )

    st.stop()


# =========================================================
# 6. BARRA LATERAL — FILTROS
# =========================================================

with st.sidebar:

    if archivo is not None:

        st.success(
            "Archivo externo cargado correctamente"
        )

    else:

        st.success(
            "Utilizando los datos del proyecto"
        )

    st.divider()

    st.markdown(
        "#### ② Selecciona los filtros"
    )

    st.caption(
        "Selecciona las categorías que deseas analizar. "
        "Si conservas todas, se utilizará el conjunto completo."
    )

    tipos_disponibles = sorted(
        completo["Tipo_Carga"]
        .dropna()
        .unique()
        .tolist()
    )

    climas_disponibles = sorted(
        completo["Condicion_Climatica"]
        .dropna()
        .unique()
        .tolist()
    )

    tipos = st.multiselect(
        "Tipo de carga",
        options=tipos_disponibles,
        default=tipos_disponibles,
        placeholder="Seleccionar cargas",
    )

    climas = st.multiselect(
        "Condición climática",
        options=climas_disponibles,
        default=climas_disponibles,
        placeholder="Seleccionar climas",
    )

    umbral = st.number_input(
        "Demora crítica (horas)",
        min_value=0.5,
        max_value=48.0,
        value=3.0,
        step=0.5,
    )

    st.caption(
        "Los indicadores y gráficos se actualizan "
        "automáticamente al cambiar los filtros."
    )

    st.divider()

    st.markdown(
        "#### ③ Consulta los resultados"
    )

    st.caption(
        "Explora las pestañas del panel principal "
        "para visualizar gráficos, alertas y datos."
    )

    st.divider()

    st.caption(
        "Proyecto académico. Los registros son simulados "
        "y no constituyen estadísticas oficiales."
    )


# =========================================================
# 7. FILTRADO DE LOS REGISTROS
# =========================================================

filtrado = completo[
    completo["Tipo_Carga"].isin(tipos)
    & completo["Condicion_Climatica"].isin(climas)
].copy()

filtrado["Alerta_Critica"] = (
    filtrado["Espera_Valida_Horas"] > umbral
)

kpi = indicadores(filtrado)


# =========================================================
# 8. ENCABEZADO PRINCIPAL — CORREGIDO
# =========================================================

# El HTML se construye como una sola cadena continua.
# Esto evita que Streamlit lo interprete como código Markdown.

encabezado = (
    '<div class="hero">'
    '<div class="eyebrow">'
    'SISTEMA DE ANALÍTICA PORTUARIA · CIPAS DDJ'
    '</div>'
    '<h1>Centro de Control Logístico</h1>'
    '<p>'
    'Monitoreo de operaciones, rendimiento de contenedores, '
    'condiciones climáticas y alertas de espera en un solo lugar.'
    '</p>'
    '<span class="tagline">'
    '⚓ Puerto de Cartagena · Escenario académico simulado'
    '</span>'
    '</div>'
)

st.markdown(
    encabezado,
    unsafe_allow_html=True,
)


# =========================================================
# 9. RESUMEN DE OPERACIONES
# =========================================================

st.markdown(
    '<div class="section-title">Resumen de operaciones</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-sub">'
    'Indicadores calculados sobre los registros seleccionados.'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# 10. TARJETAS KPI
# =========================================================

c1, c2, c3, c4, c5 = st.columns(
    5,
    gap="small",
)

with c1:

    st.metric(
        label="🚢 Operaciones",
        value=kpi["operaciones"],
    )

with c2:

    st.metric(
        label="⏱ Espera media",
        value=(
            f"{mostrar_numero(kpi['tpe_horas'])} h"
        ),
    )

with c3:

    st.metric(
        label="🛳 Permanencia media",
        value=(
            f"{mostrar_numero(kpi['tiempo_muelle_medio_horas'])} h"
        ),
    )

with c4:

    st.metric(
        label="📦 Productividad (TEU/h)",
        value=mostrar_numero(
            kpi["productividad_contenedores_teu_h"],
            1,
        ),
    )

with c5:

    st.metric(
        label="⚠️ Demoras críticas",
        value=kpi["alertas"],
    )


# =========================================================
# 11. INFORMACIÓN SOBRE LOS INDICADORES
# =========================================================

st.info(
    "**Alcance de los indicadores:** "
    "la productividad TEU/h es aproximada y "
    "se calcula utilizando el volumen registrado "
    "y las horas de permanencia en muelle. "
    "Los datos disponibles no permiten calcular "
    "la ocupación física real de los muelles."
)


# =========================================================
# 12. VALIDACIÓN DE FILTROS
# =========================================================

if filtrado.empty:

    st.warning(
        "No hay operaciones disponibles con los filtros "
        "seleccionados. Modifica las opciones del panel izquierdo."
    )

    st.stop()


# =========================================================
# 13. PESTAÑAS PRINCIPALES
# =========================================================

st.markdown(
    '<div class="section-title">Panel de análisis</div>',
    unsafe_allow_html=True,
)

tab_actividad, tab_comparativos, tab_alertas, tab_datos = st.tabs(
    [
        "📈 Actividad portuaria",
        "📊 Comparativos",
        "🚨 Alertas",
        "🗂 Datos y auditoría",
    ]
)


# =========================================================
# 14. ACTIVIDAD PORTUARIA
# =========================================================

with tab_actividad:

    st.caption(
        "Analiza la evolución diaria de operaciones "
        "y las horas de mayor llegada de buques."
    )

    grafico_1, grafico_2 = st.columns(
        2,
        gap="medium",
    )

    with grafico_1:

        mostrar_grafico(
            llegadas_diarias(filtrado),
            "llegadas_diarias",
        )

    with grafico_2:

        mostrar_grafico(
            llegadas_por_hora(filtrado),
            "llegadas_hora",
        )


# =========================================================
# 15. ANÁLISIS COMPARATIVO
# =========================================================

with tab_comparativos:

    st.caption(
        "Compara los tiempos promedio de espera "
        "según el tipo de carga y las condiciones climáticas."
    )

    grafico_3, grafico_4 = st.columns(
        2,
        gap="medium",
    )

    with grafico_3:

        mostrar_grafico(
            esperas_por_carga(filtrado),
            "esperas_carga",
        )

    with grafico_4:

        mostrar_grafico(
            esperas_por_clima(filtrado),
            "esperas_clima",
        )


# =========================================================
# 16. ALERTAS CRÍTICAS
# =========================================================

with tab_alertas:

    st.subheader(
        "Monitor de demoras críticas"
    )

    st.caption(
        "Consulta las operaciones cuyo tiempo de espera "
        "supera el umbral definido en los filtros."
    )

    alertas = filtrado[
        filtrado["Alerta_Critica"]
    ].copy()

    st.metric(
        "Operaciones con demora crítica",
        len(alertas),
    )

    if alertas.empty:

        st.success(
            "No se detectaron operaciones que superen "
            "el umbral seleccionado."
        )

    else:

        st.warning(
            f"Se identificaron {len(alertas)} operaciones "
            f"con esperas superiores a {umbral:g} horas."
        )

        st.dataframe(
            alertas[
                [
                    "ID_Registro",
                    "Buque",
                    "Tipo_Carga",
                    "Hora_Llegada",
                    "Espera_Valida_Horas",
                    "Condicion_Climatica",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "El umbral de demora es configurable y "
        "no representa un estándar portuario oficial."
    )


# =========================================================
# 17. DATOS PROCESADOS
# =========================================================

with tab_datos:

    st.subheader(
        "Registros procesados"
    )

    st.caption(
        "Información resultante del proceso ETL "
        "y de los filtros aplicados."
    )

    st.dataframe(
        filtrado,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # AUDITORÍA

    st.subheader(
        "Auditoría del proceso ETL"
    )

    st.caption(
        "Resumen de las verificaciones realizadas "
        "durante la limpieza y transformación de datos."
    )

    st.dataframe(
        auditoria,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # DICCIONARIO DE VARIABLES

    with st.expander(
        "📚 Consultar diccionario de variables"
    ):

        definiciones = [
            (
                "ID_Registro",
                "Identificador único de la operación",
            ),
            (
                "Buque",
                "Identificador del buque",
            ),
            (
                "Tipo_Carga",
                "Clasificación de la carga",
            ),
            (
                "Hora_Llegada",
                "Fecha y hora de llegada",
            ),
            (
                "Hora_Atraque",
                "Fecha y hora del atraque",
            ),
            (
                "Tiempo_Espera_Horas",
                "Tiempo de espera reportado",
            ),
            (
                "Tiempo_Muelle_Horas",
                "Permanencia registrada en muelle",
            ),
            (
                "TEUs_Ocupados",
                "Volumen registrado en TEU",
            ),
            (
                "Condicion_Climatica",
                "Condición climática registrada",
            ),
            (
                "Espera_Calculada_Horas",
                "Diferencia entre atraque y llegada",
            ),
            (
                "Espera_Valida_Horas",
                "Tiempo de espera validado",
            ),
            (
                "Muelle_Valido_Horas",
                "Permanencia válida en muelle",
            ),
            (
                "TEUs_Validos",
                "Volumen TEU válido",
            ),
            (
                "Productividad_TEU_Hora",
                "Productividad aproximada TEU/h",
            ),
            (
                "Fecha",
                "Fecha de llegada",
            ),
            (
                "Hora_Dia",
                "Hora del día de llegada",
            ),
            (
                "Alerta_Critica",
                "Espera superior al umbral",
            ),
        ]

        diccionario = pd.DataFrame(
            definiciones,
            columns=[
                "Variable",
                "Descripción",
            ],
        )

        st.dataframe(
            diccionario,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # DESCARGAS

    st.subheader(
        "Exportar información"
    )

    st.caption(
        "Descarga los registros procesados y "
        "el reporte de auditoría en formato CSV."
    )

    descargar_1, descargar_2 = st.columns(2)

    with descargar_1:

        st.download_button(
            label="⬇ Descargar datos procesados",

            data=filtrado.to_csv(
                index=False,
            ).encode("utf-8-sig"),

            file_name="datos_procesados_ddj.csv",
            mime="text/csv",

            use_container_width=True,
        )

    with descargar_2:

        st.download_button(
            label="⬇ Descargar auditoría ETL",

            data=auditoria.to_csv(
                index=False,
            ).encode("utf-8-sig"),

            file_name="auditoria_ddj.csv",
            mime="text/csv",

            use_container_width=True,
        )


# =========================================================
# 18. PIE DE PÁGINA
# =========================================================

pie_pagina = (
    '<div class="footer">'
    'CIPAS DDJ · Universidad de Cartagena · '
    'Sistema de Análisis y Optimización Logística Portuaria'
    '</div>'
)

st.markdown(
    pie_pagina,
    unsafe_allow_html=True,
)
