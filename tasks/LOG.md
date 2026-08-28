# tasks/LOG.md

## Task 01 — Research (2026-08-28)

**Produced:** `research/s0-setup.md`, `s1-git.md`, `s2-tooling.md`, `s3-api.md`, `s4-opencode.md`, `replication-module.md`, `teacher-prep.md`. Every link was fetched (HTTP 200); paywalled Cunningham posts are cited as evidence but flagged, never as student links. Endpoint facts were tested live with the instructor's `$UNISTRA_API_KEY` (no key written anywhere).

**WRONG claims found**
1. AGENTS.md rule 6 / Task 02: `presenterm --validate <file>` — the flag does not exist in presenterm 0.16.1. Nearest equivalents: `presenterm -E <file>` (HTML export) or `--validate-overflows`; both require an interactive terminal (they hang / `Inappropriate ioctl` when run non-interactively). Conflict between AGENTS.md and reality — reported, not resolved.
2. SPEC 4.1 "documented fallbacks for Git Bash" for OpenCode — OpenCode docs state no native Windows support (WSL recommended). Git Bash cannot be the Session 4 fallback; Codespaces can.
3. SPEC Session 0 deliverable command `uname -a && curl --version | head -1` fails in PowerShell; must be run inside the Ubuntu/WSL window (wording fix).
4. SPEC 4.4 "restricted tools" — OpenCode's `tools:` field is deprecated in favour of `permission:` (terminology fix, config-breaking if copied).

**Key VERIFIED facts (load-bearing):** tool calling (`tools` → `tool_calls`, and the `role: tool` round trip) works on the Unistra endpoint for all 7 chat models; model IDs `coder`, `qwen3`, `gpt-oss`, `mistral-small`, `ministral`, `gemma` (+ aliases); served context 262144 / 262144 / 131072 / 128000 / 32768 / 262144; OpenCode 1.18.22 runs the loop against `unistra/coder` headlessly (bash + write observed).

**Top 3 pedagogical risks**
1. LiteLLM fallback chains (`gpt-oss → gpt-oss-ilaas → ministral`, etc.) can silently serve Ministral 3B / 32k context under load while reporting the requested model name — wrecks the agent loop and the "which model" lesson. Ask DNUM whether fallbacks apply to API keys.
2. WSL install failures on student laptops (BIOS virtualization off = 0x80370102; managed laptops without admin) — needs an in-person clinic and a Codespaces image with OpenCode preinstalled.
3. Environment variable persistence (`~/.bashrc` vs `~/.zshrc`; new-terminal test) — the most likely cause of 401s in Session 3; `check-setup.sh` (Task 03) must test it in a fresh shell.

**Single most important unresolved UNVERIFIED item:** classroom-scale load on the Unistra endpoint — 20 concurrent requests passed with no rate-limit headers, but 30 students running multi-step tool-calling on the 80B coder is untested, and the fallback behaviour under that load is unknown. Rehearse a burst test with DNUM's knowledge before Session 3.

**Other UNVERIFIED (for Task 02/03):** max output tokens per model (needed for OpenCode `limit.output`); student (vs staff) eligibility for API keys; one-key-per-account rotation on Unistra; `opencode run` behaviour with `ask` permissions; `top_k` forwarding; which lesson files in KnuxV/advanced_programming_python cover uv/argparse/env vars; GitHub Education Codespaces bonus; Missing Semester shell-tools lecture URL.

**Needs human review:** the suggested spec edits in §4 of each note (not applied); whether to keep Git Bash as a Session 1–3-only fallback; whether the Cunningham paywalled posts can be excerpted on the site.

## Task 02 — Site & decks, **Session 0 scope only** (2026-08-28)

Run restricted by the instructor to the s0 class. Produced the site scaffold + the full setup page; no deck (Task 02 lists no s0 deck — the "why the terminal" Day-1 rationale is in `setup.md` §7 and belongs in `slides/s1-git.md` when that deck is built).

