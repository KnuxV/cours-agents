# INVENTORY — porting last year's material into the cours-agents site

Written 2026-09-24. Sources, both public and both cloned locally for this pass:

- **Primary** — `github.com/KnuxV/advanced_programming_python`, last year's course site (Jekyll): `lessons/`, `exercices/`, `code-examples/`, `data/`, `Exam.md`.
- **Secondary** — `github.com/KnuxV/slides_cours_git`, the **Génie Logiciel** decks, `Part 1` … `Part 15`. Terser, and it covers what the lessons do not: docstrings, type hints, unit testing, pytest, pdoc, GitHub Actions, licensing.

**Out of scope by instruction:** the data-structures material (`lessons/04-data_structures.md`, `code-examples/03-data_structures/`, `exercices/04-data_structures`). Listed below as *excluded* so the inventory is complete, never read for content — except that one file in the excluded exercise folder is not data-structures material at all (see §6).

Everything I wrote lives under `research/old-site-port/` and touches nothing in `site/`. The proposed destinations assume the `site/docs/reference/` + `site/docs/exercises/` structure that the concurrent site pass is building; each page carries its own nav line and `reference/index.md` row in an HTML comment at the top.

---

## 1. What I produced

| File in this folder | Destination | Size | Sources folded in |
|---|---|---|---|
| `reference/testing.md` | `site/docs/reference/testing.md` | ~600 lines | decks Part 8, Part 9, Part 13 (tests workflow), `Exam.md` §3 |
| `reference/modules-and-packages.md` | `site/docs/reference/modules-and-packages.md` | ~500 lines | `lessons/06-*` (4 of 5 files), deck Part 10, `exercices/08-project_orgs.md` |
| `reference/command-line-arguments.md` | `site/docs/reference/command-line-arguments.md` | ~600 lines | `lessons/07-arguments/071` + `072`, deck Part 11 |
| `reference/docstrings-and-type-hints.md` | `site/docs/reference/docstrings-and-type-hints.md` | ~380 lines | decks Part 6, Part 7, Part 12, Part 13 (docs workflow) |
| `reference/licensing.md` | `site/docs/reference/licensing.md` | ~200 lines | deck Part 14 (850 lines, heavily condensed) |
| `reference/shell-text-tools.md` | `site/docs/reference/shell-text-tools.md` | ~300 lines | `exercices/02-shell/02-shell.md` (lesson half), `lessons/01-shell-intro.md` (paths, wildcards, history) |
| `reference/polars.md` | `site/docs/reference/polars.md` | ~380 lines | `lessons/05-polars_vs_pandas.md`, `code-examples/05-polars_vs_pandas.ipynb` |
| `exercises/shell-data.md` | `site/docs/exercises/shell-data.md` | ~220 lines | `exercices/02-shell/02-shell.md` (questions half) |
| `exercises/project-layout.md` | `site/docs/exercises/project-layout.md` | ~170 lines | `exercices/01-architecture/` |
| `files/grades.csv` | `site/docs/files/grades.csv` | 2.2 kB | `exercices/02-shell/grades.csv`, unchanged |

Every command and every output block in those pages was run on this machine (uv 0.12.10, CPython 3.12.14, pytest 9.1.1, polars 1.44.2, pdoc 16.0.0, mypy current, GNU coreutils). The commands that prove it are in `REPORT.md` §3.

Nine new pages is a lot of site at once. If the instructor wants to stage it, the order of value is: **testing → command-line-arguments → modules-and-packages → docstrings-and-type-hints → shell-text-tools + shell-data → licensing → polars → project-layout.**

---

## 2. `advanced_programming_python` — item by item

### 2.1 `lessons/`

