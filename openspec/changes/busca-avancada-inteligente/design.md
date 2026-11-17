# Design

## Context

EduTrack AI utilizes Xano as its backend platform for database persistence and REST APIs, while Python is used for specialized computation logic (such as `scripts/calculate_progress.py`). The application maintains academic subjects in the `subjects` table and assignments in the `academic_tasks` table.

For Tarefa 14, students need to locate subjects by name or identify subjects that have urgent academic priorities (overdue tasks). Performing this search requires coordinating Xano's database and authentication security with Python's evaluation logic:
- Xano enforces request authentication via `authToken` and scopes database queries strictly to the authenticated student's `user_id`.
- Python processes the user's subjects and task records to evaluate name matching and overdue deadlines using disjunctive ("OR") filtering.

## Goals / Non-Goals

**Goals:**
- Implement `GET /subjects/search` in `apis/subjects/` with `authToken` middleware.
- Implement `scripts/search_subjects.py` accepting subject data, tasks, and search parameters (`q`, `has_overdue`, `reference_date`) and emitting JSON results.
- Implement disjunctive ("OR") filtering when both name query and overdue filters are specified.
- Guarantee strict user data isolation so that queries only process and expose records belonging to the authenticated user.

**Non-Goals:**
- No changes to existing CRUD endpoints in `apis/subjects/` (`GET /subjects`, `POST /subjects`, etc.).
- No external search engine dependencies (e.g., Elasticsearch, Algolia, Solr).
- No alterations to table schemas in `tables/`.
- No modifications to the static web application in `web/` or FlutterFlow frontend.

## Decisions

### Decision 1: Hybrid Architecture — Xano for Security & Data, Python for Search Logic
- **Rationale**: Xano is the system of record and provides authentication guards (`auth = "user"`). Scoping queries to `$auth.id` within Xano ensures data cannot leak between users. Python provides flexible string manipulation (case-insensitive search) and date comparison logic that is clean, portable, and easily tested in isolation (mirroring `scripts/calculate_progress.py`).
- **Alternatives considered**:
  - *Pure XanoScript search*: Complex filtering with relational joins across subjects and tasks involving conditional dates is cumbersome to maintain and less testable in automated CI pipelines.
  - *Separate Python microservice*: Adds hosting overhead, deployment dependencies, and network latency; decoupled script execution provides simplicity and robust isolation.

### Decision 2: Disjunctive ("OR") Logic for Combined Filters
- **Rationale**: Tarefa 14 specifically specifies filtering results by subject name OR by the presence of overdue tasks ("Filtrar os resultados por nome da disciplina OU pela existência de tarefas atrasadas"). When a request includes both `q` and `has_overdue=true`, any subject that matches the name search OR has at least one overdue task will be returned in the results.
- **Alternatives considered**:
  - *Conjunctive ("AND") filtering*: Would restrict results only to subjects that simultaneously match the name query and have overdue tasks, violating the requirement.

### Decision 3: Overdue Task Definition and Deterministic Reference Date
- **Rationale**: An academic task is defined as overdue if its `due_date` is strictly earlier than the reference date and its `status` is not completed (e.g., `completed`, `done`, `concluída`). The evaluation script will accept an optional `reference_date` (defaulting to the current date/UTC) to facilitate deterministic unit and integration testing without relying on non-deterministic clock states.
- **Alternatives considered**:
  - *Strict system clock without override*: Prevents reliable test assertions across different test dates and timezone boundaries.

### Decision 4: CLI and JSON Ingestion Interface for Python Script
- **Rationale**: Following the pattern established by `scripts/calculate_progress.py`, the search script will support JSON payload ingestion via stdin or CLI argument, returning structured JSON to stdout. This ensures decoupling, testability from the terminal, and straightforward invocation from backend stacks.
- **Alternatives considered**:
  - *Reading directly from a database file*: Bypasses Xano's security boundaries and breaks data isolation.

## Risks / Trade-offs

- **[Risk] Performance on large student datasets** → *Mitigation*: Database queries in Xano filter exclusively by `user_id == $auth.id` before passing data to the Python script. Individual student datasets are small (rarely exceeding dozens of subjects and hundreds of tasks), ensuring sub-second execution.
- **[Risk] Date format and timezone inconsistencies** → *Mitigation*: Normalize dates to standard ISO-8601 strings (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SSZ`) before comparison in Python.
- **[Risk] Malformed input payloads** → *Mitigation*: The Python script validates input structures, types, and parameter boundaries, returning structured error JSON with non-zero exit code on failure.

## Migration Plan

1. Create `scripts/search_subjects.py` and unit tests in the repository.
2. Create `apis/subjects/subjects_search_GET.xs` configuring authentication, data retrieval, and script invocation.
3. Developer manually synchronizes Xano artifacts to the backend workspace.
4. Rollback strategy: Remove `apis/subjects/subjects_search_GET.xs`. All existing subject endpoints remain completely intact.

## Open Questions

*(None — all functional requirements, security boundaries, and architectural contracts are defined.)*
