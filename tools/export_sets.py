import sqlite3
import json
import os
import subprocess
import shutil
from pathlib import Path

# Connexion à la base
conn = sqlite3.connect("database/octobase_reference.db")
cursor = conn.cursor()

# Récupération des sets
cursor.execute("""
    SELECT
        set_code,
        name,
        release_date,
        icon_svg_uri,
        total_cards
    FROM sets
    ORDER BY release_date DESC
""")
sets = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

# Création du dossier exports si nécessaire
os.makedirs("exports", exist_ok=True)

# Écriture du fichier JSON
with open("exports/sets.json", "w", encoding="utf-8") as f:
    json.dump(sets, f, ensure_ascii=False, indent=2)

print(f"✅ exports/sets.json généré ({len(sets)} entrées)")

# --- Publication GitHub Pages ---

# Copie vers le dossier data/
dst = Path("data/sets.json")
os.makedirs("data", exist_ok=True)
shutil.copyfile("exports/sets.json", dst)
print("📤 sets.json copié vers data/sets.json pour publication via GitHub Pages")

# Git commit auto (si contexte GitHub Actions ou local)
try:
    subprocess.run(["git", "config", "--global", "user.name", "OctoBot"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "bot@octodecks.dev"], check=True)
    subprocess.run(["git", "add", "-f", "data/sets.json"], check=True)
    subprocess.run(["git", "commit", "-m", "🔄 sets.json auto-publié pour GitHub Pages"], check=True)

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        remote_url = "https://x-access-token:{}@github.com/LePoulpeMTG/OctoDecks.git".format(token)
        subprocess.run(["git", "push", remote_url], check=True)
    else:
        subprocess.run(["git", "push"], check=True)

    print("✅ Fichier sets.json publié via GitHub Pages")
except subprocess.CalledProcessError as e:
    print("⚠️ Git auto-push échoué :", e)