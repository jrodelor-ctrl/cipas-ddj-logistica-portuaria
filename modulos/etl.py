"""ETL auditable para los registros de operaciones portuarias (dataset académico simulado)."""
import pandas as pd

REQUIRED = ['ID_Registro','Buque','Tipo_Carga','Hora_Llegada','Hora_Atraque','Tiempo_Espera_Horas','Tiempo_Muelle_Horas','TEUs_Ocupados','Condicion_Climatica']

def limpiar_datos(entrada: pd.DataFrame):
    faltantes = set(REQUIRED) - set(entrada.columns)
    if faltantes:
        raise ValueError(f'Faltan columnas obligatorias: {sorted(faltantes)}')
    df = entrada.copy()
    auditoria = []
    duplicados = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()
    auditoria.append({'Control':'Filas duplicadas exactas descartadas','Cantidad':duplicados})
    duplicados_id = int(df.duplicated('ID_Registro').sum())
    df = df.drop_duplicates('ID_Registro',keep='first').copy()
    auditoria.append({'Control':'Identificadores duplicados descartados','Cantidad':duplicados_id})
    for c in ['Tipo_Carga','Condicion_Climatica','Buque']:
        df[c] = df[c].astype('string').str.strip()
    for c in ['Hora_Llegada','Hora_Atraque']:
        df[c] = pd.to_datetime(df[c],errors='coerce')
    for c in ['Tiempo_Espera_Horas','Tiempo_Muelle_Horas','TEUs_Ocupados']:
        df[c] = pd.to_numeric(df[c],errors='coerce')
    auditoria.append({'Control':'Tipo de carga no informado','Cantidad':int(df.Tipo_Carga.isna().sum())})
    df['Tipo_Carga'] = df.Tipo_Carga.fillna('Sin clasificar')
    df['Espera_Calculada_Horas'] = (df.Hora_Atraque - df.Hora_Llegada).dt.total_seconds()/3600
    invalida_espera = df.Espera_Calculada_Horas.isna() | (df.Espera_Calculada_Horas<0)
    auditoria.append({'Control':'Espera sin fechas válidas','Cantidad':int(invalida_espera.sum())})
    df['Espera_Valida_Horas'] = df.Espera_Calculada_Horas.mask(invalida_espera)
    discrepancia = ((df.Tiempo_Espera_Horas - df.Espera_Valida_Horas).abs()>0.1).fillna(False)
    auditoria.append({'Control':'Diferencias de espera reportada > 0,1 h','Cantidad':int(discrepancia.sum())})
    invalida_muelle = df.Tiempo_Muelle_Horas.isna() | (df.Tiempo_Muelle_Horas<=0)
    auditoria.append({'Control':'Tiempo en muelle no válido','Cantidad':int(invalida_muelle.sum())})
    df['Muelle_Valido_Horas'] = df.Tiempo_Muelle_Horas.mask(invalida_muelle)
    invalido_teus = df.TEUs_Ocupados.isna() | (df.TEUs_Ocupados<0)
    auditoria.append({'Control':'TEUs no válidos','Cantidad':int(invalido_teus.sum())})
    df['TEUs_Validos'] = df.TEUs_Ocupados.mask(invalido_teus)
    df['Productividad_TEU_Hora'] = (df.TEUs_Validos / df.Muelle_Valido_Horas).where(df.Tipo_Carga.eq('Contenedores'))
    df['Fecha'] = df.Hora_Llegada.dt.date
    df['Hora_Dia'] = df.Hora_Llegada.dt.hour
    df['Alerta_Critica'] = df.Espera_Valida_Horas > 3  # umbral configurable; NO estándar portuario
    return df, pd.DataFrame(auditoria)

