import os
import json
import streamlit as st

# 🌐 Seite konfigurieren
st.set_page_config(page_title="Kapitel 2: Marke & Markenstrategie", layout="wide")

# 📁 Projekt prüfen
if "projektname" not in st.session_state or not st.session_state.projektname:
    st.warning("Bitte gib zuerst auf der Seite Spielidee einen Projektnamen ein.")
    st.stop()

projektname = st.session_state.projektname
daten_pfad = f"data/{projektname}.json"
os.makedirs("data", exist_ok=True)

# Gespeicherte Daten in session_state laden
if os.path.exists(daten_pfad):
    with open(daten_pfad, "r", encoding="utf-8") as f:
        gespeicherte_daten = json.load(f)
        gespeicherte_werte = gespeicherte_daten.get("kapitel_2", {})
        for key, val in gespeicherte_werte.items():
            if key not in st.session_state:
                st.session_state[key] = val

# 📁 Projektname anzeigen
st.markdown(f"**📁 Projekt:** `{projektname}`")
st.title("🌟 Kapitel 2: Marke & Markenstrategie")

# ---------- Kompaktes und einheitliches Layout per CSS ----------
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 16px !important;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .frage-label {
        font-size: 17px !important;
        font-weight: 500;
        margin-bottom: 0.2rem;
        margin-top: 0.3rem;
    }
    </style>
