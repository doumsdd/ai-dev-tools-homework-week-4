import logging
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configuration des logs structurés
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)

app = FastAPI(title="Agent Relay")

# Configuration OpenTelemetry
trace.set_tracer_provider(TracerProvider())
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrumentation de FastAPI
FastAPIInstrumentor.instrument_app(app)


@app.get("/")
async def root():
    return {"message": "Agent Relay is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/api/v1/tasks")
async def get_tasks():
    try:
        # Simulation de traitement
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
