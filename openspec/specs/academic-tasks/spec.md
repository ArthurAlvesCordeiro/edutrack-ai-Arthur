# academic-tasks Specification

## Purpose
Enables the structured tracking of coursework tasks, assignments, and deadlines linked to academic subjects in EduTrack AI.

## Requirements

### Requirement: Academic tasks table schema

The system SHALL provide an `academic_tasks` database table to store academic tasks associated with subjects, containing the following fields: `id` (integer, auto-increment primary key), `title` (text), `description` (text), `due_date` (date), `status` (text), and `subject_id` (integer foreign key referencing the `subjects` table).

#### Scenario: Persist academic task with valid fields

- **WHEN** a record is created in `academic_tasks` with valid `title`, `description`, `due_date`, `status`, and `subject_id`
- **THEN** the system persists the record with a unique `id` and maintains all field values

#### Scenario: Enforce subject relationship

- **WHEN** a task record is created in `academic_tasks`
- **THEN** the `subject_id` field MUST reference an existing subject in the `subjects` table
