# Extra — Scrabble counter: three merges in a row

Lesson: [Session 1, section 5 — Branches and merges](../sessions/s1.md#5-branches-and-merges) · [All exercises](index.md)

**Goal:** see the three outcomes of `git merge` from [S1 §5](../sessions/s1.md#5-branches-and-merges) on a real Python project, and resolve a conflict by hand.

```bash title="Any terminal"
cd ~
git clone https://github.com/KnuxV/scrabble-counter.git
cd scrabble-counter
git log --oneline
git branch -a
```

`git branch -a` lists your one local branch, `main`, and three **remote-tracking** branches: `origin/add-readme`, `origin/german`, `origin/portuguese`. They are Git's memory of the branches on GitHub; switching to one creates a local branch that follows it:

```bash title="Any terminal, inside scrabble-counter"
git switch add-readme
git switch german
git switch portuguese
git switch main
git log --oneline --all --graph
```

Read the graph: all three branches start from the same commit on `main`. Now merge them in this order and watch what Git says each time.

**Merge 1 — `add-readme`.** `main` has not moved since the branch was made.

```bash title="Any terminal, inside scrabble-counter — on main"
git merge add-readme
git log --oneline --graph
```

Expected: `Fast-forward`. No new commit; `main` simply moved up one.

**Merge 2 — `german`.** `main` *has* moved now (the README commit), and `german` does not have it.

```bash title="Any terminal, inside scrabble-counter — on main"
git merge german
git log --oneline --graph
```

Expected: an editor opens on `Merge branch 'german'` (save and quit), then `Merge made by the 'ort' strategy`. The graph shows a diamond: a merge commit with two parents. The two sides changed different lines, so Git combined them alone.

**Merge 3 — `portuguese`.** Both `german` and `portuguese` added a language *at the same place* in `score.py`, and both edited the same `choices=[...]` line.

```bash title="Any terminal, inside scrabble-counter — on main"
git merge portuguese
git status
```

Expected:

```text
Auto-merging score.py
CONFLICT (content): Merge conflict in score.py
Auto-merging tests/test_score.py
Automatic merge failed; fix conflicts and then commit the result.
```

`git status` says `both modified: score.py` (the tests file merged fine on its own). Open `score.py`; there are **two** conflict blocks. Resolve both so that the program knows *both* languages: keep the German block *and* the Portuguese block in the dictionary, and one `choices` line that lists `"DE"` and `"PT"`. Delete every `<<<<<<<`, `=======`, `>>>>>>>` line. Then:

```bash title="Any terminal, inside scrabble-counter"
git add score.py
git commit                     # accept the proposed message
git log --oneline --graph
uv run score.py HALLO -l DE    # The word 'HALLO' (DE) scores 9 points
uv run score.py CASA -l PT     # The word 'CASA' (PT) scores 5 points
uv run --with pytest pytest    # 56 passed
```

(No `uv` yet? [S2 §3](../sessions/s2.md#3-install-uv) installs it in two minutes. With a `python3` on your machine, `python3 score.py HALLO -l DE` works too.)

**Done when** `git log --oneline --graph` shows two merge commits and both languages score correctly. Lost? `git merge --abort` puts you back to before merge 3.

??? note "Solution — the resolved hunks"
    First block: the German dictionary ends with `'Q': 10, 'Y': 10` and a closing brace; the Portuguese one follows. The only thing to add by hand is the comma after the German block's closing brace:

    ```python
            "DE": {
                'A': 1, 'D': 1, 'E': 1, 'I': 1, 'N': 1, 'R': 1, 'S': 1, 'T': 1, 'U': 1,
                'G': 2, 'H': 2, 'L': 2, 'O': 2,
                'B': 3, 'M': 3, 'W': 3, 'Z': 3,
                'C': 4, 'F': 4, 'K': 4, 'P': 4,
                'J': 6, 'V': 6,
                'X': 8,
                'Q': 10, 'Y': 10
            },
            "PT": {
                'A': 1, 'E': 1, 'I': 1, 'O': 1, 'S': 1, 'U': 1, 'M': 1, 'R': 1, 'T': 1,
                'D': 2, 'L': 2, 'C': 2, 'P': 2,
                'N': 3, 'B': 3,
                'F': 4, 'G': 4, 'H': 4, 'V': 4,
                'J': 5,
                'Q': 6,
                'X': 8, 'Z': 8
            }
        }
    ```

    Second block, one line:

    ```python
        parser.add_argument("-l", "--lang", default="EN", choices=["EN", "FR", "ES", "IT", "DE", "PT"],
    ```

    Verified: after this resolution `uv run --with pytest pytest` reports `56 passed`, and the graph reads, newest first: `Merge branch 'portuguese'` (two parents) → `Merge branch 'german'` (two parents) → `Add a README with usage` → …
