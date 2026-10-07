# Spec Delta

## Purpose

Gerencia a modelagem e o armazenamento das disciplinas acadêmicas vinculadas aos estudantes no EduTrack AI.

## ADDED Requirements

### Requirement: Subjects Table Schema
The system SHALL provide a `subjects` database table to store academic courses and subjects with fields: `id` (auto integer primary key), `name` (text), `teacher` (text), `hours` (integer), and `user_id` (foreign key referencing the `user` table).

#### Scenario: Criar disciplina com campos válidos
- **WHEN** uma disciplina é criada com id auto-gerado, name, teacher, hours e user_id válido
- **THEN** o registro é salvo com sucesso e relacionado ao usuário correspondente
