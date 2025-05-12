import os
import json
import re
import smtplib
from email.message import EmailMessage
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ---------- Hilfsfunktionen ----------
def clean_unicode(text):
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "–": "-", "—": "-", "‘": "'", "’": "'", "“": '"', "”": '"',
        "…": "...", "💡": "*", "⬇️": "->", "🧠": "[i]",
        "🇯": "[ziel]", "📦": "[paket]"
    }
    return re.sub("|".join(map(re.escape, replacements)), lambda m: replacements[m.group(0)], text)

def sende_per_mail(dateipfad):
    empfaenger = "meinspieleleitfaden@gmail.com"
    msg = EmailMessage()
    msg["Subject"] = "KI-Prompt Export"
    msg["From"] = st.secrets["EMAIL_USER"]
    msg["To"] = empfaenger
    msg.set_content("Im Anhang findest du den generierten Prompt.")

    with open(dateipfad, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(dateipfad)
        msg.add_attachment(file_data, maintype="text", subtype="plain", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASS"])
        smtp.send_message(msg)

# ---------- Setup ----------
st.set_page_config(page_title="Kapitel 7: Auswertung", layout="wide")
st.title("📊 Kapitel 7: Auswertung deines Spiels")

load_dotenv()
client = OpenAI()

if "projektname" not in st.session_state or not st.session_state.projektname:
    st.warning("Bitte gib zuerst auf der Seite Spielidee einen Projektnamen ein.")
    st.stop()

projektname = st.session_state.projektname
daten_pfad = f"data/{projektname}.json"
st.markdown(f"**📁 Projekt:** `{projektname}`")

if not os.path.exists(daten_pfad):
    st.error("Projektdatei nicht gefunden.")
    st.stop()

with open(daten_pfad, "r", encoding="utf-8") as f:
    try:
        daten = json.load(f)
    except json.JSONDecodeError:
        st.error("Die Projektdatei ist ungültig.")
        st.stop()

# ---------- Leitfaden generieren ----------
leitfaden_text = ""
if st.button("✨ Jetzt Leitfaden generieren"):
    try:
        alle_antworten = []
        for kapitel, inhalte in daten.items():
            if isinstance(inhalte, dict):
                for k, v in inhalte.items():
                    v = ", ".join(map(str, v)) if isinstance(v, list) else str(v)
                    alle_antworten.append(f"{k}: {v}")
            else:
                alle_antworten.append(str(inhalte))

        prompt = (
                "Du bist ein hochspezialisierter Marketingstratege, Vertriebsexperte und Finanzplaner mit Fokus auf analoge Spiele. "
                "Deine Aufgabe ist es, auf Basis der unten stehenden Projektdaten ein vollständiges, kreatives und operativ umsetzbares Marketing-, Vertriebs- und Finanzierungs­konzept "
                "für das neue Brettspiel zu entwickeln – mit maximalem inhaltlichem Mehrwert und aktiver Eigenleistung deinerseits.\n\n"
                "Ziel: Ein detaillierter, ideenreicher und umsetzungsorientierter Masterplan mit smartem Zeitplan, realistischem Budgetrahmen, wirkungsvollen Kanälen und konkreten Inhalten. "
                "Dieser Masterplan muss **über die Projektbeschreibung hinausdenken** und eigenständige, realistische, kreative und passende Vorschläge liefern. "
                "Wiederholungen aus der Beschreibung sind zu vermeiden – stattdessen sollen auf dieser Basis konkrete Maßnahmen, Posts, Tools, Texte, Visuals und KPIs entstehen.\n\n"
                "⚠️ Deine Ausarbeitung muss …\n"
                "- ausnahmslos **konkret, umsetzbar, terminiert und realistisch** sein\n"
                "- **kreative eigene Ideen** liefern, z. B. für Instagram-Stories, Audioformate, Kooperationen, Texte, Hashtags, Events, Storytelling, Stretch Goals, Presseansprachen etc.\n"
                "- **Inhalte datumsbezogen als Tabelle auflisten**, z. B. (11.05., Instagram Story, Muttertagsspecial: „Jetzt gemeinsam mit der Familie Lumora entdecken.“)\n"
                "- **Social-Media-Content konkret vorschlagen** (inkl. Bildideen, Hashtags, Tools, Veröffentlichungszeitpunkt)\n"
                "- **Personas adressieren** mit zugeschnittenen Maßnahmen\n"
                "- **ein echtes Finanzierungskonzept liefern**, das Förderprogramme, Crowdfunding, Stretch Goals, Preismodelle und Puffer berücksichtigt\n"
                "- **alle Kapitel vollständig ausarbeiten**, numeriert nach folgender Liste\n\n"
                "📌 Gib die folgenden 13 Kapitel **direkt, lückenlos und in der angegebenen Reihenfolge** aus (nummeriert):\n"
                "1. Situationsanalyse\n"
                "2. Marketingziele (SMART)\n"
                "3. Zielgruppen & Personas\n"
                "4. Positionierung & Markenstrategie\n"
                "5. Marketingstrategien (7 Ps)\n"
                "6. Social-Media-Strategie & Redaktionsplan\n"
                "7. Community-Aufbau & -Pflege\n"
                "8. Finanzierungskonzept\n"
                "9. Vertriebsstrategie\n"
                "10. Maßnahmenplan & To-dos\n"
                "11. Budget- & Ressourcenplanung\n"
                "12. KPIs & Erfolgskontrolle\n"
                "13. Risikoanalyse & Notfallpläne\n\n"
                "✳️ Am Ende folgt eine strukturierte **Zusammenfassung mit Stichpunkten zu**:\n"
                "- Wichtigste Marketingziele\n"
                "- Zentrale Maßnahmen & Zeitpunkte\n"
                "- Gewählte Kanäle & Formate\n"
                "- Priorisierte To-dos\n"
                "- Budgetrahmen\n"
                "- KPIs zur Erfolgskontrolle\n\n"
                "🎯 Erinnere dich durchgehend an folgende Regeln:\n"
                "→ **Nichts darf vage sein.**\n"
                "→ **Keine Wiederholung der Eingaben.**\n"
                "→ **Keine allgemeinen Formulierungen.**\n"
                "→ **Alles muss mitdenken, auf das Projekt zugeschnitten und originell sein.**\n\n"
                "Hier sind alle relevanten Angaben zum Projekt:\n\n"
                + "\n".join(alle_antworten)
            )



        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        leitfaden_text = response.choices[0].message.content

        # Prompt speichern und automatisch mailen
        prompt_dateipfad = f"data/{projektname}_prompt.txt"
        with open(prompt_dateipfad, "w", encoding="utf-8") as f:
            f.write(prompt)

        sende_per_mail(prompt_dateipfad)

        st.success("Leitfaden erfolgreich generiert!")
        st.markdown(leitfaden_text)

    except Exception as e:
        st.error(f"Fehler beim Generieren oder Senden: {e}")
