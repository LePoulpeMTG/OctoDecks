#!/usr/bin/env python3
"""
Ajoute les moyennes hebdomadaires des cartes dans la table prices_weekly_card,
calculées depuis les données de prices_daily_card.
Exécuter de préférence chaque dimanche.
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
cur.execute("SELECT 1 FROM prices_weekly_card WHERE week = ? LIMIT 1;", (week,))
if cur.fetchone():
    print(f"ℹ️  Les prix hebdo pour la semaine {week} sont déjà présents.")
    conn.close()
    exit(0)

# ─── Calcul des moyennes hebdo ─────────────────────────────────────────────
cur.execute("""
    INSERT INTO prices_weekly_card
    (scryfall_id, week, eur_avg, eur_min, eur_max, eur_foil_avg,
     usd_avg, usd_min, usd_max, usd_foil_avg, usd_etched_avg)
    SELECT
        scryfall_id,
        ?,
        AVG(eur),
        MIN(eur),
        MAX(eur),
        AVG(eur_foil),
        AVG(usd),
        MIN(usd),
        MAX(usd),
        AVG(usd_foil),
        AVG(usd_etched)
    FROM prices_daily_card
    WHERE date >= date('now', '-6 days')
    GROUP BY scryfall_id;
""", (week,))

conn.commit()
print(f"✅ {cur.rowcount} lignes insérées dans prices_weekly_card pour la semaine {week}.")
conn.close()

