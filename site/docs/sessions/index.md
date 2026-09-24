# Sessions

The course is four two-hour sessions plus homework before the first one. **They come in this order, and the order is what matters** — not a calendar. The same material is taught to two cohorts that do not advance at the same speed, so no page on this site carries a date. Your cohort's dates and room are announced in class.

Each session has one **lesson page**: the complete written version of what happens in the room, so you can redo the session alone. The practice work is on the [exercise pages](../exercises/index.md), and the durable material you will want to look up again is in [Reference](../reference/index.md).

## Session 0 — Set up your machine

*Homework, before the first class.* A terminal you can type in (Windows/WSL, Git Bash, macOS, Linux, or Codespaces in the browser), an SSH key for GitHub, and your Unistra LLM API key stored as an environment variable.

- Lesson: [Session 0 — Set up your machine](../setup.md)
- Exercise: [0.1 Ten minutes in the terminal](../exercises/terminal.md)
- Reference: [WSL, explained](../reference/wsl.md) if you are on Windows
- Done when: the check command prints your system and your `curl` version.

## Session 1 — Git

Snapshots, commits, branches, merges, conflicts, GitHub. Why version control matters *more* now that agents write code: it is the undo button and the audit trail.

- Lesson: [Session 1 — Git](s1.md)
- Class plan for the practice half: [tutor, then three exercises](practice-git.md)
- Exercises: [1.1 Recipe history](../exercises/recipe.md) · [1.2 Scrabble](../exercises/scrabble.md) · [1.3 Collaboration](../exercises/collab.md)
- Reference: [Git as a collaboration tool](../reference/git-collaboration.md) (forks, pull requests, issues, CI — read at home)
- Deliverable: your personal course repository `agent-lab`, on GitHub.

## Session 2 — Python tooling

Why "it works on my machine" is not a result. `pip` and virtual environments, then `uv`: pinned interpreter, declared dependencies, lockfile. A notebook cell becomes a script with `argparse`. Environment variables, and why a secret never goes in code.

- Lesson: [Session 2 — Python tooling](s2.md)
- Exercises: [2.1](../exercises/uv-project.md) · [2.2](../exercises/argparse-script.md) · [2.3](../exercises/password-generator.md) · [2.4](../exercises/secret-audit.md) · [2.5](../exercises/polars-pandas.md)
- Needs first: your repository from Session 1.
- Deliverable: a reproducible script in your repository, and `UNISTRA_API_KEY` surviving a new terminal.

## Session 3 — What an LLM API actually is

Raw `curl` calls against the university's endpoint: tokens as the unit of account, statelessness, context as something *constructed*, model families, and **tool calling** — for one round, you are the harness.

- Lesson: [Session 3 — What an LLM API actually is](s3.md)
- Needs first: Session 2's environment variable.
- Deliverable: a `step1.json` → `step4` sequence committed to your repository.

## Session 4 — pi, a real harness

The same loop, automated by a real agent harness: provider configuration, permissions you write yourself, `AGENTS.md`, tests as the anchor, subagents and the grill/build pattern.

- Lesson: [Session 4 — pi](s4.md)
- Reference: [pi — install, connect, tutor](../reference/pi.md) (you install pi earlier than Session 4, for the course tutor)
- Deliverable: `AGENTS.md`, a project-local `.pi/`, your `models.json`, and the spec plus implementation from the experiment.

## Optional — Replication track

[LLM-assisted replication](../replication.md) of a published paper that ships a replication package. Any time after Session 2.
