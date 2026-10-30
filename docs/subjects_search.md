# Hybrid Search Service Documentation

## 1. Objective
The **Hybrid Search Service** runs a FastAPI endpoint that re‑uses the existing Python search logic (`scripts/search_subjects.py`). It lets clients filter subjects by:
- a case‑insensitive name query;
- the presence of at least one overdue task;
- an optional reference date used for overdue evaluation.
The response contains only the matching subjects, reproducing the behavior of the original CLI script.

## 2. Requirements & Installation (Python 3.12 on Windows)
```bash
# From the repository root
py -3.12 -m venv .venv          # create a virtual environment (recommended)
# Activate it in Git Bash
source .venv/Scripts/activate   # on Windows PowerShell use `.venv\Scripts\Activate.ps1`
# Install the required packages
python -m pip install -r services/search_api/requirements.txt
```
`services/search_api/requirements.txt` currently contains:
```
fastapi==0.110.0
uvicorn[standard]==0.29.0
pydantic==2.6.3
httpx==0.27.2
```
These dependencies are sufficient to run the service and its test suite.

## 3. Defining the API key in Git Bash
The service authenticates requests via the `X-API-Key` header. The expected key is read from the environment variable `SEARCH_API_KEY`.
```bash
# In Git Bash (or any POSIX‑compatible shell on Windows)
export SEARCH_API_KEY=my_secret_key
```
Replace `my_secret_key` with a value of your choice. **Do not commit** this variable to the repository.

## 4. Starting the FastAPI server
```bash
python -m uvicorn services.search_api.main:app --host 127.0.0.1 --port 8000
```
The server will be reachable at `http://127.0.0.1:8000`.

## 5. Testing the endpoint with `curl`
```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SEARCH_API_KEY" \
  -d '{
        "subjects": [
          {"id": 1, "name": "Matematica"},
          {"id": 2, "name": "Historia"}
        ],
        "tasks": [
          {"id": 10, "subject_id": 2, "due_date": "2000-01-01", "status": "pending"}
        ],
        "query": "mat",
        "has_overdue": true
      }'
```
The response is JSON of the form `{ "subjects": [ … ] }` containing the filtered subjects.

## 6. Running the test suites
```bash
# Unit tests for the pure‑Python script
python -m unittest scripts/test_search_subjects.py

# FastAPI service tests (use the same interpreter)
python -m unittest services/search_api/test_main.py
```
Both suites should run without errors after the dependencies are installed.

## 7. Building the Docker image
The Dockerfile lives at `services/search_api/Dockerfile`. Build the image from the repository root:
```bash
docker build -f services/search_api/Dockerfile -t edutrack-search-api .
```
The Dockerfile copies:
- `services/search_api/requirements.txt` and installs the Python packages;
- the FastAPI service code in `services/search_api/`;
- `scripts/search_subjects.py` (required for the import).

Run the container (still supplying the API key):
```bash
docker run -e SEARCH_API_KEY=my_secret_key -p 8000:8000 edutrack-search-api
```
The service will be accessible at `http://localhost:8000` inside the container.

## 8. Current integration state
- The FastAPI service works locally and can be exercised with the `curl` command above.
- **The Xano endpoint (`GET /subjects/search`) currently implements the same filtering logic directly in XanoScript.** It **does NOT** invoke this FastAPI service yet because a publicly reachable URL is required by Xano. That integration step remains **pending**.

---
*Documentation generated for the `feat/hybrid-search` branch. No other files were modified.*