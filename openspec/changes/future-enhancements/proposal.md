# Future Enhancements Proposal

## Overview
This proposal outlines the pending steps required to fully integrate the PDF reporting feature into the EduTrack AI production environment.

### Pending Deliverables
1. Deploy the FastAPI `/generate-pdf` service to Render (or another PaaS) with proper environment variables (`SEARCH_API_KEY`, `PDF_API_URL`).
2. Implement an Xano Function `/reports/generate` that forwards the request payload to the FastAPI endpoint and stores the resulting PDF according to the chosen storage strategy.
3. Add a UI button in the FlutterFlow application that triggers the Xano endpoint and allows the user to download the generated PDF.

The implementation of these items will complete the end‑to‑end flow:
FlutterFlow ↔ Xano ↔ FastAPI (Render) → PDF.

