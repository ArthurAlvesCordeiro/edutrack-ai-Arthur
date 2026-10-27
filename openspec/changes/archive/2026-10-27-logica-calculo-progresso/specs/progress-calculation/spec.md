# Spec Delta

## Purpose

Provides a standalone calculation utility that computes progress percentage from completed and total task numbers, returning a JSON response with zero-division safety.

## ADDED Requirements

### Requirement: Calculate progress percentage
The script SHALL calculate the completion percentage based on the number of completed tasks and the total number of tasks, returning a JSON object with the `percentage` key to standard output.

#### Scenario: Normal progress calculation
- **WHEN** the script is executed with valid completed and total task counts where total is greater than zero
- **THEN** it outputs a JSON object containing the calculated progress percentage under the `percentage` key

#### Scenario: Total task count is zero
- **WHEN** the script is executed with a total task count of 0
- **THEN** it returns a JSON object with `percentage` set to 0 and does not raise a division-by-zero error

### Requirement: Pure Python execution
The progress calculation utility MUST execute using standard Python without requiring any external third-party dependencies.

#### Scenario: Running in standard Python environment
- **WHEN** the script is invoked with standard Python 3
- **THEN** it executes cleanly using only standard library modules
