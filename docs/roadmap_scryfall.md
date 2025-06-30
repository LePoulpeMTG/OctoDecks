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
