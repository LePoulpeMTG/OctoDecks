<!-- 📁 chemin relatif : assets\README.md -->
# 📦 Dossier `assets/` – Système de fichiers partagés OctoDecks

Ce dossier contient tous les **fichiers visuels et source partagés** entre les différentes apps Flutter du projet OctoDecks.

## 🎯 Objectif

Centraliser les éléments communs (thèmes, icônes, widgets, composants) dans un seul emplacement pour :

- garantir une **cohérence visuelle** entre toutes les apps (web, desktop, mobile),
- simplifier la **maintenance** (1 source = synchronisée partout),
- éviter la duplication de code ou d’assets.

---

## 🗂 Structure recommandée

```
assets/
├── icons/
│   └── shared/               # Icônes réutilisables, poussées vers chaque app
├── theme/
│   └── shared/
│       ├── octo_theme.dart   # Thème Flutter centralisé
│       └── styleguide_page.dart # Page de test du thème
├── widgets/
│   └── shared/
│       ├── octo_button.dart
│       ├── octo_card.dart
│       ├── octo_chip.dart
│       └── octo_widgets.dart    # Exporte tous les widgets ci-dessus
```

---

## 🔁 Synchronisation via `sync_shared_assets.py`

Le script `tools/dev/sync_shared_assets.py` est chargé de :

- Copier tous les fichiers de :
  - `assets/icons/shared/` → dans `apps/*/assets/icons/`
  - `assets/theme/shared/` → dans `apps/*/lib/theme/`
  - `assets/widgets/shared/` → dans `apps/*/lib/widgets/`

Ce script est **idempotent** : il peut être relancé à tout moment pour re-synchroniser les dernières versions.

---

## ✅ Bonnes pratiques

- Toujours modifier les fichiers **dans `assets/`**, jamais dans les apps directement.
- Lancer régulièrement le script pour garder les apps à jour :
  ```bash
  python tools/dev/sync_shared_assets.py
  ```
- Nommer les fichiers sans collision avec Flutter (`octo_theme.dart` plutôt que `theme.dart`, `octo_widgets.dart` plutôt que `widgets.dart`).

---

## 💡 Exemples d'usage dans les apps

```dart
import 'package:web_admin/theme/octo_theme.dart';
import 'package:web_admin/widgets/octo_widgets.dart';
```

Chaque app peut ainsi utiliser les composants sans redondance ni conflit.

---

## 🧠 Pourquoi ce système ?

Parce que le projet OctoDecks est un **monorepo modulaire** multi-apps :  
➡️ une seule source de vérité, synchronisée proprement pour éviter les dérives UI.

---
## ✅ Checklist des Widgets OctoDecks

### 🎛️ Filtres et UI deckbuilding
- [ ] `OctoFilterChip` — Puce de filtre cliquable (mana, rareté…)
- [ ] `OctoFilterBar` — Barre horizontale avec groupes de filtres
- [ ] `OctoSegmentedControl` — Toggle multiple (ex : Toutes / Possédées / Manquantes)
- [ ] `OctoDropdown` — Menu déroulant customisé
- [ ] `OctoRangeSlider` — Slider double (mana cost, prix…)
- [ ] `OctoSearchField` — Barre de recherche avec icône

---

### 🧩 Composants visuels réutilisables
- [ ] `OctoCardTile` — Affichage d’une carte (image + nom + rareté)
- [ ] `OctoSetTile` — Affichage résumé d’un set
- [ ] `OctoPriceTag` — Étiquette de prix (avec variation)
- [ ] `OctoSectionHeader` — Titre de section (avec collapse optionnel)
- [ ] `OctoTag` — Petit label stylisé

---

### 🖱️ Interaction et navigation
- [ ] `OctoButton` — Bouton principal (avec variantes)
- [ ] `OctoIconButton` — Bouton circulaire avec icône
- [ ] `OctoFloatingPanel` — Panneau flottant (comme deck builder Arena)
- [ ] `OctoTabBar` — Barres d’onglets stylées
- [ ] `OctoBottomSheet` — Fenêtre modale basse (options ou actions)

---

### 📦 Containers et mises en forme
- [ ] `OctoCardContainer` — Conteneur avec ombre, bordure, etc.
- [ ] `OctoGridView` — Grille responsive pour affichage cartes
- [ ] `OctoListSection` — Liste groupée par section

---

### ⚠️ Statuts / Badges / Tags
- [ ] `OctoStatusBadge` — Badge d’état (Possédé, En vente, Wanted…)
- [ ] `OctoRarityIcon` — Icône rareté cohérente (C/U/R/M)
- [ ] `OctoManaIcon` — Icône de mana (WUBRG, hybrid, phyrexian…)
- [ ] `OctoLangIcon` — Icône de langue (drapeaux)
