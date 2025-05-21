import os
import json
import streamlit as st

# ---------- Seiteneinstellungen ----------
st.set_page_config(page_title="Kapitel 1: Spielidee", layout="wide")

# ---------- Kompaktes Layout per CSS ----------
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 16px !important;
    }
    input[type="text"], textarea {
        font-size: 16px !important;
        padding: 0.4rem 0.6rem;
    }
    label, .st-c3, .st-bf, .st-ag, .st-ax, .st-ay {
        font-size: 16px !important;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    .frage-label {
        font-size: 17px !important;
        font-weight: 500;
        margin-bottom: 0.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Projektordner ----------
os.makedirs("data", exist_ok=True)

# ---------- Projektname anzeigen oder abfragen ----------
st.markdown("Hier kannst du mit deiner Spielidee starten. Beschreibe dein Spiel in ein paar Sätzen, bevor du zu den nächsten Schritten gehst.")
if "projektname" not in st.session_state or not st.session_state.projektname:
    projekt_input = st.text_input("Gib deinem Projekt einen Namen, damit du deine Eingaben wieder aufrufen kannst?")
    if st.button("🚀 Projekt starten"):
        if projekt_input.strip():
            st.session_state.projektname = projekt_input.strip()
            st.rerun()
    st.stop()

projektname = st.session_state.projektname
daten_pfad = os.path.join("data", f"{projektname}.json")

st.markdown(f"**📁 Projekt:** `{projektname}`")
st.title("📌 Kapitel 1: Dein Spiel")

# ---------- Session State mit gespeicherten Daten füllen ----------
if os.path.exists(daten_pfad):
    with open(daten_pfad, "r", encoding="utf-8") as f:
        gespeicherte_daten = json.load(f)
        gespeicherte_werte = gespeicherte_daten.get("kapitel_1", {})
        for key, val in gespeicherte_werte.items():
            if key not in st.session_state:
                st.session_state[key] = val

# ---------- Eingabebereich ----------
st.markdown("#### 🔶 Spielidee & Entwicklungsstand")

spielname = st.text_input("1. Wie heisst das Spiel?", value=st.session_state.get("spielname", ""), key="spielname")

entwicklungsoptionen = ["Nur eine Idee", "Erster Prototyp", "Im Testing", "Produktionsbereit", "Bereits produziert"]
entwicklungsstand = st.radio(
    "2. In welchem Stadium befindet sich das Spiel aktuell?",
    entwicklungsoptionen,
    index=entwicklungsoptionen.index(st.session_state.get("entwicklungsstand", "Nur eine Idee")),
    key="entwicklungsstand"
)

usp = st.text_area(
    "3. Was ist der zentrale Reiz oder USP deines Spiels?",
    value=st.session_state.get("usp", ""),
    key="usp"
)

spieltyp = st.multiselect(
    "4. Welche Art von Spiel ist es?",
    ["Familienspiel", "Partyspiel", "Kennerspiel", "Rollenspiel",
     "Lernspiel", "Deduktionsspiel", "Story-basiertes Spiel", "Anderes (bitte unten angeben)"],
    default=st.session_state.get("spieltyp", []),
    key="spieltyp"
)

spieltyp_andere = st.text_input("→ Wenn 'Anderes': Bitte hier eintragen", value=st.session_state.get("spieltyp_andere", ""), key="spieltyp_andere")

inspiration = st.text_input("5. Welche Inspirationsquelle hat dich zum Spiel gebracht?", value=st.session_state.get("inspiration", ""), key="inspiration")

st.file_uploader("Optional: Moodboard oder Bild hochladen", type=["jpg", "png", "pdf"], key="inspirationsbild")

# ---------- Zielgruppe ----------
st.markdown("#### 🔶 Zielgruppe & Spielverhalten")

zielalter = st.slider(
    "6. Für welche Altersgruppe ist das Spiel gedacht?",
    min_value=4, max_value=99,
    value=st.session_state.get("zielalter", (8, 60)),
    key="zielalter"
)

spielerfahrung = st.radio(
    "7. Welche Spielerfahrung wird vorausgesetzt?",
    ["Keine (Einsteigerfreundlich)", "Erste Spielerfahrung", "Vielspieler:innen-Niveau"],
    index=["Keine (Einsteigerfreundlich)", "Erste Spielerfahrung", "Vielspieler:innen-Niveau"].index(
        st.session_state.get("spielerfahrung", "Keine (Einsteigerfreundlich)")
    ),
    key="spielerfahrung"
)

anzahl_spieler = st.slider(
    "8. Für wie viele Personen ist das Spiel geeignet?",
    min_value=1, max_value=12,
    value=st.session_state.get("anzahl_spieler", (2, 6)),
    key="anzahl_spieler"
)

solo_modus = st.checkbox("9. Enthält einen Solo-Modus?", value=st.session_state.get("solo_modus", False), key="solo_modus")

spieldauer = st.slider(
    "10. Wie lange dauert eine durchschnittliche Spielrunde?",
    min_value=10, max_value=180,
    value=st.session_state.get("spieldauer", 60),
    key="spieldauer"
)

nutzung = st.multiselect(
    "11. Eignet sich das Spiel besonders für bestimmte Situationen?",
    ["Reisen", "Bildung", "WG-Abend", "Weihnachtsfeier", "Familienwochenende", "Andere (bitte unten angeben)"],
    default=st.session_state.get("nutzung", []),
    key="nutzung"
)

nutzung_andere = st.text_input("→ Wenn 'Andere': Bitte hier eintragen", value=st.session_state.get("nutzung_andere_k1", ""), key="nutzung_andere_k1")

# ---------- Speichern und Weiter ----------
st.markdown("---")
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("➡️ Weiter zu Kapitel 2"):
        kapitel_daten = {
            "kapitel_1": {
                "spielname": st.session_state.get("spielname", ""),
                "entwicklungsstand": st.session_state.get("entwicklungsstand", ""),
                "usp": st.session_state.get("usp", ""),
                "spieltyp": st.session_state.get("spieltyp", []),
                "spieltyp_andere": st.session_state.get("spieltyp_andere", ""),
                "inspiration": st.session_state.get("inspiration", ""),
                "zielalter": st.session_state.get("zielalter", (8, 60)),
                "spielerfahrung": st.session_state.get("spielerfahrung", ""),
                "anzahl_spieler": st.session_state.get("anzahl_spieler", (2, 6)),
                "solo_modus": st.session_state.get("solo_modus", False),
                "spieldauer": st.session_state.get("spieldauer", 60),
                "nutzung": st.session_state.get("nutzung", []),
                "nutzung_andere": st.session_state.get("nutzung_andere_k1", "")
            }
        }

        if os.path.exists(daten_pfad):
            with open(daten_pfad, "r", encoding="utf-8") as f:
                bestehende_daten = json.load(f)
        else:
            bestehende_daten = {}

        bestehende_daten.update(kapitel_daten)

        with open(daten_pfad, "w", encoding="utf-8") as f:
            json.dump(bestehende_daten, f, indent=2, ensure_ascii=False)

        st.switch_page("pages/2_Marke.py")
