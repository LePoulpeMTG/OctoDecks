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


## 📚 À FAIRE (plan de développement de l'API REST)
## 🧱 **1. Base de code**
- [ ] Créer `main.py` avec FastAPI + routes de test
- [ ] Créer `database.py` pour connecter la base SQLite (lecture seule)
- [ ] Créer `models.py` avec les schémas Pydantic pour :
  - `Set`, `Card`, `Print`, `PriceDailyCard`, `PriceWeeklySet`, etc.

📦 **2. Modules CRUD (`crud/`)**
- [ ] `crud/sets.py` :
  - [ ] Fonction `get_all_sets()`
  - [ ] Fonction `get_set_by_code(set_code)`
- [ ] `crud/cards.py` :
  - [ ]Fonction `get_card_by_id(scryfall_id)`
  - [ ] Fonction `search_cards(set_code, rarity, lang, name, etc.)`
- [ ] `crud/prices.py` :
  - [ ] Fonction `get_daily_prices_card(scryfall_id)`
  - [ ] Fonction `get_daily_prices_set(set_code)`
  - [ ] Fonction `get_weekly_prices_card(scryfall_id)`
  - [ ] Fonction `get_weekly_prices_set(set_code)`

🌐 **3. Routes API (`routers/`)**
- [ ] Route `/` de test
- [ ] Router `/sets` et `/sets/{code}`
- [ ] Router `/cards` et `/cards/{scryfall_id}`
- [ ] Router `/prices/daily/card/{scryfall_id}`
- [ ] Router `/prices/daily/set/{set_code}`
- [ ] Router `/prices/weekly/card/{scryfall_id}`
- [ ] Router `/prices/weekly/set/{set_code}`
- [ ] Router `/localizations/{oracle_id}?lang=fr`

🧪 **4. Tests et vérifications**
- [ ]Test Swagger (`/docs`)
- [ ] Tester tous les cas 404
- [ ] Vérifier cohérence JSON retourné avec les schémas Pydantic
- [ ] Gérer erreurs SQLite (ex: base absente, données incomplètes)

🚀 **5. Déploiement futur**
- [ ] Dockerisation de l’API
- [ ] Déploiement Firebase Cloud Run
- [ ] Accès public via `api.octodecks.app`
 