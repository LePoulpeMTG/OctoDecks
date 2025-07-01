<!-- 📁 chemin relatif : database/schema/README.md -->

# 🔠 Schéma de la base de données OctoBase

Ce dossier contient le fichier `schema_octobase.sql` qui définit le schéma initial de la base SQLite utilisée par le projet **OctoDeck**.

Il est automatiquement appliqué à la première exécution du script `tools/import_all_cards.py` si la base est vide.

---

## 🏛️ Tables principales

| Table                  | Description |
|------------------------|-------------|
| `cards`               | Infos globales (oracle_id, nom, type, cmc...) |
| `sets`                | Infos sur les extensions Magic (code, nom, date) |
| `prints`              | Déclinaisons de cartes (scryfall_id, collector_number, rarity...) |
| `card_localizations`  | Données localisées (nom VF, texte oracle...) |
| `card_legalities`     | Format & statut de légalité par oracle_id |
| `layouts_by_face`     | Mappage layout → nombre de faces (1 ou 2) |
| `prices_daily_card`   | Historique quotidien des prix par carte (sur 90 jours) |
| `prices_daily_set`    | Historique quotidien des prix agrégés par set |
| `prices_weekly_card`  | Historique hebdomadaire (min, max, moy) par carte |
| `prices_weekly_set`   | Historique hebdomadaire (moy, total, cartes pricées) par set |

---

## 🔢 Flux d'alimentation des données

### 📅 PHASE 1 : Import initial depuis Scryfall

- Script : [`tools/import_all_cards.py`](../../tools/import_all_cards.py)
- Fonction :
  - Télécharge le bulk `all-cards.json` de Scryfall si besoin
  - Crée les tables si la base est vide (`ensure_schema()`)
  - Insère toutes les cartes, sets, impressions, localisations, legalités
  - Remplit `prices_daily_card` avec les prix du jour
  - Met à jour `layouts_by_face.json` si un nouveau layout est rencontré

### ⏰ PHASE 2 : Mise à jour quotidienne (historique)

- Scripts :
  - [`tools/prices_card_daily_add.py`](../../tools/prices_card_daily_add.py)
  - [`tools/prices_set_daily_add.py`](../../tools/prices_set_daily_add.py)
- Fonction :
  - Ajoute les prix du jour dans `prices_daily_card` et `prices_daily_set`
  - Supprime les données > 90 jours automatiquement (via `purge_old_daily_prices.py`)

### 🌐 PHASE 3 : Historique hebdomadaire

- Scripts :
  - [`tools/prices_card_weekly_add.py`](../../tools/prices_card_weekly_add.py)
  - [`tools/prices_set_weekly_add.py`](../../tools/prices_set_weekly_add.py)
- Fonction :
  - Calcule et insère la moyenne, le min et le max des prix sur 7 jours glissants
  - Les données sont conservées **sans limite** dans le temps

---

## ⚖️ Fréquence et automatisation

Tout ce pipeline est orchestré par :
- [`daily_scry_update.yml`](../../.github/workflows/daily_scry_update.yml) : 
  - Exécuté chaque heure
  - Ne fait une mise à jour que si Scryfall a publié un nouveau bulk
  - Gère l’import + l’agrégation + l’upload Firebase

---

## 🚀 Prochaine étape

L’API REST s’appuiera sur ces tables pour exposer les données aux interfaces Flutter (Viewer, WebAdmin).
