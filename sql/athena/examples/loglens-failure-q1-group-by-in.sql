SELECT day, body, severity, count(*) AS cnt
FROM telemetry_alerts_dev.int_otlp_logs_compacted_daily
WHERE day >= DATE '2026-01-01'
  AND day <= DATE '2026-01-06'
  AND service_name = 'push-server'
  AND severity IN ('error','warn','debug')
  AND body IN (
    'Failed to handle the message',
    'Error processing push notification request messages',
    'Failed to update the push token document: the document does not exist',
    'No push tokens with disabled endpoints among the failures',
    'Failed to publish a push message to the SNS endpoint',
    'Failed to send a message'
  )
GROUP BY 1,2,3
ORDER BY day DESC, cnt DESC
