# 🗄️ Schéma SQL – OctoBase

Ce dossier contient le schéma de base de données SQLite utilisé comme **référence commune** entre toutes les plateformes OctoDeck (desktop, mobile, web).

---

## 📄 Contenu

| Fichier                | Rôle |
|------------------------|------|
| `schema_octobase.sql`  | Schéma SQL de référence décrivant la structure complète de la base MTG (cartes, sets, types, légalité, prix...) |

---

## 🎯 Objectif

Le fichier `schema_octobase.sql` sert à :

- Définir la structure normalisée de la base SQLite
- Être utilisé comme source de vérité pour :
  - les scripts Python d'import/export
  - les apps Flutter (`floor`, `drift`, etc.)
  - les outils de visualisation (web_admin, viewer)
- Permettre une réinitialisation facile de la base locale

---

## 🔗 Dépendances et usage

- Utilisé par les scripts Python :
  - `import_all_cards.py`
  - `build_weekly_prices.py`
- Compatible avec Flutter SQLite (via plugins comme `sqflite`, `drift`, etc.)
- Le schéma peut être chargé via un script ou à l’init d’une app.

---

## ✅ Avancement

- [x] Structure initiale terminée
- [x] Champs clefs documentés
- [ ] Documentation technique associée (ex : ERD, relations visuelles)

---

## 🗂️ Liens utiles

- 📁 [Snapshots & données](../../data/)
- 📄 [Roadmap base Scryfall](../../shared/data/roadmap_scryfall_db.md)
- 📜 [Script import principal](../../tools/import_all_cards.py)
