# Agent Handoff Guide

Use this file when asking Codex or Claude to continue work in this repository.

## What To Provide

- Work title
- Character name
- Optional aliases
- Optional reference URLs
- Whether the user already has local images
- The current task stage

## What The Agent Should Do

1. Read `AGENTS.md`.
2. Read `README.md` and `configs/project.yaml`.
3. Check the current intake row.
4. Produce the next artifact only.
5. Leave notes in `logs/` when a decision matters.

## Expected Artifacts

- source plan
- candidate image review sheet
- caption guidance
- tool shortlist
- 10 composition prompts
- checkpoint evaluation sheet

## Response Format For Agents

When an agent finishes, it should report:

- what it changed
- where files are
- what assumptions it made
- what the next step should be

