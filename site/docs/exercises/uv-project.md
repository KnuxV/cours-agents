# 2.1 — A uv project from scratch

Lesson: [Session 2 — Python tooling](../sessions/s2.md) · [All exercises](index.md)

**Goal:** three files that make a project reproducible, and the habit of never committing `.venv`.

Follow [S2 §4](../sessions/s2.md#4-a-project-from-scratch) in your course repository. **Done when** a classmate can run `git clone <your repo> && cd agent-lab && uv sync && uv run python -c "import polars"` without errors — swap repositories with your neighbour and check.

??? note "Solution"
    ```bash title="Any terminal, inside agent-lab"
    uv init --no-package --python 3.12
    uv run main.py
    uv add polars
    git status                       # .venv must NOT appear
    git add pyproject.toml uv.lock .python-version main.py
    git commit -m "Initialise uv project with polars"
    git push
    ```
