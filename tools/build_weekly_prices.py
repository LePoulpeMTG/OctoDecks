#!/usr/bin/env python3
"""
Recalcule prices_weekly_card et prices_weekly_set sur la base
des 7 derniers jours (inclus) de prices_daily_*.
"""

import sqlite3, datetime, pathlib

DB_PATH = pathlib.Path("database/octobase_reference.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    # -- 1) CARD weekly -------------------------------------------------------
    cur.execute("DELETE FROM prices_weekly_card")  # on régénère tout

    cur.execute("""
        INSERT INTO prices_weekly_card
        SELECT
          scryfall_id,
          strftime('%G-%W', date) AS week,
          AVG(eur)        AS avg_eur,
          AVG(eur_foil)   AS avg_eur_foil,
          AVG(usd)        AS avg_usd,
          AVG(usd_foil)   AS avg_usd_foil,
          AVG(usd_etched) AS avg_usd_etched
        FROM prices_daily_card
        WHERE date >= date('now', '-7 days')
        GROUP BY scryfall_id, week
    """)

    # -- 2) SET weekly --------------------------------------------------------
    cur.execute("DELETE FROM prices_weekly_set")

    cur.execute("""
        INSERT INTO prices_weekly_set
        SELECT
          set_code,
          strftime('%G-%W', date) AS week,
          AVG(avg_eur) AS avg_eur,
          AVG(avg_usd) AS avg_usd,
          COUNT(DISTINCT scryfall_id) AS total_cards
        FROM prices_daily_set
        WHERE date >= date('now', '-7 days')
        GROUP BY set_code, week
    """)

    conn.commit()
    conn.close()
    print("✅ Weekly prices updated")

if __name__ == "__main__":
    main()
