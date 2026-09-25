# Class plan — meet the agent: four dials on pi

This is the page to keep open during the hands-on hour. We type everything together. If you fall behind, catch up from here; if something fails, say so out loud rather than silently skipping ahead.

**Before we start, you need:** pi installed and connected to the university's models ([pi — install, connect, tutor](../reference/pi.md)), and a terminal you know how to open.

**What you will have at the end:** a small git repository called `agent-lab` containing a dataset, an analysis the agent wrote, a project rules file, two skills, and one failure you caught yourself.

!!! warning "An agent changes files"
    pi can create, modify and delete files in the folder it was started in, and run commands there, **without asking you first**. That is why everything below happens inside a git repository: `git status` shows what changed, and `git restore` undoes it. Never start pi in your home folder or in a folder you care about.

## The four dials

Everything we do today is one of four things you control. Keep them in mind as we go:

| Dial | The question it answers | What we touch today |
|---|---|---|
| **Model** | Who is doing the work? | `/model`, thinking levels |
| **Context** | What does it know right now? | `AGENTS.md`, `@file`, `/new`, `/compact` |
| **Tools** | What is it allowed to do? | `--tools`, read-only mode |
| **Skills** | What procedure does it follow? | `.agents/skills/`, `/skill:name` |

---

## 1. A room to work in

```bash title="Any terminal"
mkdir ~/agent-lab
cd ~/agent-lab
git init
```

Expected: `Initialized empty Git repository in …/agent-lab/.git/`.

Then check that the model answers at all:

```bash title="Any terminal, inside ~/agent-lab"
pi -p "Reply with one word: pong"
```

