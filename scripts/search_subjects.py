#!/usr/bin/env python3
"""Search subjects with optional name query and overdue task filter.

The script reads a JSON payload from standard input with the following structure:
{
  "subjects": [{"id": int, "name": str, ...}],
  "tasks": [{"id": int, "subject_id": int, "due_date": "YYYY-MM-DD", "status": str, ...}]
}

Command line arguments:
  -q, --query TEXT          case‑insensitive substring to match against subject name.
  -o, --has_overdue         flag to include subjects that have at least one overdue task.
  -r, --reference_date DATE reference date for overdue evaluation (ISO format, defaults to today).

At least one of --query or --has_overdue must be provided.
The script outputs a JSON object to stdout with the filtered list of subjects:
{"subjects": [...]}.
On error it prints a JSON error object to stdout and exits with code 1.
"""
import argparse
import json
import sys
from datetime import datetime
from typing import List, Dict, Any

COMPLETED_STATUSES = {"completed", "done", "concluída", "concluido", "finished"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hybrid search for subjects.")
    parser.add_argument("-q", "--query", type=str, help="Case‑insensitive substring to match subject name.")
    parser.add_argument("-o", "--has_overdue", action="store_true", help="Include subjects with overdue tasks.")
    parser.add_argument(
        "-r",
        "--reference_date",
        type=str,
        help="Reference date ISO (YYYY‑MM‑DD). Defaults to today.",
    )
    return parser.parse_args()


def load_payload() -> Dict[str, List[Dict[str, Any]]]:
    try:
        data = json.load(sys.stdin)
        if not isinstance(data, dict) or "subjects" not in data or "tasks" not in data:
            raise ValueError("Payload must contain 'subjects' and 'tasks' keys.")
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON payload: {e}")


def is_overdue(task: Dict[str, Any], ref_date: datetime) -> bool:
    due_str = task.get("due_date")
    status = str(task.get("status", "")).lower()
    if not due_str:
        return False
    try:
        due_date = datetime.fromisoformat(due_str)
    except ValueError:
        # If parsing fails, treat as not overdue
        return False
    if status in COMPLETED_STATUSES:
        return False
    return due_date < ref_date


def filter_subjects(
    subjects: List[Dict[str, Any]],
    tasks: List[Dict[str, Any]],
    query: str | None,
    has_overdue: bool,
    ref_date: datetime,
) -> List[Dict[str, Any]]:
    # Build set of subject ids that have overdue tasks
    overdue_subject_ids = set()
    if has_overdue:
        for task in tasks:
            if is_overdue(task, ref_date):
                sid = task.get("subject_id")
                if sid is not None:
                    overdue_subject_ids.add(sid)
    result = []
    for subj in subjects:
        name = str(subj.get("name", "")).lower()
        match_name = query is not None and query.lower() in name
        match_overdue = has_overdue and subj.get("id") in overdue_subject_ids
        if (query is not None and has_overdue):
            if match_name or match_overdue:
                result.append(subj)
        elif query is not None:
            if match_name:
                result.append(subj)
        elif has_overdue:
            if match_overdue:
                result.append(subj)
    return result


def main() -> None:
    args = parse_args()
    if not args.query and not args.has_overdue:
        err = {"error": "At least one of --query or --has_overdue must be provided."}
        print(json.dumps(err))
        sys.exit(1)
    try:
        payload = load_payload()
    except ValueError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    subjects = payload.get("subjects", [])
    tasks = payload.get("tasks", [])
    ref_date = datetime.utcnow()
    if args.reference_date:
        try:
            ref_date = datetime.fromisoformat(args.reference_date)
        except ValueError:
            print(json.dumps({"error": "Invalid reference_date format. Use ISO YYYY-MM-DD."}))
            sys.exit(1)
    filtered = filter_subjects(
        subjects, tasks, args.query, args.has_overdue, ref_date
    )
    print(json.dumps({"subjects": filtered}, ensure_ascii=False))


if __name__ == "__main__":
    main()
