# REPORT — porting last year's material

2026-09-24. Companion to `INVENTORY.md` (read that first: it holds the verdict for every file in both source repositories). This document is what a `tasks/LOG.md` entry would need — the main session writes that entry, not this pass.

## 1. What was produced

Nine finished MkDocs pages plus one data file, all under `research/old-site-port/`, mirroring the tree they are meant to move into so that relative links keep working after a `git mv`:

```text
research/old-site-port/
├── INVENTORY.md                            ← read first
├── REPORT.md                               ← this file
├── reference/
│   ├── testing.md                          → site/docs/reference/testing.md
│   ├── modules-and-packages.md             → site/docs/reference/modules-and-packages.md
│   ├── command-line-arguments.md           → site/docs/reference/command-line-arguments.md
│   ├── docstrings-and-type-hints.md        → site/docs/reference/docstrings-and-type-hints.md
│   ├── licensing.md                        → site/docs/reference/licensing.md
│   ├── shell-text-tools.md                 → site/docs/reference/shell-text-tools.md
│   └── polars.md                           → site/docs/reference/polars.md
├── exercises/
│   ├── shell-data.md                       → site/docs/exercises/shell-data.md
│   └── project-layout.md                   → site/docs/exercises/project-layout.md
└── files/
    └── grades.csv                          → site/docs/files/grades.csv
```

Each page opens with an HTML comment naming its sources, its proposed destination, **its exact nav line** for `site/mkdocs.yml`, **its row** for `site/docs/reference/index.md` (or `exercises/index.md`), and what was rewritten rather than copied. Moving one is `git mv` + two lines.

Nothing outside `research/old-site-port/` was touched. Nothing was committed.

## 2. Conventions followed

- Material for MkDocs flavour as used by `sessions/s2.md`: `!!!`/`???` admonitions, `=== "Tab"` blocks, fenced code with `title=`, `++kbd++`, numbered sections, a *When things go wrong* table, a cheat sheet, a numbered *Going further*.
- Every runnable block carries a "where to run it" title (**Ubuntu window (WSL) / Terminal (Mac) / Linux terminal / Git Bash / Codespace terminal**, or "Any terminal, inside `<folder>`" once the project exists).
- **No `sudo` anywhere.** Last year's material installs with `sudo apt install` in at least six places (`tree`, `micro`, `sqlite3`, `python3-venv`, `pandoc`, packages generally); every one is removed or replaced with `uv run --with <tool>`, which installs nothing permanently and needs no rights.
- `pip`/`venv` → `uv` throughout, with the classic form named once where students will meet it in READMEs (`pip install -e .`, `pip install -r requirements.txt`).
- Neither discipline assumed. Where an example could only speak to one room, both are named — a corpus and a panel, an NLP tokenisation trap and an economics join trap.
- No secret anywhere; `sk-XXXX` was not needed on any of these pages.

## 3. Verification

Everything was run in the session scratchpad (`…/scratchpad/port-verify/`) on this machine: Linux, **uv 0.12.10**, **CPython 3.12.14** (uv-managed), **pytest 9.1.1**, **polars 1.44.2**, **pdoc 16.0.0**, mypy (fetched by `uv run --with`), GNU coreutils, git 2.x. Every `text` block on every page is pasted from a real run; absolute paths were rewritten to `/home/you/...`.

