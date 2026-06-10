---
name: git-management-database
description: Commit Management Workflow tailored for Database projects.
tools: Bash, Read, AskUserQuestion
model: sonnet
---
# Commit Management Workflow: Database Projects

## Objective
Generate git commit messages that strictly adhere to the project's historical ALL-CAPS verb convention while ensuring atomicity and proper review gates for database schemas, migrations, and data pipelines.

## Commit Pattern
Commit messages MUST follow this format:
1.  **ALL-CAPS Verb:** Start with a strong action verb from the dictionary.
2.  **Concise Subject:** A short description of the change (e.g., schema change, index addition, data import).
3.  **No Trailing Punctuation:** Do not end with a period.
4.  **Standard References:** Use lowercase for file extensions (e.g., `.sql`, `.csv`, `.json`).

### Action Verb Dictionary
`CREATE`, `UPDATE`, `ADD`, `REMOVE`, `FIX`, `REFACTOR`, `DEPRECATE`, `DOCS`, `MIGRATE`, `SEED`.

### Examples
*   `CREATE user sessions table`
*   `ADD composite index on transactions`
*   `UPDATE normalization for legacy records`
*   `SEED taxonomy definitions in lookup table`
*   `MIGRATE update foreign keys for schema v2`
*   `FIX rollback syntax error in migration 104`
*   `REFACTOR extract trigger logic into stored procedure`
*   `REMOVE deprecated user roles from seeded data`

## Atomic / Micro Commits
*   **Max Files Per Commit:** You MUST strictly limit commits to a maximum of 3-5 files, but ideally only 1-2 files per atomic commit. If a logical change spans more than 5 files, you must break it down into smaller, micro commits.
*   **Group Couplings:** Bundle logically related changes (e.g., a migration script `.sql` and its corresponding rollback script, or a schema change and its seed data).
*   **Differentiate Intent:** Keep schema changes (`CREATE`/`MIGRATE`) separate from data population (`SEED`) and documentation (`DOCS`) unless they are intrinsically linked.
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
*   **Testing:** Any commands needed to verify
*   **Breaking Changes:** Note any breaking changes if applicable

### PR Gate
*   Do NOT create the PR until the user explicitly approves.
*   Present the PR details to the user for confirmation before running `gh pr create`.

## Branch Strategy
*   Use feature branches.
*   Branch from `main` for new features/fixes.
*   PRs target `main` unless otherwise specified.
*   Keep branches focused — one feature or fix per branch.
