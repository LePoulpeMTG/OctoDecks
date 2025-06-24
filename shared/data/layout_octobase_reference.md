# 📦 OctoBase Reference Layout

Ce document définit les tables principales de la base de données **OctoBase**, utilisée comme source centrale pour toutes les applications OctoDecks (web, mobile, desktop).

---

## 📁 1. `cards`

| Champ            | Type    | Description                                   |
|------------------|---------|-----------------------------------------------|
| oracle_id        | TEXT PK | ID unique partagé entre éditions             |
| name             | TEXT    | Nom (VO)                                      |
| type_line        | TEXT    | Type complet (« Creature — Elf Wizard », …)   |
| cmc              | REAL    | Coût converti de mana                         |
| color_identity   | TEXT    | Couleurs (concat. « WUBRG »)                 |
| keywords         | TEXT    | Mots-clés séparés par `;`                     |
| edhrec_rank      | INTEGER | Classement EDHRec                             |
| is_reserved      | BOOL    | Dans la reserved list ?                       |
| is_promo         | BOOL    | Carte promotionnelle ?                        |
| layout           | TEXT    | Layout principal (normal, transform, …)       |

---

## 📁 2. `prints`

| Champ             | Type    | Description                                   |
|-------------------|---------|-----------------------------------------------|
| scryfall_id       | TEXT PK | ID unique de l’impression                     |
| oracle_id         | TEXT FK | Réf. vers `cards.oracle_id`                  |
| set_code          | TEXT FK | Réf. vers `sets.set_code`                    |
| collector_number  | TEXT    | Numéro de collection                          |
| lang              | TEXT    | Langue (« en », « fr », …)                    |
| rarity            | TEXT    | Rareté (« common », « mythic », …)            |
| layout            | TEXT    | Layout (normal, modal_dfc, …)                 |
| image_uri         | TEXT    | URL image principale                          |
| card_faces_json   | TEXT    | JSON brut des faces (recto/verso)             |
| scryfall_uri      | TEXT    | Lien fiche VO                                 |
| cardmarket_uri    | TEXT    | Lien MKM (si dispo)                           |
| foil              | BOOL    | Existe en foil ?                              |
| nonfoil           | BOOL    | Existe en non-foil ?                          |

---

## 📁 3. `sets`

| Champ        | Type                             | Description                                |
|--------------|----------------------------------|--------------------------------------------|
| set_id       | INTEGER PK AUTOINCREMENT         | Identifiant interne (ordre chronologique)  |
| set_code     | TEXT UNIQUE                      | Code officiel du set (ex. « neo »)         |
| name         | TEXT                             | Nom complet de l’édition                   |
| release_date | TEXT                             | Date de sortie (AAAA-MM-JJ)                |
| set_type     | TEXT                             | core, expansion, commander, …              |
| total_cards  | INTEGER                          | Nombre total de cartes                     |
| is_digital   | BOOLEAN DEFAULT 0                | 1 si set uniquement digital                |

---

## 📁 4. `prices_daily_card`

Historique **quotidien** par impression.

| Champ       | Type | Description                        |
|-------------|------|------------------------------------|
| scryfall_id | TEXT | Réf. `prints.scryfall_id`          |
| date        | TEXT | AAAA-MM-JJ                         |
| eur         | REAL | Prix € VO                          |
| eur_foil    | REAL | Prix € foil                        |
| usd         | REAL | Prix $ VO                          |
| usd_foil    | REAL | Prix $ foil                        |
| usd_etched  | REAL | Prix $ etched                      |

---

## 📁 5. `prices_weekly_card`

Même colonnes que `prices_daily_card`, mais **une ligne par semaine** (`week` ISO-8601).

---

## 📁 6. `prices_daily_set`

| Champ       | Type | Description                    |
|-------------|------|--------------------------------|
| set_code    | TEXT | Réf. `sets.set_code`           |
| date        | TEXT | AAAA-MM-JJ                     |
| avg_eur     | REAL | Prix moyen € sur le set        |
| avg_usd     | REAL | Prix moyen $ sur le set        |
| total_cards | INT  | Cartes comptabilisées          |

---

## 📁 7. `prices_weekly_set`

Même logique qu’en **daily**, mais **une ligne par semaine**.

---

## 📁 8. `users` *(Firestore, pas SQLite)*

| Champ      | Type  | Description                    |
|------------|-------|--------------------------------|
| user_id    | TEXT  | UID Firebase                   |
| email      | TEXT  | Email                          |
| created_at | TEXT  | Date création                  |

---

## 📁 9. `set_localizations`

| Champ        | Type  | Description                                  |
|--------------|-------|----------------------------------------------|
| set_code     | TEXT  | Code du set                                  |
| lang         | TEXT  | Code langue (« fr », « es », …)              |
| is_enabled   | BOOL  | Activé dans OctoDecks ?                      |
| is_available | BOOL  | Présent chez la source Scryfall ?            |
| PRIMARY KEY  | (set_code, lang) |

---

## 📁 10. `card_localizations`

| Champ             | Type | Description                             |
|-------------------|------|-----------------------------------------|
| oracle_id         | TEXT | Réf. `cards.oracle_id`                  |
| set_code          | TEXT | Réf. `sets.set_code`                    |
| collector_number  | TEXT | Numéro                                  |
| lang              | TEXT | Langue traduite                         |
| name              | TEXT | Nom traduit                             |
| oracle_text       | TEXT | Texte oracle traduit                    |
| flavor_text       | TEXT | (Optionnel) Texte d’ambiance traduit    |
| PRIMARY KEY       | (oracle_id, set_code, lang) |

---

## 📁 11. Données utilisateur hors BDD centrale

Ces collections vivent **dans Firestore** ou en **SQLite locale** par user :

- `/users/{uid}/collection`
- `/users/{uid}/wishlist`
- `/users/{uid}/decks`
- `/users/{uid}/trade`
- `/users/{uid}/sell`

---

*Document généré le 24 juin 2025 – OctoDecks 🐙*
