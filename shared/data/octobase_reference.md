# 📦 OctoBase Reference Layout

Mise à jour : 2025-06-25

---

## 📁 1. `cards`

| Champ            | Type    | Description                           |
|------------------|---------|---------------------------------------|
| oracle_id        | TEXT PK | Identifiant partagé entre éditions    |
| name             | TEXT    | Nom (VO)                              |
| type_line        | TEXT    | Type complet                          |
| cmc              | REAL    | Coût converti de mana                 |
| color_identity   | TEXT    | Couleurs WUBRG concaténées            |
| keywords         | TEXT    | Mots‑clés `;` séparés                 |
| edhrec_rank      | INT     | Classement EDHRec                     |
| is_reserved      | BOOL    | Reserved list ?                       |
| is_promo         | BOOL    | Carte promo ?                         |
| layout           | TEXT    | Layout principal                      |

---

## 📁 2. `prints`

| Champ              | Type    | Description                                   |
|--------------------|---------|-----------------------------------------------|
| scryfall_id        | TEXT PK | ID unique impression                          |
| oracle_id          | TEXT FK | → `cards.oracle_id`                           |
| set_id             | INT FK  | → `sets.set_id`                               |
| collector_number   | TEXT    | Numéro de collection                          |
| lang               | TEXT    | Langue (en, fr, es, ...)                      |
| rarity             | TEXT    | Rareté                                        |
| layout             | TEXT    | Layout                                        |
| image_front_uri    | TEXT    | URL image recto                               |
| image_back_uri     | TEXT    | URL image verso (NULL si 1 face)              |
| card_faces_json    | TEXT    | JSON brut des faces                           |
| scryfall_uri       | TEXT    | Lien Scryfall                                 |
| cardmarket_uri     | TEXT    | Lien MKM                                      |
| foil               | BOOL    | Existe en foil ?                              |
| nonfoil            | BOOL    | Existe en non‑foil ?                          |

---

## 📁 2‑bis. `card_legalities`

| Champ     | Type | Description                               |
|-----------|------|-------------------------------------------|
| oracle_id | TEXT | → `cards.oracle_id`                       |
| format    | TEXT | standard, pioneer, modern, ...            |
| status    | TEXT | legal / banned / restricted / not_legal   |
| PK        | —    | `(oracle_id, format)`                     |

---

## 📁 3. `sets`

| Champ          | Type                             | Description                            |
|----------------|----------------------------------|----------------------------------------|
| set_id         | INT PK AUTOINC                   | Identifiant interne                    |
| set_code       | TEXT UNIQUE                      | Code (neo, mom, ...)                   |
| name           | TEXT                             | Nom complet                            |
| release_date   | TEXT                             | AAAA-MM-JJ                             |
| set_type       | TEXT                             | core, expansion, ...                   |
| total_cards    | INT                              | Nombre de cartes                       |
| is_digital     | BOOL DEFAULT 0                   | Set digital only ?                     |
| icon_svg_uri   | TEXT                             | URL icône SVG                          |

---

## 📁 4. `prices_daily_card`

| Champ       | Type | Description           |
|-------------|------|-----------------------|
| scryfall_id | TEXT | → `prints.scryfall_id`|
| date        | TEXT | AAAA‑MM‑JJ            |
| eur         | REAL | Prix €                |
| eur_foil    | REAL | Prix € foil           |
| usd         | REAL | Prix $                |
| usd_foil    | REAL | Prix $ foil           |
| usd_etched  | REAL | Prix $ etched         |
| PK          | —    | `(scryfall_id, date)` |

---

## 📁 5. `prices_weekly_card`

| Champ        | Type | Description                    |
|--------------|------|--------------------------------|
| scryfall_id  | TEXT | → `prints.scryfall_id`         |
| week         | TEXT | Semaine ISO (YYYY‑Www)         |
| eur_avg      | REAL | Moyenne €                     |
| eur_min      | REAL | Min €                         |
| eur_max      | REAL | Max €                         |
| eur_foil_avg | REAL | Moyenne € foil                |
| usd_avg      | REAL | Moyenne $                     |
| usd_min      | REAL | Min $                         |
| usd_max      | REAL | Max $                         |
| usd_foil_avg | REAL | Moyenne $ foil                |
| usd_etched_avg | REAL | Moyenne $ etched            |
| PK           | —    | `(scryfall_id, week)`         |

---

## 📁 6. `prices_daily_set`

| Champ       | Type | Description                |
|-------------|------|----------------------------|
| set_id      | INT  | → `sets.set_id`            |
| date        | TEXT | AAAA‑MM‑JJ                 |
| avg_eur     | REAL | Prix moyen €               |
| avg_usd     | REAL | Prix moyen $               |
| total_cards | INT  | Cartes comptabilisées      |
| PK          | —    | `(set_id, date)`           |

---

## 📁 7. `prices_weekly_set`

| Champ       | Type | Description                  |
|-------------|------|------------------------------|
| set_id      | INT  | → `sets.set_id`              |
| week        | TEXT | Semaine ISO (YYYY‑Www)       |
| avg_eur     | REAL | Moyenne €                    |
| avg_usd     | REAL | Moyenne $                    |
| total_cards | INT  | Cartes                      |
| PK          | —    | `(set_id, week)`            |

---

## 📁 8. `card_localizations`

| Champ             | Type | Description                          |
|-------------------|------|--------------------------------------|
| oracle_id         | TEXT | → `cards.oracle_id`                 |
| set_code          | TEXT | → `sets.set_code`                   |
| collector_number  | TEXT | Numéro                              |
| lang              | TEXT | Langue FR/ES/IT…                    |
| name              | TEXT | Nom traduit                         |
| oracle_text       | TEXT | Texte oracle traduit                |
| flavor_text       | TEXT | Flavor traduit                      |
| image_front_uri   | TEXT | Image recto                         |
| image_back_uri    | TEXT | Image verso (NULL si 1 face)        |
| PK                | —    | `(oracle_id, set_code, lang)`       |

---

## 📁 9. `users` (Firestore)

| Champ        | Type | Description                    |
|--------------|------|--------------------------------|
| user_id      | TEXT | UID Firebase                   |
| email        | TEXT | Email                          |
| created_at   | TEXT | Date inscription              |
| role         | TEXT | user / admin / moderator       |
| first_name   | TEXT | Prénom                         |
| last_name    | TEXT | Nom                            |
| street, city, postal_code, country | TEXT | Adresse|

---

*Document généré le 2025-06-25 – OctoDecks 🐙*
