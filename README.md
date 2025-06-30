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

- [ ] Schéma SQLite de référence (`schema_octobase.sql`)
- [ ] Synchronisation des données Scryfall
- [ ] BDD hébergée sur firebase
- [ ] Creation API REST
- [ ] UI filtres type *Magic Arena*
- [ ] Scan de cartes (Manabox → OctoDeck)
- [ ] Historique complet de prix par carte
- [ ] Fonctionnalité d’auto-trade communautaire
- [ ] Authentification avec rôles
- [ ] Publication publique (démo utilisable en ligne)

------------------------------------------------------------------------------------
## 📈 Gestion projet 
------------------------------------------------------------------------------------
### ✨ CORE
Le CORE gère la maj depuis le bulk scryfall, met a dispo les données et agrege les datas pour l'API REST.
#### ✨ CORE BASE-Fonctionnement attendu
- [ ] Le core met a jour une bdd en ligne(firebase)
    PHASE 1 — Initialisation de la BDD Scryfall (Base de Référence)
    - [ ] Définir le schéma cible
    - [ ] Créations des Tables : cards, sets, prices, oracle_cards, layouts_by_face, etc.
    - [ ] Créer un script d’import JSON Scryfall
    - [ ] Téléchargement de l’énorme all-cards.json.
    - [ ] Traitement des layouts 1 face / 2 faces proprement. (y compris en cas de nouveau format)
    - [ ] Filtrage des champs utiles et normalisation.
    - [ ] Remplissage initial de la BDD
    PHASE 2 — Suivi des cotes
    - [ ] Création d’une table prices_daily_card,prices_daily_set,prices_weekly_card,prices_weekly_set
        - [ ]Historique quotidient des cartes sur 90jours
        - [ ]Historique quotidient des sets sur 90jours
        - [ ]Historique weekly des cartes (pas de limites)
        - [ ]Historique weekly des sets (pas de limites)
    - [ ] Agrégation des prix (moyenne, min, max )
    - [ ] Script CRON journalier sur bulk scryfall.Json ( voir comment faire des appels toutes les heures pour ne pas se prendre un decalage trop important)
        - [ ] déclenchement de l'Insertion dans prices_daily_card,prices_daily_set
        - [ ] si dimanche: déclenchement de l'Insertion dans prices_weekly_card,prices_weekly_set
#### ✨ CORE USER-Fonctionnement attendu
    - [ ] Connection en local
    - [ ] Connection en ligne (si posible ajouter connection avec Google / Facebook)
    - [ ] Gerer la synchro BDD Local (cartes dispo, en trade, en collection) avec le serveur 
#### ✨ CORE Trade-Fonctionnement attendu
    - [ ] fonction de comparaison de liste de trade vs liste wanted entre 2 utilisateurs
#### ✨ CORE MarketPlace
    - [ ] fonction de mise a disposition de carte sur le market
    
#### ✨ CORE API REST
- [ ] Le service API REST met a dispositions les data aux app
- [ ] Les app utilisent l'API REST 

------------------------------------------------------------------------------------
### 🔖 WebAdmin:adminoctodecks.web.app
c'est le tableau de bord du capitaine
- [ ] Accessible par authentificatoion sur adminoctodecks.web.app
#### 🔖 WebAdmin-Page KPI
   - [ ] Suivi des utilisateurs connectés
   - [ ] Suivi des dons
   - [ ] Suivi du nombre de cartes dans la BDD
   - [ ] Suivi du nombre de sets dans la BDD
   - [ ] Suivi des cycles d'uptade du CORE

#### 🔖 WebAdmin-Page Set_explore
   - [ ] Exploration des sets comme sur https://scryfall.com/sets
#### 🔖 WebAdmin-Page Set_detail
   - [ ] Affichage du detail SET comme sur https://scryfall.com/sets/tdm
#### 🔖 WebAdmin-Page Card_detail
   - [ ] Affichage du détail card comme sur https://scryfall.com/card/tdm/2/anafenza-unyielding-lineage
    
------------------------------------------------------------------------------------
### 🙌 WebUser:octodecks.web.app
c'est le tableau de bord de l'utilisateur
- [ ] Accessible par authentificatoion sur octodecks.web.app
#### 🙌 WebUser-Page KPI
   - [ ] Suivi valeur des cartes possédées
   - [ ] Suivi valeur des cartes en possession
   - [ ] Suivi valeur des cartes en vente  
   - [ ] Suivi du nombre de cartes dans la BDD
   - [ ] Suivi des cycles d'uptade du CORE
   - [ ] Suivi des cycles d'uptade du LOCAL
#### 🙌 WebUser-Page MesCartes_explore
   - [ ] Parcourir mes cartes
   - [ ] Stats sur mes cartes
#### 🙌 WebUser-Page MesSets_explore
   - [ ] Parcourir mes sets
   - [ ] Stats sur mes sets
#### 🙌 WebUser-Page Set_explore
   - [ ] Exploration des sets comme sur https://scryfall.com/sets
#### 🙌 WebUser-Page Set_detail
   - [ ] Affichage du detail SET comme sur https://scryfall.com/sets/tdm
#### 🙌 WebUser-Page Card_detail
   - [ ] Affichage du détail card comme sur https://scryfall.com/card/tdm/2/anafenza-unyielding-lineage
#### 🙌 WebUser-deckbuilding (facon arena)
#### 🙌 WebUser-Acquisition carte (facon arena)
#### 🙌 WebUser-Parametres
#### 🙌 WebUser-Profil



------------------------------------------------------------------------------------
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
