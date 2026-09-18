# Git branches and merges

Course page: <https://knuxv.github.io/cours-agents/sessions/s1/> (section 2 for the mental model, section 5 for branches, cheat sheet in section 7).

## The mental model the course uses

- Three places: the working folder, the staging area (`git add`), the history (`git commit`). A commit is a snapshot of the whole project.
- A branch is a pointer to a commit, a label that moves forward when you commit. `main` is the version that works; a branch is a safe copy to try something on.
- The rule for merging, which students are meant to see for themselves: **fast-forward if `main` has not moved, merge commit if it has**, conflict when both sides changed the same line.

## Course conventions

- `git switch -c <name>` creates a branch and moves to it; `git switch main` comes back. The course uses `switch`, not `checkout`.
- Merge from the receiving branch: `git switch main`, then `git merge <name>`. Delete the merged branch with `git branch -d <name>`.
- The drawing is the teaching tool: `git log --oneline --all --graph` after every commit and every merge. Ask what they see in it before explaining.
- Look before you commit: `git status`, then `git diff`.
- One branch per feature, merged before the next one starts (exercises 1.3 and 2.3).

## Usual stumbles

| What the student sees | Where to point them |
|---|---|
| Their file "disappeared" after `git switch main` | Which branch holds the commit that added it? The graph shows it |
| `Already up to date` on merge | Which branch are they on? They are merging a branch into itself, or into the wrong side |
| `error: Your local changes would be overwritten` on switch | `git status`: uncommitted work. Commit it on this branch first |
| An editor opens during `git merge` (merge commit message) | It is asking for a message. nano: Ctrl+O, Enter, Ctrl+X. vim: `:wq` (setup breakage, give it directly) |
| `CONFLICT (content)` | Open the file: what is between `<<<<<<<`, `=======` and `>>>>>>>`? Which lines should the final file keep? Then `git add`, `git commit` |
| They committed on `main` instead of the branch | Nothing is lost. What does the graph show? For a course exercise, carrying on from there is fine |
| `fatal: not a git repository` | `pwd`: which folder are they in? |

## Exercises

- **1.2 Scrabble: two features, one conflict** (<https://knuxv.github.io/cours-agents/exercises/scrabble/>), the exercise most students are on. `git clone https://gitlab.unistra.fr/cours_git/exercise_scrabble.git`, folder `exercise_scrabble`, one Python file `scrabble_score.py` plus `dico.txt`. Branches: `main`, `letter-multipliers`, `word-multipliers` (the repository's README wrongly calls them `letter-multi` and `word-multiplier`: `fatal: invalid reference` or `merge: … not something we can merge` means the student used the README's names; point them to `git branch --all`). On `main`: `git merge letter-multipliers` makes a merge commit (an editor opens for the message; not a fast-forward, `main` has its own commits); `git merge word-multipliers` stops with `CONFLICT (add/add)` in `scrabble_score.py`, two blocks. Block 1: an `import` of `Tuple` against nothing; keep the import. Block 2: two versions of `calculate_score()` and `main()`, one taking `letter_multipliers` (a tuple, applied per position inside the loop), the other `word_multiplier` (an int, applied to the total). The expected resolution is neither side: one function accepting both parameters, each with a default, letter bonuses in the loop and the word multiplier on the total. This is Python writing, so rungs 1–3 are about what the merged function must accept and do; never dictate the function. Done when no marker is left, `git status` is clean after `git add` + `git commit`, the graph shows two merge commits, and for `PYTHON` the program gives 14 (no bonus), 19 (letters `(2, 1, 3, 1, 1, 1)`), 28 (double word), 57 (both, triple word). `git merge --abort` goes back to before the conflict. `git push` is refused (teacher's repository): expected. Part 4, stretch: on a branch of their own, check the word against `dico.txt` (one uppercase word per line, French dictionary), handle the missing file, merge back: a fast-forward, and they should say why.
- **Scrabble counter: three merges in a row**, the follow-up for students who are ahead (<https://knuxv.github.io/cours-agents/exercises/scrabble-three-merges/>). `git clone https://github.com/KnuxV/scrabble-counter.git` into the home folder. Three remote branches, `add-readme`, `german`, `portuguese`, all starting from the same commit of `main`; `git switch <name>` creates the local branch that follows `origin/<name>`. Merged into `main` in that order: `add-readme` gives `Fast-forward`; `german` gives a merge commit (an editor opens for the message); `portuguese` gives `CONFLICT (content)` in `score.py` only, in two places: the dictionary of letter values (keep the `"DE"` block and the `"PT"` block, with a comma between them) and the `choices=[...]` line of `parser.add_argument` (one line listing both `"DE"` and `"PT"`). `tests/test_score.py` merges by itself. `git merge --abort` goes back to before the third merge. Done when `git log --oneline --graph` shows two merge commits, `uv run score.py HALLO -l DE` scores 9, `uv run score.py CASA -l PT` scores 5, and `uv run --with pytest pytest` reports `56 passed`. The point of the exercise is reading the conflict markers: have the student say what each side contains before anything about the fix.
- **1.1 Recipe history** (<https://knuxv.github.io/cours-agents/exercises/recipe/>). `git clone https://github.com/KnuxV/recipe-history.git`: eight commits on one file, `recipe.md`. The student reads the history (`git log --oneline`, `git show <hash>`, `git diff <a> <b>`), sees `git push` refused (`origin` is the teacher's repository, they have no write access: expected, not an error to fix), answers four questions from `git show` alone (the typo fix, whether every ingredient scaled by the same factor, what the butter-to-oil commit also touches), then must bring back the original sugar quantity while keeping the later serving suggestion. The statement makes them try `git restore --source=<hash> recipe.md` first: a trap, since `restore` works on whole-file snapshots, so the serving suggestion vanishes too and `git diff` shows it. The intended fix: `git restore recipe.md` to drop that, edit the one sugar line by hand, `git add`, `git commit`. Done when `git diff` shows exactly one changed line before the commit. Read the statement's questions with the student rather than answering them.
