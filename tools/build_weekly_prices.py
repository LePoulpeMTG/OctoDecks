#!/usr/bin/env python3
"""
Calcule prices_weekly_card et prices_weekly_set
à partir des données quotidiennes déjà présentes.
"""

import sqlite3, pathlib, sys, datetime, math
DB = pathlib.Path("database/octobase_reference.db")

conn = sqlite3.connect(DB)
cur  = conn.cursor()

# ---------- prices_weekly_card (inchangé) ----------
cur.executescript("""
  DROP TABLE IF EXISTS _tmp_weekly_card;
  CREATE TEMP TABLE _tmp_weekly_card AS
  SELECT scryfall_id,
        strftime('%Y-%W', date) AS week,
        AVG(eur)        AS eur_avg,
        MIN(eur)        AS eur_min,
        MAX(eur)        AS eur_max,
        AVG(eur_foil)   AS eur_foil_avg,
        AVG(usd)        AS usd_avg,
        MIN(usd)        AS usd_min,
        MAX(usd)        AS usd_max,
        AVG(usd_foil)   AS usd_foil_avg,
        AVG(usd_etched) AS usd_etched_avg
    FROM prices_daily_card
  GROUP BY scryfall_id, week;

  INSERT OR REPLACE INTO prices_weekly_card
  SELECT * FROM _tmp_weekly_card;
""")

# ---------- prices_weekly_set (nouvelle requête) ----------
cur.executescript("""
  CREATE TEMP TABLE IF NOT EXISTS _tmp_weekly_set AS
  SELECT s.set_code,
        strftime('%Y-%W', d.date) AS week,
        AVG(d.eur),  AVG(d.usd),
        SUM(COALESCE(d.eur,0)),
        SUM(COALESCE(d.usd,0)),
        COUNT(*)
    FROM prices_daily_card AS d
    JOIN prints            AS p ON p.scryfall_id = d.scryfall_id
    JOIN sets              AS s ON s.set_id      = p.set_id
  GROUP BY s.set_code, week;

  INSERT OR REPLACE INTO prices_weekly_set
  SELECT * FROM _tmp_weekly_set;
""")

conn.commit()
conn.close()
print("✅ Recalcul hebdo terminé")
