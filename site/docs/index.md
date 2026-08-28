# Advanced Programming for Economists

**Terminals, APIs, and coding agents** — 8 hours (4 × 2h) plus an optional research mini-module. M2, Université de Strasbourg.

## The idea of the course

An "AI coding agent" is not magic. It is an HTTP call in a loop, wrapped in engineering decisions: what goes in the context, which tools it may call, what it is allowed to do without asking, and how its work gets verified.

By the end of these four sessions you will have:

- built that loop **by hand**, with `curl`, against the university's own LLM platform (free, sovereign, no personal API key to buy);
- configured a professional agent harness (OpenCode) and made its reliability levers explicit — permissions, standing instructions, tests, separation of powers between agents;
- learned to reason about *when to trust it*, and when to drop down a level.

Along the way you leave the browser-and-Colab workflow behind: a terminal, `git`, reproducible Python projects with `uv`, and secrets kept out of code.

This is the first part of the Advanced Programming class. A later 15-hour block covers MCP and Hugging Face. The exam is a single presentation for the two classes together.

## Schedule

All sessions take place in room **A330 (Idem-Lab)**.

| When | Session | Content | Deliverable |
|---|---|---|---|
| **Before Mon 14 Sep** | [Session 0 — Setup](setup.md) *(homework)* | A working terminal (WSL / Git Bash / macOS / Codespaces) and a Unistra LLM API key | Your terminal passes the check command |
| **Mon 14 Sep 2026**, 14:00–16:00 | [S1 — Git](sessions/s1.md) | Snapshots, commits, branches, GitHub. Why version control is the undo button and the audit trail of agent-written code | Your personal course repo on GitHub |
| **Fri 18 Sep 2026**, 15:00–17:00 | [S2 — Python tooling](sessions/s2.md) | `uv` projects and lockfiles, `argparse` (notebook → script), environment variables and secrets | A reproducible script in your repo |
| **Fri 25 Sep 2026**, 14:00–16:00 | [S3 — What an LLM API actually is](sessions/s3.md) | Raw `curl` calls: tokens, statelessness, constructed context, model families, **tool calling** — you *are* the harness for one round | `step1.json` → `step4` sequence committed to your repo |
| **Fri 16 Oct 2026**, 13:00–15:00 | [S4 — OpenCode](sessions/s4.md) | A real harness: provider config, the loop observed, permissions, `AGENTS.md`, subagents, the grill/build pattern, the A/B/C reliability experiment | `opencode.json`, `AGENTS.md`, agent definitions, spec + implementation |
| Optional | [Replication track](replication.md) | LLM-assisted replication of a published economics paper | A short replication memo |

## What you need

- Your own laptop (Windows 10/11 or macOS). No software purchase.
- A [GitHub](https://github.com/) account (created in Session 1 if you do not have one; needed earlier only for the Codespaces fallback).
- Access to [conversation.ia.unistra.fr](https://conversation.ia.unistra.fr/) with your university login — see [Session 0](setup.md).

## Exam

A presentation in front of the class of a coding project on a topic of your choice, as long as you show how you applied the concepts of the course (the loop, git history of what the agent did, tests, permissions). Details and rubric: TODO.

## Links

- Course repository: [KnuxV/cours-agents](https://github.com/KnuxV/cours-agents) (last year's material: [KnuxV/advanced_programming_python](https://github.com/KnuxV/advanced_programming_python)).
- Course forum: TODO(verify) — link to the Moodle/forum.
- [Unistra AI platform](https://conversation.ia.unistra.fr/) · [Unistra API documentation](https://documentation.unistra.fr/DNUM/Intelligence_artificielle/guide_complet_IA/co/7_1API.html) (French)
- [Exercises index](exercises.md) · [Resources](resources.md)
