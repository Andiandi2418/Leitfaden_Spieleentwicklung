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
import fitz  # PyMuPDF

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

def remove_non_latin1(text):
    return ''.join(c for c in text if ord(c) < 256)

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

def render_table(pdf, table_lines):
    header = [remove_non_latin1(cell.strip()) for cell in table_lines[0].split("|")[1:-1]]
    data_rows = [line for line in table_lines[1:] if "|" in line and line.count("|") > 2]
    col_width = (pdf.w - 20) / len(header)

    pdf.set_font("Arial", "B", 10)
    for cell in header:
        pdf.cell(col_width, 8, cell, border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    for row in data_rows:
        cells = [remove_non_latin1(cell.strip()) for cell in row.split("|")[1:-1]]
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        max_height = 0
        cell_heights = []
        for cell in cells:
            lines = pdf.multi_cell(col_width, 5, cell, border=0, align="L", split_only=True)
            height = 5 * len(lines)
            cell_heights.append(height)
            max_height = max(max_height, height)
        for i, cell in enumerate(cells):
            x = x_start + col_width * i
            pdf.set_xy(x, y_start)
            pdf.multi_cell(col_width, 5, cell, border=1, align="L")
        pdf.set_y(y_start + max_height)

# ---------- Streamlit App ----------
st.set_page_config(page_title="Kapitel 7: Auswertung", layout="wide")
st.title("Kapitel 7: Auswertung deines Spiels")

load_dotenv()
client = OpenAI()

if "leitfaden_text" not in st.session_state:
    st.session_state.leitfaden_text = ""

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
                "❗Wichtig: Wenn aus den Projektdaten Einschränkungen hervorgehen – etwa der Ausschluss von bestimmten Finanzierungsformen wie Kickstarter oder Gamefound, "
                "oder der bewusste Verzicht auf bestimmte Kommunikations- oder Vertriebskanäle –, darfst du diese Optionen nicht empfehlen oder einplanen. "
                "Halte dich strikt an die ausgewählten oder ausgeschlossenen Optionen aus dem Projekt.\n"
                "❗Wichtig: Bitte bearbeite jedes der 13 Kapitel möglichst unabhängig voneinander. "
                "Einschränkungen wie Zeit, Budget oder Know-how dürfen nur dann berücksichtigt werden, wenn sie direkt im jeweiligen Kapitel relevant sind. "
                "Vermeide Rückschlüsse von einem Bereich auf einen völlig anderen (z. B. Ressourcen auf die Wettbewerbsanalyse). "
                "Analysiere objektiv und vollständig – auch wenn die Projektangaben auf begrenzte Mittel hindeuten.\n"
                "Jede deiner Ausführungen soll:\n"
                "– praxisnah, konkret und durchführbar sein,\n"
                "– mit klaren Begründungen unterlegt werden,\n"
                "– klare Entscheidungshilfen und Handlungsempfehlungen geben,\n"
                "– kritische Erfolgsfaktoren und typische Fehlerquellen benennen,\n"
                "– bei allen relevanten Punkten mit konkreten Beispielen, Formulierungen, Tabellen, Templates oder Zeitplänen arbeiten,\n"
                "– keine allgemeinen Aussagen machen, sondern individuell auf das Projekt bezogen sein.\n"
                "Bitte gliedere die Ausarbeitung strikt in folgende 13 Punkte und achte auf vollständige Bearbeitung jeder Unterfrage:\n"
                "________________________________________\n"
                "1. Situationsanalyse\n"
                "– Marktanalyse: Trends, Nischen, Chancen & Risiken (z. B. Hybridspiele, Nachhaltigkeit, Bildung)\n"
                "– Zielgruppenanalyse: Drei Zielsegmente mit Bedürfnissen, Kaufverhalten, Einstiegshürden\n"
                "– Wettbewerbsanalyse: Drei externe Konkurrenzspiele mit SWOT-Analyse (Tabellenform)\n"
                "– Eigene Ausgangslage: USP, Entwicklungsstand, Ressourcen (zeitlich, technisch, personell, finanziell)\n"
                "– 🔸 Nutze mindestens eine Tabelle zur SWOT-Analyse\n"
                "2. Marketingziele (SMART)\n"
                "– Drei kurz-, mittel- und langfristige Ziele (z. B. Reichweite, Community, Absatz)\n"
                "– 🔸 Messmethode & Tool pro Ziel angeben\n"
                "3. Zielgruppen & Personas\n"
                "– Hauptzielgruppen\n"
                "– Mind. drei Personas mit Alter, Beruf, Medienverhalten, Kaufentscheidungsprozess, Spielverhalten\n"
                "– 🔸 Tabellenform pro Persona\n"
                "4. Positionierung & Markenstrategie\n"
                "– Markenversprechen\n"
                "– Markenwerte, Designprinzipien, Tonalität, Verpackungsideen\n"
                "– 🔸 Positionierungssatz (z. B. „XYZ ist das einzige Spiel, das …“)\n"
                "5. Marketingstrategien (7 Ps)\n"
                "– Product, Price, Place, Promotion, People, Process, Physical Evidence\n"
                "– 🔸 Tabellen zur Preismodellierung und Promotion mit Kosten/Nutzen\n"
                "6. Social-Media-Strategie & Redaktionsplan\n"
                "– Plattformwahl mit Begründung (nur gewünschte Kanäle!)\n"
                "– 4–5 Content-Säulen\n"
                "– Zwei Monate Redaktionsplan (Datum, Uhrzeit, Kanal, Ziel, Content-Idee, Textvorschlag)\n"
                "– 🔸 Tabellenform mit konkreten Texten\n"
                "7. Community-Aufbau & -Pflege\n"
                "– Strategien für Aufbau, Aktivierung, langfristige Bindung\n"
                "– 🔸 Konkrete Aktionen pro Monat (z. B. August: Audio-Giveaway)\n"
                "8. Finanzierungskonzept\n"
                "– Plattformwahl mit Begründung (nur erlaubte Plattformen!)\n"
                "– Funding-Ziel, Stretch Goals, Pledge-Level (Tabellenform)\n"
                "– Kampagnenstruktur & Kommunikationsfahrplan\n"
                "– 🔸 Beispieltext für Kampagnenstart-Post & Newsletter\n"
                "9. Vertriebsstrategie\n"
                "– Planung für vorgesehene Vertriebskanäle\n"
                "– Tools (z. B. Shopify, Sendcloud), Versandmodell, Beispielrechnung\n"
                "– 🔸 Tabelle: Kanäle mit Startzeitpunkt, Aufwand, Reichweite\n"
                "10. Maßnahmenplan & To-dos\n"
                "– 14-Tage-To-do-Liste\n"
                "– Jahresplan mit Zielen, Events, Launch-Meilensteinen\n"
                "– 🔸 Tabelle mit Verantwortlichen, Aufwand, Tools\n"
                "11. Budget- & Ressourcenplanung\n"
                "– Budgetverteilung (Maßnahme, Kanal, Monat)\n"
                "– Intern vs. extern umsetzbar\n"
                "– 🔸 Tabelle inkl. Reservepositionen\n"
                "12. KPIs & Erfolgskontrolle\n"
                "– Relevante KPIs pro Kanal\n"
                "– Tools zur Auswertung\n"
                "– 🔸 Kritische Schwellenwerte & Reaktionspläne\n"
                "13. Risikoanalyse & Notfallpläne\n"
                "– Risiken mit Eintrittswahrscheinlichkeit, Auswirkung, Maßnahmen\n"
                "– 🔸 Tabelle mit Risikoplanung\n"
                "________________________________________\n"
                "📌 Abschluss: Zusammenfassung\n"
                "Bitte fasse zum Schluss in stichpunktartiger Form zusammen:\n"
                "• Die wichtigsten Marketingziele\n"
                "• Die zentralen Maßnahmen & Zeitpunkte\n"
                "• Die gewählten Kanäle & Formate\n"
                "• Die priorisierten To-dos\n"
                "• Den Budgetrahmen\n"
                "• Die wichtigsten KPIs zur Erfolgskontrolle\n\n"
                "Hier sind alle Angaben des Projekts:\n\n"
                + "\n".join(alle_antworten)
        )

        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        if hasattr(response, "choices") and response.choices:
            st.session_state.leitfaden_text = response.choices[0].message.content
            st.success("Leitfaden erfolgreich generiert!")
            st.subheader("📝 Dein KI-generierter Leitfaden")
            st.markdown(st.session_state.leitfaden_text)
        else:
            st.error("Die OpenAI-API hat keine Antwort zurückgegeben.")
            st.stop()

        prompt_dateipfad = f"data/{projektname}_prompt.txt"
        with open(prompt_dateipfad, "w", encoding="utf-8") as f:
            f.write(prompt)
        sende_per_mail(prompt_dateipfad)

    except Exception as e:
        st.error(f"Fehler beim Generieren oder Senden: {e}")
        st.stop()