| Item | Verdict | Reasoning | Destination |
|---|---|---|---|
| `01-shell-intro.md` — why the shell, WSL/Git Bash/Mac/ChromeOS install, HOME, absolute vs relative paths, the essential commands, apt/brew, SQLite quick start, "pro tips" | **merge** (in part), rest **drop** | Install and command basics are already better covered by `setup.md`, `reference/wsl.md` and exercise 0.1. What is *not* covered and is worth keeping: absolute vs relative paths, wildcards, command history (++ctrl+r++, `!!`, `$_`, `cd -`). The apt/brew sections are `sudo`-based and contradict the no-`sudo` rule outright; the ChromeOS path is not in SPEC; the SQLite section goes with the SQL exercise (§2.2). | merged into `reference/shell-text-tools.md` §7–8 |
| `02-python-env.md` — pip, venv, requirements.txt, **conda**, real-world workflows, troubleshooting | **merge** (conda only), rest **drop** | `sessions/s2.md` §2 already teaches the classic toolkit better and with the right platform tabs. The one gap is **conda**: students arriving from Anaconda have no page telling them how it relates to `uv`. Suggested three-sentence admonition in `REPORT.md` §5.1, for `s2.md` §2.4. | `sessions/s2.md` §2.4 (text supplied in REPORT) |
| `03-git-version-control.md` — architecture, config, SSH, live coding, branches, conflicts, PRs, .gitignore, commit messages | **drop** | Entirely superseded by `sessions/s1.md` (which is longer and better calibrated), `setup.md` §6 (SSH) and `reference/git-collaboration.md`. Uses `checkout` where the new site standardises on `switch`/`restore`. Nothing unique left. | — |
| `04-data_structures.md` | **excluded** | Instructor's decision. | — |
| `05-polars_vs_pandas.md` — pandas refresher, expression API, SQL-like ops, lazy, streaming, nested types, strings | **port** | The best-written lesson in the old repo, and only its first 20 % survives in `s2.md` §7. Expressions, `over()`, lazy/`scan_csv`, `sink_parquet` and the join trap are all missing from the new site and all useful to both rooms. | `reference/polars.md` |
| `06-organization_packaging/060-var_configs.md` — env vars, `.env`, config.py | **merge** | `s2.md` §6 is a strict improvement (it has the `.env` vs `~/.bashrc` comparison, `git check-ignore`, the three reasons). One idea is missing: **what belongs in `.env` versus what belongs in a plain `config.py`** (secrets and per-environment values vs application constants). One admonition, text in `REPORT.md` §5.2. | `sessions/s2.md` §6.3 |
| `06-…/061-basic_import.md` — module/script/library, `__name__`, `sys.path`, import forms, `import *` | **port** | Nothing on the new site explains `import`, and `s2.md` §5.2 currently says of `if __name__ == "__main__":` *"type it, do not question it yet"*. This is the page that answers it. | `reference/modules-and-packages.md` §1–4 |
| `06-…/062-packages.md` — `__init__.py`, `__all__`, relative imports, `src/` layout, `pyproject.toml`, `[project.scripts]` | **port** | Same. Rewritten around `uv init --package`, which generates the whole layout the lesson described by hand. | `reference/modules-and-packages.md` §5–6 |
| `06-…/063-building_config.md` — `pip install -e .`, `python -m build` | **port** (rewritten) | Two commands, both replaced: `uv run` installs editable by itself, `uv build` produces both artefacts. Kept as a paragraph, with `pip install -e .` named so students recognise it in READMEs. | `reference/modules-and-packages.md` §6–6.1 |
| `06-…/064-publishing_and_refs.md` — PyPI, sdist/wheel, semver, TestPyPI, checklists | **port** (condensed) | Publishing is not a course objective, but it is what demystifies `uv add`. Kept at concept level: global names, versions as promises, a version is forever, publish with a licence. The two checklists were dropped as filler. | `reference/modules-and-packages.md` §6.2 |
| `07-arguments/071-argv_argparse.md` — CLI anatomy, `sys.argv`, argparse, actions, types, choices, groups | **port** | `s2.md` §5 covers one positional and two options; this is the rest, and `s2.md` already links the old file on GitHub — that link should point here instead. | `reference/command-line-arguments.md` §1–5 |
| `07-arguments/072-advanced.md` — subcommands, config/env/flag precedence, verbosity, dry-run, confirmation, output formats, exit codes, "structure for testing" | **port** | The most under-appreciated file in the old repo: `--dry-run`, exit codes and the testable `main(argv)` are exactly the habits Session 4 needs. **Note:** from its line ~954 this file is a verbatim duplicate of `071`; only the first half is unique. | `reference/command-line-arguments.md` §6–9 |
| `07-arguments/seafile-ignore.txt` | **drop** | Sync artefact. | — |

### 2.2 `exercices/`

