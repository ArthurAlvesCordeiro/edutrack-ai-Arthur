
import unittest
from io import BytesIO

from pypdf import PdfReader
from scripts.generate_performance_pdf import build_pdf


class TestGeneratePerformancePDF(unittest.TestCase):

    def _pdf_text(self, pdf_bytes: bytes) -> str:
        # Extrai o texto do PDF usando pypdf
        reader = PdfReader(BytesIO(pdf_bytes))

        # Junta o texto de todas as páginas
        text = "".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        return text

    def test_full_payload(self):
        payload = {
            "student_name": "Alice Example",
            "subjects": [
                {"id": 1, "name": "Math", "hours": 5},
                {"id": 2, "name": "History", "hours": 3},
            ],
            "tasks": [
                {"id": 101, "status": "completed"},
                {"id": 102, "status": "pending"},
                {"id": 103, "status": "overdue"},
                {"id": 104, "status": "completed"},
            ],
        }

        pdf = build_pdf(payload)

        self.assertTrue(pdf.startswith(b"%PDF"))

        txt = self._pdf_text(pdf)

        self.assertIn("Alice Example", txt)
        self.assertIn("Math", txt)
        self.assertIn("History", txt)
        self.assertIn("Horas", txt)
        self.assertIn("Total de tarefas: 4", txt)
        self.assertIn("Concluídas: 2", txt)
        self.assertIn("Progresso Geral", txt)
        self.assertIn("50.0%", txt)

    def test_no_subjects_or_tasks(self):
        payload = {
            "student_name": "Bob NoData"
        }

        pdf = build_pdf(payload)

        self.assertTrue(pdf.startswith(b"%PDF"))

        txt = self._pdf_text(pdf)

        self.assertIn("Bob NoData", txt)
        self.assertIn("Nenhuma disciplina cadastrada.", txt)
        self.assertIn("Total de tarefas: 0", txt)
        self.assertIn("Progresso Geral", txt)
        self.assertIn("0.0%", txt)

    def test_missing_hours_field(self):
        payload = {
            "student_name": "Cara Example",
            "subjects": [
                {"id": 10, "name": "Science"},
                {"id": 11, "name": "Art"},
            ],
            "tasks": [
                {"id": 201, "status": "completed"}
            ],
        }

        pdf = build_pdf(payload)

        self.assertTrue(pdf.startswith(b"%PDF"))

        txt = self._pdf_text(pdf)

        self.assertIn("Cara Example", txt)
        self.assertIn("Science", txt)
        self.assertIn("Art", txt)
        self.assertNotIn("Horas", txt)


if __name__ == "__main__":
    unittest.main()
