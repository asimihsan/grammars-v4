SELECT event_ts, severity, body, error, error_code, attributes_json, cid, trace_id, service_name, message_type, source, app_id, arn, device_token
FROM telemetry_alerts_dev.int_otlp_logs_compacted_daily
WHERE day = DATE '2026-01-05'
  AND service_name = 'push-server'
  AND severity = 'error'
ORDER BY event_ts DESC
LIMIT 50