| Item | Verdict | Reasoning | Destination |
|---|---|---|---|
| `01-architecture/` (statement + `SOLUTION.md` + 7 data files) | **port** (rewritten) | Good 20-minute exercise, and the folder layout it teaches is what makes an `AGENTS.md` rule like "never write in `data/raw/`" expressible. Rewritten so the student *creates* the mess with one command block: no binary blobs to host, works on all five platforms, and the `sudo apt install tree` and `eog` steps disappear (the check uses `find`). Added a part 4 on `.gitignore` + `.gitkeep` and the agent argument. | `exercises/project-layout.md` |
| `02-shell/02-shell.md` | **port**, split in two | The first half is a lesson (redirection, `head`/`tail`/`sort`/`cut`, pipes), the second half is twelve questions. Split accordingly. | `reference/shell-text-tools.md` + `exercises/shell-data.md` |
| `02-shell/grades.csv` | **port** as-is | 50 students, 11 columns, synthetic. Needed by the exercise. | `files/grades.csv` → `site/docs/files/` |
| `02-shell/filename.csv` | **drop** | A four-row throwaway; the page recreates it with `echo` in three lines, which is part of the lesson. | — |
| `02bis-SQL_with_shell_cyberbase/` (13 `.sql` + `cyberchase.db` + instructions, in French) | **link only** | Genuinely good ("do the whole thing from the terminal"), and students have 15 h of SQL — but no SPEC session covers SQL, the instructions are French-only where the site is English, and they require `sudo apt install sqlite3` plus `micro`. Salvaged: a no-`sudo` way to run a query without the sqlite3 CLI, in `REPORT.md` §5.3. Instructor decision if it should become an optional exercise page. | link from `resources.md` |
| `03-git/03-detective_story.md` — `git log`/`show`/`diff` archaeology on a novel | **link only** | Charming, and the same skill as the published exercise 1.1 (*Recipe history*), which is already rehearsed and has a solution. Keep as an alternative the instructor can swap in; it lives in `gitlab.unistra.fr/cours_git/story_editing_exercise`. | link from `exercises/index.md` |
| `03-git/04-scrabble_git_exercice.md` | **already ported** | It is `site/docs/exercises/scrabble-three-merges.md`. No action. | — |
| `03-git/05-pull_requests.md`, `05bis-pull_requests_duo.md` | **drop** | Superseded by exercise 1.3 *Collaboration in teams of two* (rehearsed, with a solution) and `reference/git-collaboration.md`. The old version's "contribute to the course repo for bonus points" mechanism is not part of this course. | — |
| `04-data_structures/03-two_sums.md`, `04-netflix.ipynb`, `05-network.ipynb` | **excluded** | Instructor's decision. | — |
| `04-data_structures/06-country_class.md` — build a `Country` class around a REST API | **flag** | Sitting in the excluded folder, but it is an **OOP + HTTP API** exercise, not data structures. It may have been excluded by accident. See §6. | instructor decision |
| `05-sql_classes/01-departement_sql_class.md` — analytics with a SQLAlchemy ORM | **flag** | See §6. | instructor decision |
| `08-project_orgs.md` — the `texttools` module→package→installable progression | **merge** | Its five steps are the spine of `reference/modules-and-packages.md` §5 (same `texttools` name, working code, real outputs). It would also make a good exercise 2.6 if the instructor wants one — the page's §5–6 can be lifted into a statement in ten minutes. | merged into `reference/modules-and-packages.md` |
| `09-password_generator/` — instructions, starter code, wordlist | **merge** | The new site already has exercise 2.3 on the real `KnuxV/password-generator` repo, which is better (fork, `uv sync`, two branches). Worth lifting from the old version: the **xkcd 936 framing** (why word-based passwords), and **Part 1 = `sys.argv`, Part 2 = `argparse`**, which makes the "why argparse" argument by experience. Suggested two-sentence addition in `REPORT.md` §5.4. The EFF/Google wordlist download links were not re-checked and are not carried over. | `exercises/password-generator.md` intro |

### 2.3 `code-examples/`, `data/`, site machinery

