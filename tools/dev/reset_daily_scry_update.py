#!/usr/bin/env python3
"""
🧹 reset_daily_scry_update.py

Supprime les entrées du jour dans :
- prices_daily_card
- prices_daily_set

Permet de rejouer manuellement les scripts journaliers
pendant les phases de test/débogage.
"""

import sqlite3
from datetime import date

DB_PATH = "database/octobase_reference.db"
today = date.today().isoformat()

def reset_table(cur, table: str):
    cur.execute(f"DELETE FROM {table} WHERE date = ?;", (today,))
    print(f"🧹 {cur.rowcount} lignes supprimées de {table}")

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print(f"📅 Date ciblée : {today}")
    reset_table(cur, "prices_daily_card")
    reset_table(cur, "prices_daily_set")

    conn.commit()
    conn.close()
    print("✅ Nettoyage terminé.")

if __name__ == "__main__":
    main()
