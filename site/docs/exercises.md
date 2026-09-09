# Exercises

All exercises in one place. Tags: **[core]** everyone finishes it in class · **[stretch]** for students who are ahead · **[home]** homework. Sessions 3 and 4 will be added when those pages are published. Starter repositories and reference solutions are being prepared (Task 03); where a link is missing it is marked TODO(verify).

| Session | # | Exercise | Tag | Time |
|---|---|---|---|---|
| [S0](setup.md) | 0.1 | [Ten minutes in the terminal](#01-ten-minutes-in-the-terminal) | core | 10 min |
| [S1](sessions/s1.md) | 1.1 | [Your course repository on GitHub](#11-your-course-repository-on-github) | core | 20 min |
| S1 | 1.2 | [Recipe history](#12-recipe-history) | core | 25 min |
| S1 | 1.3 | [Branches: fast-forward, merge commit, conflict](#13-branches-fast-forward-merge-commit-conflict) | core | 25 min |
| [S1½](sessions/s1-collab.md) | — | [Git as a collaboration tool](sessions/s1-collab.md) (reading) | home | 40 min |
| [S2](sessions/s2.md) | 2.1 | [A uv project from scratch](#21-a-uv-project-from-scratch) | core | 20 min |
| S2 | 2.2 | [Notebook → script with argparse](#22-notebook-script-with-argparse) | core | 30 min |
| S2 | 2.3 | [Fork and extend the password generator](#23-fork-and-extend-the-password-generator) | core | 40 min |
| S2 | 2.4 | [Secret hygiene audit](#24-secret-hygiene-audit) | home | 30 min |
| S2 | 2.5 | [Polars vs pandas](#25-polars-vs-pandas) | stretch | 30 min |
| S3 | — | *Published with Session 3* | | |
| S4 | — | *Published with Session 4* | | |

## Session 0 — Setup

### 0.1 Ten minutes in the terminal

**[core]** · Goal: the six commands you will type a hundred times — `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv` — plus `cat`, `echo`, `rm`.

1. Follow [setup, section 7](setup.md#7-ten-minutes-in-the-terminal) line by line.
2. Then, without looking: create a folder `sandbox` in your home, inside it a file `a.txt` containing the word `one`, copy it to `b.txt`, rename `b.txt` to `c.txt`, list the folder with details, and delete `c.txt`.
3. Expected final state: `ls sandbox` prints `a.txt` only; `cat sandbox/a.txt` prints `one`.

??? note "Solution"
    ```bash title="Any terminal"
    cd ~
    mkdir sandbox
    cd sandbox
    echo "one" > a.txt
    cp a.txt b.txt
    mv b.txt c.txt
    ls -la
    rm c.txt
    ls
    cat a.txt
    ```

## Session 1 — Git

Three exercises, in this order. 1.1 is the session's deliverable and the repository the other two build on. Then, at home, the [Session 1½ reading](sessions/s1-collab.md).

### 1.1 Your course repository on GitHub

**[core]** · Goal: a repository you own, on GitHub, with a few commits of your own work in it. Sessions 2–4 happen inside it.

1. Follow [S1 §6](sessions/s1.md#6-the-deliverable-your-course-repository): create `agent-lab` in your home folder, `git init`, first commit, `gh auth login`, create the empty repository on GitHub, `git remote add origin`, `git push -u origin main`.
2. Put something of yours in it — anything you wrote and own: a Python script from last year, a notebook exported as `.py`, notes for another course, an essay. Copy the file(s) into `agent-lab`, then make **at least three commits**, one per change (add a file, edit a line, add another file). Look at `git status` and `git diff` before each commit.
3. `git push`. Refresh the GitHub page: your files and your commits are there (**Commits** link, top of the file list).

**Done when** `https://github.com/YOUR-USERNAME/agent-lab` shows your files and at least four commits, `git status` says `working tree clean`, and `git log --oneline` on your machine lists the same commits as the GitHub page.

??? note "Solution"
    ```bash title="Any terminal"
    cd ~/agent-lab                                   # created in §6.1, pushed in §6.3
    cp ~/Downloads/my_script.py .                    # whatever you own; any path
    git add my_script.py
    git commit -m "Add last year's plotting script"
    nano my_script.py                                # change one line, save
    git add my_script.py
    git commit -m "Rename the output file"
    echo "Ideas for the exam project" > ideas.md
    git add ideas.md
    git commit -m "Start a list of project ideas"
    git push
    git log --oneline
    ```

    The two mistakes to check for: the repository was created on GitHub *with* a README (then `git pull --no-rebase origin main` before the first push), and the push asked for a password (then [§6.2](sessions/s1.md#62-log-in-to-github-from-the-terminal-once) was skipped).

### 1.2 Recipe history

**[core]** · Goal: read a history you did not write — the skill you will use on agent-written commits — and meet `git clone` and `git remote`.

```bash title="Any terminal"
cd ~
git clone https://github.com/KnuxV/recipe-history.git
cd recipe-history
git remote -v
git log --oneline
```

**Part 0 — where did this come from?** `git remote -v` prints the address the copy came from, under the name `origin`. It is the instructor's repository: you could read it (it is public), you cannot write to it. Try `git push` — Git asks for credentials or answers `Permission denied`; either way nothing leaves your machine. Your commits will live on your machine only, which is fine for this exercise. (Compare with 1.1, where `origin` is yours.)

**Part 1 — read the history.** Using only `git log`, `git log --oneline`, `git show <hash>` and `git diff <hash1> <hash2>` — do not open `recipe.md` in an editor yet:

1. How many commits, and in one line each, what does every commit *claim* to do?
2. One early commit fixes a typo. Which one, and what was the wrong value? (`git show` it; do not trust the message alone.)
3. The serving size changes once. Did *every* ingredient scale by the same factor?
4. Butter becomes oil in one commit. Does it touch only the ingredient line, or something else too?

**Part 2 — bring back the original sugar without losing the serving suggestion.** A later commit cuts the sugar for a savoury version; a serving suggestion was added *after* that. Some classmates want the sweet version back, with the suggestion kept.

```bash title="Any terminal, inside recipe-history"
git log --oneline                           # find the hash of the commit just BEFORE the sugar cut
git restore --source=<hash> recipe.md
git diff                                    # you got more than you asked for
```

Understand why, undo that (`git restore recipe.md`), then fix it properly: edit the one sugar line by hand, `git add`, `git commit` with a message that says what you did.

??? note "Solution"
    Part 1: eight commits (`git log --oneline`), newest first: README, serving suggestion, sugar reduction, resting step, butter→oil, scale to 8, flour typo fix, initial recipe. `git show` on the typo commit shows the flour quantity changing; on the scale-up, check whether the eggs/milk/oil lines scaled by exactly 2 like the flour — read the `-`/`+` pairs. The butter→oil commit touches the ingredient line *and* a step ("whisk in the oil").

    Part 2: `git restore --source` replaces the **whole file** with that commit's version, so the serving suggestion (a later commit) disappears from your working copy too — `git diff` shows it as removed lines. Restore works on snapshots, not lines. Correct fix:

    ```bash title="Any terminal, inside recipe-history"
    git restore recipe.md                       # drop the whole-file restore
    nano recipe.md                              # put the original sugar quantity back on its line only
    git diff                                    # exactly one line changed
    git add recipe.md
    git commit -m "Restore the original sugar quantity"
    ```

    Check yourself: if the sugar change and the serving suggestion had been in the *same* commit, no `restore` trick would have separated them — you would edit by hand from the start. That is why Session 1 insists on one logical change per commit.

### 1.3 Branches: fast-forward, merge commit, conflict

**[core]** · Goal: see for yourself the rule of [S1 §5](sessions/s1.md#5-branches-and-merges) — *fast-forward if `main` has not moved, merge commit if it has* — in your own repository. Part C (the conflict) is **[stretch]**.

Work inside `agent-lab` from 1.1, starting on `main` with a clean `git status`. Run `git log --oneline --all --graph` after every commit and every merge, and look at the drawing.

**Part A — `main` does not move: fast-forward.**

```bash title="Any terminal, inside agent-lab — on main"
git switch -c add-notes
echo "# Notes" > notes.md
echo "- Session 1: git" >> notes.md
git add notes.md
git commit -m "Add a notes file"
git switch main
git log --oneline --all --graph
git merge add-notes
git log --oneline --graph
git branch -d add-notes
```

Expected from `git merge`: `Fast-forward`, then a straight line in the graph — no new commit, `main` simply moved up to the branch's commit.

**Part B — `main` moves meanwhile: merge commit.** Same again, but before merging, make a commit *on `main`* that touches a different file.

```bash title="Any terminal, inside agent-lab — on main"
git switch -c longer-readme
echo "" >> README.md
echo "This repository holds my work for the course." >> README.md
git add README.md
git commit -m "Describe the repository in the README"
git switch main
echo "- [ ] finish Session 1 exercises" > todo.md
git add todo.md
git commit -m "Add a todo list"
git log --oneline --all --graph
git merge longer-readme
git log --oneline --graph
git branch -d longer-readme
```

Expected: the graph *before* the merge shows the fork (two commits side by side under the same parent); `git merge` opens an editor with the message `Merge branch 'longer-readme'` — save and quit (nano: ++ctrl+x++, ++y++, ++enter++) — and prints `Merge made by the 'ort' strategy`; the graph *after* shows a diamond, and the merge commit has two parents. Both changes are on `main`: `cat README.md` and `ls`.

**Part C — same line on both sides: conflict [stretch].** Change the *first line* of `README.md` on a branch, then differently on `main`, then merge.

```bash title="Any terminal, inside agent-lab — on main"
git switch -c title-v1
nano README.md          # change the first line (the title) to something else, save
git commit -am "Reword the title"
git switch main
nano README.md          # change the first line to something DIFFERENT, save
git commit -am "Put my name in the title"
git merge title-v1
git status
```

Expected: `CONFLICT (content): Merge conflict in README.md` and `both modified: README.md`. Open `README.md`: the two versions of the title sit between `<<<<<<< HEAD`, `=======` and `>>>>>>> title-v1`. Edit it to the single title you want, delete the three marker lines, then `git add README.md`, `git commit` (accept the message), `git branch -d title-v1`. `git merge --abort` throws the attempt away if you get lost.

Finish with `git push` — GitHub shows every commit, merge commits included.

??? note "Solution"
    Rehearsed output of the three parts (hashes will differ):

    ```text
    # Part A, before the merge
    * 69c60e5 Add a notes file
    * 9068f52 Initial commit
    # git merge add-notes
    Updating 9068f52..69c60e5
    Fast-forward
     notes.md | 2 ++
     1 file changed, 2 insertions(+)

    # Part B, before the merge
    * fb3e302 Describe the repository in the README
    | * 216353c Add a todo list
    |/
    * 69c60e5 Add a notes file
    # git merge longer-readme
    Merge made by the 'ort' strategy.
     README.md | 2 ++
    # after
    *   00e8d36 Merge branch 'longer-readme'
    |\
    | * fb3e302 Describe the repository in the README
    * | 216353c Add a todo list
    |/
    * 69c60e5 Add a notes file

    # Part C
    Auto-merging README.md
    CONFLICT (content): Merge conflict in README.md
    Automatic merge failed; fix conflicts and then commit the result.
    ```

    In Part C the file looks like this until you edit it:

    ```text
    <<<<<<< HEAD
    # agent-lab — Kevin, M2 2026
    =======
    # agent-lab — my course repository
    >>>>>>> title-v1
    Your Name — M2, 2026
    ```

    Keep one title (or write a third), delete the marker lines, `git add README.md`, `git commit`. The graph then shows a second diamond on top of the first. `-am` in Part C stages every *tracked* file and commits in one go; it does not add new files, which is why Parts A and B use `git add` explicitly.

Practising branches online: [Learn Git Branching](https://learngitbranching.js.org/), *Main* → *Introduction Sequence*, levels 1–4 (commits, branches, merge, rebase — skip rebase) animate exactly Parts A and B. [Oh My Git!](https://ohmygit.org/) is a free game that does the same with a drag-and-drop graph.

## Session 2 — Python tooling

### 2.1 A uv project from scratch

**[core]** · Goal: three files that make a project reproducible, and the habit of never committing `.venv`.

Follow [S2 §4](sessions/s2.md#4-a-project-from-scratch) in your course repository. **Done when** a classmate can run `git clone <your repo> && cd agent-lab && uv sync && uv run python -c "import polars"` without errors — swap repositories with your neighbour and check.

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

### 2.2 Notebook → script with argparse

**[core]** · Goal: lift hard-coded values out of a notebook cell into command-line arguments.

1. Do [S2 §5](sessions/s2.md#5-from-a-notebook-cell-to-a-script-with-arguments) with `report.py` and `sales.csv`; check the four runs (`--top 2`, `--help`, missing argument, `--top two`).
2. Add a third argument: `--region` (keep only one region) **or** `--csv` (a flag: print the result as CSV instead of a table — `result.write_csv()` with no path returns a string).
3. Commit and push.

**Done when** `uv run report.py --help` documents three arguments and each behaves as advertised.

??? note "Solution (the `--csv` variant)"
    Add one line to the parser and change the `print`:

    ```python
    parser.add_argument("--csv", action="store_true", help="print CSV instead of a table")
    ...
    if args.csv:
        print(result.write_csv(), end="")
    else:
        print(result)
    ```

    `action="store_true"` makes `--csv` a flag: `args.csv` is `False` unless the flag is present. Check: `uv run report.py sales.csv --top 2 --csv` prints `region,revenue` followed by two lines.

### 2.3 Fork and extend the password generator

**[core]** · Goal: install a project you did not write with one command, read a real `argparse` program, and add two options to it — one branch per option.

The project is [github.com/KnuxV/password-generator](https://github.com/KnuxV/password-generator): a command-line tool that prints a strong password, either **memorable** (random English words: `Stubbed Congress Tiptop`) or **random** (mixed characters: `aB3$cD9#eF2@`). One dependency (`zxcvbn`, a strength estimator), a small test suite, and the three project files from [S2 §4](sessions/s2.md#4-a-project-from-scratch).

**Part A — fork and install (10 min).** You will push your work, so you need your own copy on GitHub: a **fork** ([S1½ §2](sessions/s1-collab.md#2-clone-vs-fork)). On the repository page, click **Fork** → **Create fork**. Then clone *your* fork — in your home folder, not inside `agent-lab`:

```bash title="Any terminal"
cd ~
git clone https://github.com/YOUR-USERNAME/password-generator.git
cd password-generator
uv sync
```

`uv sync` prints `Using CPython 3.12.x`, `Creating virtual environment at: .venv`, then `Installed 6 packages` — the exact versions from `uv.lock`. That was the installation. Now use it:

```bash title="Any terminal, inside password-generator"
uv run strong_password.py --help
uv run strong_password.py -t memorable -l 5
uv run strong_password.py -t random -l 16
uv run strong_password.py -t words
uv run compute_crack_time.py
uv run pytest
```

Expected: a help message with two options; a five-word password; a sixteen-character one; a refusal (`invalid choice: 'words' (choose from memorable, random)`); a comparison of the two kinds with a crack-time estimate; `13 passed`.

**Part B — read the code (10 min, together).** Open `strong_password.py` and answer, in your own words:

1. `cat pyproject.toml`, `cat .python-version`, `head -20 uv.lock`: which file says *what the project asked for*, which says *what it got*, which says *which Python*? Why is `pytest` under `[dependency-groups] dev` and not with `zxcvbn`?
2. In `main()`: which argument is **required**, which has a **default**? What does `choices=` buy you (you saw it with `-t words`)? Where does `args.length` end up?
3. Follow the value: `args.type` → `TypePassword(args.type)` → `StrongPassword(...)` → `generate()` → `generate_memorable()`. Which line joins the words with a space?
4. Where does the word list come from, and why `Path(__file__).parent` rather than just `"data/eff_large_wordlist.txt"`? (Try: `cd ~` then `uv run --project password-generator password-generator/strong_password.py -t memorable`.)
5. In `tests/test_memorable_password.py`, what does `test_has_spaces` assert? Keep it in mind for part C.

**Part C — two options, two branches (20 min).** Each option gets its own branch, merged into `main` before the next one starts (S1 §5, case 1: fast-forward).

1. `git switch -c separator`. Add an option `-s` / `--separator`: what goes *between* the words of a memorable password. Allowed values: `-`, a space, `_`, `.`, `/` (`choices=`); default: a space, so that nothing changes for existing users. Three places to touch: `parser.add_argument(...)`, the `StrongPassword` constructor (a new parameter *with a default*), and the `" ".join(...)` line. Check:

    ```bash title="Any terminal, inside password-generator"
    uv run strong_password.py -t memorable -l 4 -s -
    uv run strong_password.py -t memorable -l 4 --separator "_"
    uv run strong_password.py -t memorable -l 4 -s ,
    uv run pytest
    ```

    Expected: four words joined by `-` (`Earful-Afraid-Sapling-Helpful`), then by `_`, a refusal for `,`, and still `13 passed` — the default did not move. (To pass a space: `-s " "`, with the quotes — shell quoting, S2 §9.) Commit, `git switch main`, `git merge separator`.

2. `git switch -c numbers`. Add a **flag** `-n` / `--numbers` (`action="store_true"`, no value): when present, every word of a memorable password gets one random digit appended — `Wildlife1 Synthesis5 Useable1 Facecloth3`. Hint: `secrets.choice(DIGITS)` is already imported; the flag is ignored for `random` passwords, which have digits anyway. Same three places. Check `-l 4 -n`, then `-l 4 -s - -n`, then `uv run pytest`. Commit, switch to `main`, merge.

3. `git push`. Your fork on GitHub now carries both features on `main`.

**Done when** `uv run strong_password.py --help` documents four options, `uv run strong_password.py -t memorable -l 4 -s - -n` prints something like `Decode9-Rebuild2-Squirt4-Paper9`, `uv run pytest` passes, and `git log --oneline` on GitHub shows your two commits.

*Stretch:* add one test per option in `tests/` (a `-` separator → `password.count("-") == 3` for four words; `numbers=True` → `any(c.isdigit() for c in password)`). Then redo part C the hard way: both branches off the *same* commit, merged one after the other — Git reports conflicts in every place both branches touched; resolve them as in S1 §5, case 3.

??? note "Solution"
    Both options, as they look once the two branches are merged. The constructor:

    ```python
    def __init__(
        self, length: int, type_p: TypePassword, separator: str = " ", numbers: bool = False
    ):
        self.length = length
        self.type_p = type_p
        self.separator = separator
        self.numbers = numbers
    ```

    `generate_memorable`:

    ```python
    words = [secrets.choice(WORD_LIST) for _ in range(self.length)]
    if self.numbers:
        words = [word + secrets.choice(DIGITS) for word in words]
    return self.separator.join(words)
    ```

    The parser, before `args = parser.parse_args()`, and the call that follows it:

    ```python
    parser.add_argument(
        "-s",
        "--separator",
        choices=["-", " ", "_", ".", "/"],
        default=" ",
        help="character between words (memorable only); default: a space",
    )
    parser.add_argument(
        "-n",
        "--numbers",
        action="store_true",
        help="add a digit after each word (memorable only)",
    )
    args = parser.parse_args()

    generator = StrongPassword(
        length=args.length,
        type_p=TypePassword(args.type),
        separator=args.separator,
        numbers=args.numbers,
    )
    ```

    `--help` then lists `-s {-, ,_,.,/}` — the space in the choices makes the usage line ugly; `metavar="SEP"` on that `add_argument` tidies it. The rehearsed sequence: `separator` branch → 13 passed → fast-forward merge; `numbers` branch → 13 passed → fast-forward merge; `--help` shows four options.

### 2.4 Secret hygiene audit

**[home]** · Goal: find a leaked secret in a repository's history and say how it should have been handled.

You are given a repository in which someone committed an API key inside a script, then "removed" it in a later commit. Produce a short text file `audit.md` in your own course repo answering:

1. In which commit did the key appear, and in which was it "removed"? (Hint: `git log -p`, `git log -S "sk-"`.)
2. Is the key still recoverable from the repository? Show the command that prints it.
3. Rewrite the offending line the right way (environment variable + `os.environ.get` + a clear failure message), and give the `.gitignore` line that protects a `.env` file.
4. What must the owner do *first* — before touching git at all?

TODO(verify): the starter repository will be published with the exercises of Task 03.

??? note "Solution sketch"
    `git log -S "sk-" --oneline` lists the commits that added or removed the string; `git show <first-hash>` prints the key — it is fully recoverable by anyone with the repository, so the answer to 4 is *regenerate the key* ([setup 5.1](setup.md#51-generate-the-key)). The correct line is the one in [S2 §6.2](sessions/s2.md#62-reading-them-from-python); the `.gitignore` line is `.env`.

### 2.5 Polars vs pandas

**[stretch]** · Goal: feel the difference between expressions and chained indexing, and measure the speed.

1. `uv add pandas` in a scratch branch of your course repo (`git switch -c polars-vs-pandas`).
2. Generate a larger file: 1,000,000 rows of `region, product, units, unit_price` with random values (Python's `random` module is enough), written with `csv` or Polars.
3. Write `bench.py`: read the file and compute revenue per region with pandas, then with Polars; time each with `time.perf_counter()`.
4. In a comment at the top of the script, three sentences on how the *code* differs, not just the timing.

??? note "Solution sketch"
    ```python
    import time, pandas as pd, polars as pl

    t = time.perf_counter()
    pdf = pd.read_csv("big.csv")
    pdf["revenue"] = pdf["units"] * pdf["unit_price"]
    print(pdf.groupby("region")["revenue"].sum().sort_values(ascending=False).head(3))
    print("pandas:", round(time.perf_counter() - t, 2), "s")

    t = time.perf_counter()
    df = pl.read_csv("big.csv")
    print(df.with_columns((pl.col("units") * pl.col("unit_price")).alias("revenue"))
            .group_by("region").agg(pl.col("revenue").sum())
            .sort("revenue", descending=True).head(3))
    print("polars:", round(time.perf_counter() - t, 2), "s")
    ```

    Expect Polars to be several times faster on read and group-by; the exact ratio depends on the machine. The point for the comment: pandas mutates a column in place on a named DataFrame; Polars describes the whole computation as a chain of expressions on immutable frames, which is what lets it optimise (and parallelise) the plan.