| Page | What was executed |
|---|---|
| `testing.md` | `uv init --no-package`, `uv add --dev pytest`, the `ModuleNotFoundError` before `conftest.py` and the pass after it, `-v`, `-q`, `-k`, `-x`, `--lf`, `-s`, `-l`, `file::test`, a genuinely failing test (the `20.0 == 80` discount bug), the float trap (`0.30000000000000004 == 0.3`), `pytest.raises`, `parametrize` with four cases, a fixture composing `tmp_path`, `capsys`, `uv run --with pytest pytest`, `uv run --with pytest-cov pytest --cov` |
| `modules-and-packages.md` | the `__name__` pair (`tools.py` run vs imported), the `textkit` package with `__init__.py`/`__all__`, `sys.path`, `json.__file__`, `ModuleNotFoundError` for polars, `python textkit/__init__.py` → `ImportError: attempted relative import…`, `python -m textkit` before and after `__main__.py` (including exit code 2 on no argument), `uv init --package` (layout + generated `pyproject.toml` + `uv run pkgdemo`), `uv build`, `uvx --from ./dist/*.whl` |
| `command-line-arguments.md` | `sys.argv` types, the `ValueError` traceback, the full `wordcount.py` (choices, `append`, `count`, mutually exclusive group, `metavar`, `%(default)s`), its `--help`, both `error:` messages with exit code 2, the missing-file exit code 1, `--` ending the options, the `notes.py` subcommand tool with `set_defaults(handler=…)` and its three help screens, and the two tests calling `main(argv)` |
| `docstrings-and-type-hints.md` | `help()` and `__doc__`, mypy silent on unhinted code and correct on hinted code, the `TypeError` that arrives late without hints, `mypy textkit` on a package, `pdoc … --docformat google -o docs` (file list, `<title>`, and that a `_private` name gets no entry) |
| `shell-text-tools.md` | every pipeline on a four-row CSV and on `grades.csv`; the trailing-newline demonstration (`wc -l` 2 vs `grep -c ''` 3); `$_`, `cd -`, wildcard moves |
| `shell-data.md` | all thirteen questions, on the real `grades.csv`. Every number in the solutions is a real output |
| `project-layout.md` | the whole exercise twice — the literal solution and the wildcard variant — plus `git init`/`.gitignore`/`git status --short` and the `.gitkeep` point |
| `polars.md` | expression reuse, `group_by` with three aggregations, `over()` shares, `when/then`, `.str`, `pivot`, the join that turns 2 rows into 3, `scan_csv` + `explain()` (showing `PROJECT 3/4 COLUMNS`) + `collect()`, `sink_parquet`, CSV vs Parquet byte sizes |

**Links:** all 48 external URLs were fetched; every one returned 200. Two caveats in §7.

**Anchors:** every in-page and cross-page anchor was checked programmatically against the real headings, including the seven anchors into the live `setup.md` and `sessions/s2.md`. All resolve.

**Not run: `mkdocs build --strict`.** The pages are outside `site/`, so they are in no nav and a build would not see them — and building would write into `site/`, which this pass is forbidden to touch. **The pass that moves these files must run `mkdocs build --strict` and fix anything it catches.** The anchors were verified with hand-computed slugs, which matches Material's default slugify but is not the same thing as a build.

## 4. Needs the instructor

### 4.1 Judgment call 1 — OOP, classes and the SQL ORM

The material: `code-examples/04-class_for_sql/01-sql_python_recap.ipynb` (plain `sqlite3`: connection, cursor, `fetchall`, then `pd.read_sql_query`), `02-orm_classes_sql.ipynb` (SQLAlchemy ORM: `DeclarativeBase`, `Mapped`, `ForeignKey`, `Session`, `select`, a join with `func.count`), the `villes_france.db` database (present twice in the repo), `exercices/05-sql_classes/01-departement_sql_class.md` (five analytics questions through the ORM, including a Herfindahl index — visibly written for the economics room), and `exercices/04-data_structures/06-country_class.md` (build a `Country` class around a REST API; **this one sits in the excluded data-structures folder although it is an OOP + HTTP exercise — it may have been excluded by accident**).

Quality: the ORM notebook is the best-explained artefact in the old repo; `exercices/05-sql_classes` is a serious exercise.

**My recommendation: do not port it as taught material.** Three reasons. Nothing in SPEC needs it — the four sessions are git, tooling, the API and the harness, and the follow-on 15 hours are MCP and Hugging Face. It adds a heavy dependency (SQLAlchemy) and a whole paradigm to a site whose current Python surface is "a script, a function, a test". And the one thing this course genuinely needs from that neighbourhood — "wrap a data source in something the model can call" — is a *function with a docstring and a type hint*, which is `reference/docstrings-and-type-hints.md` plus `reference/command-line-arguments.md`, not a class hierarchy.

**If you want part of it**, the cheapest useful slice is the first notebook without the ORM: `sqlite3` from Python, `cursor.execute`, and `pl.read_database` / `pd.read_sql_query` — half a page in `reference/polars.md`, justified by Session 4 projects that keep their data in SQLite. I did not write it; say the word.

