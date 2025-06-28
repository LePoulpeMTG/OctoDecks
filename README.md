# 🐙 OctoDeck

**OctoDeck** est un projet open-source de gestion de collection de cartes Magic: The Gathering.  
Pensé par un joueur autiste pour des joueurs exigeants, OctoDeck vise la simplicité d’usage, la puissance des filtres et une totale autonomie des utilisateurs.

---

## 🎯 Objectif global

OctoDeck est conçu pour être **multiplateforme**, **offline-first** et **personnalisable**, avec une base locale enrichie automatiquement par les données publiques de Scryfall.

---


## 🧱 Structure du monorepo

L’arborescence complète du projet est générée automatiquement ici :  
📁 [Voir TREE.txt à jour](./TREE.txt)

Ce fichier reflète fidèlement l’état actuel du dépôt à chaque mise à jour.


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
