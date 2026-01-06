SELECT ordinal_position,
    column_name,
    data_type,
    is_nullable,
    comment
FROM information_schema.columns
WHERE table_schema = 'telemetry_alerts_dev'
    AND table_name = 'int_otlp_logs_compacted_daily'
ORDER BY ordinal_position