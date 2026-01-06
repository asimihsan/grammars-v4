SELECT COUNT(DISTINCT day) AS distinct_days
FROM telemetry_alerts_dev.int_otlp_logs_compacted_daily
WHERE day >= DATE '2026-01-01'
  AND day <= DATE '2026-01-06'
