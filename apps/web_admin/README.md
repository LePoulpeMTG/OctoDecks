Backoffice web pour l'administration des données Scryfall et des comptes.
# 🛠️ OctoDeck - Interface Admin Web

Cette interface web permet la **gestion technique et fonctionnelle** de la plateforme OctoDeck.  
Elle est indépendante de l’interface utilisateur, hébergée séparément, et accessible uniquement par les administrateurs.

---

## 🎯 Objectif

Permettre à l’administrateur d’OctoDeck de :
- Gérer les mises à jour de la base de données locale depuis Scryfall
- Suivre les utilisateurs et leur activité
- Superviser les scripts automatiques
- Visualiser l’historique des prix des cartes et des sets
- Maintenir un fonctionnement propre du système (logs, snapshots, alertes)

---

## ⚙️ Fonctionnalités attendues

### 🔄 Mise à jour Scryfall

- [ ] Lancer une mise à jour manuelle du bulk JSON
- [ ] Afficher la date de dernière mise à jour
- [ ] Voir un mini changelog : nouvelles cartes, sets, layouts
- [ ] Alerte si un nouveau layout est détecté
- [ ] Forcer la mise à jour des noms localisés (par langue)
- [ ] Prévisualiser les nouveautés avant import

---

### 📦 Gestion des données

- [ ] Voir le statut de la base SQLite (taille, nombre de cartes, sets, langues…)
- [ ] Recharger une base / importer un dump
- [ ] Supprimer des snapshots obsolètes
- [ ] Télécharger la base complète
- [ ] Mettre à jour la structure des tables (via scripts contrôlés)

---

### 📊 Suivi utilisateurs

- [ ] Liste des utilisateurs actifs
- [ ] Détail par utilisateur : doublons, cartes suivies, date de dernière activité
- [ ] Statistiques globales : sets populaires, cartes les plus suivies

---

### 🧰 Scripts & exécution manuelle

- [ ] Bouton pour lancer le script de mise à jour Scryfall
- [ ] Bouton pour lancer le script d'historique de prix (MKM)
- [ ] Afficher l’historique des exécutions de scripts
- [ ] Afficher la prochaine exécution automatique prévue

---

### 📈 Historique des prix

- [ ] Stockage de l’historique **daily (60 jours)** pour chaque `card_id`
- [ ] Stockage de la moyenne **weekly** pour chaque `card_id`
- [ ] Stockage de l’historique **daily + weekly** par `set`
- [ ] Affichage graphique des évolutions (cartes / sets)
- [ ] Export des données sous forme CSV

> ❗ Les alertes personnalisées sur variations brutales sont **gérées localement dans l’interface utilisateur**, selon les préférences de chaque joueur.

---

### 🔐 Accès sécurisé

- [ ] Formulaire d’authentification simple (mot de passe)
- [ ] Gestion de session minimale
- [ ] Protection des routes sensibles
- [ ] Déconnexion

---

## 🛠️ Technologies utilisées

- **Flutter Web**
- Hébergement prévu : Vercel ou Firebase Hosting
- Déploiement en dossier statique (`build/web`)
- Intégration future avec une API ou des endpoints privés

---

## 🚀 Build & Déploiement

Pour construire l’application web :

```bash
flutter build web

