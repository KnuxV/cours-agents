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

### Task 02 s0 — dates + WSL page (2026-08-28)

- Session dates/room taken from `~/Documents/plan-2026-autumn/overview.md` ("Adv programming & dataviz (M2 DS2E)", 4 × 2h, A330 Idem-Lab): S1 Mon 14 Sep 14–16, S2 Fri 18 Sep 15–17, S3 Fri 25 Sep 14–16, S4 Fri 16 Oct 13–15. Setup deadline = before 14 Sep. Needs human check: the plan has 4 slots for this course (the instructor said "8 classes" — read as 8 hours); the 6 Thursday slots are the other course (GL, M2 TDL) and were not used.
- New page `site/docs/wsl.md` (nav: Session 0 → "WSL, explained"): what WSL is, why the course uses it, vocabulary + "which window am I in", opening/closing, **the two file systems** (slashes, case sensitivity, `~` vs `C:\Users`, the `/mnt/c` and `\\wsl$` bridges, `explorer.exe .`, where to keep work), installing with `apt`, editing (`nano`, VS Code + WSL extension), managing WSL from PowerShell, virtualization check, troubleshooting table (moved here from setup.md). Facts checked against MS Learn *Working across file systems* and *VS Code with WSL* pages; the rest is from `research/s0-setup.md`.
- `setup.md` Path A cut to the why + `wsl --install` + first launch + open Ubuntu + check command, linking to the WSL page for everything else.

## Task 02 — Site, **Sessions 1 and 2** (2026-08-28)

Run restricted by the instructor to the git and tooling classes, **site only — no decks** (`slides/s1-git.md`, `slides/s2-tooling.md` still to build; both pages say "Slides: to be published").

