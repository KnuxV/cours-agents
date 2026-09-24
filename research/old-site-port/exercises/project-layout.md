<!--
PORTED FROM last year's material (KnuxV/advanced_programming_python):
  exercices/01-architecture/01-architecture.md + SOLUTION.md — "create this folder structure and put
  the files in their rightful spot", with the instructor's own research files (1.txt … 5.txt,
  neg_fake_negs.parquet, two bubble-plot PNGs)

PROPOSED DESTINATION: site/docs/exercises/project-layout.md
  Nav (site/mkdocs.yml, under "✏️ Exercises" → "Terminal"):
          - 0.3 Tidy a project folder: exercises/project-layout.md
  Row for site/docs/exercises/index.md, "Terminal" table:
      | 0.3 | [Tidy a project folder](project-layout.md) | `mkdir -p`, `mv`, `find`, and the folder layout every later session assumes | 20 min |

REWRITTEN, not pasted:
  - no `sudo apt install tree` (the check uses `find`, which is always there) and no `eog`;
  - the seven data files are **created by the student** with one command block instead of being
    downloaded, so there are no binary blobs to host and the exercise works identically on
    WSL, Mac, Linux, Git Bash and Codespaces;
  - the `economics_project` name is gone: the same layout is described for an NLP corpus and for an
    economics panel, because both rooms read this page.
Rehearsed end to end on this machine; the `find` output below is the real one.
-->

# 0.3 — Tidy a project folder

