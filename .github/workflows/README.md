<!-- 📁 chemin relatif : .github\workflows\README.md -->
# ⚙️ Workflows GitHub Actions – OctoDeck

Ce dossier contient tous les workflows d'automatisation utilisés par le projet OctoDeck.  
Ils permettent d'assurer la mise à jour régulière des données, le suivi des prix et l'intégrité de l'arborescence du dépôt.

---

## 📦 Workflows disponibles

| Fichier                | Rôle |
|------------------------|------|
| `daily_prices.yml`     | Télécharge et exporte les prix journaliers des cartes (à heure fixe) |
| `weekly_prices.yml`    | Calcule les moyennes hebdomadaires par carte ou set |
| `main.yml`             | Pipeline CI principal (lint, tests, vérifications) |
| `tree.yml`             | Génère automatiquement le fichier `TREE.txt` (arborescence) à chaque push sur `main` |

---

## 🔄 Fréquence des tâches

| Workflow           | Déclencheur       |
|--------------------|-------------------|
| `daily_prices.yml` | Tous les jours (cron) |
| `weekly_prices.yml`| Chaque semaine (cron) |
| `tree.yml`         | Push sur `main`   |
| `main.yml`         | Push / PR sur `main` |

---

## 🧪 Tests CI (main.yml)

- Formatage / lint des fichiers Dart
- Tests unitaires (à venir)
- Génération du site de doc si activée

---

## 🔗 Liens utiles

- 📁 [Scripts utilisés](../../scripts/)
- 📁 [Base SQLite + snapshots](../../data/)
- 📄 [TREE.txt](../../TREE.txt)
