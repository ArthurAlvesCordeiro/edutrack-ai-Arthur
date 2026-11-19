## ADDED Requirements
### Requirement: Deploy FastAPI service
The system SHALL deploy the FastAPI service to Render with required environment variables.
#### Scenario: Render deployment
- **WHEN** the FastAPI service is configured with `SEARCH_API_KEY` and `PDF_API_URL` environment variables on Render,
- **THEN** the service **SHALL** start without errors and the `/generate-pdf` endpoint is reachable.

### Requirement: Xano Function implementation
The system SHALL implement a Xano Function `/reports/generate` that forwards the payload to FastAPI and stores the PDF.
#### Scenario: Forward request and store PDF
- **WHEN** a Xano Function `/reports/generate` receives a request from the client,
- **THEN** it **SHALL** forward the payload to the FastAPI `/generate-pdf` endpoint, receive the PDF bytes, and store them according to the chosen storage strategy (File Resource or Base64).

The system SHALL integrate a FlutterFlow UI button to trigger PDF generation.
#### Scenario: User triggers PDF generation
- **WHEN** a user clicks the "Generate Report" button in the FlutterFlow app,
- **THEN** the app **SHALL** call the Xano `/reports/generate` endpoint, receive the response, and initiate a download of the PDF (either via signed URL or direct binary stream).