#!/usr/bin/env python3
"""
Génère ou met à jour les statistiques par set dans la table `set_statistics`.
Doit être exécuté après l'import complet des cartes et impressions.
"""

import sqlite3

DB_PATH = "database/octobase_reference.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Supprimer les anciennes stats (optionnel : ici on fait REPLACE)
cur.execute("DELETE FROM set_statistics")

# Insertion des nouvelles stats
cur.execute("""
INSERT INTO set_statistics (
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
)
SELECT
    s.set_code,
    COUNT(p.scryfall_id),
    COUNT(DISTINCT p.oracle_id),
    MAX(p.foil AND p.nonfoil AND c.is_promo),  -- approximation promo
    MAX(CASE WHEN p.layout IN ('transform', 'modal_dfc', 'double_faced') THEN 1 ELSE 0 END),
    GROUP_CONCAT(DISTINCT p.layout),
    GROUP_CONCAT(DISTINCT p.lang),
    MAX(pr.eur),
    AVG(CASE WHEN p.foil THEN 1.0 ELSE 0.0 END),
    AVG(CASE WHEN p.rarity = 'common' THEN 1.0 ELSE 0.0 END),
    AVG(CASE WHEN p.rarity = 'uncommon' THEN 1.0 ELSE 0.0 END),
    AVG(CASE WHEN p.rarity = 'rare' THEN 1.0 ELSE 0.0 END),
    AVG(CASE WHEN p.rarity = 'mythic' THEN 1.0 ELSE 0.0 END)
FROM sets s
JOIN prints p ON p.set_id = s.set_id
JOIN cards c ON c.oracle_id = p.oracle_id
LEFT JOIN prices_daily_card pr ON pr.scryfall_id = p.scryfall_id
GROUP BY s.set_code;
""")

conn.commit()
print(f"✅ Statistiques mises à jour pour {cur.rowcount} sets.")
conn.close()