""", unsafe_allow_html=True)

# 📚 Portfolio & Historie
st.markdown("#### 🔶 Portfolio & Historie")

st.markdown('<div class="frage-label">Welche Spiele hast du bisher veröffentlicht? (Titel, Jahr - jeweils eine Zeile)</div>', unsafe_allow_html=True)
st.text_area("", value=st.session_state.get("spiele_liste", ""), key="spiele_liste")

st.markdown('<div class="frage-label">Welches war dein erstes Spiel – wie kam es zustande?</div>', unsafe_allow_html=True)
st.text_area("", value=st.session_state.get("erstes_spiel", ""), key="erstes_spiel")

st.markdown('<div class="frage-label">Welche deiner bisherigen Spiele waren besonders erfolgreich – und warum?</div>', unsafe_allow_html=True)
st.text_area("", value=st.session_state.get("erfolgreiche_spiele", ""), key="erfolgreiche_spiele")

st.markdown('<div class="frage-label">Gibt es Gemeinsamkeiten im Stil deiner Spiele? (Design, Mechanik, Themen)</div>', unsafe_allow_html=True)
st.text_input("", value=st.session_state.get("spielstil_gemeinsamkeiten", ""), key="spielstil_gemeinsamkeiten")

st.file_uploader("Optional: Beispielbilder hochladen (mehrere möglich)", accept_multiple_files=True, type=["jpg", "png", "webp"], key="spielstil_bilder")

st.markdown('<div class="frage-label">Wie viele deiner Spiele sind derzeit aktiv im Vertrieb?</div>', unsafe_allow_html=True)
st.number_input("", min_value=0, step=1, value=st.session_state.get("aktive_spiele", 0), key="aktive_spiele")

# 🔶 Markenstrategie & Vision
st.markdown("#### 🔶 Markenstrategie & Vision")

st.markdown('<div class="frage-label">Was möchtest du langfristig mit deiner Marke erreichen?</div>', unsafe_allow_html=True)
st.text_input("", value=st.session_state.get("markenziel", ""), key="markenziel")

st.markdown('<div class="frage-label">Welche Werte soll deine Marke vermitteln?</div>', unsafe_allow_html=True)
st.multiselect("", ["Bildung", "Unterhaltung", "Nachhaltigkeit", "Inklusion", "Kreativität", "Anderes (bitte unten angeben)"],
               default=st.session_state.get("markenwerte", []), key="markenwerte")
st.text_input("→ Wenn 'Anderes': Bitte hier eintragen", value=st.session_state.get("markenwerte_andere", ""), key="markenwerte_andere")

st.markdown('<div class="frage-label">Willst du deine Marke vertiefen oder erweitern?</div>', unsafe_allow_html=True)
richtung_auswahl = ["Bestehende Themen vertiefen", "Neue Richtungen testen"]
st.radio("", richtung_auswahl,
         index=richtung_auswahl.index(st.session_state.get("markenrichtung", "Bestehende Themen vertiefen")),
         key="markenrichtung", label_visibility="collapsed")

st.markdown('<div class="frage-label">Welche Zielgruppen möchtest du (neu) ansprechen?</div>', unsafe_allow_html=True)
st.text_input("", value=st.session_state.get("zielgruppen", ""), key="zielgruppen")

# 🔶 Markenpräsenz & Wiedererkennung
st.markdown("#### 🔶 Markenpräsenz & Wiedererkennung")

st.markdown('<div class="frage-label">Wo ist deine Marke heute sichtbar?</div>', unsafe_allow_html=True)
st.multiselect("", ["Website", "Instagram", "YouTube", "Facebook", "TikTok", "Presseartikel", "Messen", "Podcast", "Anderswo"],
               default=st.session_state.get("sichtbarkeit", []), key="sichtbarkeit")
nutzung_andere = st.text_input("→ Wenn 'Anderswo': Bitte hier eintragen", value=st.session_state.get("nutzung_andere_marke", ""), key="nutzung_andere")

st.markdown('<div class="frage-label">An welchen Messen oder Events nimmst du teil?</div>', unsafe_allow_html=True)
st.text_input("", value=st.session_state.get("messen", ""), key="messen")

st.markdown('<div class="frage-label">Wie sieht deine visuelle Identität aus? (Logo, Farben, Claim)</div>', unsafe_allow_html=True)
st.text_area("", value=st.session_state.get("markenidentitaet", ""), key="markenidentitaet")

st.file_uploader("Optional: Logo oder Style Guide hochladen", type=["png", "jpg", "pdf"], key="logo_upload")

# 🔶 Nachhaltigkeit & Produktionsethik
st.markdown("#### 🔶 Nachhaltigkeit & Produktionsethik")

st.radio("Ist dir Nachhaltigkeit in der Produktion wichtig?", ["Ja", "Nein"],
         index=["Ja", "Nein"].index(st.session_state.get("nachhaltigkeit_wichtig", "Ja")),
         key="nachhaltigkeit_wichtig")

st.text_area("Welche Maßnahmen möchtest du treffen? (z. B. lokale Produktion, Recycling-Materialien)",
             value=st.session_state.get("nachhaltigkeit_massnahmen", ""), key="nachhaltigkeit_massnahmen")

st.radio("Kommunizierst du ethische oder ökologische Standards nach außen?", ["Ja", "Nein", "Geplant"],
         index=["Ja", "Nein", "Geplant"].index(st.session_state.get("nachhaltigkeit_kommunikation", "Ja")),
         key="nachhaltigkeit_kommunikation")

st.multiselect("Welche Standards oder Labels triffst du oder strebst du an?",
               ["Klimaneutral", "Made in EU", "Verpackung optimiert", "Cradle to Cradle", "FSC-zertifiziert", "Anderes"],
               default=st.session_state.get("nachhaltigkeit_label", []), key="nachhaltigkeit_label")
nutzung_andere = st.text_input("→ Wenn 'Anderes': Bitte hier eintragen", value=st.session_state.get("nutzung_andere_label", ""), key="nutzung_andere_label")

# 📥 Speichern
def speichere_kapitel_2():
    daten = {
        "kapitel_2": {
            "spiele_liste": st.session_state.get("spiele_liste", ""),
            "erstes_spiel": st.session_state.get("erstes_spiel", ""),
            "erfolgreiche_spiele": st.session_state.get("erfolgreiche_spiele", ""),
            "spielstil_gemeinsamkeiten": st.session_state.get("spielstil_gemeinsamkeiten", ""),
            "aktive_spiele": st.session_state.get("aktive_spiele", 0),
            "markenziel": st.session_state.get("markenziel", ""),
            "markenwerte": st.session_state.get("markenwerte", []),
            "markenwerte_andere": st.session_state.get("markenwerte_andere", ""),
            "markenrichtung": st.session_state.get("markenrichtung", ""),
            "zielgruppen": st.session_state.get("zielgruppen", ""),
            "sichtbarkeit": st.session_state.get("sichtbarkeit", []),
            "messen": st.session_state.get("messen", ""),
            "markenidentitaet": st.session_state.get("markenidentitaet", ""),
            "nachhaltigkeit_wichtig": st.session_state.get("nachhaltigkeit_wichtig", ""),
            "nachhaltigkeit_massnahmen": st.session_state.get("nachhaltigkeit_massnahmen", ""),
            "nachhaltigkeit_kommunikation": st.session_state.get("nachhaltigkeit_kommunikation", ""),
            "nachhaltigkeit_label": st.session_state.get("nachhaltigkeit_label", [])
        }
    }

    if os.path.exists(daten_pfad):
        with open(daten_pfad, "r", encoding="utf-8") as f:
            bestehende_daten = json.load(f)
    else:
        bestehende_daten = {}

    bestehende_daten.update(daten)

    with open(daten_pfad, "w", encoding="utf-8") as f:
        json.dump(bestehende_daten, f, indent=2, ensure_ascii=False)

# 📆 Navigation
st.markdown("---")
col1, _, col3 = st.columns([1, 5, 1])

with col1:
    if st.button("⬅️ Zurück zu Kapitel 1"):
        speichere_kapitel_2()
        st.switch_page("pages/1_Spielidee.py")

with col3:
    if st.button("➡️ Weiter zu Kapitel 3"):
        speichere_kapitel_2()
        st.success("✅ Kapitel 2 gespeichert.")
        st.switch_page("pages/3_Community_Vertrieb.py")
