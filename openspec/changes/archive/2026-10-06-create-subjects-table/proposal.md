# Proposal

## Why

O EduTrack AI necessita armazenar e gerenciar as disciplinas acadêmicas dos estudantes para viabilizar o acompanhamento curricular, carga horária e professores responsáveis.

## What Changes

- Criação da tabela `subjects` no banco de dados.
- Definição dos campos `id` (auto-incremento/primary key), `name` (texto), `teacher` (texto), `hours` (inteiro) e `user_id` (foreign key referenciando a tabela `user`).

## Capabilities

### New Capabilities
- `subjects`: Estrutura de dados e persistência para disciplinas acadêmicas no EduTrack AI.

### Modified Capabilities

## Impact

- Criação do modelo/tabela `tables/subjects.xs`.
- Relacionamento de chave estrangeira com a tabela `user`.
