#!/usr/bin/env python3
"""
🐙 debug_core.py

Utilitaire de débogage pour les scripts CORE :
- Reset des données journalières
- Exécution des scripts daily (carte / set)
- Vérification des résultats

Usage :
  python tools/dev/debug_core.py --reset
  python tools/dev/debug_core.py --run card
  python tools/dev/debug_core.py --run set
  python tools/dev/debug_core.py --check
"""

import argparse
import subprocess
import sqlite3
from datetime import date

DB_PATH = "database/octobase_reference.db"
today = date.today().isoformat()


def reset_daily():
    print(f"🔁 Réinitialisation des données du jour : {today}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for table in ["prices_daily_card", "prices_daily_set"]:
        cur.execute(f"DELETE FROM {table} WHERE date = ?;", (today,))
        print(f"🧹 {cur.rowcount} lignes supprimées de {table}")
    conn.commit()
    conn.close()
    print("✅ Nettoyage terminé.")


def run_script(script_name):
    path = {
        "set": "tools/prices_set_daily_add.py",
    }.get(script_name)

    if not path:
        print("❌ Script inconnu.")
        return

    print(f"🚀 Exécution : {path}")
    result = subprocess.run(["python", path], capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr:
        print("⚠️ STDERR :", result.stderr.strip())


def check_daily_counts():
    print(f"🔍 Vérification des insertions pour {today}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for table in ["prices_daily_card", "prices_daily_set"]:
        cur.execute(f"SELECT COUNT(*) FROM {table} WHERE date = ?;", (today,))
        count = cur.fetchone()[0]
        print(f"📊 {table}: {count} lignes")
    conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Supprimer les données du jour")
    parser.add_argument("--run", choices=["set", "week_card", "week_set"], help="Lancer un script de traitement")
    parser.add_argument("--check", action="store_true", help="Afficher les lignes insérées")
    args = parser.parse_args()

    if args.reset:
        reset_daily()
    if args.run:
        run_script(args.run)
    if args.check:
        check_daily_counts()

    if not any(vars(args).values()):
        parser.print_help()


if __name__ == "__main__":
    main()
