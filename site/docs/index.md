# Meta-programming

**Terminals, APIs, and coding agents** — 8 hours (4 × 2h) plus an optional research mini-module. M2, Université de Strasbourg.

!!! tip "Three kinds of page, three tabs at the top"
    **[Sessions](sessions/index.md)** — what happens in class, one lesson page per session, written in full so you can redo a session alone. Start with [Session 0](setup.md): it is homework, before the first class.

    **[✏️ Exercises](exercises/index.md)** — one page per exercise: the statement, the lesson section to lean on, how you know you are done, and a folded solution.

    **[Reference](reference/index.md)** — the durable material, not tied to a session: WSL, Git collaboration, the `pi` agent. Look things up here during the course and after it. The search box at the top searches everything.

## The idea of the course

An "AI coding agent" is not magic. It is an HTTP call in a loop, wrapped in engineering decisions: what goes in the context, which tools it may call, what it is allowed to do without asking, and how its work gets verified.

By the end of these four sessions you will have:

- built that loop **by hand**, with `curl`, against the university's own LLM platform (free, sovereign, no personal API key to buy);
- configured a professional agent harness ([pi](https://pi.dev)) and made its reliability levers explicit — permissions, standing instructions, tests, separation of powers between agents;
- learned to reason about *when to trust it*, and when to drop down a level.

Along the way you leave the browser-and-Colab workflow behind: a terminal, `git`, reproducible Python projects with `uv`, and secrets kept out of code.

This is the first part of the Advanced Programming class. A later 15-hour block covers MCP and Hugging Face. The exam is a single presentation for the two classes together.

## The four sessions, in order

This site is keyed to **content, not to a calendar**: the same material is taught to two cohorts that do not advance at the same speed, so dates and rooms are announced in class, not written here. What is fixed is the order — each session needs the one before it.

| Order | Session | Content | Exercises | Deliverable |
|---|---|---|---|---|
| **First, at home** | [Session 0 — Setup](setup.md) *(homework)* | A working terminal (WSL / Git Bash / macOS / Linux / Codespaces) and a Unistra LLM API key | [0.1](exercises/terminal.md) | Your terminal passes the check command |
| **1** | [S1 — Git](sessions/s1.md) | Snapshots, commits, branches, GitHub. Why version control is the undo button and the audit trail of agent-written code | [1.1](exercises/recipe.md) · [1.2](exercises/scrabble.md) · [1.3](exercises/collab.md) | Your personal course repo on GitHub |
| **2** | [S2 — Python tooling](sessions/s2.md) | `uv` projects and lockfiles, `argparse` (notebook → script), environment variables and secrets | [2.1](exercises/uv-project.md) · [2.2](exercises/argparse-script.md) · [2.3](exercises/password-generator.md) · [2.4](exercises/secret-audit.md) · [2.5](exercises/polars-pandas.md) | A reproducible script in your repo |
| **3** | [S3 — What an LLM API actually is](sessions/s3.md) | Raw `curl` calls: tokens, statelessness, constructed context, model families, **tool calling** — you *are* the harness for one round | *published with the session* | `step1.json` → `step4` sequence committed to your repo |
| **4** | [S4 — pi](sessions/s4.md) | A real harness: provider config, the loop observed, permissions you write yourself, `AGENTS.md`, subagents, the grill/build pattern, the A/B/C reliability experiment | *published with the session* | `AGENTS.md`, `.pi/` extensions and agent definitions, spec + implementation |
| Any time after 2 | [Replication track](replication.md) *(optional)* | LLM-assisted replication of a published paper that ships a replication package | — | A short replication memo |

More detail on each one, and the reference material it draws on: [Sessions](sessions/index.md).

## Exercises

Eleven exercises, one page each. Everything stays online, so you can finish them at home.

- **Terminal:** [0.1 Ten minutes in the terminal](exercises/terminal.md)
- **Git:** [1.1 Recipe history](exercises/recipe.md) · [1.2 Scrabble — merge and conflict](exercises/scrabble.md) · [1.3 Collaboration, in teams of two](exercises/collab.md) · [extra: three merges in a row](exercises/scrabble-three-merges.md)
- **Python tooling:** [2.1 A uv project from scratch](exercises/uv-project.md) · [2.2 Notebook → script with argparse](exercises/argparse-script.md) · [2.3 Password generator](exercises/password-generator.md) · [2.4 Secret hygiene audit](exercises/secret-audit.md) · [2.5 Polars vs pandas](exercises/polars-pandas.md)

The [exercise index](exercises/index.md) lists them with times and tells you how to work when you are stuck. You can also give yourself a [tutor that answers in your terminal](reference/pi.md).

## What you need

- Your own laptop (Windows 10/11, macOS or Linux), or one of the university's Linux desktops. No software purchase. The university desktops give you no administrator rights (no `sudo`); Sessions 0 and 1 need none, and every later tool installs into your home folder.
- A [GitHub](https://github.com/) account (created in Session 1 if you do not have one; needed earlier only for the Codespaces fallback).
- Access to [conversation.ia.unistra.fr](https://conversation.ia.unistra.fr/) with your university login — see [Session 0](setup.md).

## Exam

A presentation in front of the class of a coding project on a topic of your choice, as long as you show how you applied the concepts of the course (the loop, git history of what the agent did, tests, permissions). Details and rubric: TODO.

## Links

- Course repository: [KnuxV/cours-agents](https://github.com/KnuxV/cours-agents) (last year's material: [KnuxV/advanced_programming_python](https://github.com/KnuxV/advanced_programming_python)).
- Course forum: TODO(verify) — link to the Moodle/forum.
- [Unistra AI platform](https://conversation.ia.unistra.fr/) · [Unistra API documentation](https://documentation.unistra.fr/DNUM/Intelligence_artificielle/guide_complet_IA/co/7_1API.html) (French)
- [Sessions](sessions/index.md) · [Exercises](exercises/index.md) · [Reference](reference/index.md) · [pi — install the agent and the course tutor](reference/pi.md) · [Resources](resources.md)
