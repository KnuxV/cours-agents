# Testing lab — doctest, assert, pytest

The code for the testing class: four examples you run during the talk, one demo pipeline, two exercises.
The slides are online at https://knuxv.github.io/cours-agents/slides/testing-pytest.html (source: `slides/testing-pytest.html` in the course repo); the written lesson is the site page *Testing your code with pytest*.

## Get it

```bash
# WSL / Mac Terminal / Linux / Git Bash / Codespaces
cd ~
git clone https://github.com/KnuxV/cours-agents.git     # already cloned? instead: cd ~/cours-agents && git pull
cp -r ~/cours-agents/resources/testing-lab ~/testing-lab
cd ~/testing-lab
uv sync
```

If `git pull` refuses and mentions *stash*, you changed files inside the course repository: run `git stash -u` then `git pull` again (`git stash pop` brings your changes back).

`uv sync` creates `.venv/` and installs pandas and pytest into it. No `sudo`, nothing outside the folder.

**Always `cd` into one folder before running pytest.** Each folder is its own small example; in the folders that use pytest, the file `conftest.py` marks where that example starts.

## What is in each folder

| Folder | What it shows | Run (from inside the folder) |
|---|---|---|
| `1-doctest/` | Examples inside a docstring that Python checks; `vocabulary.py` writes them with `in` and `>` instead of an exact value | `uv run python text_tools.py -v` or `uv run python -m doctest -v text_tools.py`; same for `vocabulary.py` |
| `2-assert/` | Plain `assert`: stops at the first failure (on purpose) | `uv run python check_text_tools.py` |
| `3-pytest/` | `tests/` folder, parametrize, `pytest.raises`, `pytest.approx`, a fixture, `tmp_path`, a mock (`monkeypatch`) | `uv run pytest -v` |
| `4-pipeline/` | The demo: a four-step pipeline, three weekly CSV files, data checks, unit tests, a regression test | see below |
| `exo1-fix/` | Exercise 1 — the code is wrong, the tests say where | `uv run pytest` |
| `exo2-tdd/` | Exercise 2 — build `parse_number()` test first | `uv run pytest` |

Solutions are on the `solutions` branch of the course repo: `git -C ~/cours-agents switch solutions`, then look in `resources/testing-lab/`.

## The demo, step by step (`4-pipeline/`)

A colleague sends one CSV of product reviews every week. `pipeline.py` prints, per language, the number of reviews, the mean rating and the mean length in words.

```bash
cd ~/testing-lab/4-pipeline
uv run python pipeline.py data/week1.csv      # 1. works
uv run python pipeline.py data/week2.csv      # 2. works... is it right?
uv run python pipeline.py data/week3.csv      # 3. crashes
uv run pytest tests/test_data.py -v           # 4. check every file in data/
uv run pytest tests/test_clean.py             # 5. what clean() should do: red
#   6. fix clean() in pipeline.py (two lines, on the slide)
uv run pytest tests/test_clean.py             #    green
uv run pytest tests/test_data.py              # 7. what is left is a data problem
mkdir data/rejected
mv data/week2.csv data/week3.csv data/rejected/
uv run pytest -v                              # 8. everything green, regression test included
```

What is wrong in the files, for the instructor:

| File | Problem | Visible when you run the pipeline? |
|---|---|---|
| `week1.csv` | nothing | — |
| `week2.csv` | `lang` written `FR`, `Fr`, `fr ` (trailing space), `EN`; review 208 has no text, review 212 is only spaces; reviews 203, 205, 207, 211, 214 were rated out of 10 | Only if you read the table closely: six "languages", a French mean rating above 5 |
| `week3.csv` | saved with `;` as the separator, and the column is `note` instead of `rating` | Yes: `KeyError: 'text'` |

## Start your own project with tests

```bash
# WSL / Mac Terminal / Linux / Git Bash / Codespaces
uv init --no-package my-project
cd my-project
uv add --dev pytest
mkdir tests
touch conftest.py            # marks the project root, so tests/ can import your code
uv run pytest
```
