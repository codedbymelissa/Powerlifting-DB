"""Run the SQL queries and write docs/index.html."""
import json
import sqlite3
from datetime import datetime

con = sqlite3.connect("powerlifting.db")
con.row_factory = sqlite3.Row


def run(name):
    """Run queries/<name>.sql and return a list of dictionaries."""
    with open(f"queries/{name}.sql") as f:
        return [dict(row) for row in con.execute(f.read())]


def show(value):
    """Format a value for the page: None becomes a dash, 390.0 becomes 390."""
    if value is None:
        return "–"
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return str(value)


def make_table(rows, columns):
    """columns is a list of (key, heading) pairs."""
    head = "".join(f'<th scope="col">{heading}</th>' for _, heading in columns)
    body = ""
    for row in rows:
        cells = "".join(f"<td>{show(row[key])}</td>" for key, _ in columns)
        body += f"<tr>{cells}</tr>"
    return f'<table class="table table-sm"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


summary = run("summary")[0]
meets = run("progression")
equipment = run("equipment")
con.close()

# Headline numbers at the top of the page
stats = [
    (summary["meets"], "meets"),
    (summary["wins"], "first-place finishes"),
    (show(summary["best_total"]) + " kg", "best total"),
    (show(summary["best_dots"]), "best DOTS"),
]
stats_html = "".join(
    f'<div class="col-6 col-md-3"><div class="stat-value">{value}</div>'
    f'<div class="stat-label">{label}</div></div>'
    for value, label in stats
)

history_table = make_table(meets, [
    ("date", "Date"), ("meet_name", "Meet"), ("equipment", "Equipment"), ("place", "Place"),
    ("squat_kg", "Squat"), ("bench_kg", "Bench"), ("deadlift_kg", "Deadlift"),
    ("total_kg", "Total"), ("dots", "DOTS"), ("total_change_kg", "Change in total"),
])

equipment_table = make_table(equipment, [
    ("equipment", "Equipment"), ("meets", "Meets"), ("best_total_kg", "Best total (kg)"),
    ("avg_total_kg", "Average total (kg)"), ("avg_dots", "Average DOTS"),
])

# Data for the chart
chart_data = {
    "labels": [datetime.strptime(m["date"], "%Y-%m-%d").strftime("%b %Y") for m in meets],
    "squat": [m["squat_kg"] for m in meets],
    "bench": [m["bench_kg"] for m in meets],
    "deadlift": [m["deadlift_kg"] for m in meets],
}

# Fill the template
with open("templates/index.template.html", encoding="utf-8") as f:
    page = f.read()

page = page.replace("__STATS__", stats_html)
page = page.replace("__HISTORY__", history_table)
page = page.replace("__EQUIPMENT__", equipment_table)
page = page.replace("__DATA__", json.dumps(chart_data))
page = page.replace("__YEAR__", str(datetime.now().year))

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(page)

print("Wrote docs/index.html")