# Class plan — the tutor, then three Git exercises

This is the plan for a two-hour practice class, and it works just as well alone at home. Two parts: first you give yourself a **tutor** (about 30 minutes, together), then you work through the **three Git exercises** at your own pace, with the [Session 1 lesson](s1.md) open and the tutor beside you.

If you are looking for the exercises on their own, they are [1.1, 1.2 and 1.3 here](../exercises/index.md#git). This page adds the setup, the order, and which lesson section to lean on for each one.

| | What | Time |
|---|---|---|
| Part 1 | [Set up pi and the tutor](#part-1-set-up-pi-and-the-tutor) — steps 1 to 5 | 30 min |
| Part 2 | [Exercise 1 — Recipe history](#exercise-1-recipe-history) (read a history, undo one change) | 25 min |
| | [Exercise 2 — Scrabble](#exercise-2-scrabble) (two merges, one conflict) | 25 min |
| | [Exercise 3 — Collaboration](#exercise-3-collaboration) (teams of two: fork, pull request, conflict) | 40 min |

Not finished when the class ends? Everything here stays online, and the tutor works at home too.

## Part 1 — Set up pi and the tutor

[pi](../reference/pi.md) is a coding agent that runs in your terminal and talks to the university's own language models: free, and nothing leaves Strasbourg. Here you use it as a **tutor**: it reads your files, explains what is on your screen and gives hints, and it cannot change anything.

Do the five steps in order. Each one ends with a check; do not go on until the check passes. Raise your hand early: a setup problem is not the lesson.

### Step 1 — Your API key

You need a personal key for the university's platform, stored in the variable `UNISTRA_API_KEY`. Check whether you already have it:

```bash title="Any terminal — new window"
echo $UNISTRA_API_KEY | cut -c1-6
```

- It prints `sk-` and three characters: done, go to step 2.
- It prints an empty line: follow [Setup, section 5](../setup.md#5-your-unistra-llm-api-key) — generate the key on [conversation.ia.unistra.fr](https://conversation.ia.unistra.fr/) (5.1), store it (5.2), open a **new** terminal, run the check again.

### Step 2 — Install pi

Follow [pi, section 2](../reference/pi.md#2-install-pi): pick the tab of your machine (WSL / Linux, Mac, Git Bash, Codespaces). Then, in a **new** terminal:

```bash title="Any terminal — new window"
pi --version
```

Check: a version number, `0.85.1` or later.

### Step 3 — Connect pi to the university's models

Follow [pi, section 3](../reference/pi.md#3-connect-pi-to-the-universitys-models). It is one download, then:

```bash title="Any terminal"
pi -p "Reply with one word: pong"
```

Check: `pong`.

### Step 4 — Get the tutor, and run it

Get it, once ([pi, section 5.1](../reference/pi.md#51-install-it)):

```bash title="Any terminal"
pi install git:github.com/KnuxV/cours-agents
```

Run it, every time, **from the folder of the exercise you are working on** ([pi, section 5.2](../reference/pi.md#52-use-it)):

```bash title="Any terminal, inside the exercise's folder"
pi --tools read,grep,find,ls
```

`--tools read,grep,find,ls` is what makes it a tutor: with these four tools the model can read and search your files, and nothing else. Then call it and say where you are:

=== "English"

    ```text title="Inside pi"
    /skill:tutor I am on the recipe history exercise, question 2. I do not understand what git show prints.
    ```

=== "Français"

    ```text title="Dans pi"
    /skill:tuteur Je suis sur l'exercice recipe history, question 2. Je ne comprends pas ce qu'affiche git show.
    ```

Check: it answers with a question or a hint, not with the solution.

!!! tip "Two terminals"
    Keep **one terminal for your work** and **a second one for pi**, both in the exercise's folder. To show the tutor what you see, type the command in pi with a `!` in front: `!git status`, `!git log --oneline --graph --all`. To leave pi: `/quit`.

### Step 5 — Install `uv`

The exercises run Python programs with `uv`, which also installs Python for you. Follow [Session 2, section 3](s2.md#3-install-uv) (one command), then, in a **new** terminal:

```bash title="Any terminal — new window"
uv --version
```

Check: `uv 0.12` or later.

## Part 2 — Three exercises

How to work:

1. **Read the statement**, try it.
2. **Stuck? Open the lesson** — each exercise below names the sections to read. The lesson pages are written to be followed alone.
3. **Still stuck? Ask the tutor.** Paste the exact error or rerun the command with `!`. It gives one hint at a time, and the exact answer only after you have tried: an attempt, even a failed one, is what unlocks it.
4. **Still stuck? Raise your hand.**

You type every command yourself. The solutions are on the exercise pages, folded; open them when you are done, or after a real attempt.

### Exercise 1 — Recipe history

Clone a small repository with eight commits, read its history, and bring back one line from the past.

- **Statement:** [1.1 — Recipe history](../exercises/recipe.md)
- **Lesson to lean on:** [Session 1, sections 4.5–4.6](s1.md#45-git-log-git-show-read-the-history) (`log`, `diff`, `show`, `restore`) · [cheat sheet](s1.md#7-cheat-sheet)
- **Tutor:** start pi inside `~/recipe-history`

### Exercise 2 — Scrabble

Two developers each added a feature to a small Scrabble score calculator, on two branches. Merge both into `main`: the first merge goes through, the second stops on a conflict that you resolve by hand.

- **Statement:** [1.2 — Scrabble: two features, one conflict](../exercises/scrabble.md)
- **Lesson to lean on:** [Session 1, section 5 — Branches and merges](s1.md#5-branches-and-merges), especially [5.5, the conflict](s1.md#55-case-3-both-sides-changed-the-same-line-conflict)
- **Tutor:** start pi inside `~/exercise_scrabble`

### Exercise 3 — Collaboration

**In teams of two.** One of you creates a repository on GitHub, the other forks it; you both change the same small program at the same time, and you merge your work through a pull request, conflict included.

- **Before you start:** each of you needs a GitHub account you can push to from the terminal ([Session 1, section 6.2](s1.md#62-log-in-to-github-from-the-terminal-once)).
- **Statement:** [1.3 — Collaboration: two people, one repository](../exercises/collab.md)
- **Lesson to lean on:** [Git as a collaboration tool](../reference/git-collaboration.md), sections 1 to 3 (remotes, clone vs fork, pull requests)
- **Tutor:** each of you starts pi inside your own `~/flashcards-…` folder

Ahead of the others? [Three merges in a row](../exercises/scrabble-three-merges.md), or Phase 4 of exercise 3.

## If something breaks

| Symptom | Where to look |
|---|---|
| `pi: command not found`, `No models available`, `401`, `/skill:tutor` not offered | [pi — When things go wrong](../reference/pi.md#6-when-things-go-wrong) |
| `uv: command not found`, `No module named …` | [Session 2 — When things go wrong](s2.md#9-when-things-go-wrong) |
| Nothing installs on your machine | [GitHub Codespaces](../setup.md#path-c-github-codespaces-the-lifeboat): a full Linux terminal in your browser |
| The tutor hands out full solutions, or rambles | `/new`, then call `/skill:tutor` again |
