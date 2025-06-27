#!/usr/bin/env python3
"""Recalcule prices_weekly_card et prices_weekly_set."""
import sqlite3, pathlib, datetime, sys

DB = pathlib.Path("database/octobase_reference.db")
conn = sqlite3.connect(DB)
cur  = conn.cursor()

# ─── Ajout des colonnes TOTAL si elles n’existent pas (ignore si déjà là) ──
cur.executescript("""
PRAGMA foreign_keys = ON;
ALTER TABLE prices_weekly_set ADD COLUMN total_eur REAL;
ALTER TABLE prices_weekly_set ADD COLUMN total_usd REAL;
""")

# ──────────────────────────────────────────────────────────────────────────
# WEEKLY CARD  – 11 colonnes
# ──────────────────────────────────────────────────────────────────────────
cur.executescript("""
DROP TABLE IF EXISTS _tmp_weekly_card;
CREATE TEMP TABLE _tmp_weekly_card AS
SELECT  d.scryfall_id,
        strftime('%Y-%W', d.date)       AS week,
        AVG(d.eur)        AS eur_avg,
        MIN(d.eur)        AS eur_min,
        MAX(d.eur)        AS eur_max,
        AVG(d.eur_foil)   AS eur_foil_avg,
        AVG(d.usd)        AS usd_avg,
        MIN(d.usd)        AS usd_min,
        MAX(d.usd)        AS usd_max,
        AVG(d.usd_foil)   AS usd_foil_avg,
        AVG(d.usd_etched) AS usd_etched_avg
  FROM prices_daily_card AS d
 GROUP BY d.scryfall_id, week;

INSERT OR REPLACE INTO prices_weekly_card (
  scryfall_id, week,
  eur_avg, eur_min, eur_max,
  eur_foil_avg,
  usd_avg, usd_min, usd_max,
  usd_foil_avg, usd_etched_avg)
SELECT * FROM _tmp_weekly_card;
""")

# ──────────────────────────────────────────────────────────────────────────
# WEEKLY SET  – avec total_eur / total_usd
# ──────────────────────────────────────────────────────────────────────────
cur.executescript("""
DROP TABLE IF EXISTS _tmp_weekly_set;
CREATE TEMP TABLE _tmp_weekly_set AS
SELECT  s.set_code,
        strftime('%Y-%W', d.date) AS week,
        AVG(d.eur)               AS avg_eur,
        AVG(d.usd)               AS avg_usd,
        SUM(COALESCE(d.eur,0))   AS total_eur,
        SUM(COALESCE(d.usd,0))   AS total_usd,
        COUNT(*)                 AS total_cards
  FROM prices_daily_card AS d
  JOIN prints            AS p ON p.scryfall_id = d.scryfall_id
  JOIN sets              AS s ON s.set_id      = p.set_id
 GROUP BY s.set_code, week;

INSERT OR REPLACE INTO prices_weekly_set (
  set_code, week,
  avg_eur,  avg_usd,
  total_eur, total_usd,
  total_cards)
SELECT * FROM _tmp_weekly_set;
""")

conn.commit()
conn.close()
print("✅ Recalcul hebdo terminé")