**What I need from you either way:** whether `04-data_structures/06-country_class.md` was excluded on purpose.

### 4.2 Judgment call 2 — testing, docstrings and type hints: where do they live?

I ported them into `reference/`, not into a session. The reasoning, to accept or overrule:

SPEC §4.3 makes the test suite the anchor of agent reliability ("the most reliable component of an agent system is not a model — it is the test suite"), and §4.3 is a 30-minute slot that also has to cover `AGENTS.md` and clean context. Thirty minutes cannot teach pytest from zero. But the sentence is unusable if students have never seen a test: "run pytest after every edit" is an instruction about a program they cannot write.

So: **`reference/testing.md` is Session 4's reading, and Session 4 §4.3 should link it explicitly** (it currently links nothing). The page is written to be read alone, and its §10 ("Tests and agents") is written to be *taught* — the two `AGENTS.md` instructions, the red-green-refactor table, and the warning that deleting a failing test is a locally optimal move that both humans and models find. If you can spare 20 minutes in Session 2 or in a fifth slot, §3–§7 of that page is a class: one function, two tests, the `conftest.py` trap, one real failure, `parametrize`, `tmp_path`.

**Docstrings and type hints** are cheaper and belong earlier: they cost one line each, and `reference/docstrings-and-type-hints.md` §3 makes the argument this course cares about (a signature is the cheapest context you can give a model). Suggestion: one slide in Session 2's deck pointing at the page, not a section of the lesson.

**A third thing worth deciding:** last year's exam graded documentation (4), tests (4) and licence (1) out of 20. SPEC's exam is a presentation of a project. If any of that rubric survives, these three pages are the material behind it — and then they are not optional reading, and the sessions should say so.

### 4.3 Smaller decisions

