🔧 PHASE 1 — Initialisation de la BDD Scryfall (Base de Référence)
Définir le schéma cible

Tables : cards, sets, prices, oracle_cards, layouts_by_face, etc.

Index sur oracle_id, scryfall_id, set + collector_number.

Créer un script d’import JSON Scryfall

Téléchargement de l’énorme all-cards.json (ou en lots).

Traitement des layouts 1 face / 2 faces proprement.

Filtrage des champs utiles et normalisation.

Remplissage initial de la BDD

Chargement propre des cartes, sets, layouts, etc.

Génération des liens entre tables.

📈 PHASE 2 — Suivi des cotes
Création d’une table prices_daily

Un enregistrement par scryfall_id et date.

Champs : eur, eur_foil, usd, usd_foil, usd_etched, edhrec_rank.

Création d’une table prices_weekly

Historique hebdomadaire sans limite dans le temps (archivage).

Agrégation des prix (moyenne, min, max ?) si nécessaire.

Script CRON journalier

Requête à l’API Scryfall pour toutes les cartes trackées (au moins celles en EUR).

Insertion dans prices_daily.

Script CRON hebdomadaire

Copie ou synthèse de prices_daily dans prices_weekly.

🧠 PHASE 3 — Améliorations et usage app
Ajout des tags, keywords et types dans la BDD

Pour aider à la recherche/filtering dans les apps.

Ajout des traductions dans une table dédiée

Par oracle_id ou scryfall_id + langue.

Export des données vers Firebase / CDN

En fichiers JSON compressés par set ou par bloc.

Ou exposer une API perso si besoin.

Documentation et format standard d’import

Pour les apps Flutter, WinDev, Web Admin, etc.