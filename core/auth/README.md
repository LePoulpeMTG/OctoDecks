# 🔐 Authentification – OctoDeck

Ce module contiendra la logique d'authentification pour les différentes plateformes OctoDeck.  
Il permettra notamment de gérer :

- Les rôles utilisateurs (admin, user, guest)
- L'accès sécurisé aux fonctions sensibles
- L'authentification via Firebase ou équivalent
- La synchronisation des droits via la base centralisée

---

## 📦 Contenu prévu

| Fichier/Dossier      | Rôle prévu |
|----------------------|------------|
| `auth_service.dart`  | Gestion centralisée des tokens et sessions |
| `user_roles.dart`    | Enumération et contrôle des rôles          |

---

## 🔗 Dépendances

- À définir selon la méthode choisie (Firebase Auth ? JWT ?)

---

## ✅ État / Avancement

- [x] Dossier créé
- [ ] Choix de la méthode d'authentification
- [ ] Implémentation de base
- [ ] Tests unitaires

---

## 🧪 Tests

Des tests unitaires seront prévus pour valider :
- Les rôles accordés aux utilisateurs
- Le bon fonctionnement de l'accès sécurisé aux API/services
- L'expiration / renouvellement des tokens

---

## 🗂️ Liens utiles

- 🔧 [Services partagés](../services/)
- 📄 [Modèle utilisateur (à venir)](../models/user.dart)
- 📁 [Roadmap Scryfall + Base](../../../shared/data/roadmap_scryfall_db.md)
