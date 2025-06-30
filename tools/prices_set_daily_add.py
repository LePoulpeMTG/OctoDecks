#!/usr/bin/env python3
"""
Ajoute les prix du jour pour chaque SET dans la table prices_daily_set,
à partir des données de la table `prints` et `sets`,
uniquement si la date du jour n’est pas encore enregistrée.
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
cur.execute("SELECT 1 FROM prices_daily_set WHERE date = ? LIMIT 1;", (today,))
if cur.fetchone():
    print("ℹ️  Les prix de SET du jour sont déjà en base.")
    conn.close()
    exit(0)

# ─── Calcul agrégé des prix par SET ────────────────────────────────────────
cur.execute("""
    INSERT INTO prices_daily_set
    (set_code, date, avg_eur, avg_usd, total_eur, total_usd, cards_priced_eur, cards_priced_usd)
    SELECT
        s.set_code,
        ?,
        AVG(p.eur),
        AVG(p.usd),
        SUM(COALESCE(p.eur,0)),
        SUM(COALESCE(p.usd,0)),
        COUNT(p.eur),
        COUNT(p.usd)
    FROM prints p
    JOIN sets   s ON s.set_id = p.set_id
    WHERE p.eur IS NOT NULL OR p.usd IS NOT NULL
    GROUP BY s.set_code;
""", (today,))

conn.commit()
print(f"✅ {cur.rowcount} lignes insérées dans prices_daily_set pour la date {today}.")
conn.close()
