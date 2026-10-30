# FastAPI service exposing the hybrid search logic used by EduTrack AI.
# Re‑uses the filtering implementation from `scripts/search_subjects.py`.

import os
from datetime import datetime, date
from typing import List, Optional, Any

from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field, validator, model_validator

# Import the core filtering function from the existing script.
# The script is located at `scripts/search_subjects.py` relative to the repository root.
# Adding the repository root to sys.path allows a direct import.
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.search_subjects import filter_subjects

app = FastAPI(title="EduTrack Hybrid Search API")

# ---------------------------------------------------------------------------
# Security – a simple shared secret passed via the X‑API‑Key header.
# The secret is read from the environment variable SEARCH_API_KEY.
# ---------------------------------------------------------------------------
API_KEY_ENV = "SEARCH_API_KEY"

def get_api_key(x_api_key: Optional[str] = Header(None)):
    expected = os.getenv(API_KEY_ENV)
    if expected is None:
        # Startup mis‑configuration – the service cannot run without a key.
        raise HTTPException(status_code=500, detail="Search API key not configured.")
    if x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid API key.")
    return x_api_key

# ---------------------------------------------------------------------------
# Pydantic models that describe the request payload.
# They are deliberately permissive (allow extra fields) because the original
# script accepts arbitrary additional keys in the subject / task objects.
# ---------------------------------------------------------------------------
class Subject(BaseModel):
    id: int
    name: str
    # Accept any additional fields without validation.
    class Config:
        extra = "allow"

class Task(BaseModel):
    id: int
    subject_id: Optional[int]
    due_date: Optional[date]
    status: str
    class Config:
        extra = "allow"

class SearchRequest(BaseModel):
    subjects: List[Subject]
    tasks: List[Task]
    query: Optional[str] = None
    has_overdue: Optional[bool] = False
    reference_date: Optional[date] = None

    @validator("query")
    def strip_query(cls, v):
        return v.strip() if isinstance(v, str) else v

    @validator("has_overdue", pre=True)
    def coerce_boolean(cls, v):
        # Accept true/false strings as well as booleans.
        if isinstance(v, str):
            return v.lower() in {"true", "1", "yes"}
        return bool(v)

    @validator("reference_date", pre=True)
    def parse_date(cls, v):
        # FastAPI/Pydantic already parses ISO dates, but we keep this for safety.
        return v

    @model_validator(mode="after")
    def at_least_one_filter(self):
        # Ensure that either a query or has_overdue=True is supplied.
        if not self.query and not self.has_overdue:
            raise ValueError("Provide either a query or set has_overdue=true.")
        return self

# ---------------------------------------------------------------------------
# Helper to convert the date handling to the same semantics used in the script.
# The script treats a missing reference_date as "now" (UTC).
# ---------------------------------------------------------------------------
def resolve_reference_date(req: SearchRequest) -> datetime:
    if req.reference_date:
        # date objects are naïve; treat them as midnight UTC for consistency.
        return datetime.combine(req.reference_date, datetime.min.time())
    return datetime.utcnow()

# ---------------------------------------------------------------------------
# POST /search endpoint – the public API.
# ---------------------------------------------------------------------------
@app.post("/search", response_model=Any)
def search(req: SearchRequest, _: str = Depends(get_api_key)):
    """Execute the hybrid subject search.

    The payload must contain "subjects" and "tasks" arrays exactly as the
    command‑line script expects.  The endpoint validates the presence of at least
    one filter (query or has_overdue) and returns a JSON object:

        {"subjects": [ ... filtered subjects ... ]}
    """
    # Resolve reference date (UTC now if omitted).
    ref_dt = resolve_reference_date(req)

    # The original `filter_subjects` expects plain Python structures (list of
    # dicts).  Pydantic models are convertible via `.dict()`.
    filtered = filter_subjects(
        subjects=[s.model_dump(mode="json") for s in req.subjects],
        tasks=[t.model_dump(mode="json") for t in req.tasks],
        query=req.query,
        has_overdue=req.has_overdue,
        ref_date=ref_dt,
    )
    return {"subjects": filtered}
