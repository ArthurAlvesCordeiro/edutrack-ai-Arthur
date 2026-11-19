# EduTrack AI – Comprehensive Project Plan (Tasks 01‑16)

## Overview
This document outlines the end‑to‑end workflow for the **EduTrack AI** project, following the specifications and constraints defined in the **AGENTS.md** manual and the detailed task list you provided (Tasks 01–16). It respects the existing codebase and does **not** modify any files that have already been created.

---

## 1. Technology Stack & Architecture
| Layer | Technology | Notes |
|------|------------|-------|
| **Frontend** | **FlutterFlow** (custom Design System, NavBar, pages: HomePage, SubjectsPage, TasksPage) | No Firebase; API integration via Xano API Group |
| **API / Backend‑as‑Code** | **Xano** (workspace `edutrack-ai`) with **XanoScript** (`*.xs`) files | Managed locally via VS Code extension |
| **Advanced Processing** | **Python** scripts (ReportLab/fpdf2 for PDF, progress calculation, hybrid search) | Exposed to Xano via custom Functions / Endpoints |
| **Spec‑Driven Development** | **OpenSpec** (`openspec/` folder) | Proposals, tasks, specs, changes stored under `openspec/changes/` and `openspec/specs/` |
| **Version Control** | **Git** (GitHub) | Branch‑per‑feature workflow, Conventional Commits, no automatic push/deploy |
| **AI Assistant** | **Antigravity (AGY)** with Gemini plugins | Generates code, specs, documentation, never performs remote pushes |

---

## 2. Branch & Commit Strategy (per AGENTS.md)
- All work is performed on a dedicated branch prefixed with `feat/`, `fix/`, `docs/`, `chore/`, `style/` or `release/`.
- Commit messages follow **Conventional Commits**:
  ```
  <type>(<scope>): <short description>
  ```
  e.g. `feat(pdf-report): add PDF generation endpoint`.
- Pull Requests are opened for every branch and merged only after review.
- The final delivery resides on `release/final-delivery`.

---

## 3. Detailed Task Breakdown
### Task 01 – First Git/GitHub Contact
| Action | File(s) | Branch | Commit Message |
|--------|---------|--------|----------------|
| Create GitHub account (institutional email) | – | – | – |
| Install Git, configure global `user.name` & `user.email` | – | – | – |
| Create private repo `edutrack-ai` | – | – | – |
| Clone repo locally, add initial `README.md` | `README.md` (initial) | `main` | `docs: initial README` |
| First commit & push | – | `main` | `feat: initial project scaffold` |

### Task 02 – VS Code, Node.js, AI Setup
| Action | Files/Extensions | Branch | Commit |
|--------|------------------|--------|--------|
| Install VS Code & essential extensions (Gemini Code Assist, XanoScript, Markdown All in One) | – | – | – |
| Authenticate Gemini with Impacta email, enable Agent key | – | – | – |
| Install Node.js LTS, verify `node -v` & `npm -v` | – | – | – |
| Open project folder `edutrack‑ai` in VS Code | – | – | – |

### Task 03 – OpenSpec Installation & Init
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| Install OpenSpec CLI globally (`npm i -g @fission-ai/openspec@latest`) | – | – | – |
| Run `openspec init` (select Gemini CLI) | creates `openspec/` folder with `project.md`, `AGENTS.md`, `specs/`, `changes/` | `main` | `chore: init OpenSpec project structure` |
| Commit init files | `openspec/**` | `main` | `chore: add OpenSpec scaffolding` |

### Task 04 – First Pull/Push with XanoScript
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| Create Xano workspace `edutrack‑ai`, generate Personal Access Token (CRUD) | – | – | – |
| Authenticate XanoScript extension, pull latest `.xs` files | `tables/`, `apis/`, `functions/`, `addons/` | `main` | `feat(xano): pull initial XanoScript files` |
| Remove default tables, keep only `users` (or `user`) | `tables/` (delete) | `main` | `refactor(xano): clean default tables` |
| Push cleaned `.xs` files to GitHub | – | `main` | `feat(xano): push cleaned XanoScript files` |

