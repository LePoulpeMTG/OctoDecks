#!/usr/bin/env python3
"""
Ajoute automatiquement un commentaire en première ligne de chaque README.md
indiquant son chemin relatif depuis la racine du projet.
"""

import os

# Définit la racine du projet, peu importe où se trouve ce script
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))  # 2 niveaux au-dessus de tools/dev

def process_readme(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Vérifie si un tag chemin est déjà présent
    if lines and lines[0].strip().startswith("<!--") and "README.md" in lines[0]:
        return  # déjà traité

    relative_path = os.path.relpath(file_path, PROJECT_ROOT)
    header = f"<!-- 📁 chemin relatif : {relative_path} -->\n"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.writelines(lines)

def walk_and_process(root):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower() == "readme.md":
                process_readme(os.path.join(dirpath, filename))

if __name__ == "__main__":
    walk_and_process(PROJECT_ROOT)
    print("✅ Tous les README.md ont été annotés avec leur chemin relatif.")
