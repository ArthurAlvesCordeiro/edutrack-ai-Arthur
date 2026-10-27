# Tasks

## 1. Environment and Script Setup

- [x] 1.1 Create the `scripts/` directory and initialize `scripts/calculate_progress.py`, verifying the file exists on disk

## 2. Core Progress Calculation Implementation

- [x] 2.1 Implement the calculation logic and zero-division safety in `scripts/calculate_progress.py`, verifying that total=0 returns percentage 0 without exception
- [x] 2.2 Implement CLI argument parsing and JSON output format `{"percentage": ...}` in `scripts/calculate_progress.py`, verifying output formatting on stdout
- [x] 2.3 Execute verification commands using Python for normal cases and zero-task cases, verifying expected JSON output for each scenario
