# 🐙 OctoDeck

**OctoDeck** est un projet open-source de gestion de collection de cartes Magic: The Gathering.  
Pensé par un joueur autiste pour des joueurs exigeants, OctoDeck vise la simplicité d’usage, la puissance des filtres et une totale autonomie des utilisateurs.

---

## 🎯 Objectif global

OctoDeck est conçu pour être **multiplateforme**, **offline-first** et **personnalisable**, avec une base locale enrichie automatiquement par les données publiques de Scryfall.

---

## 🧱 Structure du monorepo

octodeck/
├── apps/
│   ├── viewer_mobile/        # Appli Flutter Android/iOS (scan à venir)
│   ├── viewer_desktop/       # Flutter Windows/macOS (mode offline)
│   ├── web_user/             # Interface web publique (exploration, collection)
│   └── web_admin/            # Backoffice (Scryfall, suivi utilisateurs)
│
├── core/
│   ├── models/               # Objets partagés (Card, Set, User...)
│   ├── services/             # Base, API, synchro, parsing
│   └── auth/                 # Système d’identification & rôles
│
├── scripts/
│   ├── update_scryfall.py    # MAJ automatique des cartes
│   ├── verify_layouts.py     # Vérifie les layouts Scryfall inconnus
│   ├── import_manabox.py     # Import depuis export CSV Manabox
│   └── track_prices.py       # Historique prix par set/carte
│
├── data/
│   ├── base.sqlite           # Base locale pour tests/démo
│   ├── snapshots/            # Données d’évolution des prix
│   └── cache/                # Temp ou fichiers de parsing
│
├── assets/                   # Logos, icônes, visuels
├── docs/                     # Architecture, schémas, TODO techniques
├── LICENSE
└── README.md


---

## 🧠 Stack technique envisagée

| Côté                    | Stack ciblée                     |
|-------------------------|----------------------------------|
| Mobile / Desktop        | Flutter                          |
| Web (user/admin)        | Flutter Web ou React             |
| Scripts de fond         | Python (avec cron/tâche planifiée) |
| Données principales     | JSON Scryfall, SQLite local      |
| Gestion comptes         | Token + rôles + base centralisée (à définir) |

---

## 🚧 Roadmap fonctionnelle

- [ ] 🧱 Création de la base SQLite à partir de Scryfall
- [ ] 🔁 Mise à jour quotidienne (cartes + sets + langues)
- [ ] 🧠 Détection de layout inconnu
- [ ] 📥 Import CSV Manabox
- [ ] 📊 Historique de prix (set + carte suivie)
- [ ] 🖼️ UI avancée de filtres type Magic Arena
- [ ] 📲 Scan de cartes (phase 2)
- [ ] 💬 Auto-trade communautaire (phase 3)

---

## 🙌 Esprit du projet

> "Ce projet est open source, pensé pour durer, pour rendre service à la commu',  
> et pour respecter la vie privée des collectionneurs."

Tu veux soutenir ? Dis-le avec des cartes ou une bière virtuelle 🍻
