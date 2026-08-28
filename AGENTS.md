# AGENTS.md — Course-building repo

## What this repo is
Source of truth for an 8h course "Advanced Programming for Economists: terminals, APIs, and coding agents". `SPEC.md` is the contract. Everything produced must trace back to a section of the spec.

## Repo layout (do not invent new top-level folders)
- `SPEC.md` — course specification. Read it fully before any task.
- `tasks/` — task definitions for agents. One task at a time.
- `research/` — output of the research task: notes, source lists, deeper-dive material.
- `site/` — MkDocs static site (published to GitHub Pages).
- `slides/` — presenterm decks, one file per session: `s1-git.md`, `s2-tooling.md`, `s3-api.md`, `s4-opencode.md`.
- `exercises/` — one folder per session, numbered exercises with solutions in `solutions/` subfolders.
- `resources/` — ready-to-use configs and payloads (opencode.json for Unistra, curl request.json files, install scripts).

## Standing rules
1. Read `SPEC.md` and the relevant `tasks/*.md` before writing anything. If the task file and SPEC.md conflict, stop and report the conflict; do not resolve it silently.
2. If a required fact is unknown (a URL, a flag, an API behavior), say UNVERIFIED in the output rather than guessing. Never invent URLs, package names, or command flags.
3. Audience calibration: students have never used a terminal. Every command shown must be copy-pasteable and prefixed with where to run it (WSL/Mac Terminal/Git Bash). No unexplained jargon on first use.
4. Language: course materials in English; occasional French asides are fine. Slides terse; site prose complete sentences.
5. All secrets via environment variables. Never write a real API key anywhere, including examples — use `sk-XXXX` placeholders.
6. Verification before done:
   - slides: `presenterm --validate <file>` (or a dry run) must pass.
   - site: `mkdocs build --strict` must pass.
   - code in exercises: must actually run; include the command that proves it.
7. Commit discipline: small commits, one concern each, message states which task and spec section (`s3: add tool-calling exercise (SPEC 3.4)`).
8. Do not touch `SPEC.md` or `tasks/` unless the task explicitly says so.
9. When a task is done, append a short report to `tasks/LOG.md`: what was produced, what is UNVERIFIED, what needs human review.
