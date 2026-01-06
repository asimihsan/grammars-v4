SELECT c.table_schema, c.table_name
FROM information_schema.columns c
JOIN information_schema.tables t
  ON c.table_schema = t.table_schema
 AND c.table_name = t.table_name
WHERE c.table_schema = 'telemetry_alerts_dev'
LIMIT 5
