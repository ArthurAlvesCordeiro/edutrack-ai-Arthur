"""
Progress calculation script for EduTrack AI.

Calculates the percentage of completed academic tasks relative to the total number
of tasks, returning the result in JSON format with division-by-zero protection.
"""

from __future__ import annotations

import argparse
import json
import sys


def calculate_progress(completed: int, total: int) -> float | int:
    """
    Calculate progress percentage based on completed and total tasks.

    Args:
        completed: Number of completed tasks (non-negative integer).
        total: Total number of tasks (non-negative integer).

    Returns:
        Progress percentage as an integer (0) or float rounded to 2 decimal places.

    Raises:
        TypeError: If completed or total are not integers.
        ValueError: If completed or total are negative, or completed > total.
    """
    if not isinstance(completed, int) or not isinstance(total, int) or isinstance(completed, bool) or isinstance(total, bool):
        raise TypeError("Completed and total task counts must be integers.")

    if completed < 0 or total < 0:
        raise ValueError("Completed and total tasks must be non-negative integers.")

    if total == 0:
        if completed > 0:
            raise ValueError("Completed tasks cannot exceed total tasks.")
        return 0

    if completed > total:
        raise ValueError("Completed tasks cannot exceed total tasks.")

    percentage = (completed / total) * 100.0
    return round(percentage, 2)


def parse_arguments(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments supporting flags and positional parameters."""
    parser = argparse.ArgumentParser(
        description="Calculate academic task progress percentage."
    )
    parser.add_argument(
        "pos_completed",
        nargs="?",
        type=int,
        default=None,
        help="Number of completed tasks (positional)",
    )
    parser.add_argument(
        "pos_total",
        nargs="?",
        type=int,
        default=None,
        help="Total number of tasks (positional)",
    )
    parser.add_argument(
        "--completed",
        "-c",
        type=int,
        default=None,
        help="Number of completed tasks",
    )
    parser.add_argument(
        "--total",
        "-t",
        type=int,
        default=None,
        help="Total number of tasks",
    )
    return parser.parse_args(args)


def main(cli_args: list[str] | None = None) -> None:
    """Main CLI entry point."""
    args = parse_arguments(cli_args)

    completed = args.completed if args.completed is not None else args.pos_completed
    total = args.total if args.total is not None else args.pos_total

    if completed is None or total is None:
        error_msg = "Both completed and total task counts must be provided."
        sys.stderr.write(f"Error: {error_msg}\n")
        print(json.dumps({"error": error_msg}))
        sys.exit(1)

    try:
        percentage = calculate_progress(completed, total)
        print(json.dumps({"percentage": percentage}))
    except (ValueError, TypeError) as err:
        sys.stderr.write(f"Error: {err}\n")
        print(json.dumps({"error": str(err)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
