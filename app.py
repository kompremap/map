import streamlit as st
import folium
from streamlit_folium import st_folium
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
        st.warning("Plik data.txt nie istnieje. Dodaj plik i dane, aby je wyświetlić.")
    return data

# Wczytaj dane z pliku
data = load_data()

# Nagłówek strony
st.title("#KompreDlaOSP")

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
