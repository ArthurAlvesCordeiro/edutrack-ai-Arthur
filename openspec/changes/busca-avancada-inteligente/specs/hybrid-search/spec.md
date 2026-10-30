# Spec Delta

## Purpose

Enables advanced hybrid search capabilities across academic subjects and their associated tasks in EduTrack AI, allowing students to filter subjects by name or by the presence of overdue academic tasks while strictly enforcing user authentication and data isolation.

## ADDED Requirements

### Requirement: Advanced Hybrid Search Endpoint

The system SHALL provide an authenticated REST API endpoint `GET /subjects/search` that allows students to find subjects by name and/or filter subjects that contain overdue academic tasks. The endpoint MUST:
- Require a valid authentication token (`authToken`) in the request header (`auth = "user"`).
- Accept the following query parameters:
  - `q` (text, optional): Search term to match against subject names.
  - `has_overdue` (boolean, optional): Flag indicating whether to filter for subjects with overdue tasks.
  - `reference_date` (text/date, optional): Reference date for overdue evaluation (defaults to current date).
- Validate that at least one search filter parameter (`q` or `has_overdue`) is provided, returning HTTP `400 Bad Request` if neither is provided.
- Enforce strict user isolation by scoping database queries for subjects and academic tasks exclusively to the authenticated user's `user_id`.
- Combine search filters with disjunctive (OR) logic when both `q` and `has_overdue=true` are provided: a subject is returned if its name matches `q` OR if it has at least one overdue task.
- Return HTTP `200 OK` with a JSON array of matching subjects on success.
- Return HTTP `401 Unauthorized` if the request lacks valid authentication.

#### Scenario: Search subjects by name substring
- **WHEN** an authenticated user sends `GET /subjects/search?q=Matematica`
- **THEN** the system returns HTTP `200 OK` containing only subjects owned by that user whose `name` field contains "Matematica" (case-insensitive)

#### Scenario: Filter subjects with overdue tasks
- **WHEN** an authenticated user sends `GET /subjects/search?has_overdue=true`
- **THEN** the system returns HTTP `200 OK` containing only subjects owned by that user that have at least one academic task with a `due_date` prior to the current date and an uncompleted status

#### Scenario: Combined search by name OR overdue tasks
- **WHEN** an authenticated user sends `GET /subjects/search?q=Historia&has_overdue=true`
- **THEN** the system returns HTTP `200 OK` containing subjects owned by that user whose name contains "Historia" OR that have one or more overdue academic tasks

#### Scenario: Reject request without search parameters
- **WHEN** an authenticated user sends `GET /subjects/search` without providing `q` or `has_overdue`
- **THEN** the system returns HTTP `400 Bad Request` with an error message stating that at least one search parameter must be specified

#### Scenario: Reject unauthenticated request
- **WHEN** a request is sent to `GET /subjects/search` without a valid authentication token
- **THEN** the system returns HTTP `401 Unauthorized` and does not query student records

#### Scenario: Enforce user data isolation
- **WHEN** an authenticated user executes a search query
- **THEN** the system only queries and returns subjects and tasks where `user_id` matches the authenticated user ID, never exposing data belonging to other students

### Requirement: Python Search and Overdue Evaluation Script

The system SHALL provide a standalone Python evaluation script `scripts/search_subjects.py` that processes subjects and academic tasks to filter matching records based on name search and overdue task detection. The script MUST:
- Accept input parameters via command-line arguments and structured JSON input containing `subjects`, `tasks`, `query`, `has_overdue`, and optional `reference_date`.
- Perform case-insensitive substring matching against subject names.
- Evaluate academic tasks as overdue when `due_date` is strictly earlier than `reference_date` and `status` is not completed.
- Map overdue tasks to their corresponding `subject_id` to flag subjects with overdue work.
- Apply disjunctive (OR) filtering logic when both `query` and `has_overdue=true` are active.
- Output deterministic JSON to standard output containing the filtered list of subjects and summary metadata.
- Terminate with exit code 0 on successful evaluation, or exit code 1 with structured JSON error output on invalid inputs or malformed payloads.

#### Scenario: Execute search with name query
- **WHEN** the script is executed with subject records and a `query` parameter
- **THEN** the script outputs a JSON object containing all subjects whose name matches the query regardless of case

#### Scenario: Identify subjects with overdue tasks
- **WHEN** the script is executed with `has_overdue=true`, a reference date, and tasks having due dates before that reference date with pending status
- **THEN** the script outputs a JSON object containing the subjects linked to those overdue tasks

#### Scenario: Evaluate disjunctive OR filter
- **WHEN** the script is executed with both `query` and `has_overdue=true`
- **THEN** the script outputs subjects that match the query by name OR possess at least one overdue task

#### Scenario: Handle empty subject or task collections
- **WHEN** the script is executed with an empty list of subjects or tasks
- **THEN** the script completes with exit code 0 and outputs an empty subjects list in its JSON response

#### Scenario: Handle invalid input payload
- **WHEN** the script is executed with malformed JSON or invalid parameter types
- **THEN** the script writes an error message and terminates with exit code 1
