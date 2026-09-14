---
title: Meta-programming
sub_title: "terminals, APIs, and coding agents — 8 hours"
author: Kevin Michoud — Université de Strasbourg
---

<!-- speaker_note: Opening deck, 15–20 min before Session 1 starts. Goal is that students know what the 8 hours are, why we live in a terminal, and that the bar is "practice", not "mastery". Course site is the reference; slides are prompts. -->

What this course is
===

An **AI coding agent** is not magic.

<!-- pause -->

It is an **HTTP call in a loop**, wrapped in engineering decisions:

- what goes in the context
- which tools it may call
- what it may do without asking
- how its work gets checked

<!-- pause -->

In 8 hours you build that loop **by hand**, then run a real one.

<!-- speaker_note: This is the thesis. Say it once now, repeat it at the start of S3 and S4. -->

<!-- end_slide -->

The 8 hours
===

| | Session | You leave with |
|---|---|---|
| 2h | **Git** | your course repo on GitHub |
| 2h | **Python tooling** — `uv`, `argparse`, env vars | a reproducible script |
| 2h | **The LLM API, raw** — `curl` | you *are* the agent for one round |
| 2h | **A real agent harness** — pi | permissions and rules you wrote |

<!-- pause -->

First half: **foundations**. Second half: **agents**.

<!-- speaker_note: Foundations are not a detour. Sessions 3 and 4 do not work without a terminal, a git repo, and a project with dependencies pinned. Say that the agent in S4 runs git and bash *for* them — they need to read what it did. -->

<!-- end_slide -->

Where this sits
===

- First part of **Advanced Programming**
- A later 15h block: MCP, Hugging Face
- **One exam** for both: a presentation of a coding project of your choice

<!-- pause -->

What we grade: did you apply the ideas?
The loop, a git history of what the agent did, tests, permissions.

<!-- speaker_note: Exam rubric is still TODO on the site. Do not promise details. -->

<!-- end_slide -->

Why a terminal?
===

Every **server** runs Linux. No mouse, no windows.

<!-- pause -->

The cloud, data pipelines, model training, deployments:
all of it is text commands in a terminal.

<!-- pause -->

The **agent** in Session 4 works the same way.
It reads files and runs commands. In a terminal.

<!-- speaker_note: Hammer point, the terminal is the interface of every machine that is not a laptop. When they watch the agent work in S4, they will recognise every command. -->

<!-- end_slide -->

Why a terminal? (2)
===

Same commands on **Mac**, **Linux**, and **Windows through WSL**.

<!-- pause -->

What you learn here transfers as is:
to a server, to a cloud machine, to a colleague's laptop.

<!-- pause -->

And any AI you ask for help will answer in terminal commands.
You need to be able to **read** them.

<!-- speaker_note: The last point lands well with students who already use ChatGPT for code. The chatbot gives them `pip install x` and they do not know where to type it. -->

<!-- end_slide -->

Honest expectations
===

Many of you will work in **Excel, Power BI, locked-down company tools**.

<!-- pause -->

That is fine. This is still worth 8 hours:

- it is the only slot in your master to see the **geeky side** of tech
- understanding how it works changes how you use the polished tools
- for some of you it is a **gateway** to something more

<!-- speaker_note: Say this plainly. It lowers anxiety and removes the "why do I need this" objection before it is voiced. Economics room, this is the price of admission to reproducible research and to any data job. -->

<!-- end_slide -->

The bar
===

**Practice**, not mastery.

<!-- pause -->

- you will type commands you do not fully understand yet — normal
- you will get errors — that is the exercise
- `git status` and the site's cheat sheet are always the next step

<!-- pause -->

Eight hours in the terminal. Then you decide what to keep.

<!-- speaker_note: Frame errors as the material, not as failure. Keep the exact error text; "it doesn't work" cannot be debugged. -->

<!-- end_slide -->

On Windows
===

Windows has no Linux terminal by default. Three doors:

| Path | What | When |
|---|---|---|
| **WSL** | a real Ubuntu inside Windows | recommended, needs admin + reboot |
| **Git Bash** | `bash` + `git`, no admin | fastest for today |
| **Codespaces** | a terminal in the browser | lifeboat if all else fails |

<!-- pause -->

Try WSL at home. It is the real thing.

<!-- speaker_note: Do not debug WSL live in class. Git Bash gets everyone through today; WSL is homework. The site has the exact steps and the error codes. -->

<!-- end_slide -->

Getting unstuck
===

- every step is on the course site, copy-pasteable
- ask **any AI** — paste the exact error, say which terminal you are in
- ask a neighbour, ask me

<!-- pause -->

Keep the **exact error message**. That is the thing we can fix.

<!-- speaker_note: Explicitly authorise AI help for setup. The course is about agents; using one to install tools is on message. -->

<!-- end_slide -->

The course site
===

Everything lives here:

```
https://knuxv.github.io/cours-agents/
```

- Session 0: setup, your Unistra LLM key, SSH keys
- one page per session, exercises with solutions
- the cheat sheet

<!-- pause -->

Slides are prompts. The site is the reference.

<!-- end_slide -->

Today
===

**Session 1 — Git.**

- the terminal, ten minutes
- one loop: `status` → `add` → `commit` → `log`, repeated
- push to **your** GitHub repo — the deliverable
- branches: watch me, do not worry yet

<!-- speaker_note: Transition to the S1 deck. If the room has many Windows machines without Git Bash yet, do the Git Bash install now, before anything else. -->
