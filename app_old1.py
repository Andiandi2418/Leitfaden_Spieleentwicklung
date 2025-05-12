import streamlit as st
# import openai
import os
from dotenv import load_dotenv
from strategien import strategiebaum
from regeln import statische_empfehlungen

load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def gpt_vorschlag(subast_text):
#     client = openai.OpenAI()
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "Du bist ein KI-Marketingberater für Brettspiele."},
#             {"role": "user", "content": f"Bitte gib mir eine konkrete Umsetzungsstrategie für: {subast_text}"}
#         ],
#         temperature=0.7,
#         max_tokens=500
#     )
#     return response.choices[0].message.content

st.set_page_config(page_title="KI-Tool Gesellschaftsspiel", page_icon="🎲", layout="centered")

st.title("🎲 KI-Tool zur Vermarktung & Finanzierung deines Spiels")

# Fragenlogik
zielgruppe = st.radio("Für welche Zielgruppe ist dein Spiel gedacht?", ["Familien", "Vielspieler:innen", "Beide"])
phase = st.selectbox("In welchem Stadium befindet sich dein Spiel derzeit?", ["Idee / Konzeption", "Spieltest / Prototyp", "Produktionsreif"])
usps = st.multiselect("Was ist das zentrale Alleinstellungsmerkmal deines Spiels?", ["Neuartige Mechanik", "Thema / Story", "Design / Haptik", "Noch unklar"])
plattformen = st.multiselect("Welche Plattformen nutzt du (bereits) oder planst zu nutzen?", ["Instagram", "TikTok", "YouTube", "BoardGameGeek", "Eigene Website", "Kickstarter"])
marke = st.radio("Wie wichtig ist dir eine konsistente visuelle Markenidentität?", ["Sehr wichtig", "Mittelwichtig", "Nicht wichtig"])
community = st.radio("Planst du eine Community aktiv aufzubauen (z. B. Discord)?", ["Ja", "Nein", "Noch nicht sicher"])
cocreation = st.radio("Wie offen bist du für Beteiligung & Co-Kreation durch die Community?", ["Hoch (z. B. Spielregeln mitentwickeln)", "Mittel (z. B. Fan-Voting)", "Gering"])
testing = st.radio("Hast du dein Spiel bereits mit der Zielgruppe getestet?", ["Ja, umfangreich", "Ja, in Teilen", "Nein"])
testformate = st.multiselect("Welche Testformate sind für dich realistisch?", ["Physische Spielrunden", "Digitale Tools (Tabletop Simulator etc.)", "Online-Umfragen", "Noch unklar"])
finanzierung = st.multiselect("Welche Finanzierungsansätze ziehst du in Betracht?", ["Crowdfunding", "Vorverkauf", "Förderung", "Eigenfinanzierung", "Partnerschaften"])

# Ausgabe
if st.button("💡 Lösungsvorschlag generieren"):
    st.markdown("## 🔍 Statische Empfehlungen auf Basis deiner Angaben:")
    for emp in statische_empfehlungen(zielgruppe, phase, plattformen, marke, community, testformate, finanzierung):
        st.markdown(f"- {emp}")

    # GPT-Nutzung auskommentiert:
    # strategie = strategiebaum[zielgruppe][phase]
    # ausgabe = gpt_vorschlag(strategie)
    # st.markdown("### 🤖 GPT-Vorschlag:")
    # st.write(ausgabe)
