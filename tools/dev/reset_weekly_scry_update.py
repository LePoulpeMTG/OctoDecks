#!/usr/bin/env python3
"""
🧹 reset_weekly_scry_update.py

Supprime les entrées de la semaine courante dans :
- prices_weekly_card
- prices_weekly_set

Utile pour rejouer les scripts hebdomadaires lors des phases de debug.
"""

import sqlite3
from datetime import datetime

DB_PATH = "database/octobase_reference.db"
week = datetime.utcnow().strftime("%Y-%W")

def reset_table(cur, table: str):
    cur.execute(f"DELETE FROM {table} WHERE week = ?;", (week,))
    print(f"🧹 {cur.rowcount} lignes supprimées de {table}")

def main():
    print(f"🔁 Réinitialisation des données de la semaine : {week}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    reset_table(cur, "prices_weekly_card")
    reset_table(cur, "prices_weekly_set")

    conn.commit()
    conn.close()
    print("✅ Nettoyage terminé.")

if __name__ == "__main__":
    main()
