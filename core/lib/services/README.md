
---

### 📄 `core/lib/services/README.md`

```markdown
# 🔌 Services

Ce dossier contient tous les services **généraux** d’accès aux données.

---

## Services existants

| Fichier | Rôle |
|--------|------|
| `octo_api_service.dart` | Accès aux fichiers JSON hébergés sur Firebase (ex: sets.json, users.json) |

---

## Exemple d'utilisation

```dart
final sets = await OctoApiService.fetchSets();
final rawJson = await OctoApiService.fetchJsonFile('stats.json');
