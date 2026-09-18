# 1.1 — Recipe history

Lesson: [Session 1 — Git](../sessions/s1.md) · [All exercises](index.md)

**Goal:** read a history you did not write — the skill you will use on agent-written commits — and meet `git clone` and `git remote`.

```bash title="Any terminal"
cd ~
git clone https://github.com/KnuxV/recipe-history.git
cd recipe-history
git remote -v
git log --oneline
```

**Part 0 — where did this come from?** `git remote -v` prints the address the copy came from, under the name `origin`. It is the instructor's repository: you could read it (it is public), you cannot write to it. Try `git push` — Git asks for credentials or answers `Permission denied`; either way nothing leaves your machine. Your commits will live on your machine only, which is fine for this exercise. (Compare with [your own course repository](../sessions/s1.md#6-the-deliverable-your-course-repository), where `origin` is yours.)

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
