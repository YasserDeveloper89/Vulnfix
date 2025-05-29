
import requests
from bs4 import BeautifulSoup
import pandas as pd
from geopy.geocoders import Nominatim
import time

def scrape_urbania():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = "https://urbania.pe/buscar/proyectos-propiedades"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all('div', class_='posting-card')
    geolocator = Nominatim(user_agent="urbania_scraper")
    projects = []

    for card in cards:
        try:
            nombre = card.find('h2').text.strip()
            direccion = card.find('span', class_='posting-location').text.strip()
            precio = card.find('span', class_='first-price').text.strip()
            detalles = card.find_all('li', class_='surface-item')
            dormitorios = detalles[0].text.strip() if len(detalles) > 0 else "N/D"
            area = detalles[1].text.strip() if len(detalles) > 1 else "N/D"
            url = "https://urbania.pe" + card.find('a')['href']

            distrito = direccion.split(',')[-1].strip()
            location = geolocator.geocode(direccion + ", Lima, Perú")
            lat = location.latitude if location else None
            lon = location.longitude if location else None

            projects.append({
                "nombre": nombre,
                "direccion": direccion,
                "distrito": distrito,
                "precio": precio,
                "dormitorios": dormitorios,
                "area_m2": area,
                "url": url,
                "lat": lat,
                "lon": lon
            })
            time.sleep(1)
        except Exception:
            continue

    return pd.DataFrame(projects)
