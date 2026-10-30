import unittest
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "search_subjects.py"

class TestSearchSubjects(unittest.TestCase):
    def run_script(self, input_data, args=None):
        args = args or []
        proc = subprocess.run([sys.executable, str(SCRIPT)] + args,
                               input=json.dumps(input_data).encode(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        return proc

    def test_name_query(self):
        data = {
            "subjects": [
                {"id": 1, "name": "Matematica"},
                {"id": 2, "name": "Historia"},
            ],
            "tasks": []
        }
        proc = self.run_script(data, ["--query", "mat"])
        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertEqual(len(out["subjects"]), 1)
        self.assertEqual(out["subjects"][0]["id"], 1)

    def test_overdue_filter(self):
        data = {
            "subjects": [
                {"id": 1, "name": "Matematica"},
                {"id": 2, "name": "Historia"},
            ],
            "tasks": [
                {"id": 10, "subject_id": 2, "due_date": "2000-01-01", "status": "pending"},
                {"id": 11, "subject_id": 1, "due_date": "2100-01-01", "status": "pending"},
            ]
        }
        proc = self.run_script(data, ["--has_overdue"])
        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertEqual(len(out["subjects"]), 1)
        self.assertEqual(out["subjects"][0]["id"], 2)

    def test_or_combination(self):
        data = {
            "subjects": [
                {"id": 1, "name": "Matematica"},
                {"id": 2, "name": "Historia"},
                {"id": 3, "name": "Geografia"},
            ],
            "tasks": [
                {"id": 20, "subject_id": 3, "due_date": "2000-01-01", "status": "pending"}
            ]
        }
        proc = self.run_script(data, ["--query", "mat", "--has_overdue"])
        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        ids = {s["id"] for s in out["subjects"]}
        self.assertEqual(ids, {1, 3})

    def test_missing_parameters(self):
        data = {"subjects": [], "tasks": []}
        proc = self.run_script(data)
        self.assertNotEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertIn("error", out)

if __name__ == "__main__":
    unittest.main()
