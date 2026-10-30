import unittest
from fastapi.testclient import TestClient
import os

# Ensure the API key is set for the test process.
os.environ["SEARCH_API_KEY"] = "testkey"

from services.search_api.main import app

client = TestClient(app)

class TestSearchAPI(unittest.TestCase):
    def setUp(self):
        self.headers = {"X-API-Key": "testkey"}
        self.base_payload = {
            "subjects": [
                {"id": 1, "name": "Matematica"},
                {"id": 2, "name": "Historia"},
                {"id": 3, "name": "Geografia"},
            ],
            "tasks": [
                {"id": 10, "subject_id": 2, "due_date": "2000-01-01", "status": "pending"},
                {"id": 11, "subject_id": 1, "due_date": "2100-01-01", "status": "pending"},
                {"id": 12, "subject_id": 3, "due_date": "2000-01-01", "status": "pending"},
            ]
        }

    def test_name_query(self):
        payload = dict(self.base_payload)
        payload["query"] = "mat"
        resp = client.post("/search", json=payload, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data["subjects"]), 1)
        self.assertEqual(data["subjects"][0]["id"], 1)

    def test_overdue_filter(self):
        payload = dict(self.base_payload)
        payload["has_overdue"] = True
        resp = client.post("/search", json=payload, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        ids = {s["id"] for s in resp.json()["subjects"]}
        self.assertEqual(ids, {2, 3})  # subjects 2 and 3 have overdue tasks

    def test_or_combination(self):
        payload = dict(self.base_payload)
        payload["query"] = "mat"
        payload["has_overdue"] = True
        resp = client.post("/search", json=payload, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        ids = {s["id"] for s in resp.json()["subjects"]}
        self.assertEqual(ids, {1, 2, 3})

    def test_missing_filters(self):
        payload = {"subjects": [], "tasks": []}
        resp = client.post("/search", json=payload, headers=self.headers)
        self.assertEqual(resp.status_code, 422)  # validation error from Pydantic

    def test_invalid_api_key(self):
        payload = dict(self.base_payload)
        payload["query"] = "mat"
        resp = client.post("/search", json=payload, headers={"X-API-Key": "wrong"})
        self.assertEqual(resp.status_code, 401)

if __name__ == "__main__":
    unittest.main()
