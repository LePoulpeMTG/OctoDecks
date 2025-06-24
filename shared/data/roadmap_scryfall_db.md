
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
