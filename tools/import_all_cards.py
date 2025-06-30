#!/usr/bin/env python3
"""
Importe le dump **All Cards** de Scryfall dans la base SQLite
`database/octobase_reference.db`.

• Télécharge le bulk si nécessaire
• Insère / met à jour cartes, impressions, prix du jour
• Ajoute automatiquement les nouveaux layouts dans layouts_by_face.json
"""

from __future__ import annotations

import gzip
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from datetime import date
from typing import Dict, Tuple

import ijson
import requests
from tqdm import tqdm

# ───────────────────────────────────────────────
# CONFIGURATION GLOBALE
# ───────────────────────────────────────────────
PROJECT_ROOT   = Path(__file__).resolve().parents[1]
DB_PATH        = PROJECT_ROOT / "database" / "octobase_reference.db"
SCHEMA_FILE    = PROJECT_ROOT / "database" / "schema" / "schema_octobase.sql"
BULK_DIR       = PROJECT_ROOT / "tools" / "data" / "bulk"
LAYOUT_FILE    = PROJECT_ROOT / "tools" / "data" / "layouts_by_face.json"
TAG_FILE       = PROJECT_ROOT / "tools" / "data" / "last_bulk_tag.txt"

WANTED_FORMATS = {
    "standard", "pioneer", "modern",
    "legacy", "vintage", "commander", "pauper",
}

VERBOSE = False          # passe à True pour avoir plus de logs


# ───────────────────────────────────────────────
# UTILITAIRES
# ───────────────────────────────────────────────
@contextmanager
def smart_open(path: Path):
    """Ouvre en lecture binaire, gzip ou texte selon l’extension."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rb") as fh:
        yield fh


def log(msg: str):
    if VERBOSE:
        print(msg)


# ───────────────────────────────────────────────
# GESTION DES LAYOUTS
# ───────────────────────────────────────────────
def load_layout_map() -> Dict[str, int]:
    data = json.loads(LAYOUT_FILE.read_text(encoding="utf-8"))
    return {l: 1 for l in data["one_face"]} | {l: 2 for l in data["two_faces"]}


def save_layout_map(layout_map: Dict[str, int]) -> None:
    one = sorted(k for k, v in layout_map.items() if v == 1)
    two = sorted(k for k, v in layout_map.items() if v == 2)
    LAYOUT_FILE.write_text(
        json.dumps({"one_face": one, "two_faces": two}, indent=2, ensure_ascii=False)
    )


def face_count_from_card(card: dict) -> int:
    return 2 if len(card.get("card_faces", [])) > 1 else 1


# ───────────────────────────────────────────────
# BASE DE DONNÉES
# ───────────────────────────────────────────────
def open_db() -> sqlite3.Connection:
    """Ouvre la base et active les clés étrangères."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Crée les tables si elles n’existent pas."""
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='cards';"
    )
    if cur.fetchone():
        return

    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(f"Schema SQL introuvable : {SCHEMA_FILE}")

    conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))
    conn.commit()
    print("➡️  Schéma SQLite créé")


def prices_already_inserted(cur: sqlite3.Cursor, today: str) -> bool:
    cur.execute(
        "SELECT 1 FROM prices_daily_card WHERE date = ? LIMIT 1;",
        (today,),
    )
    return cur.fetchone() is not None


# ───────────────────────────────────────────────
# BULK SCRYFALL
# ───────────────────────────────────────────────
def latest_bulk_info() -> Tuple[str, str, str]:
    """
    Retourne : (download_url, tag_AAAA-MM-JJ, extension [.gz | ""])
    """
    resp = requests.get("https://api.scryfall.com/bulk-data", timeout=60).json()
    rec  = next(d for d in resp["data"] if d["type"] == "all_cards")
    url  = rec["download_uri"]
    tag  = rec["updated_at"].split("T")[0]
    ext  = ".gz" if url.endswith(".json.gz") else ""
    return url, tag, ext


