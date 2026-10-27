# Proposal

## Why

EduTrack AI currently lacks a dedicated data structure to organize academic tasks, assignments, and deadlines for students. Introducing the `academic_tasks` table enables structured tracking of coursework tasks directly linked to specific subjects.

## What Changes

- Create the `academic_tasks` table schema in XanoScript to store task details and deadlines.
- Establish a foreign key relationship linking `academic_tasks.subject_id` to the `subjects` table.

## Capabilities

### New Capabilities

- `academic-tasks`: Introduces the data model and schema definition for academic tasks linked to subjects.

### Modified Capabilities

*(None — no existing spec-level behavior changes.)*

## Impact

- **Database**: New table definition `tables/academic_tasks.xs` with fields `id`, `title`, `description`, `due_date`, `status`, and `subject_id`.
- **Existing tables**: No changes to `subjects`, `user`, or `event_log`.
- **APIs**: No API endpoints created in this change.
- **Frontend / web/**: No changes to `web/` or FlutterFlow.

## Non-goals

- API endpoints (CRUD operations) for `academic_tasks` are out of scope for this change.
- Automated reminders, notification schedulers, or background tasks are out of scope.
- Frontend UI components or FlutterFlow screen implementations are out of scope.
