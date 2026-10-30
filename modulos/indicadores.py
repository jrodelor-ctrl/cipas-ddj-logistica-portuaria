"""Indicadores calculados sobre datos ya depurados."""
import pandas as pd

def indicadores(df):
    cont = df[df.Tipo_Carga.eq('Contenedores')]
    horas = cont.Muelle_Valido_Horas.sum()
    return {
        'operaciones': len(df),
        'tpe_horas': df.Espera_Valida_Horas.mean(),
        'tiempo_muelle_medio_horas': df.Muelle_Valido_Horas.mean(),
        'productividad_contenedores_teu_h': cont.TEUs_Validos.sum() / horas if horas > 0 else float('nan'),
        'alertas': int(df.Alerta_Critica.sum()),
    }
