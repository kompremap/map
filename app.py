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
                try:
                    location, url, latitude, longitude, laptops, *image_url = line.strip().split(";")
                    data.append({
                        "location": location,
                        "url": url if url else None,  # Obsługuje puste URL
                        "coordinates": [float(latitude), float(longitude)],
                        "laptops": int(laptops),
                        "image_url": image_url[0] if image_url else None  # Obsługuje brak zdjęcia
                    })
                except ValueError:
                    st.error(f"Błędny format danych w pliku: {line.strip()}")
    except FileNotFoundError:
        st.warning("Plik data.txt nie istnieje. Dodaj plik i dane, aby je wyświetlić.")
    return data

# Wczytaj dane z pliku
data = load_data()

# Debug: Wyświetlanie wczytanych danych
st.write("Wczytane dane:", data)

# Nagłówek strony
st.title("Razem możemy więcej")

# Podtytuł
st.subheader("#KompreDlaOSP #LokalniBohaterowie")

# Tworzenie mapy
m = folium.Map(location=[52.0, 19.0], zoom_start=6)

# Dodanie znaczników na mapie
for entry in data:
    try:
        popup_text = f"<b>{entry['location']}</b>: {entry['laptops']} laptopów"
        if entry['url']:
            popup_text += f"<br><a href='{entry['url']}' target='_blank'>Zobacz szczegóły</a>"
        if entry['image_url']:
            popup_text += f"<br><img src='{entry['image_url']}' width='200px'/>"
        
        folium.Marker(
            location=entry["coordinates"],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
    except Exception as e:
        st.error(f"Błąd podczas dodawania lokalizacji {entry['location']}: {e}")

# Wyświetlenie mapy
st_folium(m, width=700, height=500)

# Statystyki
st.subheader("Statystyki")
total_laptops = sum(entry["laptops"] for entry in data)
st.write(f"Łączna liczba dostarczonych laptopów: {total_laptops}")