Lesson: [Session 0 — Setup](../setup.md#7-ten-minutes-in-the-terminal) · [The shell as a data tool](../reference/shell-text-tools.md) · [All exercises](index.md)

**Goal:** `mkdir -p` and `mv` under pressure, and the folder layout that every later session — and every agent you point at a repository — will assume.

## Why this is an exercise and not a footnote

A project folder is an interface. When the raw data, the cleaned data, the script, the figure and the note to self are all in one flat pile, three things become impossible: telling which file is an input and which is a result, telling whether a number can be regenerated or only re-typed, and telling an agent "never touch anything under `data/raw/`". Ten minutes of `mkdir` buys all three.

The convention below is the one used by data projects across disciplines — a linguistics corpus and an economics panel get the same shape.

## Part 1 — make a mess

Run this block exactly as it is. It creates ten files in a flat folder, the way a fortnight of unstructured work does.

```bash title="Ubuntu window (WSL), Terminal (Mac), Linux terminal, Git Bash or Codespace terminal"
cd ~
mkdir -p messy-project
cd messy-project
for i in 1 2 3 4 5; do printf 'raw interview transcript %s\n' "$i" > "$i.txt"; done
printf 'region,year,value\nAlsace,2024,12.5\n' > cleaned_panel.csv
printf 'PNG-ish placeholder\n' > bubble_all.png
printf 'PNG-ish placeholder\n' > bubble_review.png
printf 'print("half-finished analysis")\n' > analysis.py
printf 'note to self: redo table 2\n' > notes.txt
ls
```

```text
1.txt
2.txt
3.txt
4.txt
5.txt
analysis.py
bubble_all.png
bubble_review.png
cleaned_panel.csv
notes.txt
```

(The `for … do … done` loop is the shell repeating a command five times. You are not expected to write one yet; read it and move on.)

## Part 2 — the target

Turn that pile into this, **without deleting anything**:

```text
messy-project/
├── data/
│   ├── raw/                    # exactly as it arrived. Never edited, never regenerated
│   │   ├── 1.txt … 5.txt
│   └── processed/              # produced from raw/ by a script
│       └── cleaned_panel.csv
├── scripts/                    # the code
│   └── analysis.py
├── results/
│   ├── figures/                # every image a script produced
│   │   ├── bubble_all.png
│   │   └── bubble_review.png
│   └── tables/                 # empty for now, and that is fine
├── docs/                       # notes, drafts, anything for humans
│   └── notes.txt
└── README.md                   # what this project is, and how to run it
```

Rules of the game:

1. Create the folders **first**, then move the files.
2. `mkdir -p a/b/c` creates the whole chain in one go; without `-p` it fails because `a` does not exist yet.
3. `mv` takes several sources and one destination: `mv a.txt b.txt somewhere/`.
4. `..` is the parent folder, so `mv thing.txt ../other/` works when you are one level down.
5. Create the empty `README.md` with `touch README.md`, then write two lines in it with `nano README.md` (++ctrl+o++, ++enter++, ++ctrl+x++ to save and quit) — the project's name and one sentence saying what it does.

## Part 3 — check it

```bash title="Any terminal, inside messy-project"
find . -type d | sort
find . | sort
```

**Done when** the second command prints exactly this (the order may differ slightly on macOS):

```text
.
./data
./data/processed
./data/processed/cleaned_panel.csv
./data/raw
./data/raw/1.txt
./data/raw/2.txt
./data/raw/3.txt
./data/raw/4.txt
./data/raw/5.txt
./docs
./docs/notes.txt
./README.md
./results
./results/figures
./results/figures/bubble_all.png
./results/figures/bubble_review.png
./results/tables
./scripts
./scripts/analysis.py
```

`ls -R` shows the same thing folder by folder if you prefer. (`tree` gives the prettiest output, but it is not installed everywhere and you have no administrator rights on the university desktops — `find` is always there.)

??? note "Solution"
    ```bash title="Any terminal, inside messy-project"
    mkdir -p data/raw data/processed scripts results/figures results/tables docs

    mv 1.txt 2.txt 3.txt 4.txt 5.txt data/raw/
    mv cleaned_panel.csv data/processed/
    mv bubble_all.png bubble_review.png results/figures/
    mv analysis.py scripts/
    mv notes.txt docs/

    touch README.md
    find . | sort
    ```

    One `mkdir -p` for all six paths, five `mv` commands, one `touch`. Two shortcuts worth knowing, once you trust yourself:

    ```bash title="Any terminal — the same thing, shorter"
    mv [1-5].txt data/raw/       # a character range: the five numbered files
    mv *.png results/figures/    # every png at once
    ```

    Wildcards are faster and riskier, in that order. Before an `mv` or an `rm` with a wildcard, run the pattern through `ls` first and read the list — `ls *.png` costs nothing and has saved many afternoons.

## Part 4 — make it a repository (optional, 5 minutes)

The layout above is what a project looks like the day *before* someone else has to run it. Two more files make it a project:

```bash title="Any terminal, inside messy-project"
git init
printf '.venv/\n__pycache__/\n.env\ndata/raw/*.parquet\n' > .gitignore
git add .
git status --short
```

Look at what `git status` lists, and at what it does not. That is the second half of the lesson: **the folder layout and the `.gitignore` decide what your history contains.** Raw data that is large, private or downloadable belongs outside the repository, with a line in the README saying where it came from.

One wrinkle: Git tracks files, not folders, so `results/tables/` — which is empty — does not appear in `git status` and will not exist for whoever clones your repository. The convention is to put an empty file in it, traditionally called `.gitkeep`, purely so that the folder survives:

```bash title="Any terminal, inside messy-project"
touch results/tables/.gitkeep
git add results/tables/.gitkeep
git status --short
```

## Why an agent cares

In [Session 4](../sessions/s4.md) you will write an `AGENTS.md` telling a coding agent how to behave in your repository. Compare two versions of the same instruction:

- "Be careful with the data." — nothing in the repository corresponds to this sentence.
- "Inputs are in `data/raw/` and are read-only: never write there. Everything under `data/processed/` and `results/` is generated by the scripts in `scripts/` and may be recreated." — every noun in that sentence is a folder that exists.

The second instruction is only writable because the first three parts of this exercise were done. A legible folder layout is not tidiness for its own sake; it is what makes a rule about your project expressible at all.
