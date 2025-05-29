import pandas as pd

def get_urbania_data():
    # Simulando resultados de scraping
    return pd.DataFrame([
        {"nombre": "Torre Pardo 360", "empresa": "Edifica", "tipo": "Departamento", "distrito": "Miraflores", "avance": "80%", "precio": "$180,000", "lat": -12.121, "lon": -77.03},
        {"nombre": "The Grand San Isidro", "empresa": "Imagina", "tipo": "Departamento", "distrito": "San Isidro", "avance": "60%", "precio": "$250,000", "lat": -12.097, "lon": -77.042}
    ])