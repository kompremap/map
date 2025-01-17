import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import os

# Plik do przechowywania danych
DATA_FILE = "data.txt"

# Funkcja do ładowania danych z pliku
def load_data():
    data = []
    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                try:
                    location, url, latitude, longitude, laptops = line.strip().split(";")
                    data.append({
                        "location": location,
                        "url": url if url else None,  # Obsługuje puste URL
                        "coordinates": [float(latitude), float(longitude)],
                        "laptops": int(laptops),
                    })
                except ValueError:
                    st.error(f"Błędny format danych w pliku: {line.strip()}")
    except FileNotFoundError:
        st.warning("Plik data.txt nie istnieje. Zostanie utworzony przy pierwszym zapisie.")
    return data

# Funkcja do zapisywania danych do pliku
def save_data(data):
    with open(DATA_FILE, "w") as file:
        for entry in data:
            file.write(f"{entry['location']};{entry['url'] or ''};{entry['coordinates'][0]};{entry['coordinates'][1]};{entry['laptops']}\n")

# Wczytaj dane
data = load_data()

# Geolokator (Nominatim - OpenStreetMap)
geolocator = Nominatim(user_agent="mapa_dostaw")

# Nagłówek strony
st.title("Mapa dostaw laptopów do OSB")

# Formularz dodawania lokalizacji
st.header("Dodaj nową lokalizację")
location = st.text_input("Miejscowość")
url = st.text_input("Link (opcjonalny, np. do mapy lub strony)")
laptops = st.number_input("Liczba laptopów", min_value=0, step=1)

if st.button("Dodaj lokalizację"):
    try:
        # Pobieranie współrzędnych na podstawie nazwy miejscowości
        loc = geolocator.geocode(location)
        if loc:
            new_entry = {
                "location": location,
                "url": url,
                "coordinates": [loc.latitude, loc.longitude],
                "laptops": laptops,
            }
            data.append(new_entry)
            save_data(data)  # Zapisz dane do pliku
            st.success(f"Dodano lokalizację: {location} ({loc.latitude}, {loc.longitude})")
        else:
            st.error("Nie znaleziono współrzędnych dla podanej miejscowości.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas geokodowania: {e}")

# Tworzenie mapy
m = folium.Map(location=[52.0, 19.0], zoom_start=6)

# Dodanie znaczników na mapie
for entry in data:
    popup_text = f"{entry['location']}: {entry['laptops']} laptopów"
    if entry['url']:
        popup_text += f"<br><a href='{entry['url']}' target='_blank'>Zobacz szczegóły</a>"
    
    folium.Marker(
        location=entry["coordinates"],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Wyświetlenie mapy
st_folium(m, width=700, height=500)

# Statystyki
st.subheader("Statystyki")
total_laptops = sum(entry["laptops"] for entry in data)
st.write(f"Łączna liczba dostarczonych laptopów: {total_laptops}")
