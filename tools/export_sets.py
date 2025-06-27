#!/usr/bin/env python3
"""
Exporte la liste des éditions + leur valeur €/$ du jour
dans exports/sets.json.
"""

import sqlite3, json, pathlib

DB = pathlib.Path("database/octobase_reference.db")
OUT = pathlib.Path("exports/sets.json")
OUT.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur  = conn.cursor()

# dernière date daily dispo
cur.execute("SELECT MAX(date) FROM prices_daily_set")
today, = cur.fetchone()

cur.execute("""
SELECT s.set_code,
       s.name,
       s.release_date,
       s.set_type,
       s.total_cards,
       s.icon_svg_uri,
       d.total_eur,
       d.total_usd
FROM sets s
LEFT JOIN prices_daily_set d USING(set_code)
WHERE d.date = ?
ORDER BY s.release_date DESC
""", (today,))

sets = [dict(r) for r in cur.fetchall()]
OUT.write_text(json.dumps(sets, separators=(",",":")), encoding="utf-8")

print(f"✅ {OUT} généré ({OUT.stat().st_size/1024:.1f} kB)")
