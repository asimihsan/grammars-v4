SELECT count(*) AS cnt
FROM telemetry_alerts_dev.int_otlp_logs_compacted_daily
WHERE day = DATE '2026-01-05'
