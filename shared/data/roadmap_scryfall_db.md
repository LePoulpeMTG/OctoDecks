
# Roadmap – Base de Données Scryfall Référence

Ce document décrit les étapes pour construire la base de données principale Scryfall, utilisée comme référence pour toutes les applications OctoDecks.

---

## 🎯 Objectif principal
Créer une base de données centralisée et optimisée, chargée depuis le JSON complet de Scryfall, avec les informations principales sur les cartes et les sets.

Elle stockera également :
- L’historique **quotidien** des prix sur les **90 derniers jours**
- L’historique **hebdomadaire** des prix pour **conservation permanente**

---

## Étapes de la roadmap

### 1. 📦 Préparation
- [x] Créer le dossier partagé : `LePoulpeMTG_OctoDecks/shared/data/`
- [x] Définir le schéma SQL (déjà commencé)
- [x] Identifier les layouts et simplifier leur gestion avec un fichier JSON

### 2. 📥 Téléchargement & Parsing
- Télécharger le fichier `all-cards.json` de Scryfall (~2.2 Go brut, ~220 Mo compressé)
- Parser le fichier en flux pour éviter de tout charger en mémoire
- Extraire les données pertinentes (cartes, sets, prix, layout, oracle text…)

### 3. 🛠 Création de la base SQLite
- Générer la base `scryfall_reference.db` dans `shared/data/`
- Tables prévues :
  - `cards`
  - `sets`
  - `prices_daily_card`
  - `prices_weekly_card`
  - `prices_daily_set`
  - `prices_weekly_set`
- Créer les indexes nécessaires pour performance

### 4. 📊 Insertion des données
- Insérer les cartes et sets
- Gérer les layouts multi-faces proprement
- Enregistrer les prix si disponibles
- Associer les impressions à un `oracle_id` unique

### 5. 🕓 Mise à jour et historique
- Script de mise à jour automatique chaque jour (cron, GitHub action ou app admin)
- Si un prix a changé : ajouter une ligne dans `prices_daily_card`
- Chaque semaine : injecter les valeurs hebdomadaires dans `prices_weekly_card` & `prices_weekly_set`

---

## 🔁 Fréquence de mise à jour
- Quotidienne pour les prix via endpoint Scryfall par ID
- Hebdomadaire pour archivage

---
---

## 🌍 Gestion des localisations (multi-langues)

### Étape 1 : table `set_localizations`
| Champ | Type | Description |
|-------|------|-------------|
| set_code | TEXT PK | Code du set |
| lang | TEXT PK | Langue ISO-639-1 (fr, es, de…) |
| is_available | BOOL | La langue existe chez la source ? |
| is_enabled | BOOL | Activée pour import ? |

> ⚙️  Lorsqu’on coche **is_enabled = 1**, on déclenche l’import des traductions pour ce set + langue.

---

### Étape 2 : récupération des traductions
1. Pour chaque carte du set :  
   `https://api.scryfall.com/cards/{set}/{collector_number}/{lang}`
2. Extraire `printed_name`, `printed_text` (et `flavor_text` si présent).
3. Insérer/mettre à jour la table `card_localizations` :

| Champ | Type | Description |
|-------|------|-------------|
| oracle_id | TEXT | Réf. `cards` |
| set_code | TEXT | Réf. `sets` |
| collector_number | TEXT | Numéro de collection |
| lang | TEXT | Langue |
| name | TEXT | Nom traduit |
| oracle_text | TEXT | Texte oracle traduit |
| flavor_text | TEXT | Texte d’ambiance (optionnel) |
| PRIMARY KEY | (oracle_id, set_code, lang) |

---

### Étape 3 : automatisation
- **Admin Web** : checklist par set/ langue → coche ➜ job d’import.
- **CLI** : `python import_localizations.py --set eld --lang es`.
- Historique des imports stocké pour relancer uniquement les cartes nouvelles ou mises à jour.

---

### Étape 4 : recherche multilingue
- Par défaut on cherche dans `cards.name` / `oracle_text`.
- Si l’utilisateur choisit une langue :  
  1. On joint sur `card_localizations` (si dispo)  
  2. Fallback VO si la traduction manque.

---


## 🧪 Étapes futures
- Exposer en lecture seule via une API REST
- Créer une interface web admin pour visualiser et auditer les mises à jour
- Synchronisation avec Firestore dans un second temps

---

## 📁 Localisation du fichier
Ce fichier est stocké dans :
```
LePoulpeMTG_OctoDecks/shared/data/roadmap_scryfall_db.md
```
