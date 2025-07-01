<!-- 📁 chemin relatif : core\lib\models\README.md -->
# 🧩 Modèles de données

Définitions des modèles de données communs utilisés dans tout OctoDeck.

---

## 📦 Contenu

| Fichier        | Rôle |
|----------------|------|
| `mtg_set.dart` | Modèle pour les sets Magic (nom, code, dates, parent set, icône, etc.) |

---

## 🔗 Dépendances

- Nécessite : `dart:convert`
- Utilisé par : `services/octo_api_service.dart`, `web_admin/pages/set_explore_page.dart`

---

## ✅ État / Avancement

- [x] Structure du modèle `MtgSet`
- [x] Parsing depuis JSON Firebase
- [ ] Validation / Normalisation
- [ ] Tests unitaires

---

## 🧪 Tests

Pas encore définis. À ajouter via `test/models/mtg_set_test.dart` pour valider le parsing et la cohérence des champs.

---

## 🗂️ Liens utiles

- 📄 [Schéma `schema_octobase.sql`](../../../database/schema/schema_octobase.sql)
- 🔧 [Service associé](../services/octo_api_service.dart)
