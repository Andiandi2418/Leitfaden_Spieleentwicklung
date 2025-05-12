import os
import json
import re
import smtplib
from email.message import EmailMessage
from fpdf import FPDF
from io import BytesIO
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
        "🏯": "[ziel]", "📦": "[paket]"
    }
    return re.sub("|".join(map(re.escape, replacements)), lambda m: replacements[m.group(0)], text)

def sende_per_mail(dateipfad, empfaenger):
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

# ---------- E-Mail-Adresse erfassen ----------
empfaenger = st.text_input("📧 E-Mail-Adresse für den Versand")

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
            "für ein neu entwickeltes Brettspiel zu erstellen.\n"
            "Ziel: Ein vollständiger und sehr detaillierter Plan, der in der Realität mit einem kleinen Team, begrenztem Budget und hoher strategischer Klarheit umgesetzt werden kann – aufgeteilt in 13 logisch aufgebaute Kapitel. \n"
            "Bitte berücksichtige dabei die besonderen Wünsche, Einschränkungen, Zielgruppen, Zeitressourcen, Ausschlüsse und inhaltlichen Besonderheiten des Spiels (siehe Projektdaten unten).\n"
            "Hier sind alle Angaben des Projekts:\n\n"
            + "\n".join(alle_antworten)
        )

        # Prompt speichern
        prompt_dateipfad = f"data/{projektname}_prompt.txt"
        with open(prompt_dateipfad, "w", encoding="utf-8") as f:
            f.write(prompt)

        if empfaenger:
            sende_per_mail(prompt_dateipfad, empfaenger)
            st.success(f"📧 Die Datei wurde automatisch an {empfaenger} gesendet.")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        leitfaden_text = response.choices[0].message.content
        st.success("Leitfaden erfolgreich generiert!")
        st.markdown(leitfaden_text)

    except Exception as e:
        st.error(f"Fehler beim Generieren des Leitfadens: {e}")

# ---------- PDF-Erstellung ----------
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf", uni=True)

pdf.set_font("DejaVu", "B", size=14)
pdf.cell(190, 10, clean_unicode(f"Projekt-Auswertung: {projektname}"), ln=True)
pdf.ln(5)

pdf.set_font("DejaVu", "", size=11)

kapitel_titel = {
    "kapitel_1": "Kapitel 1: Spielidee",
    "kapitel_2": "Kapitel 2: Marke & Markenstrategie",
    "kapitel_3": "Kapitel 3: Community & Vertrieb",
    "kapitel_4": "Kapitel 4: Ressourcen & Finanzierung",
    "kapitel_5": "Kapitel 5: Strategie & Zeitplanung",
    "kapitel_6": "Kapitel 6: Persönliche Erwartungen & Leitfaden-Nutzen"
}

for k in sorted(kapitel_titel.keys()):
    inhalte = daten.get(k, {})
    titel = kapitel_titel[k]

    pdf.set_font("DejaVu", "B", size=13)
    pdf.set_text_color(0, 0, 128)
    pdf.cell(190, 10, clean_unicode(titel), ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", size=11)
    pdf.ln(1)

    if not isinstance(inhalte, dict) or not inhalte:
        pdf.multi_cell(190, 8, "[Keine Daten in diesem Kapitel hinterlegt]")
        pdf.ln(3)
        continue

    for key in sorted(inhalte.keys()):
        key_clean = clean_unicode(key.replace("_", " ").capitalize())
        val = inhalte[key]
        val_str = ", ".join(clean_unicode(str(v)) for v in val) if isinstance(val, list) else clean_unicode(str(val))
        pdf.multi_cell(190, 8, f"{key_clean}: {val_str}")

    pdf.ln(5)

if leitfaden_text:
    pdf.set_font("DejaVu", "B", size=13)
    pdf.set_text_color(128, 0, 0)
    pdf.cell(190, 10, "Kapitel 7: KI-generierter Leitfaden", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", size=11)
    pdf.ln(1)
    for line in clean_unicode(leitfaden_text).split("\n"):
        pdf.multi_cell(190, 8, line)
    pdf.ln(5)

pdf_bytes = BytesIO()
pdf.output(pdf_bytes)
pdf_bytes.seek(0)

st.download_button(
    label="📄 PDF herunterladen",
    data=pdf_bytes,
    file_name=f"{projektname}_auswertung.pdf",
    mime="application/pdf"
)
