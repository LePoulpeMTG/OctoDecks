# 📚 Structure de la base de données `octobase_reference`

Ce document référence toutes les tables nécessaires pour structurer une base de données locale ou distante contenant les données issues de la source JSON des cartes Magic (ex-Scryfall), renommée ici pour une intégration neutre.

---

## 📦 1. `sets`
Une ligne par édition.

| Champ         | Type      | Description                            |
|---------------|-----------|----------------------------------------|
| id            | TEXT PK   | Code du set (ex: "neo")                |
| name          | TEXT      | Nom complet de l'édition               |
| release_date  | TEXT      | Date de sortie                         |
| set_type      | TEXT      | Type de set (core, expansion, etc.)    |
| total_cards   | INTEGER   | Nombre total de cartes                 |
| digital       | BOOLEAN   | 1 = uniquement digital                 |

---

## 🧬 2. `cards`
Une ligne par carte "conceptuelle", identifiée par `oracle_id`.

| Champ           | Type      | Description                                |
|-----------------|-----------|--------------------------------------------|
| oracle_id       | TEXT PK   | Identifiant oracle                         |
| name            | TEXT      | Nom de la carte                            |
| type_line       | TEXT      | Type                                        |
| cmc             | REAL      | Converted mana cost                        |
| color_identity  | TEXT      | "WUBRG" concaténé                          |
| keywords        | TEXT      | Mots-clés concaténés (ex: "Flying;Trample")|
| layout          | TEXT      | Layout principal (normal, transform...)    |

---

## 🖨️ 3. `prints`
Une ligne par impression (set + collector + langue)

| Champ             | Type      | Description                              |
|------------------|-----------|------------------------------------------|
| scry_id          | TEXT PK   | ID unique de l’impression (UUID)         |
| oracle_id        | TEXT FK   | Référence vers `cards.oracle_id`         |
| set_id           | TEXT FK   | Référence vers `sets.id`                 |
| collector_number | TEXT      | Numéro de collection                     |
| lang             | TEXT      | Langue (ex: "en", "fr")                  |
| rarity           | TEXT      | Rareté                                   |
| foil             | BOOLEAN   | Disponible en foil                       |
| nonfoil          | BOOLEAN   | Disponible en version normale            |
| image_uri        | TEXT      | URL de l’image                           |
| cardmarket_id    | INTEGER   | ID MKM si dispo                          |

---

## 💶 4. `prices_daily_card`
Suivi journalier des prix par carte (par impression).

| Champ       | Type    | Description                        |
|-------------|---------|------------------------------------|
| scry_id     | TEXT    | Réf vers `prints.scry_id`          |
| date        | TEXT    | AAAA-MM-JJ                         |
| eur         | REAL    | Prix € standard                    |
| eur_foil    | REAL    | Prix € foil                        |
| usd         | REAL    | Prix $ standard                    |
| usd_foil    | REAL    | Prix $ foil                        |
| usd_etched  | REAL    | Prix $ etched                      |

---

## 💶 5. `prices_weekly_card`
Même structure que `prices_daily_card`, stockée 1 fois par semaine.

---

## 📊 6. `prices_daily_set`
Moyennes quotidiennes des sets.

| Champ         | Type    | Description                           |
|---------------|---------|---------------------------------------|
| set_id        | TEXT    | Réf vers `sets.id`                    |
| date          | TEXT    | AAAA-MM-JJ                            |
| avg_eur       | REAL    | Moyenne €                             |
| total_cards   | INTEGER | Nombre de cartes prises en compte     |

---

## 📊 7. `prices_weekly_set`
Mêmes données que ci-dessus, agrégées à la semaine.

---

