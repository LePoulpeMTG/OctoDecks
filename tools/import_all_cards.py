#!/usr/bin/env python3
"""import_all_cards.py
Télécharge (si besoin) le dump *All Cards* de Scryfall, puis l’importe
dans la base SQLite `octobase_reference.db`. Gère automatiquement les layouts
inconnus en les ajoutant dans `layouts_by_face.json`.
"""

import sqlite3, gzip, ijson, json, shutil, requests, hashlib, os, sys
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

# -------------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # LePoulpeMTG_OctoDecks
DB_PATH      = PROJECT_ROOT / "database" / "octobase_reference.db"
BULK_DIR     = PROJECT_ROOT / "tools" / "data" / "bulk"
LAYOUT_FILE  = PROJECT_ROOT / "tools" / "data" / "layouts_by_face.json"
BULK_DIR.mkdir(parents=True, exist_ok=True)

WANTED_FORMATS = {
    "standard", "pioneer", "modern",
    "legacy", "vintage", "commander", "pauper"
}

# -------------------------------------------------------------------------
# OUTILS LAYOUT
# -------------------------------------------------------------------------
def load_layout_map():
    data = json.loads(LAYOUT_FILE.read_text(encoding="utf-8"))
    return {l: 1 for l in data["one_face"]} | {l: 2 for l in data["two_faces"]}

def save_layout_map(layout_map):
    one = sorted([k for k, v in layout_map.items() if v == 1])
    two = sorted([k for k, v in layout_map.items() if v == 2])
    LAYOUT_FILE.write_text(json.dumps({"one_face": one, "two_faces": two},
                                      indent=2, ensure_ascii=False))

def face_count_from_card(card: dict) -> int:
    return 2 if len(card.get("card_faces", [])) > 1 else 1

# -------------------------------------------------------------------------
# BDD
# -------------------------------------------------------------------------
def open_db():
    print(">>> DB_PATH =", DB_PATH.resolve())
    print(">>> Existe  :", DB_PATH.exists())
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# -------------------------------------------------------------------------
# TÉLÉCHARGEMENT BULK DATA
# -------------------------------------------------------------------------
def latest_bulk_info():
    url = "https://api.scryfall.com/bulk-data"
    data = requests.get(url, timeout=60).json()["data"]
    rec = next(d for d in data if d["type"] == "all_cards")
    return rec["download_uri"], rec["updated_at"]

from tqdm import tqdm
import math, requests, shutil

def download_bulk_if_needed():
    dl_url, updated_at = latest_bulk_info()
    tag   = updated_at.split("T")[0]      # 2025-06-25
    fname = f"all-cards-{tag}.json.gz"
    fpath = BULK_DIR / fname
    if fpath.exists():
        print("Bulk déjà présent :", fname)
        return fpath

    # ─── Téléchargement avec barre de progression ─────────────────────────────
    print("Téléchargement du bulk :", fname)
    with requests.get(dl_url, stream=True, timeout=300) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0))
        chunk = 1 << 20                           # 1 MiB
        with open(fpath, "wb") as fh, tqdm(
            total=total, unit="B", unit_scale=True, unit_divisor=1024
        ) as bar:
            for data in r.iter_content(chunk_size=chunk):
                fh.write(data)
                bar.update(len(data))

    return fpath


# -------------------------------------------------------------------------
# INSERTIONS
# -------------------------------------------------------------------------
def extract_images(card, face_cnt):
    if face_cnt == 2:
        faces = card["card_faces"]
        return faces[0]["image_uris"]["normal"], faces[1]["image_uris"]["normal"]
    return card["image_uris"]["normal"], None

def insert_core(cur, card):
    cur.execute("""
        INSERT OR IGNORE INTO cards
        (oracle_id, name, type_line, cmc, color_identity,
         keywords, edhrec_rank, is_reserved, is_promo, layout)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (card["oracle_id"], card["name"], card.get("type_line",""),
            float(card.get("cmc",0) or 0),
            "".join(card.get("color_identity",[])),
            ";".join(card.get("keywords",[])),
            card.get("edhrec_rank"),
            int(card.get("reserved",False)),
            int(card.get("promo",False)),
            card["layout"]))
    cur.execute("""
        INSERT OR IGNORE INTO sets
        (set_code, name, release_date, set_type, icon_svg_uri)
        VALUES (?,?,?,?,?)
    """, (card["set"], card["set_name"], card["released_at"],
            card["set_type"], card.get("set_icon_svg_uri")))
    cur.execute("SELECT set_id FROM sets WHERE set_code=?", (card["set"],))
    return cur.fetchone()[0]

def insert_print(cur, card, set_id, front, back):
    cur.execute("""
        INSERT OR IGNORE INTO prints
        (scryfall_id, oracle_id, set_id, collector_number, lang,
         rarity, layout, image_front_uri, image_back_uri,
         scryfall_uri, foil, nonfoil)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (card["id"], card["oracle_id"], set_id,
            card["collector_number"], card["lang"], card["rarity"],
            card["layout"], front, back, card["scryfall_uri"],
            int(card.get("foil",False)), int(card.get("nonfoil",False))))

def insert_localization(cur, card, front, back):
    if card["lang"] == "en":
        return
    cur.execute("""
        INSERT OR IGNORE INTO card_localizations
        (oracle_id, set_code, collector_number, lang,
         name, oracle_text, flavor_text,
         image_front_uri, image_back_uri)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (card["oracle_id"], card["set"], card["collector_number"],
            card["lang"], card.get("printed_name") or card["name"],
            card.get("printed_text"), card.get("flavor_text"),
            front, back))

def insert_legalities(cur, card):
    for fmt, status in card["legalities"].items():
        if fmt in WANTED_FORMATS:
            cur.execute("""
                INSERT OR IGNORE INTO card_legalities
                (oracle_id, format, status) VALUES (?,?,?)
            """, (card["oracle_id"], fmt, status))

# -------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------
def main():
    bulk_file = download_bulk_if_needed()
    conn = open_db()
    cur  = conn.cursor()
    layout_map = load_layout_map()
    new_layout_flag = False

    with gzip.open(bulk_file, "rb") as fh:
        cards = ijson.items(fh, "item")
        for card in tqdm(cards, unit="cards"):
            if card["layout"] not in layout_map:
                fc = face_count_from_card(card)
                layout_map[card["layout"]] = fc
                new_layout_flag = True
                print(f"[WARN] nouveau layout {card['layout']} → {fc} face(s)")

            face_cnt = layout_map[card["layout"]]
            front, back = extract_images(card, face_cnt)

            set_id = insert_core(cur, card)
            insert_print(cur, card, set_id, front, back)
            insert_localization(cur, card, front, back)
            insert_legalities(cur, card)

    conn.commit()
    conn.close()

    if new_layout_flag:
        save_layout_map(layout_map)
        print("✔ layouts_by_face.json mis à jour.")

    print("✅ Import terminé.")

if __name__ == "__main__":
    main()
