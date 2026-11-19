# Design: Student Performance PDF Report

**Change ID:** `student-performance-pdf`

## 1. High‑Level Architecture

```
+----------------+        +----------------------+        +-------------------+
|   Front‑end    |  -->   |   Xano (API layer)  |  -->   |  FastAPI Service  |
| (FlutterFlow)  |        |   /reports/generate  |        |  (Render)         |
+----------------+        +----------------------+        +-------------------+
                                 |                               |
                                 |   Store PDF (File Resource    |
                                 |   or Base64)                  |
                                 v                               v
                        +----------------------+        +-------------------+
                        |   Xano (reports)    |        |   Xano (pdf_reports)
                        +----------------------+        +-------------------+
```

* The front‑end calls the Xano endpoint **POST `/reports/generate`**.
* Xano collects user‑specific data, forwards it to the FastAPI service, receives the PDF binary, and stores it according to the chosen storage strategy.
* The user obtains a temporary signed URL (File Resource) **or** a protected download URL that points to **GET `/reports/{report_id}/download`**.

## 2. FastAPI Service (Render)

* **Framework:** FastAPI (Python 3.12) running on Render.
* **Endpoint:** `POST /generate-pdf`
* **Authentication:** The request must include the Xano‑provided `X-API-Key` header (`SEARCH_API_KEY`). No user‑level auth is performed inside FastAPI – Xano already validated the user.
* **Payload:** JSON matching the schema defined in `spec.md` (student name, subjects list, tasks breakdown, progress percent).
* **PDF Generation:** Implemented with **ReportLab**.
  * Create a `BytesIO` buffer.
  * Use a simple single‑page layout (tables, headings, no charts).
  * Include:
    - Student name.
    - Table of subjects (id, name, optional hours).
    - Summary of tasks (total, completed, pending, overdue).
    - Progress percentage.
  * Return the PDF bytes with MIME type `application/pdf`.
* **Response:** `{ "pdf": <base64‑encoded‑bytes> }` **or** raw binary with `Content‑Type: application/pdf`. The design assumes the response is raw binary for simplicity; Xano will treat the body as binary.
* **Error handling:** Returns HTTP 502 on any internal error, which propagates back to the Xano caller.

## 3. Integration with Xano

### 3.1 Generate Endpoint (`POST /reports/generate`)
1. **Authentication** – Xano enforces `auth = "user"`.
2. **Data Retrieval** – Xano queries:
   * `subjects` table filtered by `user_id == $auth.id`.
   * `academic_tasks` table joined to the user’s subjects.
3. **Payload Construction** – Assemble the JSON payload exactly as described in the spec (including empty arrays when no data exists).
4. **FastAPI Call** – `api.request` POST to `$env.PDF_API_URL` with the payload and `X-API-Key` header.
5. **PDF Storage** – Depending on the verified Xano capabilities:
   * **File Resource strategy** (preferred):
     - `api.request` to the built‑in **Create File Resource** endpoint, sending the PDF binary.
     - Capture the returned `file_resource_id`.
     - `api.request` **Create Attachment Metadata** linking the file to a new row in the `reports` table (fields: `owner_id`, `file_resource_id`, `created_at`).
   * **Base64 fallback**:
     - Encode the PDF with `base64encode`.
     - Insert a new row into `pdf_reports` table (fields: `owner_id`, `base64_pdf`, `created_at`).
6. **Response to Caller** – Return JSON as defined in the spec (see `spec.md`).

### 3.2 Download Endpoint (`GET /reports/{report_id}/download`)
* **Ownership Check** – Verify `$auth.id == reports.owner_id` (or `pdf_reports.owner_id`).
* **File Resource strategy:**
  - Use **Generate Signed URL** Xano endpoint with the stored `file_resource_id`.
  - Return `{ "url": "<signed‑url>" }`.
* **Base64 fallback:**
  - Retrieve `base64_pdf` from `pdf_reports`.
  - Decode it server‑side and stream the binary PDF with headers:
    ```
    Content-Type: application/pdf
    Content-Disposition: attachment; filename="report.pdf"
    ```

