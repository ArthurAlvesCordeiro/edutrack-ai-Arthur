# Proposal

## Why

O EduTrack AI necessita de documentação formal do dicionário de dados de suas entidades e da implementação de endpoints CRUD completos para a tabela `subjects` em XanoScript, permitindo a persistência segura de disciplinas por usuário e a integração com o frontend no FlutterFlow conforme os critérios de avaliação acadêmica.

## What Changes

- Criação da documentação formal de Dicionário de Dados em `docs/dicionario_de_dados.md` contemplando todas as tabelas, campos, tipos, índices e relacionamentos (`user`, `event_log` e `subjects`).
- Criação do grupo de APIs `Subjects` em `apis/subjects/api_group.xs`.
- Implementação dos endpoints CRUD em XanoScript:
  - `GET /subjects`: Listagem das disciplinas pertencentes ao usuário autenticado.
  - `GET /subjects/{subjects_id}`: Obtenção de detalhes de uma disciplina por ID com validação de posse do usuário.
  - `POST /subjects`: Cadastro de nova disciplina vinculada ao usuário autenticado (`name`, `teacher`, `hours`).
  - `PATCH /subjects/{subjects_id}`: Atualização dos dados de uma disciplina existente.
  - `DELETE /subjects/{subjects_id}`: Exclusão de disciplina pertencente ao usuário autenticado.

## Capabilities

### New Capabilities

### Modified Capabilities
- `subjects`: Adição de requisitos e cenários para a exposição de endpoints CRUD autenticados da tabela `subjects`.

## Impact

- Criação dos arquivos `.xs` no grupo de APIs `apis/subjects/`.
- Criação do arquivo `docs/dicionario_de_dados.md`.
- Habilitação da integração de chamadas de API no FlutterFlow para gestão de disciplinas.
