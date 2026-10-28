"""Load the OpenPowerlifting CSV into a SQLite database."""
import csv
import sqlite3

DB_FILE = "powerlifting.db"
CSV_FILE = "data/melissagrix.csv"


def to_float(value):
    """Blank cells become None (NULL in SQL)."""
    return float(value) if value else None


def to_int(value):
    """Place can be blank or text (for example a disqualification)."""
    try:
        return int(value)
    except ValueError:
        return None


con = sqlite3.connect(DB_FILE)

with open("schema.sql") as f:
    con.executescript(f.read())

with open(CSV_FILE, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cursor = con.execute(
            "INSERT INTO meets (date, meet_name, federation, town, state) VALUES (?, ?, ?, ?, ?)",
            (row["Date"], row["MeetName"], row["Federation"], row["MeetTown"], row["MeetState"]),
        )
        meet_id = cursor.lastrowid

        con.execute(
            "INSERT INTO results (meet_id, equipment, bodyweight_kg, squat_kg, bench_kg, "
            "deadlift_kg, total_kg, place, dots) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (meet_id, row["Equipment"], to_float(row["BodyweightKg"]),
             to_float(row["Best3SquatKg"]), to_float(row["Best3BenchKg"]),
             to_float(row["Best3DeadliftKg"]), to_float(row["TotalKg"]),
             to_int(row["Place"]), to_float(row["Dots"])),
        )

con.commit()
print("meets:", con.execute("SELECT COUNT(*) FROM meets").fetchone()[0])
print("results:", con.execute("SELECT COUNT(*) FROM results").fetchone()[0])
con.close()