## 4. Storage Strategies – Confirmed vs Pending
| Strategy | Confirmed Decision | Pending Verification |
|----------|--------------------|----------------------|
| **File Resource** (Create File Resource → Create Attachment Metadata) | Preferred; allows temporary signed URLs; minimal storage overhead. | Need to confirm that the current Xano plan supports private File Resources and the `Generate Signed URL` endpoint. |
| **Base64 fallback** (store PDF as Base64 in a table) | Defined as fallback; download endpoint will decode and stream PDF. | Verify that storing large Base64 strings does not breach Xano field size limits and that performance is acceptable. |

All other decisions (authentication, data isolation, PDF content) are fully defined and do not depend on Xano runtime verification.

## 5. Security Considerations
* **Authentication** – All Xano endpoints require a valid user token (`auth = "user"`).
* **Authorization** – Ownership checks (`owner_id == $auth.id`) guard both generate and download endpoints.
* **Signed URL** – Temporary (default Xano expiry, typically 1 hour). Anyone with the URL can download the PDF while it is valid; the URL is not stored permanently.
* **Base64 download** – The binary PDF is streamed only after the ownership check; no public URL is exposed.
* **Environment Variables** – `PDF_API_URL` and `SEARCH_API_KEY` are stored securely in Xano’s environment configuration and never hard‑coded.

## 6. Dockerfile for FastAPI Service (Render)
```Dockerfile
# Use official Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies required by ReportLab
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency file (assume pyproject.toml or requirements.txt exists)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port FastAPI will run on (Render defaults to 8000)
EXPOSE 8000

# Command to run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
*`requirements.txt` must include at least `fastapi`, `uvicorn[standard]`, and `reportlab`.*

## 7. Testing Strategy
### 7.1 Unit Tests (Xano side)
* **API request tests** – Verify that `POST /reports/generate` correctly builds the payload, calls FastAPI, and stores the result for both storage strategies.
* **Ownership checks** – Ensure that unauthenticated or wrong‑user requests receive 401/404.
* **Error propagation** – Simulate FastAPI returning non‑2xx and confirm Xano returns 502.

### 7.2 FastAPI Tests
* **Local test suite** (`scripts/test_generate_pdf.py` using `unittest` or `pytest`).
  - Test PDF generation with a full payload (subjects, tasks) – validate that the returned bytes are a valid PDF (e.g., start with `%PDF`).
  - Test PDF generation with empty subject/task lists – verify that the PDF still renders and contains a progress of 0 %.
  - Test handling of malformed payload – expect HTTP 400 (FastAPI side) which Xano would translate to 502.
* **Integration test** – Use a mock Xano endpoint (or a test double) to ensure the full flow (payload → PDF → storage) works end‑to‑end.

### 7.3 Docker / Render Validation
* Build the Docker image locally and run `uvicorn` to confirm it starts and serves `POST /generate-pdf`.
* Execute a curl request against the container:
  ```bash
  curl -X POST $PDF_API_URL \
       -H "Content-Type: application/json" \
       -H "X-API-Key: <SEARCH_API_KEY>" \
       -d @sample_payload.json --output report.pdf
  ```
* Verify that `report.pdf` opens and contains the expected sections.

## 8. Open Questions / Pending Validation
* Does the Xano plan allow **private** File Resources and the `Generate Signed URL` API? – required for the preferred storage strategy.
* What is the maximum size of a text field in Xano? – needed to confirm Base64 fallback will not exceed limits for large reports.
* Are there any rate‑limits on the FastAPI endpoint that might affect bulk generation? – to be checked with the Render configuration.

## 9. Summary
The design defines a clear separation of concerns:
* **FastAPI** handles PDF creation using ReportLab.
* **Xano** orchestrates data collection, calls the FastAPI service, and stores the resulting PDF using either File Resources (preferred) or a Base64 fallback.
* Security is enforced at the Xano layer (authentication, ownership checks) and the signed URL is temporary.
* Dockerfile and test plan ensure the service can be built, deployed, and verified without touching production Xano or Render resources.

*All decisions reflect the approved proposal and specification, with pending verification items clearly marked.*

