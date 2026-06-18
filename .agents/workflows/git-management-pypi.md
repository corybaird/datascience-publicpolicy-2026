---
name: git-management-pypi
description: Commit Management Workflow tailored for PyPI Python Library projects.
tools: Bash, Read, AskUserQuestion
model: sonnet
---
# Commit Management Workflow: PyPI Python Library Projects

## Objective
Generate git commit messages that strictly adhere to the project's historical ALL-CAPS verb convention while ensuring atomicity and proper review gates for open-source package development, testing, and distribution.

## Commit Pattern
Commit messages MUST follow this format:
1.  **ALL-CAPS Verb:** Start with a strong action verb from the dictionary.
2.  **Concise Subject:** A short description of the change (e.g., feature addition, bug fix, version bump).
3.  **No Trailing Punctuation:** Do not end with a period.
4.  **Standard References:** Use lowercase for file extensions (e.g., `.py`, `.toml`, `.md`).

### Action Verb Dictionary
`CREATE`, `UPDATE`, `ADD`, `REMOVE`, `FIX`, `REFACTOR`, `DEPRECATE`, `DOCS`, `RELEASE`, `TEST`.

### Examples
*   `ADD pytest coverage for core module`
*   `FIX version bump in pyproject.toml`
*   `UPDATE dependencies for pydantic v2`
*   `DOCS update api reference for new endpoints`
*   `RELEASE v1.2.0`
*   `REFACTOR simplify loop in data loader`
*   `TEST add edge case tests for string parser`
*   `REMOVE unused legacy helper functions`

## Atomic / Micro Commits
*   **Max Files Per Commit:** You MUST strictly limit commits to a maximum of 3-5 files, but ideally only 1-2 files per atomic commit. If a logical change spans more than 5 files, you must break it down into smaller, micro commits.
*   **Group Couplings:** Bundle logically related changes (e.g., a new feature `.py` file and its corresponding unit test `test_*.py`).
*   **Differentiate Intent:** Keep source code fixes (`FIX`) separate from CI/CD pipeline changes (`UPDATE`) or documentation (`DOCS`) unless they are intrinsically linked.
*   **Milestone Based:** Commit as you reach logical points in the branch, not just at the very end.

## Workflow: Commit then PR

When the user requests a commit:

1.  **Status Check:** Run `git status` and `git diff` to review staged/unstaged changes.
2.  **Analyze Scope:** Identify logical atomic units. If more than 5 files, propose splitting into multiple commits.
3.  **Select Verb:** Pick the most accurate verb from the approved list for each commit.
4.  **Draft Summary:** Write the subject line following the pattern.
5.  **Present for Approval:** Show the proposed commit message(s) and file groupings. Wait for user confirmation.
6.  **Commit:** After approval, run `git add` and `git commit -m "<subject>"` for each commit.
7.  **Propose PR:** Once all commits are made, present a PR draft for the user to review and approve before creation.

## Pull Request Workflow

### Before Creating PR
*   Verify branch is clean (`git status` shows no uncommitted changes).
*   Ensure commits are atomic and follow the commit pattern.
*   Check that commits are properly staged and pushed.

### PR Content
The PR should include:
*   **Title:** Clear summary of the feature/fix
*   **Summary:** Bulleted list of key changes
*   **Testing:** Any commands needed to verify (e.g., pytest)
*   **Breaking Changes:** Note any breaking changes if applicable

### PR Gate
*   Do NOT create the PR until the user explicitly approves.
*   Present the PR details to the user for confirmation before running `gh pr create`.

## Branch Strategy
*   Use feature branches.
*   Branch from `main` for new features/fixes.
*   PRs target `main` unless otherwise specified.
*   Keep branches focused — one feature or fix per branch.