def download_bulk_if_needed(url: str, tag: str, ext: str) -> Path:
    """
    Télécharge le fichier dans BULK_DIR si nécessaire et le retourne.
    """
    BULK_DIR.mkdir(parents=True, exist_ok=True)
    fpath = BULK_DIR / f"all-cards-{tag}.json{ext}"

    if fpath.exists():                         # déjà présent ⇒ essayer d’ouvrir
        try:
            opener = gzip.open if ext == ".gz" else open
            with opener(fpath, "rb") as fh:
                fh.read(4)                     # lecture-test
            log(f"Bulk déjà présent : {fpath.name}")
            return fpath
        except (OSError, gzip.BadGzipFile):
            fpath.unlink()                     # corrompu ⇒ on retélécharge

    # Téléchargement
    print("Téléchargement du bulk :", fpath.name)
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0))
        chunk = 1 << 20                       # 1 MiB
        with open(fpath, "wb") as fh, tqdm(
            total=total, unit="B", unit_scale=True, unit_divisor=1024
        ) as bar:
            for data in r.iter_content(chunk_size=chunk):
                fh.write(data)
                bar.update(len(data))

    return fpath


# ───────────────────────────────────────────────
# INSERTS (cards / prints / prix / …)
# ───────────────────────────────────────────────
def extract_images(card: dict, face_cnt: int) -> Tuple[str | None, str | None]:
    """Retourne (front_uri, back_uri) selon le layout."""
    if face_cnt == 1:
        return card.get("image_uris", {}).get("normal"), None

    if face_cnt == 2 and (faces := card.get("card_faces")):
        front = faces[0].get("image_uris", {}).get("normal")
        back  = faces[1].get("image_uris", {}).get("normal")
        return front, back
    return None, None


def insert_core(cur: sqlite3.Cursor, card: dict) -> int:
    """Insère les tables cards / sets et retourne set_id."""
    cur.execute(
        """
        INSERT OR IGNORE INTO cards
        (oracle_id, name, type_line, cmc, color_identity,
         keywords, edhrec_rank, is_reserved, is_promo, layout)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            card["oracle_id"],
            card["name"],
            card.get("type_line", ""),
            float(card.get("cmc", 0) or 0),
            "".join(card.get("color_identity", [])),
            ";".join(card.get("keywords", [])),
            card.get("edhrec_rank"),
            int(card.get("reserved", False)),
            int(card.get("promo", False)),
            card["layout"],
        ),
    )
    cur.execute(
        """
        INSERT OR IGNORE INTO sets
        (set_code, name, release_date, set_type, icon_svg_uri)
        VALUES (?,?,?,?,?)
        """,
        (
            card["set"],
            card["set_name"],
            card["released_at"],
            card["set_type"],
            card.get("set_icon_svg_uri"),
        ),
    )
    cur.execute("SELECT set_id FROM sets WHERE set_code = ?;", (card["set"],))
    return cur.fetchone()[0]


def insert_print(
    cur: sqlite3.Cursor,
    card: dict,
    set_id: int,
    front: str | None,
    back: str | None,
) -> None:
    cur.execute(
        """
        INSERT OR IGNORE INTO prints
        (scryfall_id, oracle_id, set_id, collector_number, lang,
         rarity, layout, image_front_uri, image_back_uri,
         scryfall_uri, foil, nonfoil)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            card["id"],
            card["oracle_id"],
            set_id,
            card["collector_number"],
            card["lang"],
            card["rarity"],
            card["layout"],
            front,
            back,
            card["scryfall_uri"],
            int(card.get("foil", False)),
            int(card.get("nonfoil", False)),
        ),
    )


def insert_localization(
    cur: sqlite3.Cursor,
    card: dict,
    front: str | None,
    back: str | None,
) -> None:
    if card["lang"] == "en":
        return

    cur.execute(
        """
        INSERT OR IGNORE INTO card_localizations
        (oracle_id, set_code, collector_number, lang,
         name, oracle_text, flavor_text,
         image_front_uri, image_back_uri)
        VALUES (?,?,?,?,?,?,?,?,?)
        """,
        (
            card["oracle_id"],
            card["set"],
            card["collector_number"],
            card["lang"],
            card.get("printed_name") or card["name"],
            card.get("printed_text"),
            card.get("flavor_text"),
            front,
            back,
        ),
    )


