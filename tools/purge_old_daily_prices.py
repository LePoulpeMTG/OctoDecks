#!/usr/bin/env python3
"""
Supprime les entrées de prices_daily_card et prices_daily_set plus vieilles que 90 jours.
À exécuter une fois par jour après l'insertion des prix.
"""
import sqlite3
from datetime import date, timedelta

DB_PATH = "database/octobase_reference.db"

cutoff = (date.today() - timedelta(days=90)).isoformat()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for table in ("prices_daily_card", "prices_daily_set"):
    cur.execute(f"DELETE FROM {table} WHERE date < ?;", (cutoff,))
    print(f"🧹 {cur.rowcount} lignes supprimées de {table}")

conn.commit()
conn.close()
print("✅ Purge des prix > 90 jours terminée")
