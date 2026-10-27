# Design

## Context

See proposal.md — Why for motivation. EduTrack AI uses Xano as its backend database, with table schemas defined locally in XanoScript (`.xs`) files under `tables/`. The `subjects` table is already established in `tables/subjects.xs`. This change creates the `academic_tasks` table schema to store tasks associated with subjects.

## Goals / Non-Goals

**Goals:**

- Define the `academic_tasks` table schema in XanoScript (`tables/academic_tasks.xs`) with fields `id`, `title`, `description`, `due_date`, `status`, and `subject_id`.
- Establish the foreign key reference from `academic_tasks.subject_id` to `subjects`.
- Add primary index on `id` and btree index on `subject_id` for efficient query performance.
- Update data dictionary documentation in `docs/dicionario_de_dados.md`.

**Non-Goals:**

- Creation of API endpoints (GET, POST, PATCH, DELETE) for `academic_tasks`.
- Modifications to existing table schemas (`user`, `subjects`, `event_log`).
- Frontend screen development or FlutterFlow integration.

## Decisions

**Decision 1 — Schema structure and field types**

The table schema uses:
- `int id`: Primary key (auto-increment).
- `text title filters=trim`: Title of the academic task.
- `text description`: Detailed task description.
- `date due_date`: Date when the task is due.
- `text status filters=trim`: Task progress status (e.g., pending, in_progress, completed).
- `int subject_id { table = "subjects" }`: Foreign key reference to `subjects`.

*Alternative considered*: Defining `status` as an enum. Rejected for now to maintain flexibility across evolving academic task workflows until API endpoints standardize status values.

**Decision 2 — Indexing strategy**

Configure a primary index on `id` and a btree index on `subject_id`. Queries for tasks will typically filter by subject, making a btree index on `subject_id` essential for performance.

*Alternative considered*: Only a primary key index on `id`. Rejected because lookups by subject would require full table scans.

**Decision 3 — Manual synchronization to Xano**

In compliance with project rules in `AGENTS.md`, AI agents do not automatically push schema definitions to Xano. The file will be created locally for the developer to sync manually.

## Risks / Trade-offs

- **Orphaned records on subject deletion** → Without explicit cascade handling, deleting a subject could leave orphaned tasks. Mitigation: When CRUD APIs are introduced in future changes, subject deletion logic must check for or clean up related academic tasks.

## Migration Plan

1. Create `tables/academic_tasks.xs` with schema and indexes.
2. Update `docs/dicionario_de_dados.md` to include `academic_tasks`.
3. Developer manually reviews and syncs the new table in the Xano workspace.