Expected: `pong`, after a second or two. If you get `No models available`, your API key is not in this terminal — see [pi, section 1](../reference/pi.md#1-check-that-your-key-is-there).

## 2. Watch the loop once

```bash title="Inside ~/agent-lab"
pi
```

Type, inside pi:

```text
What is in this folder? Change nothing.
```

Watch the lines that scroll by *before* the answer: `ls`, maybe `read`. Those are **tool calls** — the model asked pi to look, pi looked, pi sent the result back, and only then did the model speak. That is the whole agent loop, and you will see it again all hour.

Useful straight away:

| Type this | To |
|---|---|
| `/session` | see the session's token count — the running bill |
| `/model` | change model |
| `/new` | start a fresh conversation (the model forgets everything) |
| `!git status` | run a command yourself **and show its output to the model** |
| `@` | mention a file in your message |
| ++esc++ | interrupt the model |
| `/quit` | leave |

## 3. Dial one — the model

Inside pi:

```text
/model
```

You get the university's catalogue: `coder`, `qwen3`, `gemma`, `gpt-oss`, `mistral-small`, `ministral`. Same API, different trade-offs. `coder` is an 80-billion-parameter model specialised in programming and tool use; it does not "think out loud" at all.

Pick `gpt-oss` and ask something small:

```text
A shop sells pens at 1.20 € and notebooks at 3.50 €. I spent 24.30 € on 12 items. How many notebooks?
```

You now see a **thinking block** before the answer: tokens the model spends reasoning before speaking. You pay for them and you wait for them.

| Type this | To |
|---|---|
| ++ctrl+t++ | collapse or expand the thinking blocks in the transcript |
| `/session` | see what those thinking tokens cost you |
| `/thinking` | pick a thinking level — **and watch it refuse** |

That refusal is the lesson. `/thinking` only offers levels the model declares support for, and none of the university's models declare it: `coder` is a non-thinking model by construction, and the others are reached through a plain OpenAI-compatible endpoint that tells pi nothing about their thinking modes. So **reasoning here is a property of the model you chose, not a switch you flip.** You choose it at `/model`, and you pay for it in the token count.

Go back to `/model` → `coder` for the rest of the hour. **The lesson:** "reasoning" is not a brand, it is a post-training choice with a price. A coder model tuned for tool calling beats a thinking model on exactly the kind of work we are about to do.

## 4. A dataset to argue about

Ask pi:

```text
Write make_survey.py, using only the Python standard library, that generates survey.csv:
1000 rows, columns id, region, education, years_experience, hours_worked, income.
Income should depend on education and experience, with noise. Then run it and show me the first 3 rows.
```

Expected: a file appears, it runs, and you see a header line and three rows. Then, in pi:

```text
!git add -A && git commit -m "baseline data"
```

That commit is your undo button for the rest of the hour. Say it out loud once: **an agent without git is a liability.**

??? note "If the model's script fails twice, take ours (the fallback generator)"
    Copy this into `~/agent-lab/make_survey.py`, run `python3 make_survey.py`, and rejoin at section 5. The data-generating process is written in the docstring — that is the ground truth you check the analysis against later.

    ```python title="~/agent-lab/make_survey.py"
    --8<-- "resources/agent-lab/make_survey.py"
    ```

## 5. Dial two — context

Start a clean conversation with `/new`, then:

```text
Compute mean income by education level. Save a bar chart to out/income_by_edu.png.
```

It will probably work. Now break it, the way reality breaks it. In pi:

```text
!sed -i.bak 's/,income/,annual_income/' survey.csv
```

(On a Mac, `sed -i '' 's/,income/,annual_income/' survey.csv`.) You have renamed one column and told the model nothing. Start `/new` and ask:

```text
What is the average income by region?
```

Watch closely. Does it read the header first, or does it write `df["income"]` from memory and crash — or worse, quietly report a number for something else? **This is the single most common real failure of an agent on data**, and it is the reason for the next step.

Now write the project's standing instructions. In your editor, or by asking pi to write it, create `AGENTS.md` in `~/agent-lab`:

```markdown title="~/agent-lab/AGENTS.md"
--8<-- "resources/agent-lab/AGENTS.md.example"
```

pi reads `AGENTS.md` at startup and puts it in front of every request. Type `/reload`, then `/new`, then ask the same question again. Compare the two behaviours.

**The lesson:** instructions that route through a verification ("print the columns, then use them") work. Instructions that ask for virtue ("be careful") do not.

Restore the file when we are done with the drill:

```text
!git restore survey.csv && rm -f survey.csv.bak
```

## 6. Dial three — tools

Quit pi and start it again, read-only:

```bash title="Inside ~/agent-lab"
pi --tools read,grep,find,ls
```

Ask it to delete something. It cannot: those four tools read and search, and nothing else. `--tools` is an allowlist, and it is the only hard guarantee in the room — everything else is a request you hope the model honours.

## 7. Dial four — skills

A **skill** is a folder with a `SKILL.md` inside: instructions pi keeps on the shelf and hands to the model only when the task matches its `description`. Create one:

```bash title="Inside ~/agent-lab"
mkdir -p .agents/skills/data-check
```

Put this in `.agents/skills/data-check/SKILL.md`:

```markdown title="~/agent-lab/.agents/skills/data-check/SKILL.md"
--8<-- "resources/skills/data-check/SKILL.md"
```

Back in pi: `/reload`, then

```text
/skill:data-check What is the income gap between master and high school, by region?
```

The first two lines of that file are the whole mechanism: `name` becomes the command, `description` is what the model reads to decide whether the skill is relevant. Everything under them is only loaded when it is needed — which is why a skill costs you nothing until it is used.

## 8. Two agents, opposite jobs

Open a **second terminal** in the same folder. pi has no built-in sub-agents: a second agent is a second process. Create the referee's skill first:

```bash title="Terminal 2, inside ~/agent-lab"
mkdir -p .agents/skills/referee
```

```markdown title="~/agent-lab/.agents/skills/referee/SKILL.md"
--8<-- "resources/skills/referee/SKILL.md"
```

Then, in terminal 2:

```bash title="Terminal 2"
pi --tools read,grep,find,ls
```

```text
/skill:referee Review the analysis in this folder against survey.csv.
```

Terminal 1 writes; terminal 2 can only read, and is instructed to find fault. Two processes, same model, opposite incentives, separate contexts — the referee cannot be talked round by the author's reasoning, because it never saw it.

**The lesson:** reliability comes from structure — who may do what, who checks whom — far more than from picking a bigger model.

## 9. What to take away

- An agent is a model, plus tools it may *request*, plus a loop, plus your rules.
- The four dials are yours: model, context, tools, skills.
- The agent is a confident junior colleague with no memory of yesterday. You keep git, the tests, and the last word.

Now do the [exercises](../exercises/agent-lab.md) — they start where this page stops.