# ---------- Kapitelgenerator 2: Was kann ich aus bisherigen Spielen lernen ----------


kapitel_pfad = "erweiterung.pdf"

if os.path.exists(kapitel_pfad):
    with open(kapitel_pfad, "rb") as f:
        pdf_reader = fitz.open(stream=f.read(), filetype="pdf")
        pdf_text = ""
        for page in pdf_reader:
            pdf_text += page.get_text()

   
    
    if st.button("📄 Kapitel generieren"):
        chapter_prompt = (
            "Erstelle ein eigenständiges, strukturiertes Kapitel mit dem Titel:\n"
            "**Was kann ich aus bisherigen Spielen lernen?**\n\n"
            "Nutze dafür die folgenden Inhalte aus einem Fachtext (siehe unten) "
            "und kombiniere sie mit deinem allgemeinen Expertenwissen zu Brettspielen, Marketing und Finanzierung.\n"
            "Ziel ist ein klar gegliedertes Kapitel, das Learnings aus bestehenden Erfolgsbeispielen wie Catan, Azul oder Gloomhaven ableitet "
            "und konkrete Handlungsempfehlungen für neue Spielentwicklungen gibt.\n"
            "Berücksichtige u. a. Produktstrategie, Zielgruppenansprache, Vertrieb, Design, Community, Preisstrategie, Plattformwahl und Vermarktung.\n\n"
            "🔸 Bitte gliedere das Kapitel mit Zwischenüberschriften.\n"
            "🔸 Am Ende: Zusammenfassung mit 5 zentralen Takeaways.\n\n"
            "Hier ist der relevante Fachtext:\n\n"
            f"{pdf_text}"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": chapter_prompt}],
            temperature=0.7
        )

        if hasattr(response, "choices") and response.choices:
            kapitel_text = response.choices[0].message.content
            st.subheader("📝 Kapitel: Was kann ich aus bisherigen Spielen lernen?")
            st.markdown(kapitel_text)
        else:
            st.error("Keine Antwort von der KI erhalten.")


        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": chapter_prompt}],
            temperature=0.7
        )

        if hasattr(response, "choices") and response.choices:
            kapitel_text = response.choices[0].message.content
            st.subheader("📝 Kapitel: Was kann ich aus bisherigen Spielen lernen?")
            st.markdown(kapitel_text)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=11)
            for line in kapitel_text.split("\n"):
                pdf.multi_cell(0, 8, remove_non_latin1(line))

            kapitel_bytes = BytesIO()
            kapitel_bytes.write(pdf.output(dest='S').encode('latin-1'))
            kapitel_bytes.seek(0)

            st.download_button(
                label="📥 Kapitel als PDF herunterladen",
                data=kapitel_bytes,
                file_name="kapitel_was_kann_ich_lernen.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Keine Antwort von der KI erhalten.")
