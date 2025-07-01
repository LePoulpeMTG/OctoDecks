#!/usr/bin/env python3
"""
Ajoute les prix du jour pour chaque SET dans la table prices_daily_set,
en agrégeant les données de prices_daily_card + prints + sets.

Uniquement si la date du jour n’est pas encore enregistrée.
"""

import sqlite3
from datetime import date

DB_PATH = "database/octobase_reference.db"
today = date.today().isoformat()

# ─── Connexion ─────────────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ─── Vérifie si les prix du jour sont déjà présents ────────────────────────
cur.execute("SELECT 1 FROM prices_daily_set WHERE date = ? LIMIT 1;", (today,))
if cur.fetchone():
    print("ℹ️  Les prix de SET du jour sont déjà en base.")
    conn.close()
    exit(0)

# ─── Agrégation cohérente (même base de calcul) ────────────────────────────
cur.execute("""
    INSERT INTO prices_daily_set
    (set_code, date, avg_eur, avg_usd, total_eur, total_usd,
     cards_priced_eur, cards_priced_usd, total_cards)
    SELECT
        s.set_code,
        ?,                               -- date
        AVG(d.eur),
        AVG(d.usd),
        SUM(d.eur),
        SUM(d.usd),
        COUNT(d.eur),
        COUNT(d.usd),
        COUNT(*)                         -- total cartes (même celles sans prix)
    FROM prices_daily_card d
    JOIN prints            p ON p.scryfall_id = d.scryfall_id
    JOIN sets              s ON s.set_id      = p.set_id
    WHERE d.date = ?
    GROUP BY s.set_code;
""", (today, today))

conn.commit()
print(f"✅ {cur.rowcount} lignes insérées dans prices_daily_set pour la date {today}.")
conn.close()
