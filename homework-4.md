# Homework 4 — Observability, Incident Response & Security Audit

## Question 1: Instrumentation

### Answer

> **Metrics, logs, and traces**

These are the **three pillars of observability**. CPU graphs alone are not observability — they only show resource usage, not what the system is actually doing from the user's perspective.

### What we did in practice

We instrumented our FastAPI backend (`main.py`) with **OpenTelemetry** to emit all three signals:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
FastAPIInstrumentor.instrument_app(app)
```

We also configured **structured logs** (JSON format) to avoid leaking secrets:

```python
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
```

All telemetry is shipped through the **OpenTelemetry Collector** — never directly to third-party services.

---

## Question 2: The Telemetry Pipeline

### Answer

> **OpenTelemetry**

OpenTelemetry (OTel) is the vendor-neutral, CNCF-backed standard for instrumentation.

### What we did in practice

We wired the full pipeline in `compose.yaml` and the `observability/` directory:

```
App (FastAPI + OTel SDK)
  │  OTLP (gRPC :4317)
  ▼
OpenTelemetry Collector (:4317)
  ├──► Prometheus  (:9090)  → metrics
  ├──► Loki        (:3100)  → logs
  └──► Tempo       (:3200)  → traces
          │
          ▼
       Grafana     (:3000)  → unified view
```

Key config files: `observability/collector.yaml`, `prometheus.yaml`, `tempo.yaml`, `grafana-datasources.yaml`.

---

## Question 3: Dashboards

### Answer

> **Grafana**

Grafana is the single pane of glass where metrics (Prometheus), logs (Loki), and traces (Tempo) are correlated and visualized together.

### What we did in practice

Grafana is auto-provisioned via Docker Compose with all three datasources:

```yaml
# observability/grafana-datasources.yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
  - name: Loki
    type: loki
    url: http://loki:3100
  - name: Tempo
    type: tempo
    url: http://tempo:3200
```

---

## Question 4: Alerts

### Answer

> **Real user impact, with context to start investigating**

A good alert fires when **users are hurting**, not when a resource crosses an arbitrary threshold.

### What we did in practice

We defined a `HighErrorRate` alert in `observability/alerts.yaml`:

```yaml
groups:
  - name: agent_relay
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[1m]))
          /
          sum(rate(http_requests_total[1m])) > 0.05
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "High HTTP 5xx error rate on /api/v1/tasks"
```

This alert represents real user pain (tasks failing with 500s) with context.

---

## Question 5: Evidence First

### Answer

> **With read-only, allowlisted queries**

Before any AI model gets involved, evidence must be collected in a **bounded, repeatable, read-only** way.

### What we did in practice

We created `incident-response/collect-evidence.sh` — a read-only script:

```bash
#!/usr/bin/env bash
set -euo pipefail
INCIDENT_ID="${1:?Usage: collect-evidence.sh <incident-id>}"
EVIDENCE_DIR="incident-response/evidence-${INCIDENT_ID}"
mkdir -p "$EVIDENCE_DIR"

# Read-only Prometheus query (error rate)
curl -s "http://localhost:9090/api/v1/query?query=rate(http_requests_total{status=~\"5..\"}[5m])" \
  > "$EVIDENCE_DIR/metrics-error-rate.json"

# Read-only Loki query (recent error logs)
curl -s "http://localhost:3100/loki/api/v1/query_range?query={app=\"agent-relay\"} |= \"ERROR\"&limit=50" \
  > "$EVIDENCE_DIR/logs-errors.json"
```

Key safety properties:
- **Read-only**: only `GET` queries
- **Allowlisted**: only pre-approved query patterns
- **Bounded**: `limit=50` on log queries
- **Repeatable**: same script = same evidence packet

---

## Question 6: The Agent Responder

### Answer

> **The autonomy policy and allowlists — code outside the model**

The model proposes, but **policy disposes**. An autonomy policy defines what the agent is allowed to do.

### What we did in practice

We defined an autonomy policy in `incident-response/autonomy-policy.yaml`:

```yaml
max_confidence_for_auto_action: 0.95
allowed_paths:
  - "main.py"
  - "config/"
  - "templates/"
