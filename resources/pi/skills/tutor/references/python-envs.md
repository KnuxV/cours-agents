# Python environments: pip, venv, uv

Course page: <https://knuxv.github.io/cours-agents/sessions/s2/> (sections 2 to 4, troubleshooting table in section 9, cheat sheet in section 10).

## The story the course tells

1. `pip install` alone puts packages into the one system Python: every project shares them, versions collide, and nobody else can rebuild the same setup.
2. A virtual environment (`python3 -m venv .venv`, then `source .venv/bin/activate`) gives one Python per project. `requirements.txt` (`pip freeze > requirements.txt`) is the list you ship.
3. What is still missing: the Python version itself, and exact versions of the dependencies of dependencies. `uv` closes both gaps.

pip and venv are taught so students understand what `uv` automates. In their own work they use `uv`.

## Course conventions

- New project: `uv init --no-package --python 3.12`, inside the student's course repository `agent-lab`.
- Add a dependency with `uv add <pkg>`. Run everything with `uv run <script.py>`; no activation needed.
- Three files are committed: `pyproject.toml` (what the project asked for), `uv.lock` (what it got, exact versions), `.python-version` (which Python). `.venv/` is never committed; it belongs in `.gitignore`.
- Rebuild elsewhere: `git clone`, then `uv sync`.
- University Linux desktops have no `sudo`. `uv` installs into `~/.local/bin`; a new terminal is needed before `uv --version` works.
- Secrets live in environment variables (`$UNISTRA_API_KEY`), never in code or in a commit.

## Usual stumbles

| What the student sees | Where to point them |
|---|---|
| `uv: command not found` right after installing | PATH is read when a terminal starts: open a new one |
| `No module named polars` | How did they run the script? `python report.py` uses the system Python; `uv run report.py` uses the project's |
| `error: externally-managed-environment` from pip | Which Python is pip installing into? No environment is active |
| `(.venv)` missing from the prompt | The environment exists but was never activated in this window |
| `git status` lists hundreds of `.venv` files | What is in `.gitignore`? |
| Their `uv.lock` differs from a neighbour's | Compare `.python-version` on both machines |
| `python3 -m venv` fails with `ensurepip is not available` (WSL) | Ubuntu ships Python without venv: `sudo apt install python3-venv` (setup breakage, give it directly) |
| `uv init` complains that `pyproject.toml` exists | It was already run; nothing to fix |

## Exercises

- **2.1 A uv project from scratch.** Done when a classmate can run `git clone <repo> && cd agent-lab && uv sync && uv run python -c "import polars"` without errors.
- **2.2 Notebook to script with argparse.** `report.py` and `sales.csv`; the student adds a third argument (`--region` or a `--csv` flag). Done when `uv run report.py --help` documents three arguments and each behaves as advertised.
- **2.3 Fork and extend the password generator** (`github.com/KnuxV/password-generator`). Part A: fork, clone the fork, `uv sync`, `uv run pytest` shows `13 passed`. Part B: read `strong_password.py`. Part C: one branch per option, `separator` (`-s`, `choices=`, default a space) then `numbers` (`-n`, `action="store_true"`), each merged into `main` before the next starts. Three places change for each option: `parser.add_argument`, the `StrongPassword` constructor (new parameter with a default), and the line that joins the words. Done when `--help` shows four options, `-t memorable -l 4 -s - -n` prints something like `Decode9-Rebuild2-Squirt4-Paper9`, `uv run pytest` passes, and both commits are on GitHub.
