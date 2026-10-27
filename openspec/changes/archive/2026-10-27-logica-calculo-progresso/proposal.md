# Proposal

## Why

EduTrack AI requires a standardized, standalone calculation utility to determine academic progress percentages based on task completion numbers. Having a dedicated, dependency-free Python script ensures that progress calculations are consistent, reusable across automated backend processes or batch jobs, and protected against division-by-zero errors when no tasks exist.

## What Changes

- Introduce a pure Python script at `scripts/calculate_progress.py` without external dependencies.
- Implement progress percentage calculation based on the count of completed tasks and the total count of tasks.
- Format and return output as a JSON object containing the `percentage` key.
- Gracefully handle cases where the total task count is zero by returning 0 instead of triggering a division-by-zero error.

## Capabilities

### New Capabilities
- `progress-calculation`: Provides a standalone script and logic to calculate academic progress percentage from completed and total task counts, returning JSON output with zero-division safety.

### Modified Capabilities
*(None — no existing spec-level behavior changes.)*

## Impact

- **Affected code**: Adds `scripts/calculate_progress.py`.
- **Dependencies**: Python standard library only (no external dependencies).
- **APIs and Database**: No changes to Xano tables, endpoints, functions, or frontend UI.

## Non-goals

- Creation of any REST API endpoints or Xano API groups for this logic is out of scope.
- Database schema changes, table creation, or queries are out of scope.
- Integration or modifications to the `web/` application or FlutterFlow UI are out of scope.
- Inclusion of third-party libraries (e.g., NumPy, Pandas) is out of scope.