### Task 05 – Git Branching & Pull Requests
| Action | Files | Branch | PR |
|--------|-------|--------|----|
| Create branch `feat/melhoria-readme` from `main` | `README.md` | `feat/melhoria-readme` | Add `## Tecnologias Utilizadas` section |
| Commit & push | – | – | `feat: add technologies section` |
| Open PR, review, merge to `main` | – | – | – |
| Delete local branch | – | – | – |

### Task 06 – Free Template Research (Figma & Xano Marketplace)
| Action | Files | Branch | PR |
|--------|-------|--------|----|
| Research & duplicate ≥2 free Figma templates (e.g., Education Dashboard, Task Manager) | `docs/pesquisa/referencias.md` (links & analysis) | `docs/referencias-templates` | `docs: add template research` |
| Explore Xano Marketplace Starter Templates (no install) | – | – | – |

### Task 07 – FlutterFlow Initial Setup
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| Create blank FlutterFlow project `EduTrack AI` (no Firebase) | – | – | – |
| Define Theme (colors, fonts) | – | – | – |
| Configure API Group pointing to Xano workspace URL | – | – | – |
| Add progress note in `README.md` (branch `chore/flutterflow-setup`) | `README.md` | `chore/flutterflow-setup` | `chore: document FlutterFlow setup` |

### Task 08 – First OpenSpec Proposal (subjects table)
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| Fill `AGENTS.md` with language, naming, security rules | `AGENTS.md` (root) | `feat/openspec-subjects` | `docs: update AGENTS guidelines` |
| Run `/openspec:proposal` → creates `openspec/changes/subjects/proposal.md` & `tasks.md` | – | `feat/openspec-subjects` | `feat(open-spec): proposal for subjects table` |
| Apply proposal → generate `tables/subjects.xs` | `tables/subjects.xs` | – | `feat(xano): add subjects table` |
| Validate & archive proposal | – | – | `chore(open-spec): validate & archive subjects` |
| PR to `main` | – | – | – |

### Task 09 – Figma → FlutterFlow Asset Integration
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| Refine Dashboard in Figma, export icons (SVG/PNG) | `assets/icons/` | `style/assets-figma` | `style: add exported icons` |
| Recreate UI in FlutterFlow using ListView, Container, NavBar | – | – | – |
| Save assets locally (`assets/`) & commit | `assets/` | `style/assets-figma` | `chore: add UI assets` |

### Task 10 – Advanced AGENTS.md Configuration
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| Update root `AGENTS.md` with precedence rules, no auto‑push, mandatory guideline reads, delta syntax, REST, security, Conventional Commits | `AGENTS.md` | `feat/config-agents-ia` | `docs: tighten AGENTS rules` |
| Create test proposal `feature-notas-atividades` to validate behavior | `openspec/changes/feature-notas-atividades/` | `feat/config-agents-ia` | `feat(open-spec): test AGENTS config` |
| Archive after validation | – | – | `chore(open-spec): archive test proposal` |

### Task 11 – XanoScript Table *academic_tasks*
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| Draft OpenSpec proposal for `academic_tasks` table (fields: title, description, due_date, status, subject_id) | `openspec/changes/academic-tasks/` | `feat/tabela-tarefas` | `feat(open-spec): proposal academic_tasks table` |
| Apply → generate `tables/academic_tasks.xs` | `tables/academic_tasks.xs` | – | `feat(xano): add academic_tasks table` |
| Validate & archive | – | – | `chore(open-spec): archive academic_tasks` |

