# 1.3 — Collaboration: two people, one repository

Lesson: [Session 1½ — Git as a collaboration tool](../sessions/s1-collab.md) (clone vs fork, pull requests) · [All exercises](index.md)

**Goal:** work the way every software team works. Two people change the same program at the same time, one through a **fork** and a **pull request**, and the two of you resolve the conflict that follows.

**Teams of two.** Decide who is **A** (owns the repository) and who is **B** (contributes through a fork). Sit side by side. Both of you need a GitHub account you can push to from the terminal: [Session 1, section 6.2](../sessions/s1.md#62-log-in-to-github-from-the-terminal-once).

The program is a small deck of **flashcards** about the course: it prints one random question and its answer. You will write the cards yourselves, which is also a way to revise.

## Phase 1 — A creates the repository (10 min)

**A**, on [github.com/new](https://github.com/new): name `flashcards-<your-two-names>`, **Public**, tick **Add a README file**, *Create repository*. Then clone it:

```bash title="A — any terminal"
cd ~
git clone https://github.com/A-USERNAME/flashcards-<your-two-names>.git
cd flashcards-<your-two-names>
```

Create `quiz.py` in that folder (`nano quiz.py`, or VS Code) with this content:

```python title="quiz.py"
import random

# Git flashcards: (question, answer)
git_cards = [
    ("Which command shows the history, one line per commit?", "git log --oneline"),
    ("Which command creates a branch and moves to it?", "git switch -c <name>"),
    ("Which command shows what changed but is not staged yet?", "git diff"),
]


def print_random_card():
    """Print a random flashcard: the question, then the answer."""
    question, answer = random.choice(git_cards)
    print(f"Q: {question}")
    print(f"A: {answer}")


if __name__ == "__main__":
    print("Flashcards for the course")
    print_random_card()
```

Run it, commit it, push it:

```bash title="A — inside the repository"
uv run quiz.py
git add quiz.py
git commit -m "Add the flashcards program"
git push
```

**A gives the repository's URL to B.** B waits for this push before forking.

## Phase 2 — both of you work at the same time (15 min)

Each of you makes a change **on a branch**, without looking at the other's screen. Both changes touch the function `print_random_card()`: that is on purpose.

### A — a second deck

```bash title="A — inside the repository"
git switch -c add-terminal-cards
```

Your mission:

- add a second list, `terminal_cards`, with at least three cards about the terminal (`pwd`, `ls -a`, `mv`…), written by you;
- change `print_random_card()` so that it picks a card from **both** decks;
- `uv run quiz.py` a few times to check.

Then commit, merge into `main` yourself, and push:

```bash title="A — inside the repository"
git add quiz.py
git commit -m "Add a deck of terminal flashcards"
git switch main
git merge add-terminal-cards
git push
```

### B — topics

On A's repository page on GitHub, click **Fork** → *Create fork*. You now have a copy under *your* account. Clone **your fork**, not A's repository:

```bash title="B — any terminal"
cd ~
git clone https://github.com/B-USERNAME/flashcards-<your-two-names>.git
cd flashcards-<your-two-names>
git remote -v
git switch -c add-topics
```

`git remote -v` must show *your* username: `origin` is your fork, the only place you may push to.

Your mission:

- give `print_random_card()` a parameter, `topic`, with `"git"` as its default value;
- make the output start with a label, such as `[GIT] Q: …`;
- in the last lines of the file, call the function with a topic;
- `uv run quiz.py` a few times to check.

Then commit and push the **branch** to your fork:

```bash title="B — inside the repository"
git add quiz.py
git commit -m "Let the caller choose a topic, and label the output"
git push -u origin add-topics
```

On GitHub, your fork now shows a yellow banner: **Compare & pull request**. Click it, check that the arrow reads `A-USERNAME/…  main  ←  B-USERNAME/…  add-topics`, write one sentence saying what the change does, *Create pull request*.

## Phase 3 — the conflict, together (15 min)

**A** opens the pull request (tab *Pull requests* of the repository). If A pushed first, GitHub says **This branch has conflicts that must be resolved**: both of you rewrote the same lines of the same function. Nobody made a mistake; it is what happens when two people work at once.

The conflict is resolved **on B's machine**, with A sitting next to B. B first needs A's latest commits. A fork does not follow the original repository by itself; B adds it as a second remote, called `upstream` by convention:

```bash title="B — inside the repository, on the branch add-topics"
git remote add upstream https://github.com/A-USERNAME/flashcards-<your-two-names>.git
git remote -v
git fetch upstream
git merge upstream/main
```

Expected: `CONFLICT (content): Merge conflict in quiz.py`. Open `quiz.py`: between `<<<<<<< HEAD` and `=======` is B's version, between `=======` and `>>>>>>> upstream/main` is A's. **Together**, write the function that does both: it knows both decks *and* takes a topic. Delete the three marker lines, then:

```bash title="B — inside the repository"
uv run quiz.py
git add quiz.py
git commit -m "Merge upstream main: both decks, with topics"
git push
```

The pull request updates by itself. **A** reloads the page: the conflict message is gone. A reads the diff (tab *Files changed*), then *Merge pull request* → *Confirm merge*.

Finally, both of you bring your `main` up to date:

```bash title="A — inside the repository"
git switch main
git pull
uv run quiz.py
```

```bash title="B — inside the repository"
git switch main
git pull upstream main
git push
uv run quiz.py
```

**Done when** both of you run the same `quiz.py`, it shows cards from both decks with their label, and `git log --oneline --graph` shows commits by two authors joined by a merge.

## Phase 4 — another round

Swap roles in spirit: this time B's change goes in first. Ideas: a third deck (Python, `uv`), a `--topic` option read from the command line, a score, cards in French. One branch per idea, one pull request per branch. B starts every new branch from an up-to-date `main` (`git switch main`, `git pull upstream main`), and conflicts become rare.

??? note "Solution — one way to combine the two changes"
    ```python
    def print_random_card(topic="git"):
        """Print a random flashcard of one topic: the question, then the answer."""
        decks = {"git": git_cards, "terminal": terminal_cards}
        question, answer = random.choice(decks[topic])
        print(f"[{topic.upper()}] Q: {question}")
        print(f"A: {answer}")


    if __name__ == "__main__":
        print("Flashcards for the course")
        print_random_card(random.choice(["git", "terminal"]))
    ```

    Yours will differ, because each of you wrote your own version first. What matters: no marker line is left, A's deck and B's topics both survive, and the program runs.

    If B pushed the pull request *before* A pushed `main`, the pull request merges without conflict, and it is A's `git push` that is refused (`! [rejected] … fetch first`). Then A runs `git pull --no-rebase` and gets the same conflict, on A's machine: resolve it there, the same way.
