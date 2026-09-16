# Agent Relay - Week 3 Homework: DevOps & Cloud Native Deployment

## Homework Overview

This project demonstrates the complete journey of transforming a SQLite-based FastAPI application into a production-ready, cloud-native application with PostgreSQL, Docker, Kubernetes, and CI/CD pipelines.

## Learning Objectives

1. Database migration from SQLite to PostgreSQL
2. Containerization with Docker and Docker Compose
3. Kubernetes deployment with persistent storage and health checks
4. CI/CD pipeline implementation with GitHub Actions
5. Local development and testing with act

---

## Step-by-Step Process

### Step 1: Database Migration (SQLite to PostgreSQL)

**Objective**: Migrate from SQLite to PostgreSQL while maintaining backward compatibility.

**Key Changes**:
- Modified database.py to support both SQLite and PostgreSQL
- Implemented dual datetime handling (naive UTC for SQLite, timezone-aware for PostgreSQL)
- Updated transaction management:
  - SQLite: Uses BEGIN IMMEDIATE for serialization
  - PostgreSQL: Uses FOR UPDATE SKIP LOCKED for row-level locking

**Files Modified**: database.py, storage.py

---

### Step 2: Docker Containerization

**Objective**: Containerize the application for consistent deployment.

**Created Files**:
- Dockerfile - Multi-stage build using Python 3.11-slim and uv
- .dockerignore - Excludes unnecessary files from the image
- compose.yaml - Two-service stack (API + PostgreSQL)

**Question 1 Answered**: 
> **Which hostname should the API use to connect to the postgres service?**
> 
> **Answer: postgres** (the service name)
> 
> Docker Compose provides built-in DNS resolution where services can reach each other using their service names as hostnames.

---

### Step 3: Kubernetes Deployment

**Objective**: Deploy the application to a local Kubernetes cluster using kind.

**Created Manifests** (in k8s/ directory):
- Namespace, Secret, PersistentVolumeClaim
- PostgreSQL Deployment & Service (with health checks)
- API Deployment (2 replicas) & Service
- Kustomization for one-command deployment

**Question 2 Answered**:
> **Which Kubernetes resource keeps the requested number of application replicas running and manages updates?**
> 
> **Answer: Deployment**
> 
> Deployments manage replica count, handle rolling updates, provide self-healing, and enable easy scaling and rollbacks.

---

### Step 4: CI/CD Pipeline

**Objective**: Automate testing, building, and deployment.

**Created Files**:
- .github/workflows/ci.yml - GitHub Actions workflow
- .actrc - Configuration for running workflows locally with act

**Pipeline Stages**:
1. **test**: Run unit tests (SQLite) + integration tests (PostgreSQL)
2. **build-and-deploy**: Build image, deploy to kind (only if tests pass)

**Question 3 Answered**:
> **What should happen if a test fails in this workflow?**
> 
> **Answer: Keep the existing version running and stop the deployment.**
> 
> The workflow uses needs: test to ensure build-and-deploy only runs if tests pass.

---

## Documentation

- **QUESTIONS_ANSWERS.md** - All questions and answers from the homework
- **POSTGRES_MIGRATION.md** - Detailed PostgreSQL migration guide
- **KUBERNETES_DEPLOYMENT.md** - Kubernetes deployment instructions
- **K8S_SUMMARY.md** - Kubernetes implementation summary
- **CI_CD_PIPELINE.md** - CI/CD pipeline documentation
- **CI_CD_SUMMARY.md** - CI/CD implementation summary

---

## Prerequisites

### Required Tools
- Python 3.11+
- Docker Desktop (with WSL2 backend)
- kubectl, kind, act

### Installation (Windows)
`powershell
winget install Kubernetes.kubectl
winget install Kubernetes.kind
winget install nektos.act
`

### System Requirements
- **WSL2 with virtualization enabled** - Required for Docker Desktop
- Enable in BIOS/UEFI: Intel VT-x or AMD-V

---

## Quick Start

`ash
# Install dependencies
uv sync

# Run tests
uv run pytest test_agent_relay.py -v

# Start with Docker Compose
docker compose up --build

# Deploy to Kubernetes
kind create cluster --name agent-relay
docker build -t agent-relay:local .
kind load docker-image agent-relay:local --name agent-relay
kubectl apply -k k8s/

# Run CI/CD locally
act push -P ubuntu-latest=catthehacker/ubuntu:act-latest
`

---

## Architecture

`
Kubernetes Cluster
  Namespace: agent-relay
    PostgreSQL (PVC: 1Gi) <-- API (2 pods)
                           |
                           v
                localhost:8000 (port-forward)
`

---

## Key Concepts Learned

1. **Database Abstraction** - Supporting multiple backends with database-specific optimizations
2. **Containerization** - Docker builds, service orchestration, health checks
3. **Kubernetes** - Declarative infrastructure, persistent storage, rolling updates
4. **CI/CD** - Automated testing, conditional deployment, image tagging
5. **Docker Networking** - Service discovery, container communication

---

## Summary

This homework demonstrates a complete DevOps transformation:

- **Database Migration**: SQLite to PostgreSQL with dual support  
- **Containerization**: Docker + Docker Compose  
- **Kubernetes**: Full deployment with persistent storage and health checks  
- **CI/CD**: Automated testing and deployment pipeline  
- **Local Development**: Run entire pipeline locally with act

All components work together to provide a production-ready, cloud-native application with automated testing, deployment, and zero-downtime updates.
