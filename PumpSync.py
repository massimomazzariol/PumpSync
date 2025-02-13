import streamlit as st
import pandas as pd
import os

# Nome del file CSV
DATA_FILE = "workout_data.csv"

# Controlla se il file esiste, altrimenti lo crea
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Sessione", "Data", "Esercizio", "Peso (kg)", "Set", "Ripetizioni", "HR Medio", "HR Max", "Dolore", "Note"])
    df.to_csv(DATA_FILE, index=False)

# Carica il dataset
try:
    df = pd.read_csv(DATA_FILE)
except Exception as e:
    st.error(f"Errore nel caricamento dei dati: {e}")

st.title("🏋️‍♂️ PumpSync - AI Fitness Assistant")
st.write("Registra i tuoi allenamenti e analizza i tuoi progressi!")

# Creazione o selezione della sessione
sessione = st.text_input("Nome della sessione (es. 'Allenamento mattina')")
if sessione:
    session_active = True
else:
    session_active = False

# Input per i dati dell'allenamento
if session_active:
    data = st.date_input("Data", pd.to_datetime("today"))
    esercizio = st.text_input("Esercizio")
    peso = st.number_input("Peso (kg)", min_value=0, max_value=500, value=50)
    set_ = st.number_input("Set", min_value=1, max_value=10, value=4)
    ripetizioni = st.number_input("Ripetizioni", min_value=1, max_value=20, value=10)
    hr_medio = st.number_input("HR Medio", min_value=50, max_value=200, value=120)
    hr_max = st.number_input("HR Max", min_value=50, max_value=200, value=140)
    dolore = st.selectbox("Hai avuto dolore?", ["No", "Sì (leggero)", "Sì (forte)"])
    note = st.text_area("Note aggiuntive")

    # Bottone per salvare i dati
    if st.button("Aggiungi esercizio alla sessione"):
        new_entry = pd.DataFrame({
            "Sessione": [sessione],
            "Data": [data],
            "Esercizio": [esercizio],
            "Peso (kg)": [peso],
            "Set": [set_],
            "Ripetizioni": [ripetizioni],
            "HR Medio": [hr_medio],
            "HR Max": [hr_max],
            "Dolore": [dolore],
            "Note": [note]
        })
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Esercizio aggiunto alla sessione!")

# Chiusura sessione
if session_active and st.button("Chiudi sessione"):
    st.success("✅ Sessione chiusa con successo!")
    session_active = False

# Mostra i dati salvati
st.subheader("📊 Storico Allenamenti")
st.dataframe(df)