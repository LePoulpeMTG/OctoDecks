 🧠 API REST — OctoDecks

Cette API REST sert de **pont entre la base SQLite Octobase (`octobase_reference.db`) et les applications Flutter** (web, desktop, mobile).

Développée avec **FastAPI**, elle expose des routes simples pour consulter les sets, les cartes, les prix et les localisations.

---

## 🚀 Objectifs

- Accès standardisé (JSON) aux données Magic: The Gathering
- Architecture RESTful claire, modulaire et testable
- Prête pour extension future (auth, synchro, mises à jour)

---

## 🧱 Structure du dossier
api_rest/
├── main.py # Entrée FastAPI
├── config.py # Constantes et chemins
├── database.py # Connexion SQLite
├── models.py # Schémas Pydantic
├── crud/
│ ├── cards.py
│ └── sets.py
├── routers/
│ ├── cards.py
│ └── sets.py
└── utils/


---

## 📦 Setup de développement local

### 1. Lancer l’API en local

```bash
uvicorn main:app --reload
Par défaut sur : http://127.0.0.1:8000

### 2. Interface interactive Swagger
👉 Accès automatique à http://127.0.0.1:8000/docs


📚 Endpoints REST
🔹 Sets
Méthode	URL	Description
GET	/sets	Liste des sets (pagination future)
GET	/sets/{set_code}	Détail d’un set

🔹 Cartes
Méthode	URL	Description
GET	/cards/{scryfall_id}	Infos d’une carte
GET	/cards?set=neo&rarity=rare	Liste filtrée

🔹 Prix
Méthode	URL	Description
GET	/prices/daily/card/{scryfall_id}	Historique prix carte
GET	/prices/daily/set/{set_code}	Historique prix set

🔐 Sécurité / Auth (plus tard)
Pour l’instant : tout est public

Plus tard : token Firebase pour les routes d’écriture

✅ TODO technique
 Créer main.py, database.py, models.py

 Exposer route /sets et /sets/{code}

 Ajouter route /cards/{id} puis filtrage /cards

 Intégrer lecture historique prices_*

 Tests unitaires simples (ex: 404, valid JSON)

🔄 Déploiement (plus tard)
 Docker (optionnel)

 Firebase Cloud Run (avec build automatique via GitHub Action)

 Hébergement sur sous-domaine api.octodecks.app

 