<!-- 📁 chemin relatif : core\README.md -->
# 📦 core/

Ce dossier contient tout le code **partagé** entre les différentes applications Flutter du projet **OctoDecks**.

---

## 🎯 Objectif

Centraliser les éléments réutilisables entre :

- `web_admin` (interface d’administration)
- `viewer_mobile` (application utilisateur)
- `viewer_desktop` (version offline PC)
- et toute future app Flutter du projet

---

## 📁 Sous-dossiers

| Dossier | Description |
|--------|-------------|
| `lib/models/` | Modèles de données communs (`MtgSet`, `User`, `Stats`, etc.) |
| `lib/services/` | Accès aux données distantes (Firebase JSON, Firestore, plus tard SQLite offline) |

---

## ✅ Dépendances autorisées

- `http`
- `flutter` (UI agnostique)
- Aucun framework spécifique UI

---
