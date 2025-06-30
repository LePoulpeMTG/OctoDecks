#!/usr/bin/env python3
"""
Ajoute les prix du jour (cartes individuelles) dans la table prices_daily_card,
uniquement si la date du jour n'est pas encore présente.
"""
import sqlite3
from datetime import date

DB_PATH = "database/octobase_reference.db"

# ─── Connexion ─────────────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ─── Date du jour ─────────────────────────────────────────────────────────
today = date.today().isoformat()

# ─── Vérifie si les prix du jour sont déjà présents ────────────────────────
cur.execute("SELECT 1 FROM prices_daily_card WHERE date = ? LIMIT 1;", (today,))
if cur.fetchone():
    print("ℹ️  Les prix du jour sont déjà présents dans la base.")
    conn.close()
    exit(0)

# ─── Copie depuis les derniers prix connus (scryfall_id → prix) ────────────
# Supposons que la table prints contient les derniers prix dans les colonnes correspondantes
cur.execute("""
    INSERT INTO prices_daily_card
    (scryfall_id, date, eur, eur_foil, usd, usd_foil, usd_etched)
    SELECT
        scryfall_id, ?, eur, eur_foil, usd, usd_foil, usd_etched
    FROM prints
    WHERE eur IS NOT NULL OR usd IS NOT NULL;
""", (today,))

conn.commit()
print(f"✅ {cur.rowcount} lignes insérées dans prices_daily_card pour la date {today}.")
conn.close()
