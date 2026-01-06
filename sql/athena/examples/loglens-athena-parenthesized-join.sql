SELECT table_schema, table_name
FROM (
  SELECT table_schema, table_name
  FROM information_schema.columns c
  JOIN information_schema.tables t USING (table_schema, table_name)
) jt
WHERE table_schema = 'telemetry_alerts_dev'
LIMIT 5
