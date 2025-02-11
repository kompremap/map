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
                    location, url, latitude, longitude, *image_url_category = line.strip().split(";")
                    image_url = image_url_category[0] if len(image_url_category) > 0 else None
                    category = image_url_category[1] if len(image_url_category) > 1 else None
                    data.append({
                        "location": location,
                        "url": url if url else None,
                        "coordinates": [float(latitude), float(longitude)],
                        "image_url": image_url if image_url else None,
                        "category": category if category else "Nieokreślona"
                    })
                except ValueError:
                    st.error(f"Błędny format danych w pliku: {line.strip()}")
    except FileNotFoundError:
        st.warning("Plik data.txt nie istnieje. Dodaj plik i dane, aby je wyświetlić.")
    return data

# Wczytaj dane z pliku
data = load_data()

# Dodanie logo firmy na górze strony z linkiem do strony
logo_url = "https://raw.githubusercontent.com/marekkomp/mapa-dostaw/main/image/Bez%20nazwy.png"
redirect_url = "https://www.kompre.pl"
st.markdown(
    f"""
    <a href="{redirect_url}" target="_blank">
        <img src="{logo_url}" width="448" style="display: block; margin-left: auto; margin-right: auto;"/>
    </a>
    """,
    unsafe_allow_html=True
)

# Wspólny tytuł
st.title("Dziękujemy za zaufanie")

# Filtry kategorii
categories = list(set(entry["category"] for entry in data))
selected_category = st.selectbox("Wybierz kategorię", ["Wszystkie"] + categories)

# Dynamiczny podtytuł dla każdej kategorii
if selected_category == "Wszystkie":
    st.subheader("W 2025 nasza mapa będzie pełna znaczników!")
elif selected_category == "Darowizny":
    st.subheader("Darowizny #KompreDlaOSP #LokalniBohaterowie")
elif selected_category == "Referencje":
    st.subheader("Oto kilka przykładów zakończonych przetargów.")
else:
    st.subheader(f"Lokalizacje: {selected_category}")

# Filtrowanie danych na podstawie wybranej kategorii
if selected_category != "Wszystkie":
    filtered_data = [entry for entry in data if entry["category"] == selected_category]
else:
    filtered_data = data

# Tworzenie mapy
m = folium.Map(location=[52.0, 19.0], zoom_start=6)

# Dodanie znaczników na mapie
for entry in filtered_data:
    try:
        popup_text = f"<b>{entry['location']}</b>"
        if entry['url']:
            popup_text += f"<br><a href='{entry['url']}' target='_blank'>Zobacz szczegóły</a>"
        if entry['image_url'] and entry['image_url'].strip():
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
