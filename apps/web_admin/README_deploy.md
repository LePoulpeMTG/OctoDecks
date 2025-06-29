
# 🚀 Déploiement Firebase – Web Admin OctoDecks

Ce fichier documente les étapes pour compiler et déployer le module `web_admin` du projet OctoDecks.

---

## 📦 Prérequis

- Flutter installé
- Firebase CLI installée (`npm install -g firebase-tools`)
- Connexion via `firebase login`
- Projet Firebase initialisé avec `firebase init`

---

## 🔨 Compilation Flutter Web

Dans le dossier `apps/web_admin/`, exécuter :

```bash
flutter pub get
flutter build web
```

---

## 🌍 Déploiement Firebase Hosting

```bash
firebase deploy --only hosting:admin
```

Le site est accessible à l’adresse :
```
https://adminoctodecks.web.app
```

---

## 📁 Dépendance au module `core`

Ce module utilise du code partagé situé dans `../../core`.  
Assurez-vous que le fichier suivant existe :

```text
core/pubspec.yaml
core/lib/models/mtg_set.dart
```

Et que le `pubspec.yaml` de `web_admin` contient bien :

```yaml
dependencies:
  core:
    path: ../../core
```

---

## 🛠️ Exemple de fichier `firebase.json`

```json
{
  "hosting": [
    {
      "target": "admin",
      "public": "build/web",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
    }
  ]
}
```

---
