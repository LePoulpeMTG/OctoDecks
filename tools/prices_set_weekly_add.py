#!/usr/bin/env python3
"""
Ajoute les moyennes hebdomadaires des SETS dans la table prices_weekly_set,
calculées depuis les données de prices_daily_card (via prints).
À lancer une fois par semaine (de préférence le dimanche).
"""
import sqlite3
from datetime import datetime

DB_PATH = "database/octobase_reference.db"

# ─── Connexion ─────────────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ─── Semaine courante (année-semaine) ──────────────────────────────────────
week = datetime.utcnow().strftime("%Y-%W")

# ─── Vérifie si la semaine est déjà calculée ───────────────────────────────
cur.execute("SELECT 1 FROM prices_weekly_set WHERE week = ? LIMIT 1;", (week,))
if cur.fetchone():
    print(f"ℹ️  Les prix hebdo des SETS pour la semaine {week} sont déjà présents.")
    conn.close()
    exit(0)

# ─── Calcul des moyennes par SET ───────────────────────────────────────────
cur.execute("""
    INSERT INTO prices_weekly_set
    (set_code, week, avg_eur, avg_usd, total_eur, total_usd,
     cards_priced_eur, cards_priced_usd, total_cards)
    SELECT
        s.set_code,
        ?,
        AVG(d.eur),
        AVG(d.usd),
        SUM(COALESCE(d.eur,0)),
        SUM(COALESCE(d.usd,0)),
        COUNT(d.eur),
        COUNT(d.usd),
        COUNT(*)
    FROM prices_daily_card d
    JOIN prints            p ON p.scryfall_id = d.scryfall_id
    JOIN sets              s ON s.set_id      = p.set_id
    WHERE d.date >= date('now', '-6 days')
    GROUP BY s.set_code;
""", (week,))

conn.commit()
print(f"✅ {cur.rowcount} lignes insérées dans prices_weekly_set pour la semaine {week}.")
conn.close()