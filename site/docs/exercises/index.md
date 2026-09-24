# Exercises

One page per exercise. Each page names the **lesson to lean on**, says **when you are done**, and ends with a **folded solution** — open it after a real attempt, not before.

Within each topic the exercises are in order: the first one is the gentlest. The times are honest averages, not a limit. Everything stays online, so an exercise you do not finish in class you finish at home.

!!! tip "When you are stuck, in this order"
    1. **Re-read the statement** and try once more.
    2. **Open the lesson** — every exercise names the sections to read, and the lesson pages are written to be followed alone.
    3. **Ask the tutor** — a coding agent in your terminal that reads your files and gives one hint at a time, in English or in French: [set it up once](../reference/pi.md).
    4. **Raise your hand** (in class) or post on the forum.

    You type every command yourself. That is the whole point.

## Terminal

| # | Exercise | What you practise | Time |
|---|---|---|---|
| 0.1 | [Ten minutes in the terminal](terminal.md) | `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `cat`, `echo`, `rm` | 10 min |

Lesson: [Session 0 — Setup](../setup.md).

## Git

| # | Exercise | What you practise | Time |
|---|---|---|---|
| 1.1 | [Recipe history](recipe.md) | `clone`, `remote -v`, reading a history you did not write, `restore --source` | 25 min |
| 1.2 | [Scrabble: two features, one conflict](scrabble.md) | two `merge`s — one clean, one conflict you resolve by hand | 25 min |
| 1.3 | [Collaboration: two people, one repository](collab.md) | in teams of two: fork, pull request, `upstream`, the conflict that follows | 40 min |
| extra | [Scrabble counter: three merges in a row](scrabble-three-merges.md) | fast-forward, merge commit and conflict on one project — if you are ahead | 25 min |

Lesson: [Session 1 — Git](../sessions/s1.md) · reading: [Git as a collaboration tool](../reference/git-collaboration.md) (40 min, at home) · class plan: [tutor, then three exercises](../sessions/practice-git.md).

## Python tooling

| # | Exercise | What you practise | Time |
|---|---|---|---|
| 2.1 | [A uv project from scratch](uv-project.md) | `uv init`, `uv add`, `uv sync`, and never committing `.venv` | 20 min |
| 2.2 | [Notebook → script with argparse](argparse-script.md) | turning hard-coded values into command-line arguments | 30 min |
| 2.3 | [Fork and extend the password generator](password-generator.md) | installing someone else's project, then adding two options on two branches | 40 min |
| 2.4 | [Secret hygiene audit](secret-audit.md) | finding a leaked API key in a history, and the right way to store it | 30 min |
| 2.5 | [Polars vs pandas](polars-pandas.md) | the same group-by twice, and what "expressions" buys you | 30 min |

Lesson: [Session 2 — Python tooling](../sessions/s2.md).

## Sessions 3 and 4

Published with the sessions themselves: the `curl` sequence of [Session 3](../sessions/s3.md), and the harness experiment of [Session 4](../sessions/s4.md).
