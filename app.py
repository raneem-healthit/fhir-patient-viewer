import streamlit as st        # type: ignore # baut die Web-Oberfläche
import requests          # type: ignore # schickt Anfragen ans Internet

# st. bedeutet: "zeig etwas auf der Webseite an"
st.title("🏥 MediView — FHIR Patient Explorer")
st.caption("Echte Patientendaten vom FHIR Test-Server")
st.divider()  # eine Linie auf Webseite, um die Seite zu strukturieren

# suchfeld für Patienten
suche = st.text_input("🔍 Patient suchen", placeholder="Name eingeben...")

# Stell dir vor du schickst einen Brief an den FHIR-Server:
url = "https://hapi.fhir.org/baseR4/Patient?_count=50&_sort=-_lastUpdated"  #die Adresse des Servers
response = requests.get(url,headers={"Accept": "application/fhir+json; charset=utf-8"})   # #"gib mir die Daten von dieser Adresse"
data = response.json()                                   # die Antwort in Python-Format umwandeln

st.divider()

# Manchmal sind die Daten nicht richtig kodiert, z.B. "Müller" wird zu "MÃ¼ller".
def fix_encoding(text):
    try:
        return text.encode("latin-1").decode("utf-8")
    except:
        return text 
    

# Patienten anzeigen
gefunden = 0
for entry in data.get("entry", []): 
    patient = entry["resource"] 
    name_list = patient.get("name", []) 
    if name_list: 
        family = fix_encoding(name_list[0].get("family", "Unbekannt"))
        given = fix_encoding(name_list[0].get("given", [""])[0])
        voller_name = f"{given} {family}"

        # Filter anwenden
        if suche.lower() in voller_name.lower():
           geburtsdatum = fix_encoding(patient.get("birthDate", "Unbekannt"))
           geschlecht_raw = fix_encoding(patient.get("gender", "unbekannt"))
           geschlecht_map = {"male": "männlich", "female": "weiblich", "other": "divers", "unknown": "unbekannt"}
           geschlecht = geschlecht_map.get(geschlecht_raw, geschlecht_raw)
           fhir_id = fix_encoding(patient.get("id", "Unbekannt"))


           # ist wie eine Schublade — der Name ist außen sichtbar, und wenn du draufklickst öffnet sich die Schublade mit allen Details drin.
           # Das with bedeutet: "alles was ich hier einrücke, gehört in diese Schublade"
           with st.expander(f"👤 {voller_name}"):
                st.write(f"📅 Geburtsdatum: {geburtsdatum}")
                st.write(f"⚕️ Geschlecht: {geschlecht}")
                st.write(f"🔑 FHIR ID: {fhir_id}")

                # Adresse
                adresse_list = patient.get("address", [])
                if adresse_list:
                    stadt = fix_encoding(adresse_list[0].get("city", "Unbekannt"))
                    land = fix_encoding(adresse_list[0].get("country", "Unbekannt"))
                    st.write(f"📍 Stadt: {stadt}, {land}")
                else:
                    st.write("📍 Adresse: Unbekannt")

                # Telefon
                telefon_list = patient.get("telecom", [])
                if telefon_list:
                    telefon = fix_encoding(telefon_list[0].get("value", "Unbekannt"))
                    st.write(f"📞 Telefon: {telefon}")
                else:
                    st.write("📞 Telefon: Unbekannt")

           gefunden += 1


if gefunden == 0:
    st.write("Keine Patienten gefunden.") 

st.divider()
st.caption("Gebaut mit Python + Streamlit + FHIR R4") 