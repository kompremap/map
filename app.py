import streamlit as st
import folium
from streamlit_folium import st_folium

# Plik do przechowywania danych
DATA_FILE = "data.txt"

# Funkcja do ładowania danych z pliku
def load_data():
    data = []
    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                location, link, latitude, longitude, laptops = line.strip().split(";")
                data.append({
                    "location": location,
                    "link": link,
                    "coordinates": [float(latitude), float(longitude)],
                    "laptops": int(laptops),
                })
    except FileNotFoundError:
        st.error("Plik data.txt nie został znaleziony!")
    return data

# Wczytaj dane
data = load_data()

# Nagłówek strony
st.title("Mapa dostaw laptopów do OSP")

# Tworzenie mapy
m = folium.Map(location=[52.0, 19.0], zoom_start=6)

# Dodanie znaczników na mapie
for entry in data:
    folium.Marker(
        location=entry["coordinates"],
        popup=folium.Popup(
            f"<b>{entry['location']}</b><br>"
            f"Liczba laptopów: {entry['laptops']}<br>"
            f"<a href='{entry['link']}' target='_blank'>Link do Google Maps</a>",
            max_width=250,
        ),
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Wyświetlenie mapy
st_folium(m, width=700, height=500)

# Statystyki
st.subheader("Statystyki")
total_laptops = sum(entry["laptops"] for entry in data)
st.write(f"Łączna liczba dostarczonych laptopów: {total_laptops}")
