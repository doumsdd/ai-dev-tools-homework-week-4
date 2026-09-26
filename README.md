# Agent Relay - FastAPI with OpenTelemetry

A FastAPI application with OpenTelemetry instrumentation for distributed tracing.

## Features

- FastAPI web framework
- OpenTelemetry distributed tracing
- OTLP exporter for sending traces to OpenTelemetry Collector
- Structured JSON logging
- Health check endpoint

## Installation

```bash
# Install dependencies
uv sync

# Or with pip
pip install -e .
```

## Running the Application

```bash
# Start the server
uvicorn main:app --reload

# Or with uv
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

## OpenTelemetry Configuration

The application is configured to export traces to an OpenTelemetry Collector at:
- **Endpoint:** `http://otel-collector:4317`
- **Protocol:** gRPC (OTLP)

To modify the collector endpoint, edit the `OTLPSpanExporter` configuration in `main.py`.

## Project Structure

```
.
├── main.py              # FastAPI application with OpenTelemetry
├── pyproject.toml       # Project dependencies
└── README.md
```

## Development

```bash
# Install in development mode
uv sync

# Run with hot reload
uv run uvicorn main:app --reload
```
