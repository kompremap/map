import streamlit as st
import folium
from streamlit_folium import st_folium

# Nagłówek strony
st.title("Mapa dostaw laptopów do OSB")

# Przykładowe dane
data = [
    {"location": "Warszawa", "coordinates": [52.2297, 21.0122], "laptops": 50},
    {"location": "Kraków", "coordinates": [50.0647, 19.945], "laptops": 30},
]

# Formularz dodawania lokalizacji
st.sidebar.header("Dodaj nową lokalizację")
location = st.sidebar.text_input("Miejscowość")
latitude = st.sidebar.number_input("Szerokość geograficzna", value=52.0, format="%.6f")
longitude = st.sidebar.number_input("Długość geograficzna", value=19.0, format="%.6f")
laptops = st.sidebar.number_input("Liczba laptopów", min_value=0, step=1)

if st.sidebar.button("Dodaj lokalizację"):
    new_entry = {"location": location, "coordinates": [latitude, longitude], "laptops": laptops}
    data.append(new_entry)
    st.success(f"Dodano lokalizację: {location}")

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
