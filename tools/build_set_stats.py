#!/usr/bin/env python3
"""
Construit les tables :
- set_languages
- set_statistics
à partir des données existantes dans prints, cards, prices, etc.
"""

import sqlite3
from collections import defaultdict
from pathlib import Path

DB_PATH = Path("database/octobase_reference.db")

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# ─── SET_LANGUAGES ──────────────────────────────────────────────
cur.execute("DELETE FROM set_languages;")
cur.execute("""
    INSERT OR IGNORE INTO set_languages (set_code, lang)
    SELECT DISTINCT s.set_code, p.lang
    FROM prints p
    JOIN sets s ON s.set_id = p.set_id;
""")
print("✅ Table set_languages remplie")

# ─── SET_STATISTICS ─────────────────────────────────────────────

cur.execute("DELETE FROM set_statistics;")

cur.execute("""
    SELECT 
        s.set_code,
        COUNT(p.scryfall_id) AS num_prints,
        COUNT(DISTINCT p.oracle_id) AS num_oracle_ids,
        MAX(c.is_promo) AS has_promo_cards,
        MAX(CASE WHEN c.layout IN ('transform','modal_dfc','double_faced_token','reversible_card') THEN 1 ELSE 0 END) AS has_double_faced,
        GROUP_CONCAT(DISTINCT c.layout) AS available_layouts,
        GROUP_CONCAT(DISTINCT p.lang) AS available_languages,
        MAX(d.eur) AS value_card_max_eur,
        ROUND(AVG(CASE WHEN p.foil = 1 THEN 1.0 ELSE 0 END), 3) AS foil_percentage,
        ROUND(SUM(CASE WHEN p.rarity = 'common' THEN 1.0 ELSE 0 END) / COUNT(p.scryfall_id), 3) AS rarity_common_pct,
        ROUND(SUM(CASE WHEN p.rarity = 'uncommon' THEN 1.0 ELSE 0 END) / COUNT(p.scryfall_id), 3) AS rarity_uncommon_pct,
        ROUND(SUM(CASE WHEN p.rarity = 'rare' THEN 1.0 ELSE 0 END) / COUNT(p.scryfall_id), 3) AS rarity_rare_pct,
        ROUND(SUM(CASE WHEN p.rarity = 'mythic' THEN 1.0 ELSE 0 END) / COUNT(p.scryfall_id), 3) AS rarity_mythic_pct
    FROM sets s
    JOIN prints p ON p.set_id = s.set_id
    JOIN cards c ON c.oracle_id = p.oracle_id
    LEFT JOIN prices_daily_card d ON d.scryfall_id = p.scryfall_id
    GROUP BY s.set_code;
""")

rows = cur.fetchall()
columns = [desc[0] for desc in cur.description]

for row in rows:
    values = dict(zip(columns, row))
    cur.execute(f"""
        INSERT OR REPLACE INTO set_statistics (
            set_code,
            num_prints,
            num_oracle_ids,
            has_promo_cards,
            has_double_faced,
            available_layouts,
            available_languages,
            value_card_max_eur,
            foil_percentage,
            rarity_common_pct,
            rarity_uncommon_pct,
            rarity_rare_pct,
            rarity_mythic_pct
        ) VALUES (
            :set_code,
            :num_prints,
            :num_oracle_ids,
            :has_promo_cards,
            :has_double_faced,
            :available_layouts,
            :available_languages,
            :value_card_max_eur,
            :foil_percentage,
            :rarity_common_pct,
            :rarity_uncommon_pct,
            :rarity_rare_pct,
            :rarity_mythic_pct
        )
    """, values)

conn.commit()
conn.close()
print("✅ Table set_statistics remplie")
