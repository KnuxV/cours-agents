# 1.2 — Scrabble: two features, one conflict

Lesson: [Session 1, section 5 — Branches and merges](../sessions/s1.md#5-branches-and-merges) · [All exercises](index.md)

**Goal:** merge two branches written by two different people into `main`. The first merge goes through alone; the second stops on a **conflict** in a 30-line Python file, and you decide what the final code is.

The repository is on the university's GitLab: [gitlab.unistra.fr/cours_git/exercise_scrabble](https://gitlab.unistra.fr/cours_git/exercise_scrabble). It is public: no account needed to clone it. Its README explains branches and conflicts in more detail; this page is the short version, with the exact commands.

!!! warning "Branch names"
    The README calls the branches `letter-multi` and `word-multiplier`. Their real names are **`letter-multipliers`** and **`word-multipliers`**, as `git branch --all` shows. Use the real names.

**Part 1 — clone and look around.**

```bash title="Any terminal"
cd ~
git clone https://gitlab.unistra.fr/cours_git/exercise_scrabble.git
cd exercise_scrabble
git branch --all
git log --oneline --all --graph
uv run scrabble_score.py
```

`main` holds a small score calculator: `The word 'PYTHON' scores 14 points`. Two developers each added a feature, each on their own branch, both by rewriting the same function, `calculate_score()`. Visit both, run both, then come back:

```bash title="Any terminal, inside exercise_scrabble"
git switch letter-multipliers
uv run scrabble_score.py          # … With letter bonuses: 19 points
git switch word-multipliers
uv run scrabble_score.py          # … On double word score: 28 points
git switch main
git diff letter-multipliers word-multipliers -- scrabble_score.py
```

The last command shows how the two versions of the file differ. Before merging anything, say it in one sentence: what did each developer change in `calculate_score()`?

(No `uv` yet? [Session 2, section 3](../sessions/s2.md#3-install-uv) installs it in two minutes. With a `python3` on your machine, `python3 scrabble_score.py` works too.)

**Part 2 — first merge: it goes through.**

```bash title="Any terminal, inside exercise_scrabble — on main"
git merge letter-multipliers
git log --oneline --graph
uv run scrabble_score.py
```

An editor opens on the message `Merge branch 'letter-multipliers'`: save and quit (nano: ++ctrl+o++, ++enter++, ++ctrl+x++). Expected: `Merge made by the 'ort' strategy.` It is a **merge commit**, not a fast-forward, because `main` had commits of its own; the graph shows the two lines joining. The program now prints the letter bonuses.

**Part 3 — second merge: the conflict.**

```bash title="Any terminal, inside exercise_scrabble — on main"
git merge word-multipliers
git status
```

Expected:

```text
Auto-merging scrabble_score.py
CONFLICT (add/add): Merge conflict in scrabble_score.py
Automatic merge failed; fix conflicts and then commit the result.
```

Nothing is broken. Both branches rewrote the same lines, and Git refuses to guess which version you want. Open `scrabble_score.py` (`nano scrabble_score.py`, or VS Code). There are **two** conflict blocks, each shaped like this:

```text
<<<<<<< HEAD
what main has now (with the letter multipliers)
=======
what word-multipliers brings
>>>>>>> word-multipliers
```

- **Block 1**, at the top: one side has an `import` line, the other has nothing. Which side does the final program need?
- **Block 2**: two versions of `calculate_score()` and of `main()`. Keeping one side would throw away the other developer's feature. Write **one** function that does both: it accepts the letter multipliers *and* a word multiplier, applies the letter bonuses inside the loop, and multiplies the total at the end. Then one `main()` that shows both.

Delete every `<<<<<<<`, `=======` and `>>>>>>>` line, then test and finish the merge:

```bash title="Any terminal, inside exercise_scrabble"
uv run scrabble_score.py
git add scrabble_score.py
git commit -m "Resolve merge conflict: combine letter and word multipliers"
git log --oneline --graph
```

**Done when** `git status` says `nothing to commit, working tree clean`, the graph shows two merge commits, and the program handles the four cases for `PYTHON`: no bonus (14), letter bonuses `(2, 1, 3, 1, 1, 1)` only (19), double word only (28), letter bonuses on a triple word (57). Lost in the middle? `git merge --abort` puts you back to before Part 3.

`git push` will be refused: `origin` is the teacher's repository, and your merge lives on your machine, which is fine here.

**Part 4 — going further: a feature of your own.** `dico.txt` holds 411,430 valid words, one per line, in capitals (the French Scrabble dictionary). On a new branch, make the program say whether the word is valid, and handle the case where `dico.txt` is missing. The workflow is the whole point: `git switch -c <your-branch>` → code → test → `git add`, `git commit` → `git switch main` → `git merge <your-branch>`. This time the merge is a fast-forward; say why.

??? note "Solution — one way to combine the two features"
    Block 1: keep the `import` line, the merged function uses `Tuple`. Block 2:

    ```python
    def calculate_score(word: str, letter_multipliers: Tuple[int, ...] = (), word_multiplier: int = 1) -> int:
        """Calculate score with letter bonuses, then the word bonus"""
        total = 0
        for i, letter in enumerate(word):
            letter_score = get_letter_value(letter)

            # Apply letter multiplier if specified for this position
            if i < len(letter_multipliers):
                letter_score *= letter_multipliers[i]

            total += letter_score

        # Apply word multiplier to final total
        return total * word_multiplier

    def main() -> None:
        word = "PYTHON"
        multipliers = (2, 1, 3, 1, 1, 1)

        print(f"The word '{word}' scores {calculate_score(word)} points normally")
        print(f"With letter bonuses: {calculate_score(word, multipliers)} points")
        print(f"On double word score: {calculate_score(word, word_multiplier=2)} points")
        print(f"With letter bonuses on triple word score: {calculate_score(word, multipliers, 3)} points")
    ```

    Both parameters have a default, so every earlier call still works: `calculate_score(word)` is the basic score. Output: 14, 19, 28, 57. Yours may differ in its names and in what `main()` prints; what matters is that no conflict marker is left, both features survive, and the program runs. That a conflict is resolved by *writing the code you want*, not by picking a side, is the lesson.

    Part 4, the core of it:

    ```python
    def is_valid(word: str, path: str = "dico.txt") -> bool:
        try:
            with open(path, encoding="utf-8") as f:
                return word.upper() in {line.strip() for line in f}
        except FileNotFoundError:
            raise SystemExit(f"{path} not found: run the script from the repository folder.")
    ```

    The merge is a fast-forward because `main` did not move while you worked on your branch ([S1 §5.3](../sessions/s1.md#53-case-1-main-has-not-moved-fast-forward)).

Want more merges? [Scrabble counter: three merges in a row](scrabble-three-merges.md) does it again on a larger project.
