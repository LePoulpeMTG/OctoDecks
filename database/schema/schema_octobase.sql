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
  scryfall_id   TEXT,
  week          TEXT,
  eur_avg       REAL,
  eur_min       REAL,
  eur_max       REAL,
  eur_foil_avg  REAL,
  usd_avg       REAL,
  usd_min       REAL,
  usd_max       REAL,
  usd_foil_avg  REAL,
  usd_etched_avg REAL,
  PRIMARY KEY (scryfall_id, week),
  FOREIGN KEY (scryfall_id) REFERENCES prints (scryfall_id)
);
-- ------------------------------
-- prices_daily_set
-- ------------------------------
CREATE TABLE IF NOT EXISTS prices_daily_set (
  set_code    TEXT NOT NULL,          -- FK vers sets.set_code
  date        TEXT NOT NULL,          -- AAAA-MM-JJ
  avg_eur     REAL,
  avg_usd     REAL,
  total_cards INTEGER,
  PRIMARY KEY (set_code, date),
  FOREIGN KEY (set_code) REFERENCES sets (set_code)
);

-- ------------------------------
-- prices_weekly_set
-- ------------------------------
CREATE TABLE IF NOT EXISTS prices_weekly_set (
  set_code    TEXT NOT NULL,
  week        TEXT NOT NULL,          -- ISO-8601 (ex. 2025-27)
  avg_eur     REAL,
  avg_usd     REAL,
  total_cards INTEGER,
  PRIMARY KEY (set_code, week),
  FOREIGN KEY (set_code) REFERENCES sets (set_code)
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
