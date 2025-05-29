
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from geopy.geocoders import Nominatim
import time

def scrape_urbania():
    url = "https://urbania.pe/buscar/proyectos-propiedades"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  # Esperar que cargue

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

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
        except Exception as e:
            continue

    return pd.DataFrame(projects)
