"""Punto de entrada: integra los módulos sin mezclar responsabilidades."""
import pandas as pd
import streamlit as st
from modulos.config import DATOS, LOGO, TITULO
from modulos.etl import limpiar_datos
from modulos.indicadores import indicadores
from modulos.graficos import (llegadas_diarias, esperas_por_carga, llegadas_por_hora, esperas_por_clima)

st.set_page_config(page_title=TITULO,page_icon='⚓',layout='wide')
st.markdown("""<style>
.stApp {background:#f7fafc;color:#092d57} h1,h2,h3{color:#092d57}
[data-testid="stMetric"]{background:white;border:1px solid #dae6f0;border-radius:12px;padding:14px}
</style>""",unsafe_allow_html=True)

with st.sidebar:
    st.image(str(LOGO),width=220)
    st.header('Filtros')
    archivo=st.file_uploader('Cargar un archivo CSV (opcional)', type=['csv'], help='Seleccione un archivo CSV con las columnas requeridas. El botón interno del explorador puede aparecer en el idioma configurado por Streamlit o el navegador.')
try:
    fuente=pd.read_csv(archivo) if archivo else pd.read_csv(DATOS)
    completo,auditoria=limpiar_datos(fuente)
except (ValueError, OSError, pd.errors.ParserError) as ex:
    st.error(f'El archivo no pudo procesarse: {ex}')
    st.stop()

with st.sidebar:
    tipos_disponibles=sorted(completo.Tipo_Carga.dropna().unique().tolist())
    climas_disponibles=sorted(completo.Condicion_Climatica.dropna().unique().tolist())
    tipos=st.multiselect('Tipo de carga',tipos_disponibles,default=tipos_disponibles,placeholder='Seleccione uno o varios tipos de carga')
    climas=st.multiselect('Condición climática',climas_disponibles,default=climas_disponibles,placeholder='Seleccione una o varias condiciones')
    umbral=st.number_input('Demora crítica: horas',min_value=0.5,max_value=48.0,value=3.0,step=0.5)

filtrado=completo[completo.Tipo_Carga.isin(tipos)&completo.Condicion_Climatica.isin(climas)].copy()
filtrado['Alerta_Critica']=filtrado.Espera_Valida_Horas>umbral
st.title('⚓ Sistema de Analítica Logística Portuaria')
st.caption('CIPAS DDJ · Universidad de Cartagena · Datos académicos simulados: no representan operaciones portuarias reales')
st.info('**Nota metodológica:** sin identificación de muelles, capacidad y ventanas de disponibilidad, no es posible medir la ocupación física real. La productividad TEU/h es una aproximación del volumen por permanencia, no una tasa real de grúas.')
kpi=indicadores(filtrado)
a,b,c,d,e=st.columns(5)
a.metric('Operaciones',str(kpi['operaciones']))
b.metric('Espera media (h)',f"{kpi['tpe_horas']:.2f}" if pd.notna(kpi['tpe_horas']) else 'N/D')
c.metric('Permanencia media (h)',f"{kpi['tiempo_muelle_medio_horas']:.2f}" if pd.notna(kpi['tiempo_muelle_medio_horas']) else 'N/D')
d.metric('TEU/h contenedores',f"{kpi['productividad_contenedores_teu_h']:.1f}" if pd.notna(kpi['productividad_contenedores_teu_h']) else 'N/D')
e.metric('Demoras críticas',str(kpi['alertas']))
if filtrado.empty:
    st.warning('No hay registros para los filtros seleccionados.')
    st.stop()

izq,der=st.columns(2)
with izq:
    st.plotly_chart(llegadas_diarias(filtrado),use_container_width=True, config={'displaylogo': False, 'locale': 'es'})
    st.plotly_chart(esperas_por_carga(filtrado),use_container_width=True, config={'displaylogo': False, 'locale': 'es'})
with der:
    st.plotly_chart(llegadas_por_hora(filtrado),use_container_width=True, config={'displaylogo': False, 'locale': 'es'})
    st.plotly_chart(esperas_por_clima(filtrado),use_container_width=True, config={'displaylogo': False, 'locale': 'es'})
st.subheader('Alertas por demoras críticas')
alertas=filtrado[filtrado.Alerta_Critica]
if not alertas.empty:
    st.dataframe(alertas[['ID_Registro','Buque','Tipo_Carga','Hora_Llegada','Espera_Valida_Horas','Condicion_Climatica']],use_container_width=True,hide_index=True)
else:
    st.success('No se registran esperas superiores al umbral seleccionado.')
with st.expander('Auditoría de datos y diccionario de variables'):
    st.dataframe(auditoria,hide_index=True,use_container_width=True)
    st.dataframe(pd.DataFrame([
      ('ID_Registro','Identificador único de operación'),('Buque','Código de identificación del buque'),('Tipo_Carga','Categoría de carga'),('Hora_Llegada','Fecha y hora de llegada'),('Hora_Atraque','Fecha y hora de atraque'),('Tiempo_Espera_Horas','Espera reportada; fechas como fuente principal'),('Tiempo_Muelle_Horas','Permanencia en muelle declarada'),('TEUs_Ocupados','Volumen de contenedores registrado en TEU; no capacidad del muelle'),('Condicion_Climatica','Clima asignado al evento'),('Espera_Valida_Horas','Hora atraque menos hora llegada, si es válido'),('Muelle_Valido_Horas','Permanencia estrictamente positiva'),('Productividad_TEU_Hora','TEUs/horas en contenedores')],columns=['Variable','Definición']),hide_index=True,use_container_width=True)
col_a,col_b=st.columns(2)
col_a.download_button('Descargar datos procesados (CSV)',filtrado.to_csv(index=False).encode('utf-8-sig'),'datos_procesados_ddj.csv','text/csv')
col_b.download_button('Descargar auditoría (CSV)',auditoria.to_csv(index=False).encode('utf-8-sig'),'auditoria_ddj.csv','text/csv')
