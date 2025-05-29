import pandas as pd

def get_adondevivir_data():
    return pd.DataFrame([
        {"nombre": "Residencial Premium Barranco", "empresa": "Menorca", "tipo": "Casa", "distrito": "Barranco", "avance": "70%", "precio": "$320,000", "lat": -12.143, "lon": -77.02},
        {"nombre": "Vista Surco", "empresa": "Los Portales", "tipo": "Departamento", "distrito": "Santiago de Surco", "avance": "50%", "precio": "$210,000", "lat": -12.132, "lon": -76.991}
    ])