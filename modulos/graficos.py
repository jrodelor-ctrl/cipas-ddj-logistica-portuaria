"""Visualizaciones Plotly del tablero."""
import plotly.express as px

def llegadas_diarias(df):
    datos = df.groupby('Fecha',dropna=True).agg(Llegadas=('ID_Registro','count')).reset_index()
    return px.line(datos,x='Fecha',y='Llegadas',markers=True,title='Llegadas diarias (evolución temporal)',labels={'Fecha':'Fecha','Llegadas':'Número de operaciones'})

def esperas_por_carga(df):
    datos=df.groupby('Tipo_Carga',dropna=False)['Espera_Valida_Horas'].mean().reset_index()
    return px.bar(datos,x='Tipo_Carga',y='Espera_Valida_Horas',title='Espera promedio por tipo de carga',labels={'Espera_Valida_Horas':'Horas','Tipo_Carga':'Tipo de carga'},color_discrete_sequence=['#178a3c'])

def llegadas_por_hora(df):
    datos=df.groupby('Hora_Dia',dropna=True).size().reindex(range(24),fill_value=0).reset_index()
    datos.columns=['Hora','Operaciones']
    return px.line(datos,x='Hora',y='Operaciones',markers=True,title='Horas pico de llegada',labels={'Hora':'Hora del día','Operaciones':'Número de operaciones'},color_discrete_sequence=['#b88926'])

def esperas_por_clima(df):
    datos=df.groupby('Condicion_Climatica',dropna=False)['Espera_Valida_Horas'].mean().reset_index()
    return px.bar(datos,x='Condicion_Climatica',y='Espera_Valida_Horas',title='Espera promedio por clima',labels={'Espera_Valida_Horas':'Tiempo promedio (horas)','Condicion_Climatica':'Condición climática'},color_discrete_sequence=['#074785'])
