# 🚀 Déploiement Firebase – Web Admin OctoDecks

Ce fichier documente les étapes pour compiler et déployer le module web admin (`adminoctodecks.web.app`) de ton projet OctoDecks.

---

## 📦 Prérequis

- Flutter installé
- Firebase CLI installée (`npm install -g firebase-tools`)
- Être connecté avec `firebase login`
- Projet Firebase configuré (`firebase init` déjà fait)

---

## 🔨 Compilation de l'app Flutter Web

Dans le dossier `apps/web_admin/`, exécuter :

```bash
flutter build web //Cela génère les fichiers HTML/JS/CSS dans le dossier build/web/.

🚀 Déploiement sur le site admin
firebase deploy --only hosting:admin //Le site adminoctodecks.web.app est lié à la cible admin.

🌐 URL du site en production
https://adminoctodecks.web.app

🧠 Gestion des alias de sites
	🧹 En cas de conflit : firebase target:clear hosting admin
	🔁 Pour relier l’alias admin au bon site : firebase deploy --only hosting:public
	
🛠️ firebase.json attendu
{
  "hosting": [
    {
      "target": "public",
      "public": "build/web",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
    },
    {
      "target": "admin",
      "public": "build/web",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
    }
  ]
}
