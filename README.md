# Powerlifting log

My powerlifting meet history from 2017 to 2024, stored in a SQLite database, queried with SQL, and turned into a web page with Python.

**Live page:** add your GitHub Pages link here

The results come from my public [OpenPowerlifting](https://www.openpowerlifting.org/u/melissagrix) profile.

## How it works

1. `build_db.py` reads `data/melissagrix.csv` and loads it into a SQLite database using the tables in `schema.sql`.
2. `build_report.py` runs the three queries in `queries/` and builds `docs/index.html`.
3. GitHub Pages serves the `docs` folder.

## The database

| Table | One row per | Columns |
| --- | --- | --- |
| `meets` | meet | date, meet name, federation, town, state |
| `results` | meet result | equipment, bodyweight, squat, bench, deadlift, total, place, DOTS |

## The queries

| File | What it does | SQL used |
| --- | --- | --- |
| `queries/summary.sql` | Best lifts, best total, meets and wins | `MAX`, `COUNT`, `SUM` |
| `queries/progression.sql` | Every meet in order, with the change in total | `JOIN`, `LAG()`, `ORDER BY` |
| `queries/equipment.sql` | Raw compared with Wraps | `GROUP BY`, `AVG` |

## Notes

- Raw and Wraps meets are combined in the chart, so a drop in total can be an equipment change rather than lost strength.
