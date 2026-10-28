-- Two tables: one row per meet, one row per result.
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS meets;

CREATE TABLE meets (
  meet_id    INTEGER PRIMARY KEY,
  date       TEXT NOT NULL,   -- YYYY-MM-DD
  meet_name  TEXT NOT NULL,
  federation TEXT,
  town       TEXT,
  state      TEXT
);

CREATE TABLE results (
  result_id     INTEGER PRIMARY KEY,
  meet_id       INTEGER NOT NULL REFERENCES meets (meet_id),
  equipment     TEXT,         -- Raw or Wraps
  bodyweight_kg REAL,
  squat_kg      REAL,
  bench_kg      REAL,
  deadlift_kg   REAL,
  total_kg      REAL,
  place         INTEGER,
  dots          REAL
);