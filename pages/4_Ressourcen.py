import os
import json
import streamlit as st

# 🌐 Seite konfigurieren
st.set_page_config(page_title="Kapitel 4: Ressourcen & Finanzierung", layout="wide")

if "projektname" not in st.session_state or not st.session_state.projektname:
    st.warning("Bitte gib zuerst auf der Seite Spielidee einen Projektnamen ein.")
    st.stop()

projektname = st.session_state.projektname
st.markdown(f"**📁 Projekt:** `{projektname}`")
st.title("💰 Kapitel 4: Ressourcen & Finanzierung")

daten_pfad = f"data/{projektname}.json"
os.makedirs("data", exist_ok=True)

# 🔄 Daten aus Datei laden
if os.path.exists(daten_pfad):
    with open(daten_pfad, "r", encoding="utf-8") as f:
        gespeicherte_daten = json.load(f)
        gespeicherte_werte = gespeicherte_daten.get("kapitel_4", {})
        for key, val in gespeicherte_werte.items():
            if key not in st.session_state:
                st.session_state[key] = val

# 🧩 Eingabefelder
st.markdown("#### 🔶️ Zeitliche Ressourcen")

st.slider("1. Wie viele Stunden pro Woche kannst du in dieses Spiel investieren?", 0, 40,
          value=st.session_state.get("zeit_spiel", 0), key="zeit_spiel")

zeitraum = st.selectbox("2. Über welchen Zeitraum planst du mit dieser Verfügbarkeit?",
                        ["3 Monate", "6 Monate", "12 Monate", "Bis Launch", "Andere"],
                        index=["3 Monate", "6 Monate", "12 Monate", "Bis Launch", "Andere"].index(
                            st.session_state.get("zeitraum", "3 Monate")),
                        key="zeitraum")

if zeitraum == "Andere":
    st.text_input("→ Bitte Zeitraum eintragen", value=st.session_state.get("zeitraum_andere", ""), key="zeitraum_andere")

st.multiselect("3. Welche Aufgaben kannst du schnell und effizient selbst übernehmen?", [
    "Regelentwicklung", "Illustration / Grafik", "Kommunikation", "Social Media",
    "Organisation", "Versand & Logistik", "Andere"
], default=st.session_state.get("zeit_effizient", []), key="zeit_effizient")

st.text_input("→ Wenn 'Andere': Bitte eintragen", value=st.session_state.get("zeit_effizient_andere", ""), key="zeit_effizient_andere")

st.text_area("4. Welche Aufgaben kosten dich besonders viel Zeit oder Energie?", value=st.session_state.get("zeit_kosten", ""), key="zeit_kosten")

st.radio("5. Beeinflussen externe Ereignisse deinen Zeitplan?", ["Ja", "Nein"],
         index=["Ja", "Nein"].index(st.session_state.get("zeit_extern", "Nein")), key="zeit_extern")

st.text_input("→ Falls ja: Welche?", value=st.session_state.get("zeit_extern_text", ""), key="zeit_extern_text")

st.markdown("#### 🔶 Kapital & Finanzierung")

st.number_input("6. Wie viel Budget steht dir aktuell zur Verfügung?", min_value=0, step=100,
                value=st.session_state.get("budget_aktuell", 0), key="budget_aktuell")

st.selectbox("Währung", ["CHF", "EUR", "USD"],
             index=["CHF", "EUR", "USD"].index(st.session_state.get("budget_waehrung", "CHF")), key="budget_waehrung")

st.number_input("7. Wie hoch wäre dein Wunschbudget?", min_value=0, step=100,
                value=st.session_state.get("budget_wunsch", 0), key="budget_wunsch")

st.multiselect("8. Welche Kostenpositionen sind eingeplant?", [
    "Produktion", "Illustrationen / Grafik", "Marketing", "Versand / Lager",
    "Messeauftritte", "Software / Tools", "Anderes"
], default=st.session_state.get("kosten_positionen", []), key="kosten_positionen")

st.text_input("→ Wenn 'Anderes': Bitte eintragen", value=st.session_state.get("kosten_andere", ""), key="kosten_andere")

st.number_input("9. Welcher Umsatz wäre nötig, um kostendeckend zu sein (Break-even)?",
                min_value=0, step=100, value=st.session_state.get("break_even", 0), key="break_even")

