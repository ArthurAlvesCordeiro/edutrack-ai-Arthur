# AGENTS.md

This repository is currently minimal and does not yet define a concrete application stack. Keep all instructions below in mind when working on login-related changes.

## Core expectations

- Prefer the smallest, most explicit change that solves the task.
- Preserve existing project structure and conventions before introducing new patterns or dependencies.
- Keep code readable, testable, and easy to review.

## Login-focused guidance

- Prefer secure authentication defaults: HTTPS, environment-based secrets, no hardcoded credentials, and hashed passwords.
- Validate user input on both client and server sides: required fields, email format, password requirements, and clear user feedback.
- Avoid leaking account existence or internal state through error messages. Use generic responses such as “Invalid email or password.”
- Protect auth flows against brute-force abuse with rate limiting or lockout logic when appropriate.
- Keep sessions and tokens secure: secure cookie settings, short-lived tokens when relevant, and explicit logout behavior.
- Ensure login, registration, and session recovery flows share consistent validation rules and error handling.

## Implementation checklist

- Confirm the project framework before editing login code.
- Keep secrets in environment variables or the platform secret store; never commit them.
- Add or update tests for successful login, invalid credentials, empty fields, and session expiry or logout flows.
- Maintain accessibility for login screens: labels, focus states, keyboard support, and clear error announcements.

## Repo-specific note

- The workspace currently contains only a lightweight project stub and no source implementation, so confirm the actual app structure before making auth changes.
- If the repo grows into a real stack, add project-specific conventions alongside this file rather than duplicating broad framework guidance here.
