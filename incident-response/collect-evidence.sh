#!/bin/bash
# incident-response/collect-evidence.sh
# Usage: ./collect-evidence.sh <incident_id>

INCIDENT_ID=$1
TIME_RANGE="1h"

echo "=== Collecting Evidence for Incident $INCIDENT_ID ==="

# 1. Récupérer les métriques d'erreur récentes (Prometheus)
echo "--- Metrics (Error Rate) ---"
curl -s "http://localhost:9090/api/v1/query?query=rate(http_server_response_status_code_count{status_code=~'5..'}[$TIME_RANGE])"

# 2. Récupérer les logs d'erreur associés (Loki)
echo "--- Logs (Errors) ---"
curl -s -G "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={job="agent-relay"} |= "error" or "exception"' \
  --data-urlencode "limit=10"

echo "Evidence collection complete. No write operations were performed."
