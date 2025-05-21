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
                "für ein neu entwickeltes Brettspiel zu erstellen.\n"
                "Ziel: Ein vollständiger und sehr detaillierter Plan, der in der Realität mit einem kleinen Team, begrenztem Budget und hoher strategischer Klarheit umgesetzt werden kann – aufgeteilt in 13 logisch aufgebaute Kapitel. \n"
                "Bitte berücksichtige dabei die besonderen Wünsche, Einschränkungen, Zielgruppen, Zeitressourcen, Ausschlüsse und inhaltlichen Besonderheiten des Spiels (siehe Projektdaten unten).\n"
                "❗Wichtig: Wenn aus den Projektdaten Einschränkungen hervorgehen – etwa der Ausschluss von bestimmten Finanzierungsformen wie Kickstarter oder Gamefound, "
                "oder der bewusste Verzicht auf bestimmte Kommunikations- oder Vertriebskanäle –, "
                "darfst du diese Optionen nicht empfehlen oder einplanen. "
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
                "Gliederung:\n"
                "1. Situationsanalyse\n"
                "o Marktanalyse: Nenne konkrete Trends, Nischen, Chancen & Risiken im aktuellen Brettspielmarkt (z. B. Hybridspiele, Audioelemente, Nachhaltigkeit, Bildung).\n"
                "o Zielgruppenanalyse: Beschreibe mindestens drei relevante Zielsegmente mit Bedürfnissen, Kaufverhalten, potenziellen Einstiegshürden.\n"
                "o Wettbewerbsanalyse: Bitte analysiere mindestens drei neue, externe Konkurrenzspiele, die dem Konzept ähneln, aber *nicht bereits in den Projektdaten (z. B. aus Frage 55)* genannt wurden. Gib zu jedem Spiel eine SWOT-Analyse in Tabellenform an.\n"
                "o Eigene Ausgangslage: USP, Entwicklungsstand, Ressourcenanalyse (zeitlich, technisch, personell, finanziell).\n"
                "o 🔸 Nutze mindestens eine Tabelle zur SWOT-Analyse und gib konkrete Beispiele für Markttrends.\n"
                "2. Marketingziele (SMART)\n"
                "o Jeweils drei Ziele für kurz-, mittel- und langfristige Zeiträume, klar messbar (z. B. 1.000 Newsletter-Abos bis September).\n"
                "o Beziehe dich auf Reichweite, Community, Conversion, Absatz, Wiederkäufe.\n"
                "o 🔸 Gib zu jedem Ziel die passende Messmethode und Tools zur Überwachung an.\n"
                "3. Zielgruppen & Personas\n"
                "o Definiere Hauptzielgruppen.\n"
                "o Erstelle mindestens drei realistische Personas (mit Alter, Beruf, Medienverhalten, Kaufentscheidungsprozess, Spielverhalten).\n"
                "o 🔸 Nutze für jede Persona eine übersichtliche Darstellung in Tabellenform.\n"
                "4. Positionierung & Markenstrategie\n"
                "o Formuliere ein prägnantes Markenversprechen.\n"
                "o Leite differenzierende Markenwerte, Designprinzipien, Tonalität und Packaging-Ideen ab.\n"
                "o 🔸 Integriere einen Positionierungssatz („Echoes of Aether ist das einzige Spiel, das …“) und beschreibe bewusst gewählte Designentscheidungen.\n"
                "5. Marketingstrategien (7 Ps)\n"
                "o Für jedes P (Product, Price, Place, Promotion, People, Process, Physical Evidence): detaillierte Beschreibung inkl. konkreter Umsetzungsmaßnahmen.\n"
                "o 🔸 Ergänze eine Tabelle zur Preismodellierung und Promo-Beispielen mit Kosten-/Nutzen-Abschätzung.\n"
                "6. Social-Media-Strategie & Redaktionsplan\n"
                "o Auswahl der Plattformen mit Begründung – aber nur aus den im Projekt gewünschten Optionen; ausgeschlossene Kanäle dürfen nicht berücksichtigt werden\n"
                "o 4–5 Content-Säulen (z. B. Storytelling, Behind-the-Scenes, Audio-Vorschau)\n"
                "o Detaillierter Posting-Zeitplan für mind. 2 Monate (Datum, Uhrzeit, Kanal, Ziel, Content-Idee, Textvorschlag)\n"
                "o 🔸 Bitte alles in Tabellenform, mit konkreten Textvorschlägen und Bildideen – keine Platzhalter.\n"
                "7. Community-Aufbau & -Pflege\n"
                "o Strategien für Aufbau, Aktivierung während der Kampagne, und langfristige Bindung (z. B. Discord-Rollen, exklusive Audioinhalte, Fan-Votings).\n"
                "o 🔸 Gib konkrete Aktionen pro Monat an (z. B. August: 1. Give-Away mit Mini-Quest für Audiobeiträge).\n"
                "8. Finanzierungskonzept\n"
                "o Wahl der Plattform mit Begründung (aber nur aus den in den Projektdaten ausdrücklich genannten Optionen – ausgeschlossene Optionen dürfen nicht verwendet werden!)\n"
                "o Funding-Ziel, Stretch Goals, Pledge-Level (Tabellarisch)\n"
                "o Kampagnenstruktur (Pre-Launch, Launch, Post-Launch)\n"
                "o Kommunikationsfahrplan mit konkretem Ablaufplan und Kanälen\n"
                "o 🔸 Inklusive Beispieltext für Kampagnenstart-Post und Newsletter-Betreffzeile\n"
                "9. Vertriebsstrategie\n"
                "o Detaillierte Planung – aber nur für die im Projekt aktiv vorgesehenen Vertriebskanäle. Nicht gewünschte Kanäle bitte auslassen.\n"
                "o Tools für Shop & Versand (z. B. Shopify, Sendcloud)\n"
                "o Kooperationen, Preisgestaltung, Versandmodell (inkl. Beispielrechnung)\n"
                "o 🔸 Tabelle: Vertriebskanäle mit Startzeitpunkt, Aufwand, erwartete Reichweite\n"
                "10. Maßnahmenplan & To-dos\n"
                "o Konkrete To-do-Liste für nächste 14 Tage\n"
                "o Jahresplan: Quartalsweise Ziele, Events, Launch-Meilensteine\n"
                "o 🔸 Übersicht als Tabelle mit Zuständigkeiten, Zeitaufwand, Tools\n"
                "11. Budget- & Ressourcenplanung\n"
                "o Budgetverteilung (nach Maßnahmen, pro Kanal, pro Monat)\n"
                "o Was ist intern umsetzbar, was sollte extern erledigt werden\n"
                "o Tools, Plattformen und Freelancer-Budgets\n"
                "o 🔸 Budgettabelle inkl. Reservepositionen\n"
                "12. KPIs & Erfolgskontrolle\n"
                "o Relevante KPIs pro Kanal (Socials, Website, Kampagne, Newsletter, Vertrieb)\n"
                "o Tools zur Erfassung & Auswertung (z. B. Mailchimp, Kickstarter-Dashboard)\n"
                "o 🔸 Definiere kritische Schwellenwerte & sinnvolle Reaktionspläne\n"
                "13. Risikoanalyse & Notfallpläne\n"
                "o Identifiziere potenzielle Risiken (z. B. Community-Stagnation, App-Fehler, Versandprobleme)\n"
                "o Nenne präventive Maßnahmen und konkrete Notfallpläne\n"
                "o 🔸 Mit Tabelle: Risiko, Eintrittswahrscheinlichkeit, Auswirkung, Maßnahme\n"
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
