import os
import json
import re
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
from fpdf import FPDF
from io import BytesIO

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
st.title("\U0001F4CA Kapitel 7: Auswertung deines Spiels")

load_dotenv()
client = OpenAI()

if "projektname" not in st.session_state or not st.session_state.projektname:
    st.warning("Bitte gib zuerst auf der Seite Spielidee einen Projektnamen ein.")
    st.stop()

projektname = st.session_state.projektname
daten_pfad = f"data/{projektname}.json"
st.markdown(f"**\U0001F4C1 Projekt:** `{projektname}`")

if not os.path.exists(daten_pfad):
    st.error("Projektdatei nicht gefunden.")
    st.stop()

with open(daten_pfad, "r", encoding="utf-8") as f:
    try:
        daten = json.load(f)
    except json.JSONDecodeError:
        st.error("Die Projektdatei ist ungültig.")
        st.stop()

leitfaden_text = ""

# ---------- Leitfaden generieren ----------
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

        with open("prompt_basis.txt", "r", encoding="utf-8") as pfile:
            prompt_basis = pfile.read()

        prompt = prompt_basis + "\n\n" + "\n".join(alle_antworten)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        leitfaden_text = response.choices[0].message.content

        prompt_dateipfad = f"data/{projektname}_prompt.txt"
        with open(prompt_dateipfad, "w", encoding="utf-8") as f:
            f.write(prompt)

        sende_per_mail(prompt_dateipfad)

        st.success("Leitfaden erfolgreich generiert!")
        st.markdown(leitfaden_text)

        # ---------- PDF generieren ----------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
        pdf.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf", uni=True)
        pdf.set_font("DejaVu", "B", size=14)
        pdf.cell(0, 10, "\U0001F4D8 KI-generierter Leitfaden", ln=True)
        pdf.ln(5)

        pdf.set_font("DejaVu", "", size=11)
        for line in leitfaden_text.split("\n"):
            pdf.multi_cell(0, 8, line)

        leitfaden_bytes = BytesIO()
        pdf.output(leitfaden_bytes)
        leitfaden_bytes.seek(0)

        st.download_button(
            label="⬇️ Nur KI-Leitfaden als PDF herunterladen",
            data=leitfaden_bytes,
            file_name=f"{projektname}_leitfaden.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"Fehler beim Generieren oder Senden: {e}")
