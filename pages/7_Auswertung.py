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
            "Deine Aufgabe ist es, eine umfassende, strategisch fundierte, realistisch umsetzbare und kreative Vermarktungs-, Vertriebs- und Finanzierungsstrategie "
            "für ein neu entwickeltes Brettspiel zu erstellen – vollständig abgestimmt auf die Projektdaten weiter unten.\n\n"
            "Ziel: Ein vollständig ausgearbeiteter, extrem detaillierter und umsetzungsorientierter Masterplan, der mit einem kleinen Team und begrenztem Budget realistisch durchführbar ist. "
            "Alle Inhalte müssen in die Tiefe gehen, individuell für dieses Projekt formuliert sein und dürfen keinerlei allgemeine Phrasen oder Platzhalter enthalten.\n\n"
            "⚠️ **Wichtig: Jede deiner Ausführungen soll …**\n"
            "- maximal konkret und realistisch sein (keine Theorie, keine Floskeln!)\n"
            "- mit klaren Begründungen und Beispielen unterlegt sein\n"
            "- echte Handlungsempfehlungen liefern, die direkt umgesetzt werden können\n"
            "- bei jeder Gelegenheit Beispiele, Templates, Tabellen, Formulierungen, Zeitpläne etc. enthalten\n"
            "- bei Social Media & Contentplanung: auch Textideen, Hashtags, Bildvorschläge, Tools und Veröffentlichungszeitpunkte nennen\n"
            "- alle Kapitel und Unterfragen vollständig beantworten\n\n"
            "📌 Gliedere deine Ausarbeitung **vollständig und direkt** in exakt diese 13 Kapitel (in der Reihenfolge, nummeriert):\n"
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
            "🔄 **Gib alle Kapitel direkt in einem einzigen, durchgängigen Text aus. Keine Rückfragen, keine Pausen.**\n\n"
            "✳️ Abschluss: Erstelle am Ende eine strukturierte Zusammenfassung mit Stichpunkten zu:\n"
            "- Wichtigste Marketingziele\n"
            "- Zentrale Maßnahmen & Zeitpunkte\n"
            "- Gewählte Kanäle & Formate\n"
            "- Priorisierte To-dos\n"
            "- Budgetrahmen\n"
            "- KPIs zur Erfolgskontrolle\n\n"
            "🎯 Erinnere dich während der gesamten Ausarbeitung immer daran:\n"
            "→ Keine vagen Aussagen.\n"
            "→ Keine leeren Floskeln oder Platzhalter.\n"
            "→ Keine Wiederholungen.\n"
            "→ Alles muss spezifisch für das Projekt sein.\n\n"
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
