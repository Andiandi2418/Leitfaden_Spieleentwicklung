import os
import json
import streamlit as st

# 🌐 Seite konfigurieren
st.set_page_config(page_title="Kapitel 3: Community & Vertrieb", layout="wide")
st.title("🧑‍🤝‍🧑 Kapitel 3: Community & Vertrieb")

# 📁 Projekt prüfen
if "projektname" not in st.session_state or not st.session_state.projektname:
    st.warning("Bitte gib zuerst auf Seite 1 einen Projektnamen ein.")
    st.stop()

projektname = st.session_state.projektname
st.markdown(f"**📁 Projekt:** `{projektname}`")
daten_pfad = f"data/{projektname}.json"
os.makedirs("data", exist_ok=True)

# 🔄 Daten aus Datei laden
if os.path.exists(daten_pfad):
    with open(daten_pfad, "r", encoding="utf-8") as f:
        gespeicherte_daten = json.load(f)
        gespeicherte_werte = gespeicherte_daten.get("kapitel_3", {})
        for key, val in gespeicherte_werte.items():
            if key not in st.session_state:
                st.session_state[key] = val

# 🧩 Eingabefelder
st.markdown("#### 🔶 Community-Aufbau & -Pflege")
st.multiselect("1. Wo befindet sich deine Community aktuell?", [
    "Discord", "Instagram", "Facebook", "YouTube", "Mailingliste",
    "Offline (Messen, Café, Events)", "Noch keine aktive Community", "Anderes"
], default=st.session_state.get("community_orte", []), key="community_orte")

nutzung_andere = st.text_input("→ Wenn 'Anderswo': Bitte hier eintragen", value=st.session_state.get("nutzung_andere_mcommunity", ""), key="nutzung_andere_community")

st.number_input("2. Wie gross ist deine Community (Anzahl)?", min_value=0, step=10,
                value=st.session_state.get("community_groesse", 0), key="community_groesse")
st.text_input("→ Was ist deine qualitative Einschätzung zu deiner Community?", value=st.session_state.get("community_einschaetzung", ""), key="community_einschaetzung")

st.radio("3. Wie häufig interagierst du mit deiner Community?", [
    "Mehrmals pro Woche", "Wöchentlich", "Monatlich", "Punktuell", "Noch nicht"
], index=["Mehrmals pro Woche", "Wöchentlich", "Monatlich", "Punktuell", "Noch nicht"].index(
    st.session_state.get("interaktion", "Noch nicht")
), key="interaktion")

st.multiselect("4. Welche Formate nutzt du zur Aktivierung?", [
    "Umfragen", "Feedbackaktionen", "Giveaways", "Behind-the-Scenes-Content",
    "Prototypentests", "Challenges", "Gar keine"
], default=st.session_state.get("aktivierungsformate", []), key="aktivierungsformate")

st.text_area("5. Was funktioniert in deiner Community besonders gut?", value=st.session_state.get("community_erfolgreich", ""), key="community_erfolgreich")
st.text_area("6. Welche Community-Arbeit liegt dir persönlich besonders?", value=st.session_state.get("persoenliche_community_arbeit", ""), key="persoenliche_community_arbeit")
st.text_area("7. Was möchtest du künftig nicht mehr machen?", value=st.session_state.get("community_verzicht", ""), key="community_verzicht")
st.multiselect("8. Welche Plattformen oder Formate würdest du gern ausprobieren?", [
    "YouTube", "TikTok", "Twitch", "Live-Events", "Blogs", "Sonstiges"
], default=st.session_state.get("plattformen_neu", []), key="plattformen_neu")
st.text_input("→ Wenn 'Sonstiges': Bitte eintragen", value=st.session_state.get("plattformen_sonst", ""), key="plattformen_sonst")

st.markdown("#### 🔶 Vertriebskanäle & Vertriebsstrategie")

st.text_input("In welchen Ländern möchtest du dein Spiel vertreiben?", value=st.session_state.get("vertrieb_zusatz_land", ""), key="vertrieb_zusatz_land")

st.multiselect("9. Welche Vertriebskanäle nutzt du aktuell aktiv?", [
    "Eigener Webshop", "Kickstarter", "Messen", "Buch-/Spielhandel",
    "Amazon", "Direktvertrieb (z. B. bei Events)"
], default=st.session_state.get("vertrieb_aktiv", []), key="vertrieb_aktiv")
st.text_input("Gibt es noch weitere Vertriebskanäle, welche du nutzt?", value=st.session_state.get("plattformen_sonst_verteibe", ""), key="plattformen_sonst_verteibe")

# 🔹 Titel normal, nicht fett
# Titel ohne Fettung
st.markdown("Wie viele sind dies total?")

vertrieb_kuchen = {}

aktive_kanaele = st.session_state.get("vertrieb_aktiv", [])
zusatz_text = st.session_state.get("vertrieb_andere_vertrieb", "")
zusatz_kanaele = [k.strip() for k in zusatz_text.split(",") if k.strip()]
alle_kanaele = aktive_kanaele + zusatz_kanaele

# Slider ohne sichtbares Label anzeigen (leerer String)
for kanal in alle_kanaele:
    vertrieb_kuchen[kanal] = st.slider(
        label="",  # keine Bezeichnung
        min_value=0,
        max_value=100,
        value=st.session_state.get(f"kuchen_{kanal}", 0),
        key=f"kuchen_{kanal}"
    )


