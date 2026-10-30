import pandas as pd
from pathlib import Path
from modulos.etl import limpiar_datos
from modulos.indicadores import indicadores
BASE=Path(__file__).resolve().parents[1]
def test_integridad():
    original=pd.read_csv(BASE/'data/datos_puerto.csv')
    limpio,aud=limpiar_datos(original)
    assert len(limpio)==150
    assert len(limpio[limpio.Muelle_Valido_Horas.isna()])==1
    assert len(limpio[limpio.Espera_Valida_Horas.isna()])==1
    assert limpio.Tipo_Carga.eq('Sin clasificar').sum()==1
    assert indicadores(limpio)['operaciones']==150

def test_nulos_y_duplicados():
    original=pd.read_csv(BASE/'data/datos_puerto.csv').head(1)
    df=pd.concat([original,original],ignore_index=True)
    limpio,aud=limpiar_datos(df)
    assert len(limpio)==1
    assert aud.loc[0,'Cantidad']==1
