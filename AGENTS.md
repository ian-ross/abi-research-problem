# Project instructions

This repository is a uv-managed Python project.

- Use `uv` for all dependency management.
- Run Python through uv, e.g. `uv run python ...`.
- Do not run bare `python ...` commands in this repository.
- Prefer `uv run pytest ...` or other `uv run ...` forms for project tools.

## Project guardrails

- Work should start from a backlog task. Assign it, set it to `In Progress`, add an implementation plan, and get approval before coding unless explicitly told otherwise.
- Treat `planning-inputs/` as temporary local planning material. Do not make persistent code, tests, or docs depend on it; move durable context into `CONTEXT.md`, ADRs, backlog docs, provider brief/profile, or source code.
- The `data` symlink points to external training data and may not exist in every environment. Unit tests should use tiny fixtures unless explicitly marked as data-dependent integration tests.
- Do not perform real model training on this machine. Use this environment for scaffolding, unit tests, smoke tests, and lightweight fixture runs; real training is expected to happen on the cluster.
- Candidate models must never receive longitude or latitude inputs. These encourage route-location priors and reduce transferability.
- Candidate code must not own data loading, loss definitions, metric definitions, Artifact Filters, Baseline Segmenter loading, or sampling policies. These belong in trusted provider or harness code.
- Use `../ml-autoresearch` as the harness reference and integration target. Use `../gvccs-research-problem` as a structural pattern, not as domain truth to copy blindly.

# Backlog task management

Use Backlog.md as the project issue tracker. This section is intentionally organized for progressive disclosure: read the quick rules first, then use the command reference only when needed.

## Always-follow rules

- **Use the CLI for task operations.** Do not edit files under `backlog/tasks/` directly.
- **Use `--plain` when reading/listing/searching tasks** so output is agent-friendly.
- **Keep task metadata synchronized** by using `backlog task create`, `backlog task edit`, etc.
- **Do not mark a task Done** unless all acceptance criteria, Definition of Done items, final summary, and validation are complete.

## Normal implementation workflow

When you start implementing a task:

1. Read the task:
   ```bash
   backlog task ABI-001 --plain
   ```
2. Assign it and move it to In Progress:
   ```bash
   backlog task edit ABI-001 -s "In Progress" -a @agent
   ```
3. Add an implementation plan:
   ```bash
   backlog task edit ABI-001 --plan $'1. Inspect relevant files\n2. Implement\n3. Test'
   ```
4. Share the plan and wait for approval unless the user explicitly told you to proceed.
5. Implement only the acceptance criteria.
6. Append concise progress notes as needed:
   ```bash
   backlog task edit ABI-001 --append-notes $'- Implemented provider scaffold\n- Added import smoke test'
   ```
7. Check acceptance criteria as they become true:
   ```bash
   backlog task edit ABI-001 --check-ac 1 --check-ac 2
   ```
8. When complete, add a PR-style final summary and mark Done:
   ```bash
   backlog task edit ABI-001 --final-summary $'Implemented ...\n\nTests:\n- uv run pytest ...'
   backlog task edit ABI-001 -s Done
   ```

## Common task commands

### Find work

```bash
backlog task list --plain
backlog task list -s "To Do" --plain
backlog search "filtered dice" --plain
backlog search "baseline" --type task --plain
```

### Create tasks

Create tasks with title, description, labels, priority, and acceptance criteria. Do **not** add implementation plans at creation time unless the user specifically asks for planning capture.

```bash
backlog task create "Task title" \
  -d "Why this task exists" \
  -l provider,tests \
  --priority high \
  --ac "Outcome one is true" \
  --ac "Outcome two is verifiable"
```

### Edit task metadata/content

```bash
backlog task edit ABI-001 -t "New title"
backlog task edit ABI-001 -s "In Progress"
backlog task edit ABI-001 -a @agent
backlog task edit ABI-001 -l provider,tests
backlog task edit ABI-001 --priority medium
backlog task edit ABI-001 -d "New description"
backlog task edit ABI-001 --dep ABI-000
```

### Manage acceptance criteria and DoD

```bash
backlog task edit ABI-001 --ac "New acceptance criterion"
backlog task edit ABI-001 --check-ac 1 --check-ac 2
backlog task edit ABI-001 --uncheck-ac 2
backlog task edit ABI-001 --remove-ac 3

backlog task edit ABI-001 --dod "Run tests"
backlog task edit ABI-001 --check-dod 1
backlog task edit ABI-001 --uncheck-dod 1
backlog task edit ABI-001 --remove-dod 1
```

Multiple `--check-ac`, `--uncheck-ac`, `--remove-ac`, `--check-dod`, etc. flags are allowed. Do not use comma-separated lists or ranges.

## Documents and decisions

Use backlog docs for durable planning/context that is not a domain glossary or ADR:

```bash
backlog doc create "Document title" --path document-slug --type planning
backlog doc list --plain
```

Use ADR files under `docs/adr/` for hard-to-reverse, non-obvious tradeoff decisions. Keep ADRs short.

`CONTEXT.md` is a glossary only. Do not put implementation plans or operational rules there.

## Multi-line CLI input

The CLI preserves input literally. In Bash/Zsh, use ANSI-C quoting for real newlines:

```bash
backlog task edit ABI-001 --plan $'1. First step\n2. Second step'
backlog task edit ABI-001 --notes $'- Note one\n- Note two'
backlog task edit ABI-001 --final-summary $'Summary\n\nTests:\n- uv run pytest'
```

Do not expect `"...\n..."` in normal quotes to become a newline.

## What not to do

- Do not edit `backlog/tasks/*.md` directly.
- Do not manually change task checkboxes in files.
- Do not browse task files instead of using `backlog task ... --plain`, except for emergency diagnostics.
- Do not add hidden work beyond a task’s acceptance criteria; add an AC or create a follow-up task first.
- Do not mark tasks Done without tests/validation, final summary, and completed checklists.

## Backlog CLI help

If a command is unclear, ask the CLI:

```bash
backlog --help
backlog task --help
backlog task create --help
backlog task edit --help
backlog doc --help
backlog decision --help
```
