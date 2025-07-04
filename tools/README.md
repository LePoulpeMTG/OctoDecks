<!-- 📁 chemin relatif : tools\README.md -->
# Scripts back-office OctoDecks

| Script | Rôle | Lance… |
|--------|------|--------|
| **import_all_cards.py** | • Télécharge le bulk *All Cards* <br>• Alimente la DB + `prices_daily_card` | workflow **update OctoBase** |
| **export_daily_prices.py** | • Calcule `prices_daily_set` <br>• Écrit `prices_daily.json` (cartes + sets du jour) | workflow **daily update + export** |
| **build_weekly_prices.py** | • Recompile `prices_weekly_card` et `prices_weekly_set` à partir des daily | workflow **weekly rebuild** |

### Variables d’environnement
| Nom | Utilisé par | Commentaire |
|-----|-------------|-------------|
| `FIREBASE_SERVICE_ACCOUNT` | Workflows GitHub | JSON de compte service |
| `FIREBASE_BUCKET` | Workflows GitHub | `octodecks.appspot.com` |

> Les scripts ne dépendent que de `sqlite3`, `ijson`, `tqdm`, `requests`.  
> Lancer `python tools/import_all_cards.py` crée la base et charge **~500 000** impressions en 3-4 min sur une machine locale décente.
# 🧪 Outils de Debug — CORE OctoDecks

Ce dossier contient les outils internes de test pour valider le fonctionnement du **core** (import Scryfall, historique de prix, intégrité des données).

---

## 📂 Contenu

| Script                          | Description |
|---------------------------------|-------------|
| `reset_daily_scry_update.py`    | Supprime les prix journaliers de la date du jour (`prices_daily_*`) |
| `reset_weekly_scry_update.py`   | Supprime les prix hebdomadaires de la semaine courante (`prices_weekly_*`) |
| `debug_core.py`                 | Outil CLI pour enchaîner facilement les tests (reset, run, check) |

---

## ⚙️ Utilisation de `debug_core.py`

```bash
python tools/dev/debug_core.py [options]
