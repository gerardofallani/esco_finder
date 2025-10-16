import pandas as pd
import sqlite3
import os

# Percorso della cartella CSV
CSV_FOLDER = "ESCO dataset - v1.2.0 - classification - it - csv"
DB_NAME = "esco_it.sqlite"

# Elenco dei file CSV da importare e tabelle da creare
csv_files = {
    "skills": "skills_it.csv",
    "occupations": "occupations_it.csv",
    "occupationSkillRelations": "occupationSkillRelations_it.csv",
    "skillGroups": "skillGroups_it.csv",
    "skillsHierarchy": "skillsHierarchy_it.csv",
    "skillSkillRelations": "skillSkillRelations_it.csv"
}

# Connessione al DB
conn = sqlite3.connect(DB_NAME)

for table_name, file_name in csv_files.items():
    path = os.path.join(CSV_FOLDER, file_name)
    print(f"Importing {path} into {table_name}...")

    # Leggi CSV
    df = pd.read_csv(path)

    # Opzionale: rimuovi colonne superflue (solo per test)
    # df = df[['id', 'preferredLabel']]  # <-- personalizza se vuoi

    # Scrivi nel DB
    df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.close()
print("✅ Database creato con successo: esco_it.sqlite")
