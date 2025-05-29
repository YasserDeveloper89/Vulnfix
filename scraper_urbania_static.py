
import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from geopy.geocoders import Nominatim
import time
import json

async def scrape_urbania():
    geolocator = Nominatim(user_agent="urbania_scraper_static")
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://urbania.pe/buscar/proyectos-propiedades", timeout=60000)
        await page.wait_for_selector('.posting-card', timeout=15000)
        cards = await page.query_selector_all('.posting-card')

        for card in cards[:20]:  # limitar para pruebas
            try:
                title = await card.query_selector('.posting-title')
                nombre = await title.inner_text() if title else "Sin nombre"
                location_span = await card.query_selector('.posting-location')
                direccion = await location_span.inner_text() if location_span else "Sin dirección"
                price_span = await card.query_selector('.first-price')
                precio = await price_span.inner_text() if price_span else "Sin precio"
                href = await card.query_selector('a')
                href_val = await href.get_attribute('href') if href else ''
                url = "https://urbania.pe" + href_val if href_val else ''

                distrito = direccion.split(',')[-1].strip()
                location = geolocator.geocode(direccion + ", Lima, Perú")
                lat = location.latitude if location else None
                lon = location.longitude if location else None

                data.append({
                    "nombre": nombre,
                    "direccion": direccion,
                    "distrito": distrito,
                    "precio": precio,
                    "url": url,
                    "lat": lat,
                    "lon": lon
                })
                time.sleep(1)
            except:
                continue

        await browser.close()
    return data

def save_data_to_json():
    data = asyncio.run(scrape_urbania())
    with open("urbania_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    save_data_to_json()
