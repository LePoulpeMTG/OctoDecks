# 🐙 OctoDeck

**OctoDeck** est un projet open-source de gestion de collection de cartes *Magic: The Gathering*.  
Pensé par un joueur autiste pour des joueurs exigeants, OctoDeck vise la **simplicité d’usage**, la **puissance des filtres** et une **autonomie totale** de l’utilisateur.

---

## 🎯 Objectif global

OctoDeck est conçu pour être **multiplateforme**, **offline-first**, **open-source** et **personnalisable**, avec une base locale enrichie automatiquement par les données publiques de [Scryfall](https://scryfall.com).

---

## 🧱 Structure du monorepo

L’arborescence complète du projet est générée automatiquement ici :  
📁 [Voir TREE.txt à jour](./TREE.txt)

Ce fichier reflète fidèlement l’état actuel du dépôt à chaque mise à jour.

---

## 🧠 Stack technique

| Côté                    | Stack ciblée                          |
|-------------------------|---------------------------------------|
| Mobile / Desktop        | Flutter (Android/iOS/Windows/macOS)   |
| Web (user/admin)        | Flutter Web                           |
| Scripts de fond         | Python (avec cron / GitHub Actions)   |
| Données principales     | JSON Scryfall, SQLite                 |
| Gestion comptes         | Firebase Auth (à confirmer)           |

---

## 📦 Modules principaux

### `apps/` – Interfaces utilisateur
| Dossier         | Description |
|-----------------|-------------|
| `viewer_mobile` | App Flutter mobile. Scan de cartes à venir |
| `viewer_desktop`| App Flutter desktop, full offline          |
| `web_user`      | Interface web publique d’exploration       |
| `web_admin`     | Backoffice admin (mise à jour Scryfall, utilisateurs, sets) |

### `core/` – Coeur métier
| Dossier         | Description |
|-----------------|-------------|
| `models/`       | Modèles de données partagés (`Card`, `Set`, etc.) |
| `services/`     | Services de parsing, API, synchronisation         |
| `auth/`         | Authentification et rôles (à venir)              |

### `scripts/` – Automatisations Python
| Script               | Fonction |
|----------------------|----------|
| `update_scryfall.py` | Mise à jour de la base depuis Scryfall |
| `track_prices.py`    | Historique de prix (set/carte)         |
| `import_manabox.py`  | Import de fichiers exportés depuis Manabox |
| `verify_layouts.py`  | Analyse des layouts inconnus            |

### `tools/` – Utilitaires complémentaires
| Script / Donnée               | Fonction |
|-------------------------------|----------|
| `build_weekly_prices.py`      | Génère les moyennes hebdomadaires |
| `layouts_by_face.json`        | Typologie des layouts (1 face, 2 faces…) |
      |

### `data/` – Données du projet
| Dossier        | Contenu |
|----------------|---------|
| `basesqlite/`  | Base SQLite utilisée pour tests/démos |
| `snapshots/`   | Snapshots de prix journaliers/hebdo  |
| `cache/`       | Données temporaires                  |

---

## 🚧 Roadmap fonctionnelle

- [x] Schéma SQLite de référence (`schema_octobase.sql`)
- [x] Synchronisation des données Scryfall
- [x] BDD hébergée sur firebase
- [ ] Creation API REST
- [ ] UI filtres type *Magic Arena*
- [ ] Scan de cartes (Manabox → OctoDeck)
- [ ] Historique complet de prix par carte
- [ ] Fonctionnalité d’auto-trade communautaire
- [ ] Authentification avec rôles
- [ ] Publication publique (démo utilisable en ligne)

---

## 🙌 Esprit du projet

> "Ce projet est open source, pensé pour durer, pour rendre service à la commu',  
> et pour respecter la vie privée des collectionneurs."

Tu veux soutenir ? Dis-le avec des cartes ou une bière virtuelle 🍻  
[🔗 Tipeee ou sponsoring à venir]

---

## 🔗 Ressources

- 📄 [Roadmap Scryfall DB](shared/data/roadmap_scryfall_db.md)
- 🗂️ [Fichier `TREE.txt`](TREE.txt)
- 📁 [Template README modules](docs/README_TEMPLATE.md)
