#!/usr/bin/env python3
"""
Extrait toutes les cartes d’un set spécifique depuis le bulk Scryfall.
"""
import gzip
import ijson
import json
import decimal
from pathlib import Path

# 📁 Adapte le chemin vers ton bulk ici
BULK_PATH = Path("tools/data/bulk/all-cards-2025-06-*.json.gz")
SET_CODE = "dft"  # ⇦ set cible
OUT_FILE = Path("dft-cards.json")

# Encoder pour Decimal → float (sinon json.dumps plante)
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)

def main():
    bulk_file = next(BULK_PATH.parent.glob(BULK_PATH.name))
    result = []

    with gzip.open(bulk_file, "rb") as f:
        for card in ijson.items(f, "item"):
            if card.get("set") == SET_CODE:
                result.append(card)

    print(f"✅ {len(result)} cartes extraites pour le set '{SET_CODE}'")

    OUT_FILE.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, cls=DecimalEncoder),
        encoding="utf-8"
    )
    print(f"📤 Fichier exporté : {OUT_FILE} ({OUT_FILE.stat().st_size / 1024:.1f} Ko)")

if __name__ == "__main__":
    main()