**Produced**
- `site/docs/sessions/s1.md` (~4,300 words) — goals; before-class (GitHub account at home, `git --version` per platform); why-git-doubly-now with the two agent-era rules (commit before the agent touches the repo; `git diff` is the review); three-places mental model; one-time `git config` (name, email, `init.defaultBranch main`, `core.editor nano`); hands-on on the Riverside Coding Club practice site (init → add/commit → diff/log/show → three levels of `restore` incl. `--source` → `.gitignore`); branches lightly (`switch -c`, fast-forward merge, conflict deferred to stretch); GitHub (login via `gh auth login`, empty remote, `push -u`, edit-on-GitHub → `pull`, `push`); §7 the deliverable = personal `cours-agents` repo with a `.gitignore` pre-seeded for S2 (`.venv/`, `.env`, `__pycache__/`); troubleshooting table; cheat sheet; exercises list; top-5 resources from `research/s1-git.md`. Content adapted from `~/Codebase/fake-website-to-teach-git/` lessons 0–6 and 8 (commands cross-checked against them; `switch`/`restore` primary, `checkout` as recognition only, as in that course).
- `site/docs/files/practice-site/` (4 files, copied verbatim from `~/Codebase/fake-website-to-teach-git/practice-site/`) and `site/docs/files/practice-site.tar.gz` (built with `tar --owner=0 --group=0 --mtime='2026-08-28 00:00' -czf practice-site.tar.gz practice-site` from `site/docs/files/`; **rebuild it if the folder changes**) and `practice-site.zip` (same content, built with Python's `zipfile`, fixed timestamps; for students whose `curl | tar` line fails — they download it in the browser and unzip by double-click; rebuild both archives together). Students fetch with `curl -L …/files/practice-site.tar.gz | tar xz` — chosen over zip because `unzip` is not guaranteed on WSL/Git Bash while `tar xz` works on all four paths.
- `site/docs/sessions/s2.md` (~3,300 words) — why reproducibility (three layers → `.python-version` / `pyproject.toml` / `uv.lock`); install uv per platform; `uv init --no-package --python 3.12` in place in the course repo, `uv run`, `uv add polars`, `uv sync`, commit; notebook cell → `report.py` with `argparse` (positional + `--top` int + `--product`), the four runs (`--top 2`, `--help`, missing arg, bad type); env vars (`export` vs startup file, `os.environ.get` with a loud failure, three reasons a key never goes in code, `.env`/dotenv mentioned as last year's alternative); Polars bonus table; deliverable checklist; troubleshooting; cheat sheet; exercises; top-5 resources from `research/s2-tooling.md`.
- `site/docs/files/sales.csv` (9 rows, **synthetic**, labelled as invented) and `site/docs/files/report.py`.
- `site/docs/exercises.md` — index table with tags/times; full statements + collapsed solutions for 0.1, 1.1–1.5, 2.1–2.4 (Task 03's minimum set for s1/s2 plus the S1 deliverable as 1.3). S3/S4 rows say "published with Session 3/4".
- Stub wording on `s3.md`, `s4.md`, `resources.md`, `replication.md` updated ("not written yet; Task 02 has covered Sessions 0, 1 and 2"). `resources.md` stays a stub: `resources/` only holds `links.md` until Task 03 delivers the configs/payloads.

**Verification**
- `cd site && uvx --from mkdocs-material==9.7.7 mkdocs build --strict` → exit 0, 0 warnings (anchors validated too; one broken relative link caught and fixed during the run).
- Every uv/argparse/env-var command and every expected output on `s2.md` was run on this machine (uv 0.12.5, Python 3.12.14 managed by uv, polars 1.44.1) in the scratchpad; outputs quoted verbatim. Findings that changed the page: **uv ≥ 0.12 defaults to a `src/` package layout with a build system** (docs confirm: "Prior to v0.12, uv did not define a build system for applications by default"), so the page uses `--no-package` to get the flat `main.py` layout; `uv init` inside an existing git repo creates no `.gitignore` (hence the pre-seeded one in S1 §7); `.venv/.gitignore` contains `*` (belt-and-braces claim on the page is true).
- Git commands cross-checked against the fake-website lessons and git 2.55 locally; the merge-conflict recipe in 1.4 follows lesson 0008's two-branches-same-line design.
- `gh` on Ubuntu: `packages.ubuntu.com` confirms `gh 2.45.0` in noble (24.04) and 2.4.0 in jammy (22.04). `gh auth login` prompt sequence and the "Authenticate Git with your GitHub credentials?" step are from the gh manual page (fetched) and memory of the current CLI — **not rehearsed on a clean WSL** (docker unavailable in this session: socket permission denied). Needs the rehearsal the research note asked for.
- All 30 external links used return HTTP 200 (`github.com/signup` returns 403 to curl — bot protection; it is the same link the setup page already uses).

**TODO(verify) markers added (5)**
- s1 §8: GitHub personal-access-token menu path (fallback if `gh auth login` fails).
- s1 exercises 5 / exercises.md 1.5: clone URL of the recipe-history repo (`~/Codebase/fake-website-to-teach-git/exercises/01-recipe-history/repo/`, 8 commits, ready to push — Task 03 or the instructor).
- s2 §2: Git Bash finds `uv` after the PowerShell installer (PATH inheritance) — needs a Windows laptop.
- s2 §7: `check-setup.sh` link (Task 03).
- s2 exercises 3 / exercises.md 2.3: the "bad repo" starter for the secret-hygiene audit (Task 03).

**Stated without a marker, judged safe:** `explorer.exe index.html` opens the file with the Windows default browser from WSL; `start index.html` in Git Bash; Codespaces auto-forwards `python3 -m http.server 8000` with an *Open in Browser* prompt; Git Bash's bundled credential manager opens a browser on first push (from the fake-website lesson 8, written for that path); `gh` preinstalled and logged in inside Codespaces.

**Deviations from SPEC / research notes, for human review**
1. GitHub account creation is asked for **at home before S1** (page: "Before class"), while SPEC Session 1 says "account creation = course outcome". Research s1 §4 suggested exactly this move; SPEC not edited (rule 8). Index still says "created in Session 1 if you do not have one" — consistent enough, but decide.
2. First-push authentication fixed to **one path: `gh auth login`** (apt on WSL, `.pkg` on Mac, nothing on Git Bash/Codespaces), PAT as documented fallback. Research recommended "one documented path, rehearsed on clean WSL"; the rehearsal is still owed.
3. Codespaces students are told to create the course repo on GitHub *with* a README and open a codespace on it (so push is authenticated), i.e. the opposite of the "empty remote" rule used for everyone else. Practice-site work happens in `~` there.
4. S2 pins **Python 3.12** and commits `.python-version` (research s2 §4 suggestion, applied on the page; SPEC silent).
5. The S1 page sends S1 users to `nano`/VS Code without a dedicated editor section; if a Windows-VS-Code-with-WSL walkthrough is wanted, `wsl.md#editing-files` is where it lives.
6. `site/docs/files/` now holds student-facing starter files (practice site, csv, script). AGENTS.md lists `exercises/` for exercise material; these were placed under the site so they are downloadable by URL from the published page. Task 03 may prefer to move/duplicate them under `exercises/s1/` and `exercises/s2/` — if so, update the `curl` URLs in s1 §4.1 and s2 §4.1.
7. Pages are long (≈4k and 3k words). SPEC/Task 02 say "site prose complete sentences" and "the site holds the prose", so this is intended; the decks must be the terse counterpart.

- 2026-08-28, instructor review: S1 §8 "When things go wrong" removed (cheat sheet is now §8); the PAT fallback is one sentence in §6.1. The Git Bash CRLF note and the `Updates were rejected` recipe went with it.

### Task 02 S1 — restructure after instructor review (2026-08-28, afternoon)

Instructor decisions applied:
- **S1 §6 (GitHub walkthrough) removed.** The only GitHub steps left in class are inside §6 "The deliverable": `gh auth login` (per-platform tabs), create an empty repo, `git remote add` + `git push -u`. Push is kept because the deliverable is on GitHub in the SPEC and S2's clone/`uv sync` exercise depends on it.
- **S1 §5 goes deeper on merging**, with mermaid diagrams (`pymdownx.superfences` custom fence added to `mkdocs.yml`; Material renders them client-side): branch = pointer; case 1 fast-forward (`main` has not moved); case 2 merge commit with two parents (`main` moved, different lines — done live on the practice site with `footer-year` vs a contact-email commit); case 3 conflict (same line) — marker anatomy and the edit/add/commit resolution, practised in exercise 1.2. Diagrams render-checked in Chrome on the built site (six on s1, one on s1-collab).
- **New page `sessions/s1-collab.md` "Session 1½ — Git as a collaboration tool"**, reading at home (~40 min, nothing to hand in; nav entry after S1): remotes and `origin` (several remotes, GitLab), clone vs fork (+`upstream`, syncing), the PR loop (GitHub flow, review, merge flavours, MR on GitLab, conflicts in PRs), issues (as audit trail; link to the replication track), CI/CD (GitHub Actions, the course site's own `site.yml` as the example, a minimal `uv`+pytest workflow shown for recognition), what it means for agents (branch → diff review → CI → merge), vocabulary table, optional GitHub Skills hands-on. All GitHub/GitLab/Pro Git links fetched (200).
- **Student repository renamed `cours-agents` → `agent-lab`** everywhere (S1 §6, S2, exercises), to avoid a clash with the course repo of the same name.
- **S1 exercises replaced** by the instructor's prepared repositories, now published (public) under the instructor's GitHub account with `gh repo create` from this session:
  - `github.com/KnuxV/recipe-history` — the 8-commit crêpe repo from `~/Codebase/fake-website-to-teach-git/exercises/01-recipe-history/repo/` (+1 commit pointing the README at the site). Exercise 1.1 [core]: clone, `git remote -v`, the refused push (meaning of `origin`), history reading, `restore --source` trap.
  - `github.com/KnuxV/scrabble-counter` — from `~/Codebase/fake-website-to-teach-git/exercises/scrabble_counter/` (`main`, 6 original commits) **plus commits/branches built in this session**: on `main`, `.gitignore` and a root `conftest.py` (the tests did not import `score` when run from the repo root — `ModuleNotFoundError`; with `conftest.py`, 52 pass); three branches off the same tip: `add-readme` (README only → fast-forward), `german` (DE values + tests appended → merge commit), `portuguese` (PT values + tests inserted elsewhere → conflicts with `german` in exactly two hunks of `score.py`: the language dict and the `choices=` line; the tests file auto-merges). Exercise 1.2 [core]. Rehearsed end to end: ff → `Merge made by the 'ort' strategy` → `CONFLICT (content)`; after the documented resolution `56 passed`, `HALLO -l DE` = 9, `CASA -l PT` = 5. German/Portuguese letter values are the standard editions' (from memory; only used as exercise data).
  - The local originals were given `origin` remotes and fast-forwarded to match GitHub; `scrabble_counter` also has local tracking branches for the three exercise branches. Its untracked `AGENTS.md` and `.opencode/` (instructor's Session 4 material) were left alone and are now in the published `.gitignore`.
  - 1.3 [core] the `agent-lab` deliverable; 1.4 [stretch] fork vs second remote (`mine`, `upstream`); 1.5 [home] the S1½ reading. The practice site stays as the in-class walkthrough (§4–5), not an exercise.
- Push from this machine went over HTTPS with `gh auth git-credential` (the SSH key is a hardware key needing a passphrase; `gh` had set SSH remotes by default).

**Verification:** `mkdocs build --strict` exit 0, 0 warnings; anonymous `git clone` of both repos tested; all merges rehearsed in a throwaway clone; diagrams inspected in a browser.

**Still TODO(verify) on the site:** Git Bash `uv` on PATH; `check-setup.sh` link; the secret-hygiene starter repo (2.3). Removed: the recipe-history clone URL marker (now real).

**Needs human review:** 1.2 asks students to run `python3 score.py` — no `python3` on Git Bash; the page says to skip until Session 2. Whether exercise 1.2 fits in class alongside 1.1 and the deliverable (≈70 min of exercises for a 2h session that also has §4–5 live) — tags may need to move 1.2 to [home].
