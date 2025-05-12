import streamlit as st

def anzeigen_leitfaden():
    st.title("🎲 Marketing- & Finanzierungsleitfaden für dein neues Spiel")

    st.header("1. Spielidee & Entwicklungsstand")
    st.text_input("Wie heißt das Spiel?", placeholder="z. B. Lügi Hund")
    st.selectbox("In welchem Stadium befindet sich das Spiel?", ["Idee", "Prototyp", "Testing", "Kurz vor Markteintritt", "Bereits produziert"])
    st.text_area("Was ist der zentrale Reiz oder USP deines Spiels? (Mechanik, Thema, Gestaltung, Zielgruppe)")
    st.selectbox("Welche Art von Spiel ist es?", ["Familienspiel", "Partyspiel", "Kennerspiel", "Rollenspiel", "Lernspiel"])
    st.markdown("---")

    st.header("2. Zielgruppe & Spielverhalten")
    st.slider("Für welche Altersgruppe ist das Spiel gedacht?", 4, 99, (8, 12))
    st.radio("Welche Spielerfahrung wird vorausgesetzt?", ["Einsteiger", "Vielspieler", "Kinder"])
    st.number_input("Für wie viele Personen ist das Spiel ausgelegt?", min_value=1, max_value=12, value=2)
    st.checkbox("Gibt es einen Solo-Modus?")
    st.slider("Wie lange dauert eine durchschnittliche Spielrunde (Minuten)?", 5, 180, 60)
    st.multiselect("Für welche Situationen eignet sich das Spiel besonders?", ["Reisen", "Bildung", "Events", "Familienfeiern", "Therapie", "Schule"])


    st.header("3. Produktion & Preis")
    st.number_input("In welcher Auflagenhöhe planst du den Erstdruck?", min_value=10, step=100)
    st.number_input("Welcher Verkaufspreis ist angedacht (in CHF)?", min_value=0.0, step=0.5)
    st.radio("Ist der Preis im Marktvergleich…", ["Eher niedrig", "Durchschnittlich", "Eher hoch"])
    st.multiselect("Welche Produktionsmaterialien werden verwendet?", ["Standard-Karton", "Holz", "Miniaturen", "Plastik", "Recyceltes Material"])
    st.radio("Wurde bereits ein Produzent oder Verlag kontaktiert?", ["Ja", "Nein"])
    st.number_input("Welche Mindeststückzahl brauchst du für eine rentable Produktion?", min_value=10)
    st.radio("Hast du bereits Angebote oder Kalkulationen eingeholt?", ["Ja", "Nein"])

    st.header("4. Länder & Vertrieb")
    st.multiselect("In welchen Ländern möchtest du das Spiel vertreiben?", ["Schweiz", "Deutschland", "Österreich", "Frankreich", "USA", "Andere"])
    st.multiselect("Welche Sprachversionen soll es geben?", ["Deutsch", "Englisch", "Französisch", "Italienisch", "Spanisch"])
    st.radio("Ist das Spiel kulturell oder sprachlich spezifisch?", ["Ja", "Nein"])
    st.multiselect("Über welche Kanäle möchtest du das Spiel verkaufen?", ["Eigener Webshop", "Einzelhandel", "Kickstarter", "Amazon", "Fachhändler", "Events"])

    st.header("5. Community & Vertrieb")
    st.multiselect("Wo befindet sich deine Community aktuell?", ["Discord", "Instagram", "Mailingliste", "Events/Messen", "Facebook", "Sonstiges"])
    st.text_input("Wie groß ist deine Community ungefähr? (Zahl oder Beschreibung)")
    st.multiselect("Wie bist du mit deiner Community in Kontakt?", ["Regelmäßig", "Punktuell", "Automatisiert", "Persönlich", "Gar nicht aktiv"])
    st.multiselect("Welche Formate nutzt du zur Aktivierung?", ["Umfragen", "Giveaways", "Playtests", "Newsletter", "Kommentare beantworten"])
    st.text_area("Was funktioniert in deiner Community besonders gut – und was weniger?")
    st.multiselect("Welche neuen Formate oder Plattformen würdest du gerne ausprobieren?", ["YouTube", "TikTok", "Live-Events", "Twitch", "Substack", "Sonstiges"])

    st.multiselect("Welche Vertriebskanäle nutzt du derzeit aktiv?", ["Webshop", "Einzelhandel", "Amazon", "Kickstarter", "Fachhandel", "Events", "Direktverkauf"])
    st.text_area("Welche Vertriebskanäle möchtest du in Zukunft zusätzlich erschließen?")
    st.text_area("Gibt es Vertriebskanäle, die du bewusst meidest – und warum?")
    st.text_area("Welche Erfahrungen hast du mit Handelspartnern, Plattformen oder Direktvertrieb gemacht?")

    st.header("6. Ressourcen & Finanzierung")
    st.slider("Wie viele Stunden pro Woche kannst du investieren?", 0, 40, 10)
    st.selectbox("Über welchen Zeitraum planst du mit dieser Verfügbarkeit?", ["1–3 Monate", "3–6 Monate", "6–12 Monate", "Unbefristet"])
    st.text_area("Welche Aufgaben rund um dieses Spiel kannst du gut selbst übernehmen?")
    st.text_area("Welche Aufgaben kosten dich besonders viel Zeit?")
    st.multiselect("Gibt es externe Ereignisse, die deinen Zeitplan beeinflussen?", ["Messen", "Urlaub", "Hauptberuf", "Familie"])

    st.number_input("Wie viel eigenes Budget steht dir zur Verfügung?", min_value=0)
    st.number_input("Wie viel Wunschbudget planst du ein?", min_value=0)
    st.multiselect("Welche Kostenpositionen fallen an?", ["Produktion", "Illustration", "Marketing", "Versand", "Lagerung", "Plattformgebühren"])
    st.number_input("Welcher Umsatz ist nötig für den Break-even?", min_value=0)
    st.multiselect("Welche Finanzierungswege ziehst du in Betracht?", ["Vorbestellungen", "Crowdfunding", "Fördergelder", "Co-Publishing", "Privatinvestor"])
    st.radio("Bist du offen für alternative Finanzierungswege?", ["Ja", "Nein"])
    st.multiselect("Welche Fachbereiche deckst du gut ab?", ["Grafik", "Regelentwicklung", "Marketing", "Finanzen"])
    st.text_area("Wo brauchst du Unterstützung?")
    st.multiselect("Welche Tools nutzt du bereits?", ["Canva", "Kickstarter", "Mailchimp", "Trello"])

    st.success("✅ Alle Eingaben erfasst. Du kannst sie jetzt speichern oder weiter auswerten.")
