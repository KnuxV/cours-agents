# Exercises

All exercises in one place. Tags: **[core]** everyone finishes it in class · **[stretch]** for students who are ahead · **[home]** homework. Sessions 3 and 4 will be added when those pages are published. Starter repositories and reference solutions are being prepared (Task 03); where a link is missing it is marked TODO(verify).

| Session | # | Exercise | Tag | Time |
|---|---|---|---|---|
| [S0](setup.md) | 0.1 | [Ten minutes in the terminal](#01-ten-minutes-in-the-terminal) | core | 10 min |
| [S1](sessions/s1.md) | 1.1 | [Website under version control](#11-website-under-version-control) | core | 30 min |
| S1 | 1.2 | [Recover a deleted file](#12-recover-a-deleted-file) | core | 15 min |
| S1 | 1.3 | [Your course repository on GitHub](#13-your-course-repository-on-github) | core | 20 min |
| S1 | 1.4 | [Branch, merge, conflict](#14-branch-merge-conflict) | stretch | 20 min |
| S1 | 1.5 | [History as evidence](#15-history-as-evidence) | home | 25 min |
| [S2](sessions/s2.md) | 2.1 | [A uv project from scratch](#21-a-uv-project-from-scratch) | core | 20 min |
| S2 | 2.2 | [Notebook → script with argparse](#22-notebook-script-with-argparse) | core | 30 min |
| S2 | 2.3 | [Secret hygiene audit](#23-secret-hygiene-audit) | home | 30 min |
| S2 | 2.4 | [Polars vs pandas](#24-polars-vs-pandas) | stretch | 30 min |
| S3 | — | *Published with Session 3* | | |
| S4 | — | *Published with Session 4* | | |

## Session 0 — Setup

### 0.1 Ten minutes in the terminal

**[core]** · Goal: the six commands you will type a hundred times — `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv` — plus `cat`, `echo`, `rm`.

1. Follow [setup, section 6](setup.md#6-ten-minutes-in-the-terminal) line by line.
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

### 1.1 Website under version control

**[core]** · Goal: the everyday cycle on a folder you can *see* change in a browser.

1. Download the practice site and open it in your browser ([S1 §4.1](sessions/s1.md#41-get-the-files)).
2. Make it a repository and take the first snapshot.
3. Make three separate edits, each followed by `git diff`, `git add`, `git commit -m`: the meetup time, the tagline, the header colour in `style.css` (`--header-bg`).
4. Add a `notes.txt` and make Git ignore it.

**Done when** `git log --oneline` shows at least five commits and `git status` says `working tree clean`.

??? note "Solution"
    Sections 4.2–4.7 of the [Session 1 page](sessions/s1.md#42-git-init-start-tracking) are the solution, step by step. The expected `git log --oneline` shape:

    ```text
    3f2a1c9 Ignore local scratch notes
    b7e4d02 Darken the header background
    91c0aa5 Add 'all levels welcome' to the tagline
    5d8e7b3 Move meetup time to 7:30 PM
    a1b2c3d Initial commit of the club website
    ```

    (Hashes will differ — they depend on your name, email and the time of each commit.)

### 1.2 Recover a deleted file

**[core]** · Goal: trust the undo button. Do this inside the `practice-site` repository from 1.1, with a clean working tree.

1. Delete `style.css` and `about.html` from disk (`rm`). Refresh the browser: the page is unstyled and the About link is broken.
2. Put both files back using only Git — no retyping, no re-downloading. The browser must show the site as before.
3. Now the harder one: the *first* commit had the meetup at `7:00 PM`. Bring the version of `index.html` from that first commit into your working copy, look at what `git diff` says, and commit it with a message that says what you did.
4. Question to answer in one sentence: after step 3, is the "7:30 PM" commit still in the history?

??? note "Solution"
    ```bash title="Any terminal, inside practice-site"
    rm style.css about.html
    git status                       # both listed as deleted
    git restore style.css about.html
    git status                       # clean again

    git log --oneline                # copy the hash of "Initial commit ..."
    git restore --source=<hash> index.html
    git diff                         # shows 7:30 -> 7:00, and any later edits to index.html undone
    git add index.html
    git commit -m "Revert index.html to the original meetup time"
    ```

    Step 4: yes. `git restore --source` changes the *working copy*; the commit you made is a new snapshot on top of the history, which still contains the 7:30 commit. Nothing was erased. (Also note that `--source` replaces the *whole file*: if you had changed the tagline in `index.html` in a later commit, that change is undone too — one file, one snapshot, not one line.)

### 1.3 Your course repository on GitHub

**[core]** · The session's deliverable. Goal: a repository you own, on GitHub, that Sessions 2–4 will live in.

Follow [S1 §7](sessions/s1.md#7-the-deliverable-your-course-repository). **Done when** your repository page on GitHub shows the README, `git status` is clean, and `git remote -v` prints your GitHub URL twice.

??? note "Solution"
    The commands are in §7 verbatim. The two mistakes to check for: the repository was created on GitHub *with* a README (then `git pull --no-rebase origin main` before the push), and the push asked for a password (then [§6.1](sessions/s1.md#61-log-in-once-from-the-terminal) was skipped).

### 1.4 Branch, merge, conflict

**[stretch]** · Goal: see a conflict, read the markers, resolve it by hand. Inside `practice-site`, on `main`, clean tree.

1. Create a branch `shorter-tagline`; change the tagline in `index.html` to `We build weird little projects.`; commit.
2. Back on `main`, create a branch `friendlier-tagline`; change the *same* line to `Come build weird little projects with us — all levels welcome.`; commit.
3. On `main`, merge `shorter-tagline` (fast-forward), then merge `friendlier-tagline`. Git stops: `CONFLICT (content): Merge conflict in index.html`.
4. Open `index.html`, find the block between `<<<<<<<` and `>>>>>>>`, keep the version you prefer (or write a third one), delete the markers, save, `git add index.html`, `git commit` (no `-m` this time: accept the proposed message, ++ctrl+x++ in nano).
5. `git log --oneline --graph` shows the history fork and rejoin.

??? note "Solution"
    ```bash title="Any terminal, inside practice-site"
    git switch -c shorter-tagline
    # edit the tagline line in index.html, save
    git commit -am "Shorten the tagline"
    git switch main
    git switch -c friendlier-tagline
    # edit the same line differently, save
    git commit -am "Make the tagline friendlier"
    git switch main
    git merge shorter-tagline          # Fast-forward
    git merge friendlier-tagline       # CONFLICT
    git status                         # "both modified: index.html"
    # edit index.html: keep one version, remove <<<<<<< ======= >>>>>>> lines, save
    git add index.html
    git commit                         # accept the "Merge branch ..." message
    git log --oneline --graph
    ```

    `git commit -am` stages every *already tracked* modified file and commits in one step — handy here, dangerous when you have unrelated edits lying around.

### 1.5 History as evidence

**[home]** · Goal: read a history you did not write — the skill you will use on agent-written commits.

A prepared repository holds a crêpe recipe with eight commits: a typo fix, a scale-up from 4 to 8 servings, a butter→oil swap, an added step, a sugar reduction, a serving suggestion, a README. Using only `git log`, `git show` and `git diff <hash> <hash>` (do not open the file in an editor for part 1):

1. List every commit and what it *claims* to do; then check with `git show` whether the scale-up scaled every ingredient by the same factor.
2. Bring the original sugar quantity back *without* losing the serving suggestion added after the sugar cut. (`git restore --source` will give you more than you asked for; understand why, undo it, and do it by hand.)

TODO(verify): clone URL — the repository will be published with the exercises of Task 03.

## Session 2 — Python tooling

### 2.1 A uv project from scratch

**[core]** · Goal: three files that make a project reproducible, and the habit of never committing `.venv`.

Follow [S2 §3](sessions/s2.md#3-a-project-from-scratch) in your course repository. **Done when** a classmate can run `git clone <your repo> && cd <repo> && uv sync && uv run python -c "import polars"` without errors — swap repositories with your neighbour and check.

??? note "Solution"
    ```bash title="Any terminal, inside cours-agents"
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

1. Do [S2 §4](sessions/s2.md#4-from-a-notebook-cell-to-a-script-with-arguments) with `report.py` and `sales.csv`; check the four runs (`--top 2`, `--help`, missing argument, `--top two`).
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

### 2.3 Secret hygiene audit

**[home]** · Goal: find a leaked secret in a repository's history and say how it should have been handled.

You are given a repository in which someone committed an API key inside a script, then "removed" it in a later commit. Produce a short text file `audit.md` in your own course repo answering:

1. In which commit did the key appear, and in which was it "removed"? (Hint: `git log -p`, `git log -S "sk-"`.)
2. Is the key still recoverable from the repository? Show the command that prints it.
3. Rewrite the offending line the right way (environment variable + `os.environ.get` + a clear failure message), and give the `.gitignore` line that protects a `.env` file.
4. What must the owner do *first* — before touching git at all?

TODO(verify): the starter repository will be published with the exercises of Task 03.

??? note "Solution sketch"
    `git log -S "sk-" --oneline` lists the commits that added or removed the string; `git show <first-hash>` prints the key — it is fully recoverable by anyone with the repository, so the answer to 4 is *regenerate the key* ([setup 5.1](setup.md#51-generate-the-key)). The correct line is the one in [S2 §5.2](sessions/s2.md#52-reading-them-from-python); the `.gitignore` line is `.env`.

### 2.4 Polars vs pandas

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
