-- Every meet in date order. LAG() looks at the previous row,
-- so total_change_kg is this meet's total minus the last meet's total.
SELECT
  m.date,
  m.meet_name,
  r.equipment,
  r.place,
  r.squat_kg,
  r.bench_kg,
  r.deadlift_kg,
  r.total_kg,
  r.dots,
  r.total_kg - LAG(r.total_kg) OVER (ORDER BY m.date) AS total_change_kg
FROM results r
JOIN meets m ON m.meet_id = r.meet_id
ORDER BY m.date;