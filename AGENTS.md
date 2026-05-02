# Agent Guide

This repository is a local ACG character image experiment workspace.

Maintainer note: this guide was updated by Codex / GPT-5 on 2026-05-02.

## Read First

1. `README.md`
2. `docs/current_project_handoff.md`
3. `docs/06_project_knowledge_notes.md`
4. `docs/character_ai_pipeline_sop.md`
5. `configs/project.yaml`
6. `docs/01_data_collection_pipeline.md`
7. `docs/03_tool_setup_plan.md`
8. `docs/04_generation_test_plan.md`
9. `templates/character_intake.csv`
10. `templates/dataset_review_sheet.csv`

## Core Rules

- Treat everything as local experiment work only.
- Prefer ASCII in new files unless the file already uses non-ASCII text.
- Keep changes small, explicit, and easy to hand off.
- Write outputs into `outputs/` and notes into `logs/`.
- Do not assume one specific franchise. The workflow should work for any ACG work or character.

## Standard Workflow

1. Read the intake row for the work title and character name.
2. Build a source plan.
3. Collect candidate images or ask the user for local files if needed.
4. Review and reject weak images.
5. Caption the final set.
6. Train one first-pass LoRA.
7. Run the 10 composition tests.
8. Record the result and next tuning step.

## Output Contract

When you finish a task, leave behind:

- what changed
- where the result lives
- what the next agent should do next
- any assumptions or unknowns

## Good Handoff Shape

- Inputs used
- Files changed or created
- Decisions made
- Open questions
- Next step
