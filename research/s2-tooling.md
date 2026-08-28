# Research note — Session 2: Python tooling

Verified 2026-08-28. Local test environment: uv 0.12.5, Python 3.14.7. Status legend: VERIFIED / UNVERIFIED / WRONG.

## 1. Claims check

| Claim in SPEC (Session 2) | Status | Evidence |
|---|---|---|
| "Content owned by existing material" (github.com/KnuxV/advanced_programming_python) | VERIFIED (repo exists) | Public repo, default branch `main`, last updated 2025-09-29; contains `lessons/`, `exercices/`, `code-examples/`, `data/`, `Exam.md`. Which lesson covers uv/argparse/env vars: UNVERIFIED (not read in this task — Task 02 should inventory `lessons/`). |
| `uv`: project init, venv, add dependencies, lockfile | VERIFIED locally | `uv init uvdemo` → `pyproject.toml`, `README.md`, `src/`; `uv add polars` → `dependencies = ["polars>=1.44.1"]` in `pyproject.toml` and a `uv.lock`; `uv run python -c "import polars"` works with no manual venv activation. Docs: [uv projects guide](https://docs.astral.sh/uv/guides/projects/). Note `uv init` defaults `requires-python = ">=3.13"` on this machine — the class must pin a Python (`uv python install 3.12` / `uv init --python 3.12`) so lockfiles match across laptops. |
| uv install command | VERIFIED | [installation docs](https://docs.astral.sh/uv/getting-started/installation/): macOS/Linux/WSL `curl -LsSf https://astral.sh/uv/install.sh \| sh`; Windows PowerShell `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"`; also `brew install uv`, `pipx install uv`. |
| Reproducibility is a scientific requirement | VERIFIED (framing) | Same stance as the AEA Data Editor / Vilhuber (see replication note); lockfile = the "pin everything" requirement of the mini-module. |
| `argparse`: notebook → script with arguments | VERIFIED | [Python HOWTO: Argparse Tutorial](https://docs.python.org/3/howto/argparse.html) (official, beginner-paced). Students have 20h Python; positional + one optional flag is the right ceiling. |
| Environment variables: `export`, `.bashrc`, secrets never in code | VERIFIED | Standard; canonical justification [The Twelve-Factor App — Config](https://12factor.net/config). Platform trap: on WSL/Mac the login shell may read `~/.profile`/`~/.zshrc` rather than `~/.bashrc` (macOS default shell is **zsh** → `~/.zshrc`). Session 3 depends on `$UNISTRA_API_KEY` surviving a new terminal — this is the single most likely Session 3 failure. |
| Polars bonus | VERIFIED | `uv add polars` installed 1.44.1; [Polars user guide](https://docs.pola.rs/) live; [Coming from pandas](https://docs.pola.rs/user-guide/migration/pandas/) page is the right bridge for this audience. |

## 2. Best deeper-dive resources

1. [uv docs — Working on projects](https://docs.astral.sh/uv/guides/projects/) — `init`/`add`/`run`/`lock`/`sync` in one page; assign before class.
2. [Python HOWTO — Argparse Tutorial](https://docs.python.org/3/howto/argparse.html) — official, incremental, exactly the notebook→script scope.
3. [The Twelve-Factor App — Config](https://12factor.net/config) — two paragraphs that settle "why env vars"; quotable on a slide.
4. [Polars — Coming from pandas](https://docs.pola.rs/user-guide/migration/pandas/) — the bonus track; expressions vs. chained indexing.
5. *Ambitious:* [The Missing Semester — Shell Tools and Scripting](https://missing.csail.mit.edu/2020/shell-tools/) — variables, `$()`, scripts, `~/.bashrc`; the bridge from "I run commands" to "I automate them". *(lecture page URL UNVERIFIED — the course root is verified live; link the root.)*

## 3. Pedagogical risks

- **The env var doesn't persist**: student sets `export UNISTRA_API_KEY=…` in one window, opens another, Session 3 fails with 401. Mitigation: exercise ends with "close the terminal, open a new one, `echo $UNISTRA_API_KEY | cut -c1-6`"; give the exact file per platform (WSL Ubuntu: `~/.bashrc`; macOS: `~/.zshrc`; Git Bash: `~/.bashrc`).
- **Python version drift**: `uv init` picks the newest Python it finds; lockfiles then differ between laptops and Codespaces. Mitigation: `uv init --python 3.12` in the exercise and a `.python-version` file in the course template.
- **`uv` not on PATH after install** (installer adds to `~/.local/bin`; needs a new shell). Mitigation: same "open a new terminal" ritual.
- **Notebook habits**: `input()`/global state don't survive the move to a script. Mitigation: the exercise starts from a provided notebook with exactly two parameters to lift into `argparse`.
- **Windows path/quoting** for `uv run script.py --file data.csv` in PowerShell vs WSL. Mitigation: WSL only.

## 4. Suggested spec edits

- Session 2, uv bullet: add « pin the interpreter: `uv init --python 3.12`; commit `uv.lock` and `.python-version` ».
- Session 2, env-var bullet: « `.bashrc` » → « the shell startup file for *your* shell (`~/.bashrc` on WSL, `~/.zshrc` on macOS) — verified by opening a new terminal ».
- Session 2, add deliverable: « `UNISTRA_API_KEY` set persistently and `uv` on PATH, checked by `resources/install/check-setup.sh` (Task 03) — this is Session 3's prerequisite ».
- Header: « Content owned by existing material » → add the path to the lesson file(s) in `KnuxV/advanced_programming_python` once inventoried.