1. **The secondary source is another course.** `slides_cours_git` is *Génie Logiciel* (M2 TDL), not last year's Advanced Programming. Five of the nine pages here come mostly from it. Merging two courses' material into one site is a choice; it is the right one in my view (the site becomes "the knowledge", independent of the class), but you should know it is happening — and that a GL student may recognise the pages.
2. **`Exam.md` — the AI-agent-with-tools project.** Teams of 3, a mandatory database, 5–8 tool functions, a movie-recommender worked example, last year's deadlines. It is a *better fit for this course's thesis* than for the course it was written for, and it is exactly the project shape Session 4 sets up. **Link only** for now: the taxonomy of tool categories (database / API / analysis / visualisation / report) is a genuinely good "what could I build?" page, but the document as a whole is an assessment brief and SPEC's exam is a presentation. If you want it as `site/docs/project-ideas.md`, say so and I will strip the deadlines and the team size.
3. **Deck `Part 15` — the 20-point rubric**, in French: git / documentation / tests / licence / README / justifications, including an explicit and well-judged section on declaring AI use. Not ported (assessment document, and SPEC's assessment differs). The AI-declaration paragraph is worth reusing verbatim in whatever the new exam brief becomes.
4. **The SQL-in-the-shell exercise** (`02bis-…cyberbase`): **link only**, see §5.3 for the one piece worth salvaging.
5. **Nine new pages at once.** A staging order is in `INVENTORY.md` §1 if you would rather land them over three passes.

## 5. Texts for the merges (not applied — `site/` belongs to another pass)

### 5.1 `sessions/s2.md` §2.4 — conda

```markdown
!!! question "What about conda?"
    If you have used Anaconda, `conda` is the tool you know: it creates environments *and*
    installs packages, including non-Python ones (a C compiler, a CUDA runtime), which is why
    it took over scientific Python. It answers the same three questions as the table in
    section 1, with an `environment.yml` in place of `pyproject.toml` + `uv.lock`.
    Two reasons this course uses `uv` instead: it is far faster, and it needs nothing installed
    beyond itself — no 3 GB distribution, no administrator rights. If you arrive with a working
    conda setup, keep it for the projects that depend on it and use `uv` for this course's;
    the one thing not to do is install packages with `pip` inside a conda environment and expect
    `environment.yml` to know about it.
```

### 5.2 `sessions/s2.md` §6.3 — `.env` versus `config.py`

```markdown
!!! note "`.env` is not where your settings go"
    `.env` is for values that are **secret** or that **change between machines**: API keys,
    a database URL, a debug flag. Ordinary constants of your program — a default page size, the
    list of accepted file extensions, a timeout — are not configuration in that sense: they belong
    in the code, typically a small `config.py` that the rest of the project imports. The test is
    simple: if a classmate running your project would need a *different* value, it goes in `.env`;
    if everyone would use the same one, it goes in the code, where it can be read and reviewed.
```

### 5.3 The one thing worth salvaging from the SQL exercise

Last year's instructions open with `sudo apt install sqlite3`, which fails on the university desktops and on Git Bash. Python has SQLite built in, and since 3.12 it can be driven from the command line, so a query needs no installation at all:

```bash title="Any terminal — a SQL query with nothing installed"
uv run --python 3.12 python -m sqlite3 cyberchase.db "SELECT count(*) FROM episodes;"
```

```text
(140,)
```

Verified on this machine (SQLite 3.53.1 as bundled with the uv-managed CPython 3.12.14). Two limits, both verified: results print as Python tuples rather than a formatted table, and the **dot-commands do not work** (`.tables` → `OperationalError (SQLITE_ERROR): near "."`), so schema exploration needs `SELECT name FROM sqlite_master WHERE type='table';` instead. If the exercise is ever revived, that line replaces the whole `sudo` prerequisites section.

### 5.4 `exercises/password-generator.md` — the framing that was lost

```markdown
**Why word-based passwords?** The generator you are about to fork builds passwords out of random
words rather than random characters, for the reason [xkcd 936](https://xkcd.com/936/) made famous:
four common words chosen at random are harder to guess *and* easier to remember than `Tr0ub4dor&3`.
The entropy is in the number of words and the size of the list, not in the punctuation.
```

And, optionally, before Part C: *"Before adding `--separator` with `argparse`, try it with `sys.argv` — read the number of words from `sys.argv[1]` and handle the missing argument yourself. Ten minutes of that is the best argument for `argparse` there is."* (That two-part structure is how last year's exercise was built.)

### 5.5 `sessions/s2.md` §5.2 — the sentence to replace

The page currently says of `if __name__ == "__main__":` — *"You will see it in every Python script from now on; type it, do not question it yet."* Replace the second half with: *"It is explained in [Modules, packages and imports, §3](../reference/modules-and-packages.md#3-__name__-and-if-__name__-__main__)."*

**Careful:** `tasks/LOG.md` (2026-09-24) records a plan to add `s2.md` §5.4–5.6 covering script → module → import, from the new `slides/s2-tooling.md`. That overlaps `reference/modules-and-packages.md` §1–3. The division that avoids duplication: **the session teaches the two-file experiment and the four words; the reference page explains `sys.path`, packages, `__init__.py`, `python -m` and installability.** Whoever writes §5.4–5.6 should link out rather than re-explain, and the anchor above is the target.

## 6. Contradictions and duplications found

Between last year's material and the current site — reported, not resolved.

| # | What | Where |
|---|---|---|
| 1 | **`sudo` everywhere.** Last year installs `tree`, `micro`, `sqlite3`, `python3-venv` and `pandoc` with `sudo apt`. The new site forbids it (AGENTS.md rule 3; no rights on the A330 desktops). Nothing carried over: `find` replaces `tree`, `uv run --with` replaces the rest. | `01-shell-intro`, `02-python-env`, `01-architecture`, `02bis`, `02-demo_venv`, the slides' deploy workflow |
| 2 | **`pip install --user` is recommended** as the no-`sudo` solution ("Install packages for current user only — no sudo needed"). The new site's position is stricter and better: never install into a shared Python at all, one environment per project. Not carried over. | `lessons/02-python-env.md` |
| 3 | **`git checkout`** for switching branches and restoring files, where `sessions/s1.md` standardises on `switch`/`restore` and shows `checkout` for recognition only. One more reason the old git lesson is dropped entirely. | `lessons/03-git-version-control.md` |
| 4 | **A wrong answer in the shell exercise.** The statement says the class has 49 students; it has **50**. `grades.csv` has no trailing newline, so `wc -l` under-counts by one. Fixed in the port, and turned into a teaching point on both new pages. | `exercices/02-shell/02-shell.md` |
| 5 | **A wrong claim about `import *`.** The lesson says `from math import *` "imports math.sum and overwrites YOUR sum function". `math` has no `sum`. The warning is right, the example is not; rewritten around namespace collisions in general. | `lessons/06-…/061-basic_import.md` |
| 6 | **`sys.path` order described inaccurately** ("built-ins, then current directory, then PYTHONPATH, then stdlib, then site-packages"). The real order is: already-imported modules, built-ins, then the entries of `sys.path` in order — where `sys.path[0]` is the script's directory. The port shows the real `sys.path` instead of describing it. | `lessons/06-…/061-basic_import.md` |
| 7 | **Two versions of the same starter file disagree.** The password-generator instructions embed `WORDS_PATH = Path(".") / "data" / "wordlist.txt"` while `starter_code.py` in the same folder uses `Path(__file__).parent`. Only the second works when the script is run from elsewhere. The published `KnuxV/password-generator` already uses the correct form (per `tasks/LOG.md`), so this is historical. | `exercices/09-password_generator/` |
| 8 | **A test whose function does not exist.** The TDD slide asserts `calculate_vat(100, 0.20) == 120` and then defines `calculate_tva`. Amusing on a slide about tests; fixed in the port. | deck `Part 8` |
| 9 | **Unverified figures presented as facts.** Ariane 5 "€370M", Knight Capital "$440M in 45 minutes", "MIT: 44.7 % of GitHub in 2025", Red Hat "$3.4B/year", "IBM paid $34B", kernel contributor counts, "Google made 94 % of Chromium commits". All widely repeated, none checked against a primary source. **Dropped**, with a visible note on both pages saying why. | decks `Part 8`, `Part 14` |
| 10 | **Copy-pasted front matter.** Four unrelated exercises all carry `title: "Department SQL Class Exercise"` (the shell-SQL exercise, the country-class exercise, the password generator, the modules exercise). Harmless in Jekyll, but if any of those files is ported later, do not trust its title. | `exercices/*` |
| 11 | **Pinned action versions disagree across the repo.** The course's own `.github/workflows/site.yml` uses `actions/checkout@v4` and `setup-python@v5`; last year's deck used `@v6` for both; the workflows I ported use `checkout@v7.0.1` (as pinned by uv's official guide) and `@v6` (as pinned by pdoc's own published workflow). Not a student-facing problem, but if you want one convention across the repository, decide it once. | `Part 13`, `site.yml`, the two new workflows |
| 12 | **Session 2 says "do not question it yet"** about `if __name__ == "__main__":` while `slides/s2-tooling.md` (new, uncommitted) explains it and my reference page explains it in depth. Three places, one idea. See §5.5 for the division of labour. | `sessions/s2.md` §5.2 |
| 13 | **Overlap with `reference/git-collaboration.md` §5** (CI/CD): it introduces GitHub Actions conceptually and shows a minimal uv+pytest workflow "for recognition". `reference/testing.md` §9 now has the real one. Not a contradiction, but whoever lands these pages should make that section point forward rather than duplicate. | `reference/git-collaboration.md` |
| 14 | **The old repo's "contribute for bonus points" mechanism** (fork the course repo, open a PR, earn 0.5–1 point) has no equivalent on the new site. Dropped as an assessment decision, not a content one — but it was a good idea and it is cheap to reinstate. | old `index.md`, `exercices/03-git/05-pull_requests.md` |

## 7. UNVERIFIED

In rough order of how much it matters.

1. **`mkdocs build --strict` was not run** on these pages (see §3). Anchors and links were checked programmatically, not by a build. Run it as part of the move.
2. **`files/grades.csv` must be moved** to `site/docs/files/` before `exercises/shell-data.md` works: the page's `curl -LO https://knuxv.github.io/cours-agents/files/grades.csv` returns 404 today, as expected. (`files/sales.csv`, used by `reference/polars.md`, is already published and returns 200.)
3. **The two GitHub Actions workflows have not been run on GitHub.** The tests workflow in `reference/testing.md` §9 is copied verbatim from uv's official guide, including the commit-pinned action versions. The docs workflow in `reference/docstrings-and-type-hints.md` §4.1 is pdoc's own published workflow with the install/build steps swapped for the `uv` ones — that *combination* is untested, and the page carries a visible `TODO(verify)` saying so. Run both once on a scratch repository.
4. **Only Linux was tested.** Every command was run on this machine (Arch, uv-managed CPython). Not rehearsed on **Git Bash**, **macOS**, a **fresh WSL Ubuntu**, an **A330 desktop** or a **Codespace**. Specific risks: `printf`/`find`/`awk`/`grep -c ''` in Git Bash's MSYS environment (expected to work, unverified); `find . | sort` ordering on macOS (the page says the order may differ); `uv run --with <tool>` first-run download sizes on the room's network (pytest is small; mypy, pdoc and polars are not free, and the university home-folder quota versus `~/.local/share/uv` is still unknown — the same open question `tasks/LOG.md` raises for pi's 350 MB of Node).
5. **`gh auth refresh -h github.com -s workflow`** — the warning box in `reference/testing.md` §9 quotes the *situation* from `tasks/LOG.md` (the instructor hit it pushing a workflow file) but not the exact refusal message, which was not reproduced. Marked `TODO(verify)` on the page.
6. **Two last-year GitLab practice repositories** are linked from `reference/testing.md` §14 (`gitlab.unistra.fr/cours_test/intro_test`, `…/testing_username_password`) with a visible `TODO(verify)`: they were not opened, and I cannot check whether they are still public. Same for `gitlab.unistra.fr/cours_git/story_editing_exercise`, mentioned in `INVENTORY.md` as a link-only alternative.
7. **`gnu.org` intermittently unreachable.** All four `gnu.org` links in `reference/licensing.md` returned 200 earlier in this session; a later re-check timed out for all of them (connection timeout to 209.51.188.116, including URLs that had just answered). Treat as a transient network or rate-limit issue rather than bad URLs — but re-check once before publishing.
8. **`uv init --package` fills `authors` from your `git config`.** The page shows a placeholder (`Your Name`, `you@example.com`) and says so; the real generated file on this machine contained the instructor's name and address, which is worth knowing before a student publishes a wheel.
9. **Licence content is not legal advice**, and the page says so in its first admonition. The characterisations of MIT / Apache / GPL / AGPL are standard, drawn from the licences' own texts and from choosealicense.com, but they are a programmer's summary.
10. **Claims about models and code provenance** in `reference/licensing.md` §7 are deliberately hedged ("the legal landscape is unsettled and moving") because they are. No case law is cited and none should be added without checking.
11. **`pdoc` and private names:** verified that `_helper` gets no documented entry, and that it can still appear in the rendered source of a function that calls it. The page states exactly that, nothing stronger.
12. **The `over()` percentages, the coverage table and the query plan** in `reference/polars.md` are this machine's real output for polars 1.44.2. The `explain()` output format is version-specific and will drift; if the page ages badly, re-run the snippet.

## 8. If someone continues this work

Out of scope or out of room, in order of value:

1. **An exercise on testing.** `reference/testing.md` §3–§7 is a walkthrough; what is missing is a "here is a repository with three bugs and no tests" exercise. `KnuxV/password-generator` already has 13 tests and is forked by every student in exercise 2.3 — adding a *failing* test to it and asking them to fix the code is nearly free, and it makes exercise 2.3 the bridge to Session 4.
2. **The `texttools` exercise** (module → package → installable), which is `exercices/08-project_orgs.md` and now lives as the worked example in `reference/modules-and-packages.md` §5–6. Ten minutes to turn into a statement with a folded solution.
3. **`site/docs/project-ideas.md`** from `Exam.md`'s tool taxonomy, if the instructor wants it (§4.3.2).
4. **The `sqlite3`-from-Python half-page** for `reference/polars.md`, if the answer to §4.1 is "keep a slice".
5. **`resources/` entries.** Nothing was added there. Candidates: the two new workflow files (`tests.yml`, `docs.yml`) as ready-to-copy files, and an empty `conftest.py` with a one-line README explaining why it exists.
