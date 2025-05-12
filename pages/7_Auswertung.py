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
            "Erstelle eine konkrete, umsetzbare und kreative Vermarktungs-, Vertriebs- und Finanzierungsstrategie für ein neues Brettspiel. "
            "Ziel ist ein realistischer, direkt umsetzbarer Plan mit originellen Ideen, Zeitplänen, Textvorschlägen, Finanzierungsstrategien und Community-Maßnahmen.\n\n"
            
            "⚠️ Verwende die folgenden Projektangaben aktiv für alle Inhalte. Sie sind vollständig ausgefüllt und enthalten wichtige Informationen, auf denen deine Vorschläge aufbauen sollen. "
            "Entwickle daraus eigenständig Ideen, Inhalte, Zeitpläne und Konzepte – keine Wiederholungen oder allgemeinen Aussagen.\n\n"
        
            "✅ Deine Antwort soll beinhalten:\n"
            "- realistische Social-Media-Posts mit Datum, Text, Bildideen, Hashtags\n"
            "- Vorschläge für Community-Aktionen und Audio-Formate\n"
            "- konkrete Finanzierungsstrategie mit mehreren Bausteinen\n"
            "- Tabellen mit To-dos und Redaktionsplan\n\n"
            
            "📌 Gliedere deine Antwort in diese Kapitel:\n"
            "1. Situationsanalyse\n"
            "2. Marketingziele\n"
            "3. Zielgruppen & Personas\n"
            "4. Markenstrategie\n"
            "5. Marketingmaßnahmen\n"
            "6. Social-Media-Plan (inkl. Tabelle mit konkreten Inhalten und Terminen)\n"
            "7. Community-Aufbau\n"
            "8. Finanzierungskonzept\n"
            "9. Vertriebsstrategie\n"
            "10. To-do-Plan (mit Terminen)\n"
            "11. Budgetplanung\n"
            "12. Erfolgskontrolle\n"
            "13. Risiken & Lösungen\n\n"
            
            "Hier sind die Projektdaten:\n\n"
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