**Produced**
- `site/mkdocs.yml` (stock Material, indigo, copy buttons, tabs, `pymdownx.keys`, anchor/link validation set to `warn` so `--strict` catches broken `#anchors` too), `site/requirements.txt` (`mkdocs-material==9.7.7`, current on PyPI today), `site/.gitignore`.
- `site/docs/index.md` — pitch from SPEC thesis, schedule table, needs, exam, links.
- `site/docs/setup.md` — Session 0 page: path chooser; Path A WSL (winver check, Task-Manager virtualization check *first*, admin PowerShell install, first-launch user/password, "Ubuntu window not PowerShell" warning, error-code table from `research/s0-setup.md`, files-in-`~` habit); Path B Mac (Xcode CLT trigger via `git --version` at home); Path C Codespaces (blank template, VS Code web terminal); Path D Git Bash + Scoop (Sessions 1–3 only, OpenCode-on-Windows caveat); §5 API key (Profil → Réglages → Compte, per-shell startup file `~/.bashrc`/`~/.zshrc`, new-window test `cut -c1-6`, live `/api/models` ping with real truncated output and the real 401 body); §6 forum deliverable (six characters, never the key); §7 ten-minute terminal warm-up (mv/cp/ls/pwd per SPEC S0 exercise); §8 clinic; top-5 resources from the research note.
- Stubs `sessions/s1–s4.md`, `exercises.md`, `resources.md`, `replication.md` — each a single "Not built yet" admonition, so the nav is final and the build is strict now. To be overwritten by the remaining Task 02 runs.
- `.github/workflows/site.yml` — mkdocs-material's recommended workflow (checkout@v4, setup-python@v5, cache@v4 weekly key, `gh-deploy --force`), pinned via `requirements.txt`, plus a `mkdocs build --strict` gate before deploy, `working-directory: site`.

**Verification:** `cd site && uvx --from mkdocs-material==9.7.7 mkdocs build --strict` → exit 0, 0 warnings. Workflow YAML parses. Live checks done from this machine with the instructor's key (nothing written): `/api/models` returns `{"data":[{"id":"bge-m3",…` ; a wrong key returns `{"detail":"Your session has expired or the token is invalid…"}` — both quoted in setup.md. Scoop install commands checked against github.com/ScoopInstaller/Install; Codespaces blank-template steps checked against docs.github.com; mkdocs-material workflow checked against its publishing page.

**TODO(verify) markers on the site (8)**
- index: forum link; fresh repo URL (also `repo_url`/`site_url` commented out in `mkdocs.yml`); session dates ×4 + clinic date/room + exam rubric are plain `TODO:`.
- setup: student (vs staff) eligibility for API keys (blocking — confirm with DNUM before publishing); Codespaces idle-stop/deletion defaults (30 min / 30 days written from memory, not from the fetched page); GitHub Education Codespaces bonus; key regeneration = rotation on Unistra; forum link; `check-setup.sh` link (Task 03).

**UNVERIFIED but stated without a marker (judged safe):** VS Code web terminal shortcut ++ctrl+grave++ / menu path; Windows Terminal preinstalled on Win 11 (worded as "if you don't have it, Microsoft Store"); Git Bash `MINGW64_NT` first line of `uname -a`.

**Needs human review before first deploy**
1. This folder is **not a git repository** (no `git init` done — SPEC says a fresh repo/remote will be created; commit-discipline rule 7 could not be applied). Once created: enable Pages → branch `gh-pages` after the first workflow run, and set `site_url`.
2. Whether Path D (Git Bash) should stay on the page at all, given the Session 4 constraint — it is currently framed as "last resort, Sessions 1–3 only, prefer Codespaces".
3. Menu labels in §5.1 are quoted in French from the Unistra doc (Profil / Réglages / Compte / Générer une nouvelle clé); confirm on a student account.
4. `presenterm --validate` conflict (Task 01 LOG) still open; no deck was validated in this run.

### Task 02 s0 — revision after instructor review (2026-08-28)

Instructor decisions applied (these deviate from SPEC Session 0 on purpose; SPEC not edited, rule 8):
- **No forum deliverable** — `setup.md` §6 removed; index schedule now says "your terminal passes the check command". SPEC still mentions the forum post.
- **No install clinic** — `setup.md` §8 and every clinic mention removed from the site and this log. SPEC still mentions it (Session 0 bullet + Known risks).
- **Git Bash stays**, first-class for Session 1: Path D reframed as "quickest way to git + bash on Windows, fine for S1–S3, WSL/Codespaces needed by S4"; path table and A2 fallback text updated accordingly.
- **Student API-key access confirmed** by the instructor → `TODO(verify): student access` admonition removed.
- Repo pushed as `KnuxV/cours-agents`: `repo_url`/`site_url` set in `mkdocs.yml`, index links the repo. Pages source (`gh-pages`) still to be enabled after the first workflow run.

Remaining TODO(verify) on the site: forum link (index), Codespaces idle/deletion defaults, GitHub Education bonus, key regeneration = rotation, `check-setup.sh` link. Plain `TODO:` for session dates and exam rubric.