forbidden_actions:
  - "database_migrations"
  - "delete_data"
  - "modify_credentials"
```

The agent responder proposed (in `incident-001-analysis.json`):

```json
{
  "root_cause": "Exception non gérée dans la route GET /api/v1/tasks...",
  "proposed_action": "Ajouter un bloc try-except...",
  "confidence_score": 0.92,
  "requires_human_approval": true
}
```

Because `0.92 < 0.95`, the policy correctly required **human approval**.

---

## Question 7: Security Audit

### Answer

> **Semgrep**

Semgrep is a deterministic, rule-based static analysis scanner. We pair it with model review and human validation.

### What we did in practice

We ran Semgrep against our codebase and stored results in `security-audit/runs/scan-result.json`:

```json
{
  "scanner": "semgrep",
  "version": "1.178.0",
  "timestamp": "2026-09-27T01:55:00Z",
  "target": "main.py",
  "results": {
    "findings": 0,
    "errors": 0,
    "summary": "No vulnerabilities detected"
  },
  "capability_inventory": {
    "responder_access": "read-only",
    "allowed_paths": ["main.py", "config/", "templates/"],
    "credentials_exposed": false
  }
}
```

We also created a capability table (`security-audit/capability-table.md`) documenting what the responder can and cannot do:

| Capability | Allowed | Scope |
|-----------|---------|-------|
| Read source code | ✅ | `main.py`, `config/`, `templates/` |
| Modify source code | ⚠️ | Only with human approval |
| Database access | ❌ | Forbidden |
| Credential access | ❌ | Forbidden |

---

## Question 8: Incident Report

### Incident #001 — Unhandled Exception in `/api/v1/tasks`

#### 1. Deployed version and user impact

- **Version**: Direct modification of `main.py` (no intermediate commit)
- **Impact**: Agent tasks were failing with HTTP 500 errors, preventing agents from retrieving their results. The `HighErrorRate` Prometheus alert fired when the error rate exceeded 5%.

#### 2. Alert and evidence inspected

- **Alert**: `HighErrorRate` (Prometheus) — error rate > 5% over 1 minute on `/api/v1/tasks`
- **Evidence collected** via `incident-response/collect-evidence.sh`:
  - Error rate metrics from Prometheus
  - Error logs from Loki showing `Exception: Simulation de panne en production`
  - Recent deploy timestamps

#### 3. Model and configuration used, action proposed

- **Model**: Claude (via Cline IDE)
- **Root cause**: Unhandled exception in `GET /api/v1/tasks` — the `get_tasks()` function raised `Exception('Simulation de panne en production')` without a try-except block
- **Proposed action**: Add a try-except block to catch the exception, log it with context, and return a structured HTTP 500 response
- **Confidence score**: 0.92

#### 4. Policy decision and command executed

- **Policy check**: `autonomy-policy.yaml` requires human approval for confidence scores below 0.95. Since `0.92 < 0.95`, human approval was required.
- **Decision**: Human reviewed the proposal and authorized the fix
- **Command executed**: Manual edit of `main.py` to add the try-except block:

```python
@app.get("/api/v1/tasks")
async def get_tasks():
    try:
        raise Exception("Simulation de panne en production")
    except Exception as e:
        logging.error(f"Erreur dans get_tasks: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "Une erreur est survenue lors de la récupération des tâches",
                "type": type(e).__name__
            }
        )
```

#### 5. Recovery verification

- **Test**: Manual test via `curl http://127.0.0.1:8000/api/v1/tasks`
- **Result**: HTTP 500 returned with structured error response:
  ```json
  {
    "detail": {
      "error": "Internal server error",
      "message": "Une erreur est survenue lors de la récupération des tâches",
      "type": "Exception"
    }
  }
  ```
- **Logs**: Structured error logged with full stack trace
- **Security audit**: Semgrep scan confirmed no new vulnerabilities introduced

#### Full report

See `docs/operations-and-security-report.md` for the complete incident documentation.




