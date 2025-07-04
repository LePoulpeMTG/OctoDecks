PRAGMA foreign_keys = ON;


-- ------------------------------
-- sets
-- ------------------------------
CREATE TABLE sets (
  set_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  set_code     TEXT UNIQUE NOT NULL,
  name         TEXT,
  release_date TEXT,
  set_type     TEXT,
  total_cards  INTEGER,
  is_digital   BOOLEAN DEFAULT 0,
  icon_svg_uri TEXT
);
-- ------------------------------
-- set_statistics
-- ------------------------------
CREATE TABLE IF NOT EXISTS set_statistics (
  set_code            TEXT PRIMARY KEY,
  num_prints          INTEGER,
  num_oracle_ids      INTEGER,
  has_promo_cards     BOOLEAN,
  has_double_faced    BOOLEAN,
  available_layouts   TEXT, -- ex: "normal,adventure,transform"
  available_languages TEXT, -- ex: "en,fr,de"
  value_card_max_eur  REAL,
  foil_percentage     REAL,
  rarity_common_pct   REAL,
  rarity_uncommon_pct REAL,
  rarity_rare_pct     REAL,
  rarity_mythic_pct   REAL,
  FOREIGN KEY (set_code) REFERENCES sets (set_code)
);

-- ------------------------------
-- set_languages
-- ------------------------------
CREATE TABLE IF NOT EXISTS set_languages (
  set_code TEXT NOT NULL,
  lang     TEXT NOT NULL,
  PRIMARY KEY (set_code, lang),
  FOREIGN KEY (set_code) REFERENCES sets (set_code)
);

-- ------------------------------
-- cards
-- ------------------------------
CREATE TABLE cards (
  oracle_id      TEXT PRIMARY KEY,
  name           TEXT,
  type_line      TEXT,
  cmc            REAL,
  color_identity TEXT,
  keywords       TEXT,
  edhrec_rank    INTEGER,
  is_reserved    BOOLEAN,
  is_promo       BOOLEAN,
  layout         TEXT
);

-- ------------------------------
-- prints
-- ------------------------------
CREATE TABLE prints (
  scryfall_id      TEXT PRIMARY KEY,
  oracle_id        TEXT NOT NULL,
  set_id           INTEGER NOT NULL,
  collector_number TEXT,
  lang             TEXT,
  rarity           TEXT,
  layout           TEXT,
  image_front_uri  TEXT,
  image_back_uri   TEXT,
  card_faces_json  TEXT,
  scryfall_uri     TEXT,
  cardmarket_uri   TEXT,
  foil             BOOLEAN,
  nonfoil          BOOLEAN,
  FOREIGN KEY (oracle_id) REFERENCES cards (oracle_id),
  FOREIGN KEY (set_id) REFERENCES sets (set_id)
);
CREATE INDEX idx_prints_oracle ON prints(oracle_id);
CREATE INDEX idx_prints_setlang ON prints(set_id, lang);

-- ------------------------------
-- card_legalities
-- ------------------------------
CREATE TABLE card_legalities (
  oracle_id TEXT,
  format    TEXT,
  status    TEXT,
  PRIMARY KEY (oracle_id, format),
  FOREIGN KEY (oracle_id) REFERENCES cards (oracle_id)
);
-- ------------------------------
-- prices_daily_card
-- ------------------------------
CREATE TABLE IF NOT EXISTS prices_daily_card (
  scryfall_id TEXT,
  date        TEXT,
  eur         REAL,
  eur_foil    REAL,
  usd         REAL,
  usd_foil    REAL,
  usd_etched  REAL,
  PRIMARY KEY (scryfall_id, date),
  FOREIGN KEY (scryfall_id) REFERENCES prints (scryfall_id)
);

-- ------------------------------
-- prices_weekly_card
-- ------------------------------
CREATE TABLE IF NOT EXISTS prices_weekly_card (
  scryfall_id    TEXT,
  week           TEXT,   -- ISO-8601 YYYY-WW
  eur_avg        REAL,
  eur_min        REAL,
  eur_max        REAL,
  eur_foil_avg   REAL,
  usd_avg        REAL,
  usd_min        REAL,
  usd_max        REAL,
  usd_foil_avg   REAL,
  usd_etched_avg REAL,
  PRIMARY KEY (scryfall_id, week),
  FOREIGN KEY (scryfall_id) REFERENCES prints (scryfall_id)
);

CREATE TABLE IF NOT EXISTS prices_daily_set (
  set_code         TEXT NOT NULL,
  date             TEXT NOT NULL,
  avg_eur          REAL,
  avg_usd          REAL,
  total_eur        REAL,
  total_usd        REAL,
  cards_priced_eur INTEGER,
  cards_priced_usd INTEGER,
  total_cards      INTEGER,
  PRIMARY KEY (set_code, date),
  FOREIGN KEY (set_code) REFERENCES sets (set_code)
);

-- ------------------------------
-- prices_weekly_set
-- ------------------------------
CREATE TABLE prices_weekly_set (
  set_code          TEXT,
  week              TEXT,
  avg_eur           REAL,
  avg_usd           REAL,
  total_eur         REAL,
  total_usd         REAL,
  cards_priced_eur  INTEGER,
  cards_priced_usd  INTEGER,
  total_cards       INTEGER,
  PRIMARY KEY (set_code, week)
);

-- ------------------------------
-- card_localizations
-- ------------------------------
CREATE TABLE card_localizations (
  oracle_id        TEXT,
  set_code         TEXT,
  collector_number TEXT,
  lang             TEXT,
  name             TEXT,
  oracle_text      TEXT,
  flavor_text      TEXT,
  image_front_uri  TEXT,
  image_back_uri   TEXT,
  PRIMARY KEY (oracle_id, set_code, lang),
  FOREIGN KEY (oracle_id) REFERENCES cards (oracle_id),
  FOREIGN KEY (set_code)  REFERENCES sets  (set_code)
);
