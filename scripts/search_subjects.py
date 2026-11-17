#!/usr/bin/env python3
"""Search subjects by name or overdue tasks."""

import argparse
import json
import sys
from datetime import datetime
from typing import Any, Dict, List


COMPLETED_STATUSES = {
    "completed",
    "done",
    "concluida",
    "concluída",
    "concluido",
    "concluído",
    "finished",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Hybrid search for subjects."
    )
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="Case-insensitive subject name search.",
    )
    parser.add_argument(
        "-o",
        "--has_overdue",
        action="store_true",
        help="Include subjects with overdue tasks.",
    )
    parser.add_argument(
        "-r",
        "--reference_date",
        type=str,
        help="Reference date in ISO format (YYYY-MM-DD).",
    )
    return parser.parse_args()


def load_payload() -> Dict[str, Any]:
    try:
        data = json.load(sys.stdin)

        if (
            not isinstance(data, dict)
            or "subjects" not in data
            or "tasks" not in data
        ):
            raise ValueError(
                "Payload must contain 'subjects' and 'tasks' keys."
            )

        return data

    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON payload: {error}")


def is_overdue(
    task: Dict[str, Any],
    ref_date: datetime,
) -> bool:
    due_str = task.get("due_date")
    status = str(task.get("status", "")).strip().lower()

    if not due_str:
        return False

    try:
        due_date = datetime.fromisoformat(str(due_str))
    except ValueError:
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

    # Treat an empty query as no name filter.
    normalized_query = (
        query.strip().lower()
        if query and query.strip()
        else None
    )

    # Find subjects that have overdue tasks.
    overdue_subject_ids = set()

    if has_overdue:
        for task in tasks:
            if is_overdue(task, ref_date):
                subject_id = task.get("subject_id")

                if subject_id is not None:
                    overdue_subject_ids.add(subject_id)

    result = []

    for subject in subjects:
        name = str(subject.get("name", "")).lower()

        match_name = (
            normalized_query is not None
            and normalized_query in name
        )

        match_overdue = (
            has_overdue
            and subject.get("id") in overdue_subject_ids
        )

        # Return subjects matching the name OR overdue condition.
        if match_name or match_overdue:
            result.append(subject)

    return result


def main() -> None:
    args = parse_args()

    if (
        not (args.query and args.query.strip())
        and not args.has_overdue
    ):
        print(json.dumps({
            "error": (
                "At least one of --query or --has_overdue "
                "must be provided."
            )
        }))
        sys.exit(1)

    try:
        payload = load_payload()
    except ValueError as error:
        print(json.dumps({"error": str(error)}))
        sys.exit(1)

    subjects = payload.get("subjects", [])
    tasks = payload.get("tasks", [])

    ref_date = datetime.utcnow()

    if args.reference_date:
        try:
            ref_date = datetime.fromisoformat(args.reference_date)
        except ValueError:
            print(json.dumps({
                "error": "Invalid reference_date format. Use ISO YYYY-MM-DD."
            }))
            sys.exit(1)

    filtered = filter_subjects(
        subjects,
        tasks,
        args.query,
        args.has_overdue,
        ref_date,
    )

    print(json.dumps(
        {"subjects": filtered},
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()