st.multiselect("10. Welche Finanzierungsformen ziehst du in Betracht?", [
    "Crowdfunding", "Vorbestellungen", "Verlag / Lizenzen", "Investoren",
    "Öffentliche Fördergelder", "Eigenmittel", "Andere"
], default=st.session_state.get("finanzierung_optionen", []), key="finanzierung_optionen")

st.text_input("→ Wenn 'Andere': Bitte eintragen", value=st.session_state.get("finanzierung_andere", ""), key="finanzierung_andere")

st.radio("11. Bist du offen für alternative Finanzierungswege?", ["Ja", "Nein", "Kommt drauf an"],
         index=["Ja", "Nein", "Kommt drauf an"].index(st.session_state.get("finanzierung_offen", "Ja")),
         key="finanzierung_offen")

st.text_area("12. Was kommt für dich nicht infrage – und warum?",
             value=st.session_state.get("finanzierung_ausgeschlossen", ""), key="finanzierung_ausgeschlossen")

st.markdown("#### 🔶 Know-how & Unterstützung")

st.multiselect("13. Welche Bereiche kannst du gut abdecken?", [
    "Grafik", "Regelentwicklung", "Marketing", "Finanzen", "Projektleitung", "Eventmanagement"
], default=st.session_state.get("kenntnisse", []), key="kenntnisse")

st.text_area("14. Wo brauchst du Unterstützung?", value=st.session_state.get("support_bedarf", ""), key="support_bedarf")

st.checkbox("15. Hast du bereits ein Netzwerk oder Team, das dich unterstützt?",
            value=st.session_state.get("netzwerk", False), key="netzwerk")

st.text_input("→ Falls ja, wer oder was?", value=st.session_state.get("netzwerk_text", ""), key="netzwerk_text")

st.multiselect("16. Nutzt du Tools oder Services? (z. B. Trello, Canva, Print-on-Demand)", [
    "Trello", "Canva", "Print on Demand", "PR-Agentur", "Sonstige"
], default=st.session_state.get("tools", []), key="tools")

st.text_input("→ Weitere Tools, die du nutzt:", value=st.session_state.get("tools_andere", ""), key="tools_andere")

# 💾 Speicherfunktion
def speichere_kapitel_4():
    daten = {
        "kapitel_4": {
            "zeit_spiel": st.session_state.get("zeit_spiel", 0),
            "zeitraum": st.session_state.get("zeitraum", ""),
            "zeitraum_andere": st.session_state.get("zeitraum_andere", ""),
            "zeit_effizient": st.session_state.get("zeit_effizient", []),
            "zeit_effizient_andere": st.session_state.get("zeit_effizient_andere", ""),
            "zeit_kosten": st.session_state.get("zeit_kosten", ""),
            "zeit_extern": st.session_state.get("zeit_extern", ""),
            "zeit_extern_text": st.session_state.get("zeit_extern_text", ""),
            "budget_aktuell": st.session_state.get("budget_aktuell", 0),
            "budget_waehrung": st.session_state.get("budget_waehrung", ""),
            "budget_wunsch": st.session_state.get("budget_wunsch", 0),
            "kosten_positionen": st.session_state.get("kosten_positionen", []),
            "kosten_andere": st.session_state.get("kosten_andere", ""),
            "break_even": st.session_state.get("break_even", 0),
            "finanzierung_optionen": st.session_state.get("finanzierung_optionen", []),
            "finanzierung_andere": st.session_state.get("finanzierung_andere", ""),
            "finanzierung_offen": st.session_state.get("finanzierung_offen", ""),
            "finanzierung_ausgeschlossen": st.session_state.get("finanzierung_ausgeschlossen", ""),
            "kenntnisse": st.session_state.get("kenntnisse", []),
            "support_bedarf": st.session_state.get("support_bedarf", ""),
            "netzwerk": st.session_state.get("netzwerk", False),
            "netzwerk_text": st.session_state.get("netzwerk_text", ""),
            "tools": st.session_state.get("tools", []),
            "tools_andere": st.session_state.get("tools_andere", "")
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
    if st.button("⬅️ Zurück zu Kapitel 3"):
        speichere_kapitel_4()
        st.switch_page("pages/3_Community_Vertrieb.py")
with col3:
    if st.button("➡️ Weiter zu Kapitel 5"):
        speichere_kapitel_4()
        st.success("✅ Kapitel 4 gespeichert.")
        st.switch_page("pages/5_Strategie.py")