st.text_input("11. Welche Vertriebskanäle möchtest du zusätzlich erschliessen?", value=st.session_state.get("vertrieb_zusatz", ""), key="vertrieb_zusatz")
st.text_area("12. Welche Kanäle schließt du bewusst aus – und warum?", value=st.session_state.get("vertrieb_ausgeschlossen", ""), key="vertrieb_ausgeschlossen")
st.text_input("13. Zu welchem Zeitpunkt möchtest du das Spiel veröffentlichen?", value=st.session_state.get("veroeffentlichung", ""), key="veroeffentlichung")
st.slider("14. Wie viel Zeit investierst du pro Woche in den Vertrieb? (in Stunden)", 0, 30,
          value=st.session_state.get("vertriebszeit", 0), key="vertriebszeit")

st.radio("15. Wärst du bereit, diesen Aufwand zu erhöhen?", [
    "Ja, mit Unterstützung", "Ja, zeitlich begrenzt", "Nein, lieber effizienter werden"
], index=["Ja, mit Unterstützung", "Ja, zeitlich begrenzt", "Nein, lieber effizienter werden"].index(
    st.session_state.get("vertriebsaufwand", "Ja, mit Unterstützung")
), key="vertriebsaufwand")

st.checkbox("16. Planst du strategische Partnerschaften oder Kooperationen?",
            value=st.session_state.get("kooperation", False), key="kooperation")
st.text_input("→ Falls ja, bitte Details", value=st.session_state.get("kooperation_details", ""), key="kooperation_details")
st.text_input("17. Welche Regionen oder Zielgruppen möchtest du stärker ansprechen?",
              value=st.session_state.get("vertriebsregionen", ""), key="vertriebsregionen")

st.markdown("#### 🔶 Marktanalyse & Wettbewerb")

st.text_area("Welche vergleichbaren Spiele gibt es – wie positionierst du dich im Vergleich?",
             value=st.session_state.get("wettbewerb_spiele", ""), key="wettbewerb_spiele")
st.text_area("Was gefällt dir an den erfolgreichsten Spielen deiner Nische?",
             value=st.session_state.get("vorbilder", ""), key="vorbilder")
st.text_area("Wo siehst du Marktlücken oder Trends?", value=st.session_state.get("marktluecken", ""), key="marktluecken")
st.text_input("Wer oder welches Spiel ist dein größter Konkurrent?", value=st.session_state.get("konkurrenz", ""), key="konkurrenz")

# 💾 Speicherfunktion
def speichere_kapitel_3():
    daten = {
        "kapitel_3": {
            "community_orte": st.session_state.get("community_orte", []),
            "community_groesse": st.session_state.get("community_groesse", 0),
            "community_einschaetzung": st.session_state.get("community_einschaetzung", ""),
            "interaktion": st.session_state.get("interaktion", ""),
            "aktivierungsformate": st.session_state.get("aktivierungsformate", []),
            "community_erfolgreich": st.session_state.get("community_erfolgreich", ""),
            "persoenliche_community_arbeit": st.session_state.get("persoenliche_community_arbeit", ""),
            "community_verzicht": st.session_state.get("community_verzicht", ""),
            "plattformen_neu": st.session_state.get("plattformen_neu", []),
            "plattformen_sonst": st.session_state.get("plattformen_sonst", ""),
            "vertrieb_aktiv": st.session_state.get("vertrieb_aktiv", []),
            "vertrieb_andere": st.session_state.get("vertrieb_andere", ""),
            "vertrieb_kuchen": {kanal: st.session_state.get(f"kuchen_{kanal}", 0) for kanal in st.session_state.get("vertrieb_aktiv", [])},
            "vertrieb_zusatz": st.session_state.get("vertrieb_zusatz", ""),
            "vertrieb_ausgeschlossen": st.session_state.get("vertrieb_ausgeschlossen", ""),
            "veroeffentlichung": st.session_state.get("veroeffentlichung", ""),
            "vertriebszeit": st.session_state.get("vertriebszeit", 0),
            "vertriebsaufwand": st.session_state.get("vertriebsaufwand", ""),
            "kooperation": st.session_state.get("kooperation", False),
            "kooperation_details": st.session_state.get("kooperation_details", ""),
            "vertriebsregionen": st.session_state.get("vertriebsregionen", ""),
            "wettbewerb_spiele": st.session_state.get("wettbewerb_spiele", ""),
            "vorbilder": st.session_state.get("vorbilder", ""),
            "marktluecken": st.session_state.get("marktluecken", ""),
            "konkurrenz": st.session_state.get("konkurrenz", "")
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

# 🔘 Navigation
st.markdown("---")
col1, _, col3 = st.columns([1, 5, 1])

with col1:
    if st.button("⬅️ Zurück zu Kapitel 2"):
        speichere_kapitel_3()
        st.switch_page("pages/2_Marke.py")

with col3:
    if st.button("➡️ Weiter zu Kapitel 4"):
        speichere_kapitel_3()
        st.success("✅ Kapitel 3 gespeichert.")
        st.switch_page("pages/4_Ressourcen.py")
