# app.py
import streamlit as st

st.set_page_config(page_title="Marketing- & Finanzierungsleitfaden", layout="wide")

st.title("🎲 Marketing- & Finanzierungsleitfaden")
st.write("Willkommen in deinem persönlichen Leitfaden zur Vermarktung und Finanzierung deines Spiels! 🎉")

st.markdown("""
Um dein Spiel, deine Marke und deine Ziele kennen zu lernen, habe ich foolgende Fragen für dich vorbereitet:

1. 📌 Spielidee & Entwicklungsstand  
2. 🎯 Zielgruppe & Spielverhalten  
3. 🧾 Produktion & Preis  
4. 🌍 Länder & Vertrieb  
5. 🧑‍🤝‍🧑 Community & Vertrieb  
6. 💰 Ressourcen & Finanzierung

Am Ende werden alle Eingaben zusammengeführt, ausgewertet und könnenn exportiert werden. Wenn du den gleichen Projektnamen wiederverwendest, kommst du jederzeit auf deine Eingaben zurück. 

Disclaimer: Bitte beachte, dass deine Eingaben gespeichert werden. Diese Daten werden jedoch nur für die Auswertung des Leitfadens benötigt. 
""")

# 🔘 Start-Button unten hinzufügen
st.markdown("---")
if st.button("🚀 Los geht’s – Starte mit Kapitel 1"):
    st.switch_page("pages/1_Spielidee.py")

