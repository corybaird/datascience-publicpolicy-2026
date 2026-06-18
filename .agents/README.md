# Coding Agent Workflow & Instructions Reference

Welcome, Agent. This directory contains instructions, guardrails, and templates designed to guide AI coding assistants (e.g., Claude Code, Antigravity, or other LLMs running with workspace tools) in managing, code-editing, and committing changes in this repository.

## 1. Directory Structure of Agent Tooling

- `.agents/README.md`: Overall entry point and context bridge (this file).
- `.agents/workflows/`: Specific workflows for executing tasks:
  - `git-management-research.md`: Committing and PR workflows tailored for research and analytical scripts.
  - `git-management-pypi.md`: Committing and release workflows tailored for Python libraries and packages.
  - `git-management-database.md`: Committing and migration workflows tailored for database changes.

---

## 2. Project Directory Structure

Coding agents must strictly adhere to the following project structure:

```
├── data/
│   ├── raw/           # Immutable original data (never modified)
│   ├── processed/     # Cleaned, transformed data ready for analysis
│   ├── pipeline/      # Intermediate artifacts from pipeline stages 
│   └── temp/          # Temporary working files (gitignored)
├── docs/              # System guides and domain-level references
│   ├── architecture_data.md # Code architecture & data standards
│   ├── analysis.md          # Analytical methodology, model designs, and metrics
│   ├── figures.md           # Plotting specifications, color palettes, visual style rules
│   └── executive_summary.md # Core research findings and policy implications
├── src/               # Modular Python source code packages
│   ├── data/          # Data loading, scraping, and ETL logic
│   ├── model/         # Model definitions and training code
│   ├── pipeline/      # Pipeline orchestration and stage runners
│   ├── llm/           # LLM API calls, prompt templates, and inference
│   ├── viz/           # Custom plotting and visualization engines
│   ├── dashboard/     # Interactive UI files (e.g., Streamlit)
│   └── utils/         # Shared utility functions
├── references/        # Configuration files, dictionaries, and prompt templates
│   ├── configs/       # YAML configurations loaded via yaml.safe_load()
│   └── dictionaries/  # Dictionary files (>3 keys, constant assignments only)
├── models/            # Serialized trained models (.joblib, .pkl, .pt)
├── reports/           # Generated figures, tables, and presentation summaries
├── notebooks/         # Exploratory Jupyter notebooks
└── tests/             # Unit and integration tests
```

---

## 3. Connection: `.agents/` Context & Project `README.md`

An agent operates at two layers of understanding: the **Domain/Subject Level** and the **Operational/Execution Level**.

```
+------------------------------------------------------------------+
|                     Project README.md                            |
|  - Domain Context (Macroeconomics, Public Policy, Class schedule)|
|  - System Software Requirements & Notebook structure             |
|  - Individual & Group Assignments (Deliverables)                 |
+-------------------------------+----------------------------------+
                                | (Translates Domain into Action)
                                v
+------------------------------------------------------------------+
|                     .agents/ Tooling                             |
|  - Strict Execution Guardrails & Rules                           |
|  - Git Commit Conventions (ALL-CAPS Verbs, Atomic commits)       |
|  - Step-by-Step Approval Gates (Human-in-the-Loop)               |
+------------------------------------------------------------------+
```

### Why this README-to-Agent Connection is Crucial

1. **Context Density and Reduced Hallucination**:
   - The root `README.md` outlines the "What" and "Why" of the project (e.g., grading milestones, weekly schedules). 
   - The `.agents/README.md` provides the "How". 
   - By matching these two sources, an agent understands the boundaries of its current week's assignment or project scope, and uses that narrow context to prevent hallucinating modifications to unrelated folders.

2. **AI-Ready Hierarchy & System Documentation (docs/)**:
   - Structured markdown files under `docs/` allow parsing tools to quickly ingest codebase layouts and requirements.
   - **architecture_data.md** guides the agent on code design rules and ingestion logic.
   - **analysis.md**, **figures.md**, and **executive_summary.md** serve as domain-specific guidelines.

3. **Human-in-the-Loop (HITL) Gatekeeping**:
   - Coding agents must never bypass human verification. 
   - The workflows mandate explicit validation gates:
     1. Proposing changes to the human before writing them.
     2. Verifying test suite execution before committing.
     3. Presenting the exact commit message draft for approval.
     4. Drafting PR details for review before push.

---

## 4. Domain Reference Files (docs/)

To ensure analytical and visual correctness, agents must reference the following documentation before editing or creating code:

1. **analysis.md**:
   - Explains the analytical methodology, statistical models (e.g., regression specifications), metrics, and validation strategy.
   - Checked by agents before writing pipeline stages (`src/pipeline/`) or model code (`src/model/`) to ensure implementation matches the research design.

2. **figures.md**:
   - Defines plotting conventions, style guidelines, color palettes, and file formats (e.g., PNG, SVG).
   - Consulted by agents before writing visualization functions in `src/viz/` to keep figures looking premium and consistent.

3. **executive_summary.md**:
   - Outlines the research findings, policy interpretations, and key summary statements.
   - Used by agents to write text inside interactive dashboards (`src/dashboard/`), reporting summaries, or slide outlines without hallucinating outcomes.

---

## 5. Git Management Guidelines

When performing any Git changes, you must:
1. **Analyze Stage**: Run `git status` and `git diff` first.
2. **Commit Atomicity**: Commit a maximum of 3-5 files per commit (ideally 1-2 files).
3. **Convention**: Start the commit subject line with an approved ALL-CAPS verb (e.g., `ADD`, `FIX`, `UPDATE`, `DOCS`, `CREATE`, `REFACTOR`). Do not end with a period.
4. **Approval Gate**: Output the proposed commit message and ask the user for confirmation. Only commit once confirmed.
