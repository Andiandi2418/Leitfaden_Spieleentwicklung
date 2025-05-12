import os
import json
import streamlit as st

# 🌐 Seite konfigurieren
st.set_page_config(page_title="Kapitel 6: Persönliche Erwartungen & Leitfaden-Nutzen", layout="wide")

if "projektname" not in st.session_state or not st.session_state.projektname:
    st.warning("Bitte gib zuerst auf der Seite Spielidee einen Projektnamen ein.")
    st.stop()

projektname = st.session_state.projektname
st.markdown(f"**📁 Projekt:** `{projektname}`")
st.title("🎯 Kapitel 6: Persönliche Erwartungen & Leitfaden-Nutzen")

daten_pfad = f"data/{projektname}.json"
os.makedirs("data", exist_ok=True)

# 🔄 Daten laden
if os.path.exists(daten_pfad):
    with open(daten_pfad, "r", encoding="utf-8") as f:
        gespeicherte_daten = json.load(f)
        gespeicherte_werte = gespeicherte_daten.get("kapitel_6", {})
        for key, val in gespeicherte_werte.items():
            if key not in st.session_state:
                st.session_state[key] = val

# 🧩 Eingabefelder
st.markdown("#### 🔶 Erwartungen an den Leitfaden")

st.text_area("1. Welche Herausforderungen hast du aktuell beim Marketing oder bei der Finanzierung?",
             value=st.session_state.get("leitfaden_hürden", ""), key="leitfaden_hürden")

st.multiselect("2. Was erhoffst du dir konkret vom Leitfaden?", [
    "Struktur", "Inspiration", "Schritt-für-Schritt-Anleitung", "Entscheidungshilfe",
    "Benchmarks / Vergleichswerte", "Zeitplan auf ein Jahr heraus", "Social Media Stategie"
], default=st.session_state.get("leitfaden_erwartungen", []), key="leitfaden_erwartungen")

st.text_area("3. Welche Themen sollen auf keinen Fall zu technisch oder zu theoretisch behandelt werden?",
             value=st.session_state.get("leitfaden_themen_warnung", ""), key="leitfaden_themen_warnung")

st.multiselect("4. Welche Formate helfen dir beim Umsetzen?", [
    "Checklisten", "Canva-Vorlagen", "interaktive Module", "Beispiele & Best Practices", "Downloadbare PDFs"
], default=st.session_state.get("leitfaden_formate", []), key="leitfaden_formate")

st.markdown("#### 🔶 Ausblick & Perspektiven")

st.text_area("5. Was möchtest du nach der Veröffentlichung des Spiels erreichen?",
             value=st.session_state.get("ausblick_ziel", ""), key="ausblick_ziel")

st.multiselect("6. Welche Themen willst du künftig vertiefen?", [
    "Internationalisierung", "Community-Building", "Storytelling", "Nachhaltigkeit", "Verlag gründen", "Andere"
], default=st.session_state.get("ausblick_themen", []), key="ausblick_themen")

st.text_input("→ Falls 'Andere': Bitte hier eintragen",
              value=st.session_state.get("ausblick_themen_andere", ""), key="ausblick_themen_andere")

st.multiselect("7. Wie könnte dich ein erweitertes Angebot unterstützen?", [
    "Coaching", "Peer-Mentoring", "Toolkits", "Webinare", "Netzwerk-Treffen"
], default=st.session_state.get("ausblick_unterstuetzung", []), key="ausblick_unterstuetzung")

st.markdown("#### 🔶 Wünsche")

st.text_area("Was möchtest du der KI am Ende noch mitgeben?",
             value=st.session_state.get("letzter_wunsch", ""), key="letzter_wunsch")

# 💾 Speicherfunktion
def speichere_kapitel_6():
    daten = {
        "kapitel_6": {
            "leitfaden_hürden": st.session_state.get("leitfaden_hürden", ""),
            "leitfaden_erwartungen": st.session_state.get("leitfaden_erwartungen", []),
            "leitfaden_themen_warnung": st.session_state.get("leitfaden_themen_warnung", ""),
            "leitfaden_formate": st.session_state.get("leitfaden_formate", []),
            "ausblick_ziel": st.session_state.get("ausblick_ziel", ""),
            "ausblick_themen": st.session_state.get("ausblick_themen", []),
            "ausblick_themen_andere": st.session_state.get("ausblick_themen_andere", ""),
            "ausblick_unterstuetzung": st.session_state.get("ausblick_unterstuetzung", []),
            "letzter_wunsch": st.session_state.get("letzter_wunsch", "")
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
col1, spacer, col3 = st.columns([2, 8, 2])  # Summe = 12
with col1:
    if st.button("⬅️ Zurück zu Kapitel 5"):
        speichere_kapitel_6()
        st.switch_page("pages/5_Strategie.py")

with col3:
    if st.button("➡️ Weiter zu Auswertung"):
        speichere_kapitel_6()
        st.success("✅ Kapitel 6 gespeichert.")
        st.switch_page("pages/7_Auswertung.py")
