SELECT t.*
FROM telemetry_alerts_dev.int_otlp_logs_compacted_daily t
WHERE day = DATE '2026-01-05'
LIMIT 1
