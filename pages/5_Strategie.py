import os
import json
from datetime import datetime as dt, date
import streamlit as st


# 🌐 Seite konfigurieren
st.set_page_config(page_title="Kapitel 5: Strategie & Zeitplanung", layout="wide")

# 📁 Projektname prüfen
if "projektname" not in st.session_state or not st.session_state.projektname:
    st.warning("Bitte gib zuerst auf der Seite Spielidee einen Projektnamen ein.")
    st.stop()

projektname = st.session_state.projektname
daten_pfad = f"data/{projektname}.json"
os.makedirs("data", exist_ok=True)
st.markdown(f"**📁 Projekt:** `{projektname}`")
st.title("⏱️ Kapitel 5: Strategie & Zeitplanung")

# 🛠️ Robuste Datumsumwandlung
def parse_date(val):
    if isinstance(val, list) and val:
        val = val[0]
    if isinstance(val, str):
        try:
            return dt.strptime(val, "%Y-%m-%d").date()
        except Exception:
            return date.today()
    if isinstance(val, date):
        return val
    return date.today()

# 🧼 Reparatur verdächtiger Felder beim Laden
def repariere_datum(name):
    if name in st.session_state:
        st.session_state[name] = parse_date(st.session_state[name])

# 🔄 Daten laden & session_state initialisieren
if os.path.exists(daten_pfad):
    with open(daten_pfad, "r", encoding="utf-8") as f:
        gespeicherte_daten = json.load(f)
        gespeicherte_werte = gespeicherte_daten.get("kapitel_5", {})
        for key, val in gespeicherte_werte.items():
            if key not in st.session_state:
                st.session_state[key] = val

# 🧼 Datumsfelder reparieren
for feld in ["messetermin", "vorverkauf", "produktion", "versand", "kommunikationsstart"]:
    repariere_datum(feld)

# 🧩 Eingabefelder
st.markdown("#### 🔶 Zeitplan für das Spiel")

st.text_area("1. Was ist für das kommende Jahr geplant? (bitte als Meilensteine strukturieren)",
             value=st.session_state.get("jahresplanung", ""), key="jahresplanung")
st.date_input("→ Produktionsstart", value=st.session_state.get("produktion"), key="produktion")

st.date_input("→ Vorverkaufsstart", value=st.session_state.get("vorverkauf"), key="vorverkauf")

st.date_input("→ Versandbeginn", value=st.session_state.get("versand"), key="versand")

st.text_area("3. Gibt es interne Deadlines oder Zeitpuffer?",
             value=st.session_state.get("deadlines", ""), key="deadlines")

st.markdown("#### 🔶 Kommunikationsstrategie")

st.date_input("4. Ab wann willst du über das Spiel kommunizieren?",
              value=st.session_state.get("kommunikationsstart"), key="kommunikationsstart")

st.multiselect("5. Welche Kommunikationsformate planst du?", [
    "Teaser", "Dev-Blogs", "Behind the Scenes", "Live-Streams",
    "Previews", "Newsletter", "Werbung (Ads)"
], default=st.session_state.get("kommunikationsformate", []), key="kommunikationsformate")

st.text_area("6. Wer soll wann und wie vom Spiel erfahren?",
             value=st.session_state.get("zielgruppen_story", ""), key="zielgruppen_story")

st.multiselect("7. Welche Plattformen sind für dich zentral?", [
    "Instagram", "Discord", "YouTube", "TikTok", "Website", "Presseverteiler", "Anderes"
], default=st.session_state.get("plattformen", []), key="plattformen")

st.text_input("→ Wenn 'Anderes': Bitte eintragen",
              value=st.session_state.get("plattformen_andere", ""), key="plattformen_andere")

st.markdown("#### 🔶 Reichweite & Nachhaltigkeit")

st.radio("8. Wie breit möchtest du deine Botschaft streuen?",
         ["Lokal", "National", "International"],
         index=["Lokal", "National", "International"].index(st.session_state.get("reichweite", "National")),
         key="reichweite")

st.checkbox("9. Planst du gezielte PR- oder Medienansprache?",
            value=st.session_state.get("pr_strategie", False), key="pr_strategie")

st.text_input("→ Falls ja: Welche?", value=st.session_state.get("pr_details", ""), key="pr_details")

st.text_area("10. Was passiert nach dem Launch? (z. B. Sichtbarkeit aufrechterhalten)",
             value=st.session_state.get("nach_launch", ""), key="nach_launch")

st.text_area("11. Gibt es Ideen für Fortsetzungen, Erweiterungen oder langfristige Formate?",
             value=st.session_state.get("fortsetzungen", ""), key="fortsetzungen")

st.markdown("#### 🔶 Post-Launch-Kundenbindung & Retargeting")

st.text_area("Wie möchtest du Käufer:innen nach dem Launch weiter ansprechen?",
             value=st.session_state.get("retargeting", ""), key="retargeting")

st.selectbox("Welche Tools planst du dafür zu nutzen?", [
    "Mailchimp", "Discord", "CRM", "Sonstiges"
], index=["Mailchimp", "Discord", "CRM", "Sonstiges"].index(
    st.session_state.get("newsletter_tools", "Mailchimp")
), key="newsletter_tools")

st.text_input("→ Falls 'Sonstiges': Bitte eintragen",
              value=st.session_state.get("retargeting_tools_andere", ""), key="retargeting_tools_andere")

# 💾 Speicherfunktion
def speichere_kapitel_5():
    daten = {
        "kapitel_5": {
            "jahresplanung": st.session_state.get("jahresplanung", ""),
            "messetermin": str(st.session_state.get("messetermin", "")),
            "vorverkauf": str(st.session_state.get("vorverkauf", "")),
            "produktion": str(st.session_state.get("produktion", "")),
            "versand": str(st.session_state.get("versand", "")),
            "deadlines": st.session_state.get("deadlines", ""),
            "kommunikationsstart": str(st.session_state.get("kommunikationsstart", "")),
            "kommunikationsformate": st.session_state.get("kommunikationsformate", []),
            "zielgruppen_story": st.session_state.get("zielgruppen_story", ""),
            "plattformen": st.session_state.get("plattformen", []),
            "plattformen_andere": st.session_state.get("plattformen_andere", ""),
            "reichweite": st.session_state.get("reichweite", "National"),
            "pr_strategie": st.session_state.get("pr_strategie", False),
            "pr_details": st.session_state.get("pr_details", ""),
            "nach_launch": st.session_state.get("nach_launch", ""),
            "fortsetzungen": st.session_state.get("fortsetzungen", ""),
            "retargeting": st.session_state.get("retargeting", ""),
            "newsletter_tools": st.session_state.get("newsletter_tools", "Mailchimp"),
            "retargeting_tools_andere": st.session_state.get("retargeting_tools_andere", "")
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
    if st.button("⬅️ Zurück zu Kapitel 4"):
        speichere_kapitel_5()
        st.switch_page("pages/4_Ressourcen.py")

with col3:
    if st.button("➡️ Weiter zu Kapitel 6"):
        speichere_kapitel_5()
        st.success("✅ Kapitel 5 gespeichert.")
        st.switch_page("pages/6_Erwartungen.py")
