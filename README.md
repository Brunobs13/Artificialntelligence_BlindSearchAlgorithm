# Corporate Blind Search Control Room

A production-structured modernization of an academic blind-search algorithm into a corporate decision-support platform.

The system simulates how a security operations team can deploy mobile response stations under strict budget constraints to maximize protected population in high-risk zones.

## Project Overview
This repository converts a single-script academic implementation into a modular backend + interactive website with:
- live BFS/DFS depth-limited simulation,
- measurable operational KPIs,
- structured API for scenario execution,
- deployment-ready engineering standards.

## Business Problem
Large retail and logistics organizations must decide where to deploy limited security resources.
Given a fixed budget and possible station radius combinations, the platform searches relocation states to maximize protected families in risk-weighted territory grids.

## Architecture Diagram
```text
[Web Control Room UI]
        |
        | REST
        v
[FastAPI Controller Layer] -------------------------+
        |                                           |
        v                                           v
[Search Engine: BFS/DFS Limited]         [Territory + Budget Data Catalog]
        |                                           |
        +-------------------[Metrics + Trace]-------+
                            |
                            v
                    [Telemetry & Benchmark Views]
```

## Tech Stack
- Python 3.11
- FastAPI + Uvicorn
- Vanilla HTML/CSS/JavaScript
- Pytest
- Docker + Docker Compose
- GitHub Actions CI

## Project Structure
```text
.
├── src/blindsearch_engine/
│   ├── api/
│   │   ├── app.py
│   │   ├── schemas.py
│   │   └── static/
│   ├── core/
│   │   ├── data.py
│   │   └── models.py
│   ├── engine/
│   │   └── search.py
│   └── utils/
├── tests/
├── configs/
├── scripts/
├── docs/
├── legacy/academic_project/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── .env.example
```

## Setup Instructions
### 1. Local environment
```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the application
```bash
./scripts/run_api.sh
```
Open `http://localhost:8080`.

### 3. Run tests
```bash
./scripts/test.sh
```

## CI/CD Overview
CI pipeline (`.github/workflows/ci.yml`) runs on push/PR to `main`:
- dependency installation,
- automated tests,
- quality gate before merge.

Recommended CD path:
- release tags (`vX.Y.Z`),
- Docker image publish,
- deployment to container-hosting platform.

## Data Versioning Strategy
Current territory and budget data are versioned directly in Git (`core/data.py`) for deterministic reproducibility.
For scale-up:
- move large evolving scenario datasets to DVC,
- track scenario snapshots by release tags,
- introduce remote storage for enterprise governance.

## Model Tracking Strategy
This project uses deterministic search logic, not ML models.
If predictive risk scoring is added in future:
- use MLflow for experiment and model tracking,
- link dataset versions via DVC,
- apply promotion gates in CI.

## Deployment Strategy
### Docker
```bash
docker compose up --build
```
Application becomes available at `http://localhost:8080`.

### Production recommendation
- run behind reverse proxy/load balancer,
- enable autoscaling,
- centralize logs and metrics.

## Security Considerations
- no hardcoded credentials,
- environment-based config via `.env`,
- `.gitignore` protects local secrets and artifacts,
- input validation on API payloads,
- structured logs for auditability.

## Lessons Learned
- modular architecture dramatically improves maintainability vs monolithic scripts,
- algorithm transparency (live trace) improves stakeholder trust,
- repository hygiene is essential for interview and production readiness.

## Future Improvements
- add persistent scenario storage (PostgreSQL),
- add authentication/authorization,
- stream trace via WebSockets for true real-time updates,
- add rate limiting and API contract tests,
- integrate observability stack (Prometheus + Grafana).

## Additional Documentation
- Technical audit: `docs/repository_audit.md`
- Technical deep dive + interview prep: `docs/TECHNICAL_OVERVIEW.md`
- Portfolio package: `docs/portfolio_ready.md`
