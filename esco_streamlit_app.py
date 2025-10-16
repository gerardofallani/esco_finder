# esco_streamlit_app.py

import os
import zipfile
import urllib.request

DB_ZIP_URL = "https://github.com/gerardofallani/esco_finder/releases/download/v1.0/esco_it.sqlite.zip"
DB_ZIP_NAME = "esco_it.sqlite.zip"
DB_NAME = "esco_it.sqlite"

if not os.path.exists(DB_NAME):
    # Scarica il file zip
    urllib.request.urlretrieve(DB_ZIP_URL, DB_ZIP_NAME)
    
    # Estrai lo zip
    with zipfile.ZipFile(DB_ZIP_NAME, 'r') as zip_ref:
        zip_ref.extractall()
    
    # Rimuovi lo zip dopo l’estrazione (opzionale)
    os.remove(DB_ZIP_NAME)


import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "esco_it.sqlite"

# Funzioni per interrogare il DB
def get_occupations(conn):
    query = "SELECT DISTINCT preferredLabel FROM occupations ORDER BY preferredLabel"
    return pd.read_sql_query(query, conn)

def get_skills_for_occupation(conn, occupation_label):
    query = """
    SELECT s.preferredLabel AS skill, s.description
    FROM occupations o
    JOIN occupationSkillRelations osr ON o.conceptUri = osr.occupationUri
    JOIN skills s ON osr.skillUri = s.conceptUri
    WHERE o.preferredLabel = ?
    ORDER BY s.preferredLabel
    """
    return pd.read_sql_query(query, conn, params=(occupation_label,))

# UI Streamlit
st.set_page_config(page_title="ESCO Skills Explorer - IT", page_icon="💼")

st.sidebar.title("Navigazione")
selezione = st.sidebar.radio("Scegli cosa esplorare:", [
    "Skill per Occupazione",
    "Skill Gerarchiche",
    "Occupazioni per Skill",
    "Collezioni Speciali"
])

st.title("💼 ESCO Skills Explorer - IT")

if selezione == "Skill per Occupazione":
    st.header("🔍 Competenze associate a un'occupazione")

    conn = sqlite3.connect(DB_PATH)
    occupations_df = get_occupations(conn)
    selected_occupation = st.selectbox("Cerca occupazione (es. 'insegnante'):", occupations_df["preferredLabel"])

    if selected_occupation:
        skills_df = get_skills_for_occupation(conn, selected_occupation)
        st.subheader(f"Competenze per: {selected_occupation}")
        st.dataframe(skills_df)

    conn.close()
