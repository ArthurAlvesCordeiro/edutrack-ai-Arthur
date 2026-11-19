
import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

# Import the FastAPI app defined in the service module
from services.search_api.main import app

# API key used only in PDF tests
TEST_API_KEY = "test-secret"


class GeneratePDFTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Save the previous API key
        cls.previous_api_key = os.environ.get("SEARCH_API_KEY")

        # Set a temporary API key for PDF tests
        cls.api_key_patcher = patch.dict(
            os.environ,
            {"SEARCH_API_KEY": TEST_API_KEY}
        )
        cls.api_key_patcher.start()

        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Restore the previous API key
        cls.api_key_patcher.stop()

    def test_successful_pdf_generation(self):
        payload = {
            "student_name": "Alice Example",
            "subjects": [
                {"id": 1, "name": "Math", "hours": 5}
            ],
            "tasks": [
                {"id": 101, "status": "completed"}
            ],
        }

        with patch(
            "services.search_api.main.build_pdf",
            return_value=b"%PDF-1.4\n...binary..."
        ):
            response = self.client.post(
                "/generate-pdf",
                json=payload,
                headers={"X-API-Key": TEST_API_KEY},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("content-type"),
            "application/pdf"
        )
        self.assertTrue(response.content.startswith(b"%PDF"))

    def test_empty_subjects_and_tasks(self):
        payload = {
            "student_name": "Bob NoData",
            "subjects": [],
            "tasks": [],
        }

        with patch(
            "services.search_api.main.build_pdf",
            return_value=b"%PDF-1.4\n...binary..."
        ):
            response = self.client.post(
                "/generate-pdf",
                json=payload,
                headers={"X-API-Key": TEST_API_KEY},
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b"%PDF"))

    def test_missing_api_key(self):
        payload = {
            "student_name": "Charlie",
            "subjects": [],
            "tasks": [],
        }

        response = self.client.post(
            "/generate-pdf",
            json=payload
        )

        self.assertEqual(response.status_code, 401)

    def test_invalid_api_key(self):
        payload = {
            "student_name": "Charlie",
            "subjects": [],
            "tasks": [],
        }

        response = self.client.post(
            "/generate-pdf",
            json=payload,
            headers={"X-API-Key": "wrong-key"},
        )

        self.assertEqual(response.status_code, 401)

    def test_missing_student_identifier(self):
        payload = {
            "subjects": [],
            "tasks": [],
        }

        response = self.client.post(
            "/generate-pdf",
            json=payload,
            headers={"X-API-Key": TEST_API_KEY},
        )

        self.assertEqual(response.status_code, 422)

    def test_pdf_generation_failure(self):
        payload = {
            "student_name": "Dave",
            "subjects": [],
            "tasks": [],
        }

        with patch(
            "services.search_api.main.build_pdf",
            side_effect=Exception("generation error")
        ):
            response = self.client.post(
                "/generate-pdf",
                json=payload,
                headers={"X-API-Key": TEST_API_KEY},
            )

        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