### Task 12 – Python Progress Calculator
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| OpenSpec proposal for script `scripts/calculate_progress.py` (returns JSON `{ "percentage": … }` with zero‑division guard) | `openspec/changes/python-progress/` | `feat/python-progress` | `feat(open-spec): proposal progress calculator` |
| Apply → create script | `scripts/calculate_progress.py` | – | `feat(python): add progress calculator` |
| Add unit tests (optional) | `scripts/test_calculate_progress.py` | – | `test(python): add progress calculator tests` |
| Validate & archive | – | – | `chore(open-spec): archive progress script` |

### Task 14 – Hybrid Search Endpoint
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| OpenSpec proposal for hybrid search (`POST /search`) integrating Xano queries + Python processing | `openspec/changes/hybrid-search/` | `feat/hybrid-search` | `feat(open-spec): proposal hybrid search` |
| Apply → implement in `services/search_api/main.py` and supporting Xano functions | `services/search_api/main.py`, Xano `.xs` files | – | `feat(search): add hybrid search endpoint` |
| Validate & archive | – | – | `chore(open-spec): archive hybrid search` |

### Task 15 – Advanced PDF Report Feature
| Action | Files | Branch | Commit |
|--------|-------|--------|--------|
| OpenSpec proposal for PDF generation (script `scripts/generate_performance_pdf.py`, FastAPI route `/generate-pdf`) | `openspec/changes/student-performance-pdf/` | `feat/pdf-report` | `feat(open-spec): proposal PDF report` |
| Apply → create/adjust script, FastAPI route, tests, Dockerfile updates (already done) | `scripts/generate_performance_pdf.py`, `services/search_api/main.py`, `services/search_api/test_generate_pdf.py`, `services/search_api/Dockerfile` | – | `feat(pdf): implement PDF generation` |
| Validate, run all unit tests, ensure OpenSpec spec passes (already validated) | – | – | `chore(open-spec): archive PDF report` |

### Task 16 – Audit, Maintenance & Final Delivery
| Action | Files / Artifacts | Branch | Commit |
|--------|-------------------|--------|--------|
| Run `openspec validate --all` – confirm no errors (already confirmed) | – | – | – |
| Ensure all proposals are archived under `openspec/changes/archive/` | `openspec/changes/archive/` | – | – |
| Clean up test code/comments in `.xs` and `.py` files (retain only production code) | `tables/`, `functions/`, `scripts/` | `chore/cleanup` | `chore: remove test artifacts` |
| Update `README.md` with final status table (already updated) | `README.md` | – | – |
| Perform end‑to‑end manual test in FlutterFlow (Login → Create Subject → Create Task → View Progress → Generate PDF) – document result in `docs/e2e-test.md` | `docs/e2e-test.md` | `docs/e2e-test` | `test: add end‑to‑end verification notes` |
| Create branch `release/final-delivery`, commit final state, push and open PR (no merge) | – | `release/final-delivery` | `release: final delivery of EduTrack AI` |
| Add links to PR, FlutterFlow project, and final PDF report in `README.md` | `README.md` | – | `docs: add final delivery links` |

---

## 4. OpenSpec Validation Checklist (Current State)
- `openspec validate --all --strict` returns **0 errors** (validated after previous updates).
- All changes are archived under `openspec/changes/archive/` except the pending **future‑enhancements** change, which remains open for the next sprint.
- The `student-performance-pdf` spec now contains a proper `## Purpose` and `## Requirements` section with `SHALL` statements.
- The `future‑enhancements` spec uses `## ADDED Requirements` with clear requirement text and scenarios.

---

## 5. Next Immediate Actions (If you want to proceed)
1. **Create the `docs/e2e-test.md` file** with the manual test steps and outcome.
2. **Finalize the `future‑enhancements` change** (if any further refinement is needed).
3. **Create the `release/final-delivery` branch** (you will do the `git checkout -b release/final-delivery` and push).
4. **Open the final Pull Request** and add the required links to the `README.md`.

All of the above respects the AGENTS.md constraints: no automatic pushes, no changes to existing files beyond what is described, and everything is documented in English with proper naming conventions.

---

*This plan is generated by Antigravity AI and is ready for you to follow step‑by‑step.*

