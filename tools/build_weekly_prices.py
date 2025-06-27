#!/usr/bin/env python3
import sqlite3, pathlib

DB = pathlib.Path("database/octobase_reference.db")
conn = sqlite3.connect(DB)
cur  = conn.cursor()

# ── WEEKLY CARD ───────────────────────────────────────────────
cur.executescript("""
DROP TABLE IF EXISTS _tmp_weekly_card;
CREATE TEMP TABLE _tmp_weekly_card AS
SELECT d.scryfall_id,
       strftime('%Y-%W', d.date) AS week,
       AVG(d.eur)        AS eur_avg,
       MIN(d.eur)        AS eur_min,
       MAX(d.eur)        AS eur_max,
       AVG(d.eur_foil)   AS eur_foil_avg,
       AVG(d.usd)        AS usd_avg,
       MIN(d.usd)        AS usd_min,
       MAX(d.usd)        AS usd_max,
       AVG(d.usd_foil)   AS usd_foil_avg,
       AVG(d.usd_etched) AS usd_etched_avg
FROM prices_daily_card d
GROUP BY d.scryfall_id, week;

INSERT OR REPLACE INTO prices_weekly_card
SELECT * FROM _tmp_weekly_card;
""")

# ── WEEKLY SET ────────────────────────────────────────────────
cur.executescript("""
DROP TABLE IF EXISTS _tmp_weekly_set;
CREATE TEMP TABLE _tmp_weekly_set AS
SELECT  s.set_code,
        strftime('%Y-%W', d.date) AS week,
        AVG(d.eur)                AS avg_eur,
        AVG(d.usd)                AS avg_usd,
        SUM(COALESCE(d.eur,0))    AS total_eur,
        SUM(COALESCE(d.usd,0))    AS total_usd,
        COUNT(d.eur)              AS cards_priced_eur,
        COUNT(d.usd)              AS cards_priced_usd,
        COUNT(*)                  AS total_cards
FROM prices_daily_card AS d
JOIN prints            AS p ON p.scryfall_id = d.scryfall_id
JOIN sets              AS s ON s.set_id      = p.set_id
WHERE d.eur IS NOT NULL OR d.usd IS NOT NULL
GROUP BY s.set_code, week;

INSERT OR REPLACE INTO prices_weekly_set (
  set_code, week,
  avg_eur, avg_usd,
  total_eur, total_usd,
  cards_priced_eur, cards_priced_usd,
  total_cards
)
SELECT * FROM _tmp_weekly_set;
""")

# ── DEBUG ─────────────────────────────────────────────────────
for tbl in ("prices_weekly_card", "prices_weekly_set"):
    cur.execute(f"SELECT COUNT(*) FROM {tbl}")
    print(f"🛈 {tbl} lignes :", cur.fetchone()[0])

conn.commit()
conn.close()
print("✅ Recalcul hebdo terminé")
