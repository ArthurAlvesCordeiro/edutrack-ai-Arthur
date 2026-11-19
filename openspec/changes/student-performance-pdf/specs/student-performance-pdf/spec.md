## ADDED Requirements

### Requirement: Authenticated PDF Report Generation
The system MUST generate a PDF report for the authenticated user.

#### Scenario: Generate PDF when user is authenticated
- WHEN an authenticated user requests a performance report via `POST /reports/generate`
- THEN the system forwards the request to the FastAPI service and returns a signed URL (or Base64 payload) for the generated PDF.

### Requirement: User Data Isolation
The system MUST ensure that a user can only access reports that they own.

#### Scenario: User can only access own reports
- WHEN a user attempts to download a report with `GET /reports/{report_id}/download`
- THEN the endpoint validates that the `owner_id` of the report matches the authenticated user and denies access otherwise.

### Requirement: PDF Generation Without Subjects or Tasks
The system SHALL generate a PDF report even when the request payload contains no subjects or academic tasks.

#### Scenario: Generate PDF even when no subjects or tasks exist
- WHEN the request payload contains no subjects or academic tasks
- THEN the FastAPI service still returns a valid (empty‑content) PDF without returning HTTP 400.

### Requirement: Secure Xano → FastAPI Communication
Xano SHALL include a valid `X‑API‑Key` header when invoking the FastAPI `/generate-pdf` endpoint, and FastAPI MUST validate this header before processing the request.

#### Scenario: Xano calls FastAPI with X‑API‑Key header
- WHEN Xano invokes the FastAPI endpoint `/generate-pdf`
- THEN it includes a valid `X‑API‑Key` header and FastAPI validates it before processing.

### Requirement: Configurable PDF Storage Strategy
Xano MUST store the generated PDF either as a File Resource with Attachment Metadata or as a Base64‑encoded field, depending on the validated storage configuration.

#### Scenario: Store PDF according to selected strategy
- WHEN the FastAPI service returns the PDF binary
- THEN Xano stores the file either as a File Resource (with Attachment Metadata) or as Base64 in a fallback table, based on the validated storage configuration.

### Requirement: Download with Ownership Verification
The download endpoint MUST verify that the authenticated user (`$auth.id`) matches the report’s owner before providing a signed URL or Base64 content.

#### Scenario: Protected download endpoint
- WHEN a user calls `GET /reports/{report_id}/download`
- THEN the endpoint checks `$auth.id` against the report’s owner before providing the signed URL or Base64 content.

### Requirement: Comprehensive HTTP Error Handling
The system MUST return appropriate HTTP status codes (e.g., 401, 502, 500) with clear error messages for authentication failures, service unavailability, or storage errors.

#### Scenario: Appropriate error responses
- WHEN authentication fails, the FastAPI service is unavailable, or storage errors occur
- THEN the system returns suitable HTTP status codes (401, 502, 500, etc.) with clear error messages.

### Requirement: FlutterFlow Integration
The FlutterFlow client MUST handle both signed URL and Base64 responses, display the PDF, and enforce ownership constraints.

#### Scenario: FlutterFlow app consumes the report endpoints
- WHEN the mobile app requests a report and later downloads it
- THEN the app handles both signed URL and Base64 responses, displays the PDF, and respects ownership constraints.
