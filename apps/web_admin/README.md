README_deploy
# 🛠️ OctoDeck - Interface Web Admin

**OctoDeck Admin** est une interface web Flutter dédiée à la gestion technique et fonctionnelle de la plateforme OctoDeck.

---

## 🎯 Objectif

- Centraliser les mises à jour Scryfall pour éviter que chaque client n’interroge l’API.
- Gérer la base de référence (cartes, sets, prix, layouts) depuis un point unique.
- Superviser les scripts périodiques et manuels.
- Suivre l’activité des utilisateurs.
- Offrir une interface d’administration simple et fiable.

---

## ⚙️ Fonctionnalités attendues

Voir la roadmap fonctionnelle complète dans le fichier source.

---

## 📦 Dépendances

L’application dépend du module partagé `core/` du projet :

```yaml
dependencies:
  core:
    path: ../../core
```

Ce module contient :

- Les modèles partagés (`MtgSet`, `User`, etc.)
- Les services d’accès à Firebase Storage (via `OctoApiService`)

### Exemple d’utilisation

```dart
import 'package:core/services/octo_api_service.dart';

final sets = await OctoApiService.fetchSets();
```

---

## 📁 Organisation Flutter

| Dossier | Contenu |
|--------|---------|
| `lib/screens/` | Pages avec affichage dynamique |
| `lib/pages/` | Déclarations de routes ou wrappers |
| `lib/models/` | (à migrer) → désormais dans `core/models/` |
| `lib/services/` | (à migrer) → désormais dans `core/services/` |

---

## 🔌 Source JSON attendue

Les données utilisées (cartes, sets, stats...) sont hébergées dans Firebase Storage via les URLs publiques (`alt=media`). Elles sont accessibles via des fichiers comme :

- `sets.json`
- `stats.json`
- `users.json`

---
