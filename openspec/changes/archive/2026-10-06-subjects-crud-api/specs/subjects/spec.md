# Spec Delta

## ADDED Requirements

### Requirement: Subjects CRUD Endpoints
The system SHALL provide authenticated REST API endpoints for full CRUD operations on the `subjects` table, scoped to the authenticated user:
- `GET /subjects`: Returns a list of subjects belonging to the authenticated user.
- `GET /subjects/{subjects_id}`: Returns the subject with the specified ID if owned by the authenticated user, or error otherwise.
- `POST /subjects`: Creates a new subject associated with the authenticated user with fields `name`, `teacher`, and `hours`.
- `PATCH /subjects/{subjects_id}`: Updates name, teacher, and/or hours of an existing subject owned by the authenticated user.
- `DELETE /subjects/{subjects_id}`: Deletes an existing subject owned by the authenticated user.

#### Scenario: List subjects for authenticated user
- **WHEN** an authenticated user sends a GET request to `/subjects`
- **THEN** the system returns only the subjects where `user_id` matches the authenticated user ID

#### Scenario: Create a new subject
- **WHEN** an authenticated user sends a POST request to `/subjects` with `name`, `teacher`, and `hours`
- **THEN** the system persists the record in `subjects` with `user_id` set to the authenticated user ID and returns the created record

#### Scenario: Get subject by ID
- **WHEN** an authenticated user sends a GET request to `/subjects/{subjects_id}` for an existing subject they own
- **THEN** the system returns the subject details

#### Scenario: Update existing subject
- **WHEN** an authenticated user sends a PATCH request to `/subjects/{subjects_id}` with updated fields
- **THEN** the system updates the record and returns the updated subject

#### Scenario: Delete subject
- **WHEN** an authenticated user sends a DELETE request to `/subjects/{subjects_id}` for an existing subject they own
- **THEN** the system removes the record from the database and returns success
