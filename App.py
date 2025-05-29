import requests
from bs4 import BeautifulSoup
import pandas as pd
from geopy.geocoders import Nominatim
import time

def get_urbania_data():
    url = 'https://urbania.pe/buscar/proyectos-propiedades'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    projects = []
    geolocator = Nominatim(user_agent="urbania_scraper")

    # Este es un ejemplo; la estructura real del sitio puede variar
    listings = soup.find_all('div', class_='project-card')
    for listing in listings:
        name = listing.find('h2').get_text(strip=True)
        address = listing.find('p', class_='address').get_text(strip=True)
        price = listing.find('span', class_='price').get_text(strip=True)
        bedrooms = listing.find('span', class_='bedrooms').get_text(strip=True)
        area = listing.find('span', class_='area').get_text(strip=True)
        link = listing.find('a', href=True)['href']

        # Geocoding
        location = geolocator.geocode(address)
        if location:
            lat = location.latitude
            lon = location.longitude
        else:
            lat = None
            lon = None

        projects.append({
            'nombre': name,
            'direccion': address,
            'precio': price,
            'dormitorios': bedrooms,
            'area_m2': area,
            'url': link,
            'lat': lat,
            'lon': lon
        })

        time.sleep(1)  # Para respetar las políticas del servicio de geocodificación

    return pd.DataFrame(projects)
