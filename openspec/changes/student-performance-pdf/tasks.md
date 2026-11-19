- [x] 1.1 Implement Python PDF generator (`scripts/generate_performance_pdf.py`) using ReportLab to create student‑performance PDFs.
  - **Verification Criteria:** Unit tests validate PDF structure, content, and successful generation.

- [x] 1.2 Write unit tests for the PDF builder (`scripts/test_generate_performance_pdf.py`).
  - **Verification Criteria:** Tests cover successful PDF creation, content correctness, and error handling.

- [x] 1.3 Add FastAPI endpoint **POST `/generate-pdf`** in `services/search_api/main.py`.
  - **Requirements:** Require `X‑API‑Key` header, invoke `build_pdf`, return raw PDF bytes with `Content‑Type: application/pdf`.
  - **Verification Criteria:** Endpoint returns PDF bytes, enforces API‑key authentication, and returns appropriate error codes (401, 500, etc.).

- [x] 1.4 Create FastAPI HTTP tests (`services/search_api/test_generate_pdf.py`).
  - **Verification Criteria:** Tests verify HTTP 200 on success and proper error responses for missing/invalid API key, malformed payload, and internal failures.

- [x] 1.5 Update Dockerfile and requirements.
  - **Requirements:** Keep existing Dockerfile (`services/search_api/Dockerfile`) configuration (Python 3.12, non‑privileged `appuser`, dynamic port `${PORT:-8000}`, build context at repo root). Add `reportlab==4.2.0` to `services/search_api/requirements.txt` and copy `scripts/generate_performance_pdf.py` to `/app/scripts/` with `--chown=appuser:appuser`.
  - **Verification Criteria:** `docker build -f services/search_api/Dockerfile -t edutrack-pdf .` succeeds and the container starts without missing dependencies.

- [ ] 1.6 Verify Xano data structures.
  - **Tasks:** Identify the exact name of the user table and confirm required fields; confirm `reports` table has `Attachment` (File Resource) and `owner_id`; verify `subjects.hours`, `academic_tasks.status`, and relation `academic_tasks.subject_id → subjects.id`; check File Resource and Base64 storage limits; confirm binary format required by FastAPI `/generate-pdf`; ensure Attachment Metadata creation and Signed URL generation are supported.
  - **Verification Criteria:** Manual inspection in Xano workspace confirms each item.

- [ ] 1.7 Document Xano endpoints (no FastAPI description).
  - **POST `/reports/generate`** – Xano forwards payload to FastAPI (`PDF_API_URL` ending in `/generate-pdf`) and stores the PDF according to the selected storage strategy.
  - **GET `/reports/{report_id}/download`** – Protected endpoint that validates `$auth.id` against the report owner and returns either a temporary signed URL (File Resource) or the Base64 PDF.
  - **Verification Criteria:** Endpoints enforce authentication, ownership checks, and return `application/pdf` (or signed URL) as appropriate.

- [ ] 1.8 Security review.
  - **File Resource:** Signed URL temporary; anyone with the link can download while valid. Ownership is verified only when the URL is issued.
  - **Base64:** Protected download endpoint checks `owner_id` before returning the PDF binary.
  - **Verification Criteria:** Security review sign‑off confirming the above behavior.

- [ ] 1.9 FlutterFlow integration test.
  - **Task:** Manually request a performance report from the FlutterFlow app using an authenticated token, handle both storage strategies, and display the PDF.
  - **Verification Criteria:** End‑to‑end flow completes without errors and the PDF renders correctly.

- [ ] 1.10 Final validation and OpenSpec archival.
  - **Steps:**
    1. Run `openspec.cmd validate student-performance-pdf --strict`.
    2. Execute `git diff --check`.
    3. Run all Python unit tests and FastAPI HTTP tests.
    4. Build Docker image with `docker build -f services/search_api/Dockerfile -t edutrack-pdf .`.
    5. Generate a real PDF via the full workflow and open it in a PDF reader.
    6. Provide the GitHub URL of `scripts/generate_performance_pdf.py`.
    7. Test the full integration Xano → Render (FastAPI) → download.
    8. **Archive the OpenSpec change** (only after all prior steps succeed) using:
       ```
       openspec.cmd archive student-performance-pdf
       ```
  - **Verification Criteria:** All validation commands succeed, the PDF is viewable, the GitHub link is correct, the integration test passes, and the archive command completes successfully.