def insert_legalities(cur: sqlite3.Cursor, card: dict) -> None:
    for fmt, status in card["legalities"].items():
        if fmt in WANTED_FORMATS:
            cur.execute(
                "INSERT OR IGNORE INTO card_legalities (oracle_id, format, status) VALUES (?,?,?)",
                (card["oracle_id"], fmt, status),
            )


def insert_daily_price(cur: sqlite3.Cursor, card: dict, today: str) -> None:
    cur.execute(
        """
        INSERT OR IGNORE INTO prices_daily_card
        (scryfall_id, date, eur, eur_foil, usd, usd_foil, usd_etched)
        VALUES (?,?,?,?,?,?,?)
        """,
        (
            card["id"],
            today,
            card["prices"]["eur"],
            card["prices"]["eur_foil"],
            card["prices"]["usd"],
            card["prices"]["usd_foil"],
            card["prices"]["usd_etched"],
        ),
    )


# ───────────────────────────────────────────────
# MAIN WORKFLOW
# ───────────────────────────────────────────────
def main() -> None:
    bulk_path = next(Path("tools/data/bulk/").glob("all-cards-*.json.gz"))
    seen_oracle_ids = set()

    with smart_open(bulk_path) as f:
        for card in ijson.items(f, "item"):
        if "oracle_id" not in card:
            continue
        if card.get("layout") in ("token", "emblem", "art_series", "double_faced_token"):
            continue

        # Insert card une seule fois
        if card["oracle_id"] not in seen_oracle_ids:
            insert_legalities(cur, card)
            seen_oracle_ids.add(card["oracle_id"])

        # Récupération images (nécessaire pour print ET localization)
        face_cnt = face_count_from_card(card)
        front, back = extract_images(card, face_cnt)

        # Insert core (set + card) et récupère le set_id
        set_id = insert_core(cur, card)

        # Insert du print physique
        insert_print(cur, card, set_id, front, back)

        # Localisation (non-EN uniquement)
        insert_localization(cur, card, front, back)

        # Prix du jour
        insert_daily_price(cur, card, today)

    # 1) DB
    conn = open_db()
    ensure_schema(conn)
    cur  = conn.cursor()

    # 2) Bulk Scryfall
    url, tag, ext = latest_bulk_info()
    bulk_path     = download_bulk_if_needed(url, tag, ext)

    # 3) Skip si déjà traité + prix du jour déjà présents
    if tag == TAG_FILE.read_text().strip() if TAG_FILE.exists() else None:
        if prices_already_inserted(cur, today):
            print("ℹ️  Rien à faire : bulk + prix déjà en base")
            conn.close()
            return

    TAG_FILE.write_text(tag, encoding="utf-8")      # mémorise la version

    # 4) Layouts connus
    layout_map      = load_layout_map()
    new_layout_flag = False

    # 5) Parsing & insertion
    with smart_open(bulk_path) as fh:
        for card in tqdm(ijson.items(fh, "item"), unit="cartes"):
            if "oracle_id" not in card:        # tokens, helpers…
                continue

            if card["layout"] not in layout_map:
                fc = face_count_from_card(card)
                layout_map[card["layout"]] = fc
                new_layout_flag = True
                print(f"[WARN] nouveau layout '{card['layout']}' → {fc} face(s)")

            face_cnt            = layout_map[card["layout"]]
            img_front, img_back = extract_images(card, face_cnt)

            set_id              = insert_core(cur, card)
            insert_print(cur, card, set_id, img_front, img_back)
            insert_localization(cur, card, img_front, img_back)
            insert_legalities(cur, card)
            insert_daily_price(cur, card, today)

    conn.commit()
    conn.close()

    if new_layout_flag:
        save_layout_map(layout_map)
        print("✔ layouts_by_face.json mis à jour.")

    print("✅ Import terminé !")


if __name__ == "__main__":
    main()