| Item | Verdict | Reasoning |
|---|---|---|
| `02-demo_venv.md` — instructor's live-demo checklist | **drop** | Teacher notes, not student material; `sudo apt install python3-venv`/`snap install micro` throughout; superseded by `s2.md` §2 and `slides/s2-tooling.md`. |
| `02-git/03-git-demo.md`, `03-git-tokens.md`, `03-ssh-demo.md` | **drop** | Same: instructor checklists. SSH and tokens are now `setup.md` §6 and `s1.md` §6.2. |
| `03-data_structures/*` | **excluded** | Instructor's decision. |
| `04-class_for_sql/01-sql_python_recap.ipynb` — `sqlite3`, cursors, `fetchall`, `pd.read_sql_query` | **flag** | See §6. The `pd.read_sql_query` recap is the only part with a use outside OOP. |
| `04-class_for_sql/02-orm_classes_sql.ipynb` — SQLAlchemy ORM, `select`, joins, aggregations | **flag** | See §6. |
| `04-class_for_sql/data/villes_france.db`, `data/villes_france.db` | **flag** | 
Goes with the above. Two copies of the same database in the old repo. |
| `05-polars_vs_pandas.ipynb` — Titanic + SQLite live coding | **merge** | Source of the examples in `reference/polars.md`, which uses `sales.csv` instead so nothing has to be downloaded. The notebook itself can be linked for anyone who wants the Titanic version. |
| `.ipynb_checkpoints/` | **drop** | Jupyter artefact. |
| `data/conte.txt` — a French tale | **drop** | Not referenced by any lesson or exercise I could find. If it was a text-processing input, `sales.csv` and `grades.csv` cover the same need in English. |
| `data/xkcd-password-strength.png` | **link only** | Do not re-host the comic; link `xkcd.com/936` from the password-generator exercise. |
| `Exam.md` — "Final Project: Building an AI Agent with Tools" (teams of 3, database + API + analysis + report tools, movie-recommender worked example) | **flag / link only** | See §6. This is *not* the same exam as the deck's Part 15. |
| `index.md`, `README.md`, `_config.yml`, `_data/navigation.yml`, `_includes/`, `_layouts/`, `assets/`, `Gemfile`, `.gitignore`, `.seafileignore`, `convert_md_to_ipynb.py` | **drop** | Jekyll site machinery and a one-off conversion script. The new site is MkDocs Material. |

---

## 3. `slides_cours_git` — item by item

This is the **Génie Logiciel** course, not last year's Advanced Programming. Porting from it merges two courses into one site; the material is worth it, but the instructor should know that is what is happening (`REPORT.md` §4.3).

| Item | Verdict | Reasoning | Destination |
|---|---|---|---|
| `Part 1 - Introduction & Setup` | **drop** | Superseded by `setup.md` (which has five platform paths and no `sudo`). | — |
| `Part 2 - Basic Commands & First Repository` | **drop** | Superseded by `s1.md` §4 and `slides/s1-git.md`. | — |
| `Part 3 - Remote Repositories & Collaboration` | **drop** | Superseded by `s1.md` §6 and `reference/git-collaboration.md`. | — |
| `Part 4 - Branches` | **drop** | Superseded by `s1.md` §5, which has mermaid diagrams for the three merge cases. | — |
| `Part 5 - Virtual Environments` | **drop** | Superseded by `s2.md` §2–4. | — |
| `Part 6 - Docstrings` | **port** | Nothing on the new site mentions docstrings, and they are the cheapest context you can give a model. | `reference/docstrings-and-type-hints.md` §1 |
| `Part 7 - Type Hints` | **port** | Same. The typing-spectrum slides (JavaScript, Java) are cut to two sentences; the mypy demonstration is replaced by a run that shows mypy silent on unhinted code and correct on hinted code. | `reference/docstrings-and-type-hints.md` §2 |
| `Part 8 - Unit_testing` | **port** | The concepts half of the testing material: why, TDD, CI, the pyramid. | `reference/testing.md` §1–2, §10–11 |
| `Part 9 - Pytest` | **port** | The practice half: assert, parametrize, fixtures, `tmp_path`, `capsys`, coverage. **Highest-value item in either repo** — SPEC §4.3 makes the test suite the anchor of agent reliability and no session teaches it. | `reference/testing.md` §3–9 |
| `Part 10 - __main__` | **port** | Folded in as the explanation `s2.md` currently defers. | `reference/modules-and-packages.md` §3 |
| `Part 11 - arguments` | **port** | The terser twin of `lessons/07`; used to decide what the session needs versus what the reference page needs. | `reference/command-line-arguments.md` |
| `Part 12 - pdoc` | **port** | Docstrings → a published website, in one command. Good payoff for the docstring habit, and a natural bridge to Pages. | `reference/docstrings-and-type-hints.md` §4 |
| `Part 13 - github_actions` | **merge** | `reference/git-collaboration.md` §5 already introduces CI conceptually, so a third page would duplicate it. The concrete workflows go where they are used: the tests workflow in `reference/testing.md` §9, the pdoc/Pages workflow in `reference/docstrings-and-type-hints.md` §4.1. Both rewritten for `uv` from the official published workflows, not from the deck's `pip install pytest`. | two pages |
| `Part 14 - licensing` (850 lines) | **port** (condensed to ~200) | Completely absent from the new site, needed the day a student makes a repository public, and the "who pays for open source" part is a genuine economics lesson. Every monetary figure and market-share percentage was **dropped** as unverified (`REPORT.md` §4.1). Added: a section on what "open" means for a model, which the original could not have had. | `reference/licensing.md` |
| `Part 15 - exam` (French, with the 20-point rubric) | **flag** | See §6. | instructor decision |
| `index.md`, `README.md`, `header.html`, `obsidian-theme.css`, `img/*.png`, `exam.html`, `exam_génie_logiciel_2026.pdf`, `.github/workflows/pages.yml` | **drop** | reveal.js machinery, a rendered copy of `Part 15`, and a deploy workflow that uses `sudo apt-get install pandoc`. The three branch images are reveal-specific and the new site draws its branch diagrams with mermaid. | — |

