#!/usr/bin/env python3
"""
Ajoute les prix du jour dans prices_daily_set
puis exporte les tables du jour (cards + sets) dans un fichier JSON.
"""

import json
import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timezone


DB_PATH   = Path("database/octobase_reference.db")
OUT_FILE  = Path("prices_daily.json")
TODAY     = datetime.now(timezone.utc).strftime("%Y-%m-%d")



def insert_daily_set(cur):
    """
    Calcule le prix moyen et total de chaque set pour la date du jour,
    puis insère dans la table prices_daily_set.
    """
    cur.execute("""
        INSERT OR REPLACE INTO prices_daily_set (
            set_code, date,
            avg_eur, avg_usd,
            total_eur, total_usd,
            total_cards
        )
        SELECT 
            s.set_code,
            ?,  -- TODAY
            AVG(d.eur), AVG(d.usd),
            SUM(COALESCE(d.eur, 0)),
            SUM(COALESCE(d.usd, 0)),
            COUNT(*)  -- nombre d'impressions avec un prix
        FROM prices_daily_card AS d
        JOIN prints AS p ON p.scryfall_id = d.scryfall_id
        JOIN sets   AS s ON s.set_id      = p.set_id
        WHERE d.date = ?
        GROUP BY s.set_code;
    """, (TODAY, TODAY))


def export_json(conn):
    cur = conn.cursor()

    cur.execute("SELECT * FROM prices_daily_card WHERE date = ?", (TODAY,))
    cards = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT * FROM prices_daily_set WHERE date = ?", (TODAY,))
    sets = [dict(row) for row in cur.fetchall()]

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(
        {"date": TODAY, "cards": cards, "sets": sets},
        separators=(",", ":")
    ), encoding="utf-8")

    size_mb = OUT_FILE.stat().st_size / 1_048_576
    print(f"✅ Export {OUT_FILE} généré ({size_mb:.1f} MiB)")


def main():
    if not DB_PATH.exists():
        print("❌ DB introuvable", DB_PATH, file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur  = conn.cursor()

    # (Les prix_daily_card du jour sont déjà insérés par import_all_cards.py)
    insert_daily_set(cur)
    conn.commit()

    export_json(conn)
    conn.close()
    print(f"✅ Export {OUT_FILE} généré ({OUT_FILE.stat().st_size/1_048_576:.1f} MiB)")

if __name__ == "__main__":
    main()
