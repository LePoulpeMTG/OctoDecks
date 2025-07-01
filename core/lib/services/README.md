<!-- 📁 chemin relatif : core\lib\services\README.md -->
# 🔌 Services

Ce dossier contient tous les services **généraux** d’accès aux données partagées.

---

## 📦 Contenu

| Fichier              | Rôle |
|----------------------|------|
| `octo_api_service.dart` | Service d’accès aux fichiers JSON hébergés sur Firebase (sets, stats, users...) |

---

## Exemple d'utilisation

```dart
final sets = await OctoApiService.fetchSets();
final rawJson = await OctoApiService.fetchJsonFile('stats.json');


## Exemple d'utilisation
```dart
final sets = await OctoApiService.fetchSets();
final rawJson = await OctoApiService.fetchJsonFile('stats.json');
