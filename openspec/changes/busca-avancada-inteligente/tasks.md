# Tasks

## 1. Python Search and Overdue Evaluation Script

- [x] 1.1 Create `scripts/search_subjects.py` with argument parsing and JSON payload ingestion, verifying with `python scripts/search_subjects.py --help`
- [x] 1.2 Implement subject name matching logic (case-insensitive substring) and verify with test executions using matching and non-matching names
- [ ] 1.3 Implement overdue task detection based on `due_date` and `status`, verifying against sample tasks with past, current, and future due dates
- [ ] 1.4 Implement disjunctive (OR) filter logic combining name matching and overdue checks, verifying that subjects meeting either criterion are returned
- [ ] 1.5 Add automated unit tests for `scripts/search_subjects.py` covering all filter scenarios, edge cases (empty lists, invalid inputs), and error handling, verifying with `python -m unittest`

## 2. Xano Advanced Search Endpoint Definition

- [ ] 2.1 Create the endpoint definition `apis/subjects/subjects_search_GET.xs` for `GET /subjects/search` with parameters `q`, `has_overdue`, and `reference_date`, protected by `auth = "user"`, verifying file syntax
- [ ] 2.2 Add database queries in `subjects_search_GET.xs` to fetch subjects and associated tasks scoped strictly to `$auth.id`, verifying user isolation logic
- [ ] 2.3 Implement the execution step in the endpoint stack to invoke the Python search logic with user records and search parameters, verifying response formatting
- [ ] 2.4 Add input validation and error responses for requests lacking search criteria (HTTP 400) and unauthenticated calls (HTTP 401), verifying response codes

## 3. Integration Verification and Documentation

- [ ] 3.1 Execute end-to-end verification passing simulated Xano payloads to `scripts/search_subjects.py` for name-only, overdue-only, and combined OR searches, verifying expected JSON outputs
- [ ] 3.2 Verify user isolation test scenario ensuring tasks and subjects belonging to different user IDs are excluded from search results
- [ ] 3.3 Document the advanced search endpoint specification, query parameters, and Python script usage in `docs/` or API documentation, verifying Markdown formatting
