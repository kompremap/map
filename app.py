import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Nagłówek strony
st.title("Mapa dostaw laptopów do OSB")

# Przykładowe dane
data = [
    {"location": "Warszawa", "coordinates": [52.2297, 21.0122], "laptops": 50},
    {"location": "Kraków", "coordinates": [50.0647, 19.945], "laptops": 30},
]

# Geolokator (Nominatim - OpenStreetMap)
geolocator = Nominatim(user_agent="mapa_dostaw")

# Panel administratora
st.sidebar.header("Panel administratora")
password = st.sidebar.text_input("Hasło administratora", type="password")
if password == "admin123":  # Ustaw swoje hasło
    st.sidebar.success("Zalogowano jako administrator!")

    # Formularz dodawania lokalizacji
    location = st.sidebar.text_input("Miejscowość")
    laptops = st.sidebar.number_input("Liczba laptopów", min_value=0, step=1)

    if st.sidebar.button("Dodaj lokalizację"):
        try:
            # Pobieranie współrzędnych na podstawie nazwy miejscowości
            loc = geolocator.geocode(location)
            if loc:
                new_entry = {
                    "location": location,
                    "coordinates": [loc.latitude, loc.longitude],
                    "laptops": laptops,
                }
                data.append(new_entry)
                st.success(f"Dodano lokalizację: {location} ({loc.latitude}, {loc.longitude})")
            else:
                st.error("Nie znaleziono współrzędnych dla podanej miejscowości.")
        except Exception as e:
            st.error(f"Wystąpił błąd podczas geokodowania: {e}")
else:
    st.sidebar.warning("Wprowadź poprawne hasło, aby dodać lokalizacje.")

# Tworzenie mapy
m = folium.Map(location=[52.0, 19.0], zoom_start=6)

# Dodanie znaczników na mapie
for entry in data:
    folium.Marker(
        location=entry["coordinates"],
        popup=f"{entry['location']}: {entry['laptops']} laptopów",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Wyświetlenie mapy
st_folium(m, width=700, height=500)

# Statystyki
st.subheader("Statystyki")
total_laptops = sum(entry["laptops"] for entry in data)
st.write(f"Łączna liczba dostarczonych laptopów: {total_laptops}")