---

## 4. Where the merges land (for the pass that edits `site/`)

Nothing below was applied — `site/` belongs to another pass. Full text for each is in `REPORT.md` §5.

| Target | Change | Source |
|---|---|---|
| `sessions/s2.md` §2.4 | add a "What about conda?" admonition | `lessons/02-python-env.md` |
| `sessions/s2.md` §5.2 | replace *"type it, do not question it yet"* with a link to `reference/modules-and-packages.md` §3 | deck Part 10 |
| `sessions/s2.md` §5.3 | repoint the "last year's complete class guide" GitHub link at `reference/command-line-arguments.md` | `lessons/07` |
| `sessions/s2.md` §6.3 | add one line on `.env` (secrets, per-environment) versus `config.py` (constants) | `lessons/06-…/060` |
| `sessions/s2.md` §7 + `Going further` | link `reference/polars.md`; repoint the old-lesson link | `lessons/05` |
| `sessions/s4.md` §4.3 | this section's reading is `reference/testing.md`; the `AGENTS.md` example in §10 of that page is ready to reuse | decks Part 8–9 |
| `exercises/password-generator.md` | add the xkcd 936 framing and an optional `sys.argv`-first step | `exercices/09` |
| `exercises/index.md` | rows for 0.2 (`shell-data.md`) and 0.3 (`project-layout.md`) | — |
| `reference/index.md` | a new "Python and quality" section (five rows) and a "Publishing and sharing" section (one row); one row added to "Machines and terminals" | — |
| `resources.md` | links to the SQL-in-the-shell and detective-story GitLab exercises | — |

---

## 5. Counts

| Verdict | Items |
|---|---|
| **port** (a new page, or a large part of one) | 13 source items → 9 pages |
| **merge** (into an existing page) | 6 |
| **link only** | 4 |
| **drop** | 23 |
| **excluded by the instructor** | 5 |
| **flagged for a decision** | 7 (§6) |

---

## 6. The decisions I did not take

Detailed in `REPORT.md` §4. In short:

1. **OOP / classes / SQL-ORM** (`code-examples/04-class_for_sql/` ×2 notebooks + the `villes_france.db` database, `exercices/05-sql_classes/`, and `exercices/04-data_structures/06-country_class.md` which is an OOP exercise misfiled in the excluded folder). My recommendation: **do not port as taught material**, keep the `sqlite3`-with-Python recap as an optional page if anything, and revisit only if Session 4's projects need a class. Not silently included, not silently dropped.
2. **`Exam.md`** (the AI-agent-with-tools project brief) and **deck `Part 15`** (the Génie Logiciel rubric: git 4, documentation 4, tests 4, licence 1, README 1, justifications 3). Both are assessment documents for other course formats, and SPEC's exam is a presentation. They need the instructor, not me.
3. **Whether testing belongs in a session at all.** I put it in `reference/`, because no session has room for it, and pointed Session 4 §4.3 at it. If the instructor wants it taught rather than referenced, the page's §3–7 is a 45-minute class.
