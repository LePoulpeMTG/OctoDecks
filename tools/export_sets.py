import sqlite3
import json
import os
import subprocess
import shutil
from pathlib import Path

DB_PATH = Path("database/octobase_reference.db")
EXPORT_PATH = Path("exports/sets.json")
PUBLIC_PATH = Path("data/sets.json")

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# ─── Lecture des sets de base ─────────────────────────────────
cur.execute("""
    SELECT 
        s.set_code,
        s.name,
        s.release_date,
        s.set_type,
        s.total_cards,
        s.icon_svg_uri,

        d.total_eur,
        d.total_usd,
        d.avg_eur,
        d.avg_usd,
        d.total_cards AS cards_priced_eur,
        d.date AS last_updated,

        w.total_eur AS value_total_eur_7d_ago

    FROM sets s
    LEFT JOIN prices_daily_set d ON d.set_code = s.set_code
    LEFT JOIN prices_daily_set w ON w.set_code = s.set_code AND w.date = (
        SELECT date FROM prices_daily_set
        WHERE set_code = s.set_code AND date < d.date
        ORDER BY date DESC LIMIT 1
    )
    WHERE d.date = (SELECT MAX(date) FROM prices_daily_set)
    ORDER BY s.release_date DESC
""")

sets_raw = cur.fetchall()
cols = [desc[0] for desc in cur.description]

# ─── Lecture des statistiques par set ────────────────────────
cur.execute("SELECT * FROM set_statistics")
stats_by_code = {row[0]: dict(zip([desc[0] for desc in cur.description], row)) for row in cur.fetchall()}

# ─── Construction JSON final ─────────────────────────────────
sets = []

for raw in sets_raw:
    base = dict(zip(cols, raw))
    code = base["set_code"]
    stats = stats_by_code.get(code, {})

    total = base.get("total_eur", 0) or 0
    total_7d = base.get("value_total_eur_7d_ago")
    delta = round(total - total_7d, 2) if total_7d is not None else 0.0

    entry = {
        "set_code": code,
        "name": base["name"],
        "release_date": base["release_date"],
        "set_type": base["set_type"],
        "total_cards": base["total_cards"],
        "icon_svg_uri": base["icon_svg_uri"],
        "value_total_eur": round(total, 2),
        "value_total_usd": round(base.get("total_usd", 0) or 0, 2),
        "avg_card_eur": round(base.get("avg_eur", 0) or 0, 2),
        "avg_card_usd": round(base.get("avg_usd", 0) or 0, 2),
        "last_updated": base["last_updated"],
        "cards_priced_eur": base["cards_priced_eur"] or 0,
        "value_eur_weekly_delta": delta,
        "num_prints": stats.get("num_prints", 0),
        "num_oracle_ids": stats.get("num_oracle_ids", 0),
        "has_promo_cards": bool(stats.get("has_promo_cards", 0)),
        "has_double_faced_cards": bool(stats.get("has_double_faced", 0)),
        "available_languages": stats.get("available_languages", "").split(",") if stats.get("available_languages") else [],
        "available_layouts": stats.get("available_layouts", "").split(",") if stats.get("available_layouts") else [],
        "value_card_max_eur": round(stats.get("value_card_max_eur", 0) or 0, 2),
        "foil_percentage": stats.get("foil_percentage", 0),
        "rarity_ratio_common": stats.get("rarity_common_pct", 0),
        "rarity_ratio_uncommon": stats.get("rarity_uncommon_pct", 0),
        "rarity_ratio_rare": stats.get("rarity_rare_pct", 0),
        "rarity_ratio_mythic": stats.get("rarity_mythic_pct", 0),
        "digital_only": False
    }
    sets.append(entry)

# ─── Sauvegarde JSON ─────────────────────────────────────────
EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(EXPORT_PATH, "w", encoding="utf-8") as f:
    json.dump(sets, f, ensure_ascii=False, indent=2)

print(f"✅ {EXPORT_PATH} généré ({len(sets)} sets)")

# ─── Copie pour publication GitHub Pages ─────────────────────
os.makedirs(PUBLIC_PATH.parent, exist_ok=True)
shutil.copyfile(EXPORT_PATH, PUBLIC_PATH)
print(f"📤 sets.json copié vers {PUBLIC_PATH}")

# ─── Git auto-commit/push (facultatif) ───────────────────────
try:
    subprocess.run(["git", "config", "--global", "user.name", "OctoBot"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "bot@octodecks.dev"], check=True)
    subprocess.run(["git", "add", str(PUBLIC_PATH)], check=True)
    subprocess.run(["git", "commit", "-m", "🔄 sets.json enrichi auto-publié"], check=True)

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        remote_url = f"https://x-access-token:{token}@github.com/LePoulpeMTG/OctoDecks.git"
        subprocess.run(["git", "push", remote_url], check=True)
    else:
        subprocess.run(["git", "push"], check=True)

    print("✅ Fichier sets.json publié via GitHub Pages")
except subprocess.CalledProcessError as e:
    print("⚠️ Git auto-push échoué :", e)
