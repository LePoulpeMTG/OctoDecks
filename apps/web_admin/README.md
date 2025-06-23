Backoffice web pour l'administration des données Scryfall et des comptes.
# 🛠️ OctoDeck - Interface Web Admin

**OctoDeck Admin** est une interface web séparée, dédiée à la gestion technique et fonctionnelle de la plateforme OctoDeck.  
Elle permet de centraliser les mises à jour de la base de cartes depuis Scryfall, de superviser l'activité des utilisateurs et de maintenir les données critiques.

---

## 🎯 Objectif

- Centraliser les interactions avec Scryfall pour éviter que chaque utilisateur interroge l’API.
- Générer et valider une base unique (`SQLite` ou `JSON`) propre à distribuer.
- Gérer les historiques de prix, les utilisateurs, et les événements critiques.
- Superviser les scripts périodiques (MAJ, synchro, nettoyage).
- Maintenir la cohérence du système et détecter toute anomalie (layouts, formats…).

---

## ⚙️ Fonctionnalités attendues

### 🔄 Mise à jour Scryfall (centralisée)

- [ ] Lancer une mise à jour manuelle du bulk JSON Scryfall
- [ ] Afficher la date de dernière mise à jour
- [ ] Voir un changelog synthétique : nouvelles cartes, nouveaux sets, nouveaux layouts
- [ ] Maintenir une **liste locale de layouts connus**, séparés :
  - `layouts_one_face.txt` pour les layouts 1 face
  - `layouts_two_faces.txt` pour les layouts 2 faces
- [ ] Lors de l’analyse des cartes :
  - Si le `layout` est **inconnu**, déterminer automatiquement s’il s’agit d’un layout 1 ou 2 faces (via présence de `card_faces`)
  - Ajouter dynamiquement ce `layout` dans le fichier approprié
  - Logguer l’événement dans un tableau ou une alerte visuelle
- [ ] Forcer la mise à jour des noms localisés (toutes langues ou ciblées)
- [ ] Prévisualiser les nouvelles cartes/sets/layouts avant import définitif
- [ ] Stocker la base nettoyée en `.sqlite` ou `.json` prête à être distribuée aux clients

---

### 📦 Gestion des données

- [ ] Statut de la base actuelle (taille, cartes, sets, langues…)
- [ ] Import manuel ou restauration depuis un dump
- [ ] Suppression ciblée de snapshots obsolètes
- [ ] Téléchargement direct de la base
- [ ] Gestion des migrations (`ALTER TABLE`, évolutions structurelles)

---

### 📈 Historique des prix (cartes & sets)

- [ ] Stockage quotidien (**daily**) du prix de chaque carte (`card_id`) pendant 60 jours
- [ ] Calcul et stockage de la moyenne **weekly**
- [ ] Même système pour le prix moyen par **set**
- [ ] Visualisation graphique de l’évolution (carte ou set)
- [ ] Export CSV des historiques

> ℹ️ Les **alertes personnalisées (écarts brutaux de prix)** sont gérées **localement** côté client, selon les préférences utilisateur.

---

### 👥 Suivi des utilisateurs

- [ ] Liste des utilisateurs actifs récemment
- [ ] Détails individuels : doublons, cartes suivies, fréquence d’usage
- [ ] Statistiques globales : sets populaires, volume de scans, usage moyen
- [ ] Gestion des comptes utilisateurs (via Firebase)

---

### 🧰 Scripts & exécution manuelle

- [ ] Bouton “Lancer script MAJ Scryfall”
- [ ] Bouton “Lancer script prix MKM”
- [ ] Historique des exécutions + logs
- [ ] Affichage de la prochaine exécution automatique planifiée

---

### 🔐 Authentification

- Connexion admin par **mot de passe** statique (phase 1)
- Intégration prévue avec **Firebase Auth** (phase 2) :
  - Connexion avec Google
  - Connexion avec Facebook
  - Inscription classique (email + mot de passe)
- Gestion simple de rôles (`admin`, `user`) côté base ou Firestore

---

## 🛠️ Stack technique

| Élément            | Techno                        |
|--------------------|-------------------------------|
| Frontend           | Flutter Web                   |
| Authentification   | Firebase Auth                 |
| Stockage           | SQLite (pour la base Scryfall)|
| Hébergement        | Vercel ou Firebase Hosting    |

---

## 🚀 Build & Déploiement

Pour construire l’application web :
cd apps/web_admin
flutter build web
