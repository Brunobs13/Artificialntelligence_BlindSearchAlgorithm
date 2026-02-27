# Technical Overview

## 1. Deep Architectural Explanation
### Full Flow
1. User selects territory, budget combination, strategy, and depth in the web control room.
2. Frontend calls `/api/run`.
3. FastAPI validates payload and loads domain objects from `core/data.py`.
4. Search engine executes BFS- or DFS-limited traversal.
5. Engine returns trace + metrics.
6. Frontend animates each step and updates telemetry cards.

### Technical Decision Rationale
- **FastAPI**: fast delivery of typed API contracts and async-ready architecture.
- **Modular search engine**: isolates algorithmic logic from transport/UI concerns.
- **Static frontend served by API**: single deployable service for portfolio demos.
- **State cap guardrail**: prevents runaway exploration under high complexity.

### Trade-offs
- In-memory execution is simple and fast but non-persistent.
- Depth-limited blind search is predictable but can miss globally optimal configurations.
- Static data catalog ensures reproducibility but limits runtime extensibility.

### Alternatives Considered
- A* or informed search: rejected to preserve blind-search requirement.
- React dashboard: rejected to keep deployment lightweight.
- Database-backed scenarios: deferred to future phase.

## 2. Junior Interview Questions
- What is the difference between BFS and DFS in this project?
- Why is depth limit necessary in blind search?
- How does the algorithm compute protected families?
- Why did you separate API and engine modules?
- What does the state cap protect against?

## 3. Senior Interview Questions
- How would you scale this service for multi-tenant enterprise use?
- How would you persist and version scenario datasets safely?
- What SLOs would you define for simulation latency and reliability?
- How would you add role-based access and audit trails?
- How would you redesign this for distributed search execution?

## 4. Critical Code Walkthrough
### `engine/search.py -> run_search`
- Executes bounded state-space exploration with strategy selection.
- Tracks expansions, generated states, frontier size, and target hits.
- Captures a trace for replay in the dashboard.

### `engine/search.py -> calculate_coverage`
- Computes unique-cell coverage for multiple stations and radii.
- Avoids double-counting overlapping protected cells.

### `api/app.py -> /api/run`
- Validates input and orchestrates domain + engine interaction.
- Central API entrypoint for enterprise simulation flows.

### `api/static/app.js`
- Plays back algorithm states in a live operational UI.
- Converts algorithm telemetry into business-readable metrics.

## 5. Scaling Discussion
- Persist scenarios/results in PostgreSQL.
- Add Redis caching for repeated runs.
- Use task queue (Celery/RQ) for heavy simulations.
- Expose WebSocket stream for incremental trace delivery.
- Deploy behind horizontal autoscaling with sticky-less stateless API instances.

## 6. Memory Management Discussion
- Current memory pressure is driven by:
  - `visited` state set
  - trace storage
- Controls in place:
  - `max_states`
  - `max_trace_steps`
- Future optimization:
  - compress state representation,
  - optional trace sampling,
  - external storage for long runs.

## 7. Concurrency Discussion
- Current execution is per-request synchronous compute.
- Concurrency strategy for production:
  - worker queue per simulation,
  - request-level idempotency keys,
  - cancellation tokens for long-running jobs.
