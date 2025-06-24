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
| oracle_id         | TEXT FK | Réf. vers `cards.oracle_id`                   |
| set_code          | TEXT FK | Réf. vers `sets.set_code`                     |
| collector_number  | TEXT    | Numéro de collection                          |
| lang              | TEXT    | Langue (« en », « fr », …)                    |
| rarity            | TEXT    | Rareté (« common », « mythic », …)            |
| layout            | TEXT    | Layout (normal, modal_dfc, …)                 |
| image_front_uri   | TEXT    | URL image **recto**                           |
| image_back_uri    | TEXT    | URL image **verso** (NULL si carte 1 face)    |
| card_faces_json   | TEXT    | JSON brut des faces (recto/verso)             |
| scryfall_uri      | TEXT    | Lien fiche VO                                 |
| cardmarket_uri    | TEXT    | Lien MKM (si dispo)                           |
| foil              | BOOL    | Existe en foil ?                              |
| nonfoil           | BOOL    | Existe en non-foil ?                          |

## 📁 2-bis. `card_legalities`

Légalité par **design de carte** (oracle_id).

| Champ     | Type | Description                                  |
|-----------|------|----------------------------------------------|
| oracle_id | TEXT | Réf. `cards.oracle_id`                       |
| format    | TEXT | Nom du format (standard, pioneer, …)         |
| status    | TEXT | `legal`, `not_legal`, `banned`, `restricted` |
| PRIMARY KEY | —  | `(oracle_id, format)`                        |


---

## 📁 3. `sets`

| Champ          | Type                             | Description                                    |
|----------------|----------------------------------|------------------------------------------------|
| set_id         | INTEGER PK AUTOINCREMENT         | Identifiant interne (ordre chronologique)      |
| set_code       | TEXT UNIQUE                      | Code officiel du set (ex. « neo »)             |
| name           | TEXT                             | Nom complet de l’édition                       |
| release_date   | TEXT                             | Date de sortie (AAAA-MM-JJ)                    |
| set_type       | TEXT                             | core, expansion, commander, …                  |
| total_cards    | INTEGER                          | Nombre total de cartes                         |
| is_digital     | BOOLEAN DEFAULT 0                | 1 si set uniquement digital                    |
| icon_svg_uri   | TEXT                             | URL du logo/icone SVG de l’édition             |


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

Historique **hebdomadaire** (conservation permanente) des prix d’une impression.  
Une ligne par combinaison **carte × semaine** (semaine ISO-8601 : `YYYY-Www`, ex. `2025-W26`).

| Champ        | Type  | Description                                       |
|--------------|-------|---------------------------------------------------|
| scryfall_id  | TEXT  | Réf. `prints.scryfall_id`                          |
| week         | TEXT  | Semaine ISO-8601 (`YYYY-Www`)                      |
| eur_avg      | REAL  | **Moyenne** € VO sur la semaine                    |
| eur_min      | REAL  | **Min** € VO                                      |
| eur_max      | REAL  | **Max** € VO                                      |
| eur_foil_avg | REAL  | Moyenne € foil                                     |
| usd_avg      | REAL  | Moyenne $ VO                                       |
| usd_min      | REAL  | Min $ VO                                           |
| usd_max      | REAL  | Max $ VO                                           |
| usd_foil_avg | REAL  | Moyenne $ foil                                     |
| usd_etched_avg | REAL| Moyenne $ etched                                   |

> **Clé primaire** recommandée : `(scryfall_id, week)`  
> Les valeurs *_avg*/*_min*/*_max* proviennent de l’agrégation des _prices_daily_card_ sur la semaine concernée.

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

Historique **hebdomadaire** des prix agrégés par set.  
Une ligne par **set × semaine** (ISO : `YYYY-Www`).

| Champ        | Type   | Description                                              |
|--------------|--------|----------------------------------------------------------|
| set_id       | INT    | Réf. `sets.set_id` (clé interne du set)                  |
| week         | TEXT   | Semaine ISO-8601 (`YYYY-Www`, ex. `2025-W26`)            |
| avg_eur      | REAL   | **Moyenne** € de toutes les impressions du set           |
| min_eur      | REAL   | **Prix minimum** € trouvé sur la semaine                 |
| max_eur      | REAL   | **Prix maximum** € trouvé sur la semaine                 |
| avg_usd      | REAL   | Moyenne $                                                |
| min_usd      | REAL   | Minimum $                                                |
| max_usd      | REAL   | Maximum $                                                |
| total_cards  | INT    | Nombre d’impressions prises en compte                    |

> **Clé primaire** recommandée : `(set_id, week)`  
> Les valeurs sont issues d’une agrégation hebdomadaire des données présentes dans `prices_daily_card`.


---

## 📁 8. `users`  *(Firestore)*

| Champ          | Type    | Description                                                     |
|----------------|---------|-----------------------------------------------------------------|
| user_id        | TEXT PK | UID Firebase (clé du document)                                  |
| email          | TEXT    | Adresse e-mail de connexion                                     |
| created_at     | TEXT    | Date de création du compte (timestamp ISO)                      |
| role           | TEXT    | `user` (défaut) / `admin` / `moderator`                         |
| display_name   | TEXT    | Pseudo visible dans l’app                                       |
| first_name     | TEXT    | Prénom (pour les envois)                                        |
| last_name      | TEXT    | Nom de famille                                                  |
| street_address | TEXT    | Adresse (rue + n°)                                              |
| city           | TEXT    | Ville                                                           |
| postal_code    | TEXT    | Code postal                                                     |
| country        | TEXT    | Pays (ISO-3166)                                                 |
| avatar_url     | TEXT    | URL avatar / gravatar                                           |
| address        | TEXT    | (Optionnel) Zone libre pour « Tinder MTG » (rayon, région…)     |

> 🔒 **Règles Firestore (exemple)**  
> ```js
> match /users/{uid} {
>   allow read, write: if request.auth != null && request.auth.uid == uid;
>   allow read: if request.auth != null && request.auth.token.role == 'admin';
> }
> ```


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

| Champ              | Type | Description                                     |
|--------------------|------|-------------------------------------------------|
| oracle_id          | TEXT | Réf. `cards.oracle_id`                          |
| set_code           | TEXT | Réf. `sets.set_code`                            |
| collector_number   | TEXT | Numéro de collection                            |
| lang               | TEXT | Langue traduite                                 |
| name               | TEXT | Nom traduit                                     |
| oracle_text        | TEXT | Texte oracle traduit                            |
| flavor_text        | TEXT | (Optionnel) Texte d’ambiance traduit            |
| image_front_uri    | TEXT | URL de l’image **recto** dans cette langue      |
| image_back_uri     | TEXT | URL de l’image **verso** (NULL si 1 face)       |
| **PRIMARY KEY**    | —    | `(oracle_id, set_code, lang)`                   |

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
