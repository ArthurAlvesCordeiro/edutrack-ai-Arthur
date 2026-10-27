# Design

## Context

EduTrack AI tracks academic activities and tasks. To compute student and subject progress metrics safely and predictably, a standalone calculation utility is required at `scripts/calculate_progress.py`. The utility must run without external third-party dependencies so it can be executed reliably in standard Python environments, automated jobs, or test suites. See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Provide a pure Python 3 script at `scripts/calculate_progress.py`.
- Calculate completion percentage from completed task count and total task count: `(completed / total) * 100`.
- Return output strictly formatted as a JSON object with the `percentage` key (e.g., `{"percentage": 50.0}`).
- Handle zero total tasks gracefully by returning `{"percentage": 0}` (or `0.0`) without raising a `ZeroDivisionError`.
- Use standard library modules (`argparse`, `json`, `sys`) to handle input arguments and output serialization.

**Non-Goals:**
- No external Python dependencies (e.g., requests, numpy, pandas).
- No database connections, Xano endpoints, or table modifications.
- No frontend UI modifications or FlutterFlow integrations.

## Decisions

- **Command-line Interface**: Use `argparse` to accept input parameters `--completed` and `--total`. Provide positional or flag-based inputs with integer type casting.
- **Division-by-Zero Handling**: Perform an explicit validation check `if total == 0: return 0` prior to any division arithmetic.
- **JSON Serialization**: Use `json.dumps()` to print the result directly to standard output, allowing downstream callers to parse the output cleanly.
- **Pure Standard Library**: Restrict all logic to Python standard libraries (`argparse`, `json`, `sys`) ensuring zero setup overhead and portability.

## Risks / Trade-offs

- **[Risk] Float formatting inconsistency across Python versions** → Mitigation: Use standard Python float or numeric formatting with consistent JSON serialization via `json.dumps`.
- **[Risk] Completed count exceeds total count or negative inputs** → Mitigation: Enforce input validation ensuring non-negative values and, if completed exceeds total, cap at 100% or report an error predictably.
