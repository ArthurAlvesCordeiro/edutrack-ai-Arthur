
import unittest
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "search_subjects.py"


class TestSearchSubjects(unittest.TestCase):

    def run_script(self, input_data, args=None):
        args = args or []

        if isinstance(input_data, bytes):
            raw_input = input_data
        elif isinstance(input_data, str):
            raw_input = input_data.encode()
        else:
            raw_input = json.dumps(input_data).encode()

        return subprocess.run(
            [sys.executable, str(SCRIPT)] + args,
            input=raw_input,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_name_query(self):
        data = {
            "subjects": [
                {"id": 1, "name": "Matematica"},
                {"id": 2, "name": "Historia"},
            ],
            "tasks": [],
        }

        proc = self.run_script(data, ["--query", "mat"])

        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertEqual(len(out["subjects"]), 1)
        self.assertEqual(out["subjects"][0]["id"], 1)

    def test_overdue_past_current_future_and_completed(self):
        data = {
            "subjects": [
                {"id": 1, "name": "Matematica"},
                {"id": 2, "name": "Historia"},
                {"id": 3, "name": "Geografia"},
                {"id": 4, "name": "Fisica"},
            ],
            "tasks": [
                {
                    "id": 10,
                    "subject_id": 1,
                    "due_date": "2026-11-07",
                    "status": "pending",
                },
                {
                    "id": 11,
                    "subject_id": 2,
                    "due_date": "2026-11-08",
                    "status": "pending",
                },
                {
                    "id": 12,
                    "subject_id": 3,
                    "due_date": "2026-11-09",
                    "status": "pending",
                },
                {
                    "id": 13,
                    "subject_id": 4,
                    "due_date": "2026-11-07",
                    "status": "completed",
                },
            ],
        }

        proc = self.run_script(
            data,
            ["--has_overdue", "--reference_date", "2026-11-08"],
        )

        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        ids = {s["id"] for s in out["subjects"]}
        self.assertEqual(ids, {1})

    def test_or_combination(self):
        data = {
            "subjects": [
                {"id": 1, "name": "Matematica"},
                {"id": 2, "name": "Historia"},
                {"id": 3, "name": "Geografia"},
            ],
            "tasks": [
                {
                    "id": 20,
                    "subject_id": 3,
                    "due_date": "2026-11-07",
                    "status": "pending",
                }
            ],
        }

        proc = self.run_script(
            data,
            [
                "--query",
                "mat",
                "--has_overdue",
                "--reference_date",
                "2026-11-08",
            ],
        )

        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        ids = {s["id"] for s in out["subjects"]}
        self.assertEqual(ids, {1, 3})

    def test_empty_lists(self):
        data = {"subjects": [], "tasks": []}

        proc = self.run_script(
            data,
            ["--has_overdue", "--reference_date", "2026-11-08"],
        )

        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertEqual(out["subjects"], [])

    def test_empty_query_with_overdue(self):
        data = {
            "subjects": [
                {"id": 1, "name": "Matematica"},
                {"id": 2, "name": "Historia"},
            ],
            "tasks": [
                {
                    "id": 30,
                    "subject_id": 1,
                    "due_date": "2026-11-07",
                    "status": "pending",
                }
            ],
        }

        proc = self.run_script(
            data,
            [
                "--query",
                "",
                "--has_overdue",
                "--reference_date",
                "2026-11-08",
            ],
        )

        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        ids = {s["id"] for s in out["subjects"]}
        self.assertEqual(ids, {1})

    def test_missing_parameters(self):
        data = {"subjects": [], "tasks": []}

        proc = self.run_script(data)

        self.assertNotEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertIn("error", out)

    def test_invalid_payload_missing_key(self):
        data = {"subjects": []}

        proc = self.run_script(data, ["--has_overdue"])

        self.assertNotEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertIn("error", out)

    def test_invalid_json_payload(self):
        proc = self.run_script("{invalid json", ["--has_overdue"])

        self.assertNotEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertIn("error", out)


if __name__ == "__main__":
    unittest.main()
