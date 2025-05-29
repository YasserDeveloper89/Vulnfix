import pandas as pd

def get_properati_data():
    return pd.DataFrame([
        {"nombre": "Mirador de La Molina", "empresa": "Grupo T&C", "tipo": "Departamento", "distrito": "La Molina", "avance": "90%", "precio": "$270,000", "lat": -12.082, "lon": -76.934},
        {"nombre": "Residencial San Borja Norte", "empresa": "Viva Grupo", "tipo": "Oficina", "distrito": "San Borja", "avance": "65%", "precio": "$150,000", "lat": -12.105, "lon": -76.998}
    ])