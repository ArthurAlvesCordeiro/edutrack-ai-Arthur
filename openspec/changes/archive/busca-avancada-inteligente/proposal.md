# Proposal

## Why

Students and educators using EduTrack AI need an efficient way to locate academic subjects not only by name but also by urgent academic priorities, specifically identifying subjects with overdue assignments or coursework. Currently, subjects can only be listed in bulk or retrieved by ID, requiring manual inspection of each subject's individual tasks to detect overdue work. A hybrid search endpoint combining Xano's secure data storage and authentication with Python's evaluation logic provides a responsive, priority-driven search capability that helps students stay on top of their academic commitments.

## What Changes

- Add a new authenticated REST API endpoint `GET /subjects/search` in the Subjects API group to search subjects by name or filter by the presence of overdue tasks.
- Create a standalone Python evaluation script `scripts/search_subjects.py` to perform case-insensitive name matching, overdue task identification based on due dates and status, and disjunctive (OR) filter combination.
- Connect Xano data retrieval (scoped to the authenticated student's `user_id`) with the Python search logic, ensuring strict data isolation and standard error handling.

## Capabilities

### New Capabilities

- `hybrid-search`: Provides advanced hybrid search and filtering across subjects and academic tasks by combining Xano data extraction and Python evaluation logic.

### Modified Capabilities

*(None — existing CRUD endpoints and schemas remain intact.)*

## Impact

- **APIs**: New endpoint `GET /subjects/search` in `apis/subjects/` protected by `authToken` middleware (`auth = "user"`).
- **Scripts**: New script `scripts/search_subjects.py` for search and overdue task evaluation.
- **Database**: Queries existing `subjects` and `academic_tasks` tables scoped by `user_id`. No table schema modifications required.
- **Frontend / web/**: No changes to `web/` in this change.

## Non-goals

- Modifying existing CRUD endpoints (`GET /subjects`, `POST /subjects`, `PATCH /subjects/{id}`, `DELETE /subjects/{id}`) is out of scope.
- Integration of external third-party search engines (e.g., Elasticsearch, Meilisearch) is out of scope.
- Automatic task status updates, grade calculations, or deadline modifications are out of scope.
- Modifications to the `web/` directory or FlutterFlow frontend are out of scope for this change.
