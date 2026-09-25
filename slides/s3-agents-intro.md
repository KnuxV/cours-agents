---
title: What is inside the chatbot
sub_title: "model, API, context, tools, skills — and the loop that turns them into an agent"
author: Kevin Michoud — Université de Strasbourg
---

<!-- speaker_note: 30 minutes of slides for the economics cohort, then 45 minutes hands-on in pi, then the exercises. They have done Git and Python tooling; they have NOT done the raw curl session, so this deck carries the whole mechanical story at talking speed instead of at typing speed. Every JSON block here is real output from the Unistra endpoint, tested 2026-08-28. Cut marks are in the notes — if you are late, drop the two slides marked CUT. -->

Today
===

Three parts.

1. **30 minutes** — what is actually inside the tab you have been using
2. **45 minutes** — we drive a real agent together, in the terminal
3. **the rest** — exercises where the agent is wrong and you catch it

<!-- pause -->

By the end you should be able to say, without hand-waving, what these five words mean:

**model · API · context · tool · skill** — and then, for free, **agent**.

<!-- speaker_note: 0:00–0:02. Tell them the thesis of the whole course in one line — an AI coding agent is not magic, it is an HTTP call in a loop wrapped in engineering decisions. Today they see the loop from the outside; in the next session they build it by hand with curl. -->

<!-- end_slide -->

Where you are now
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

**A chatbot**

You ask. It answers.

Nothing in the world changes.

You copy the code, you paste it, you run it. **You** are the machinery.

<!-- column: 1 -->

**An agent**

You ask. It reads your files, runs commands, writes files, reads the errors, tries again.

Something in the world changes.

It changes on **your** disk, under **your** user account.

<!-- reset_layout -->

<!-- pause -->

Same model in both columns. The difference is engineering, not intelligence.

<!-- speaker_note: 0:02–0:04. This framing is the spine of the hour. Say the sentence "same model, different engineering" twice — it is what they should remember if they remember one thing. -->

<!-- end_slide -->

1 — The model
===

A **model** is a fixed mathematical function. Text in, text out.

- trained once, at enormous cost, then **frozen**
- it predicts the next piece of text, over and over
- between two calls it learns nothing and remembers nothing

<!-- pause -->

You already know this part: it is the estimated function of a very large supervised problem. The weights are the coefficients. Nobody re-estimates them because you talked to it.

<!-- speaker_note: 0:04–0:06. The economics room knows estimation — lean on that. The surprise to plant here is the amnesia, because every later concept (context, agents, skills) is a workaround for it. -->

<!-- end_slide -->

The unit of account
===

Models do not read characters or words. They read **tokens** — pieces of words.

```text
"econometrics"  ->  "econom" + "etrics"     2 tokens
"survey.csv"    ->  "survey" + "." + "csv"  3 tokens
```

<!-- pause -->

Everything is counted in tokens:

- what you send (**input tokens**) and what comes back (**output tokens**)
- the price you pay
- the **limit** on how much the model can see at once

**Tokens are the price system of this entire industry.**

<!-- speaker_note: 0:06–0:08. If there is a projector and wifi, tiktokenizer.vercel.app is the 30-second demo that makes this land. The university platform is free for them, which hides the cost — say explicitly that "free" here means "someone else pays", and that the limit stays even when the bill does not. -->

<!-- end_slide -->

2 — The API
===

The model runs in a machine room. You never touch it.

You get a **counter with a fixed contract**: you hand over a form, you get a form back.

```json
{
  "model": "coder",
  "messages": [
    {"role": "user", "content": "How many .md files are here?"}
  ]
}
```

One HTTPS request. That is all a chatbot is, plus a web page around it.

<!-- speaker_note: 0:08–0:10. Say that this exact JSON is what they will type themselves with curl in the next session, against conversation.ia.unistra.fr — nothing leaves Strasbourg, no key to buy. API means the contract, not the intelligence. -->

<!-- end_slide -->

What comes back
===

```json
{
  "choices": [{"message": {"role": "assistant",
                           "content": "There are 3 .md files."}}],
  "usage": {"prompt_tokens": 412, "completion_tokens": 9,
            "total_tokens": 421}
}
```

<!-- pause -->

Two things to notice:

- the answer is **one field of a JSON document** — everything else is packaging
- `usage` is the invoice, on every single call

<!-- speaker_note: 0:10–0:12. Point at usage and say that the whole session in pi later has a running total behind /session. The model in the example could not have counted the files — it would have had to guess. Hold that thought for four slides. -->

<!-- end_slide -->

3 — Context
===

Send a second request:

```json
{"model": "coder", "messages": [{"role": "user", "content": "Make it faster."}]}
```

**"Make what faster?"**

The model has no idea. It never saw the first message. Each call starts from zero.

<!-- speaker_note: 0:12–0:13. This is the demo they will remember. If the room looks sceptical, promise them they will do exactly this with curl next session and watch it fail. -->

<!-- end_slide -->

A conversation is a re-send
===

```json
{"messages": [
  {"role": "system",    "content": "You are a helpful assistant."},
  {"role": "user",      "content": "Write a function that sorts a list."},
  {"role": "assistant", "content": "def my_sort(...): ..."},
  {"role": "user",      "content": "Make it faster."}
]}
```

Every turn, **the whole transcript is sent again**.

<!-- pause -->

So "memory" is a file you are re-uploading, and it grows. And since it is only a file — it can be **edited**. Change what the assistant said, and the model believes it said that.

**Context is constructed, not recalled.**

<!-- speaker_note: 0:13–0:16. The forged-assistant-message trick is the moment the mystique dies. Consequences they now get for free — why long chats cost more, why "it forgot", why the same question gives different answers in a fresh tab. -->

<!-- end_slide -->

The context window
===

The contract has a size limit. Everything must fit:

**the standing instructions + the whole transcript + the file contents you pasted + the tool definitions + the tool outputs**

| model | window |
|---|---|
| `coder` (80B, tuned for code) | 262 144 tokens |
| `gpt-oss` | 131 072 tokens |
| `ministral` (3B) | 32 768 tokens |

<!-- pause -->

And before the hard limit, a soft one: **the more you stuff in, the worse the attention gets**. A long polluted session degrades the answer well before the window is full.

<!-- speaker_note: 0:16–0:18. Context rot — Anthropic's engineering blog documents it, the mechanism is attention spread thin over more tokens. Practical rule for them — a fresh session plus a short written brief beats a three-hour transcript. That is why /new exists and why we write AGENTS.md later. -->

<!-- end_slide -->

4 — Tools
===

You add one paragraph to the request. Not code — a **description**:

```json
"tools": [{"type": "function", "function": {
  "name": "run_bash",
  "description": "Run a shell command and return its output",
  "parameters": {"type": "object",
                 "properties": {"command": {"type": "string"}}}}}]
```

You are telling the model: *these are the actions you may ask for.*

<!-- speaker_note: 0:18–0:20. Insist — you did not give it any power, you gave it a vocabulary. The model has no hands, no network, no shell. -->

<!-- end_slide -->

The punchline
===

```json
{"choices": [{"finish_reason": "tool_calls",
  "message": {"content": null,
    "tool_calls": [{"function": {"name": "run_bash",
      "arguments": "{\"command\": \"ls *.md | wc -l\"}"}}]}}]}
```

<!-- pause -->

`"content": null` — **there is no answer.**

The model did not run anything. It returned a **request** for someone else to run something.

<!-- pause -->

Someone must execute it and send the result back as a new message. That someone is a **program**. That program is the agent harness.

<!-- speaker_note: 0:20–0:23. This is the centre of the whole course. Next session they play the harness by hand for one round — copy the command, run it, paste the output back into a second curl. Tedious on purpose. Also — this is exactly where permissions live, because the decision to execute is made by the program, not by the model. -->

<!-- end_slide -->

5 — The loop
===

```text
          you: "find the income gap by region"
                        |
                        v
   +--->  model  --->  tool call?  ---no--->  answer to you
   |        ^               |
   |        |              yes
   |        |               v
   |        |        the harness runs it
   |        |               |
   +--------+---------------+
        result appended to the context
```

**That is an agent.** A model, a set of tools, and a loop that keeps feeding results back until the model stops asking.

<!-- speaker_note: 0:23–0:25. Say the definition slowly, twice. Everything in the terminal later is this diagram with colours. The loop is about twenty lines of Python — they could write it, and in a sense they will. -->

<!-- end_slide -->

Three things people call "AI"
===

| | who decides the steps | example |
|---|---|---|
| **chatbot** | you, one turn at a time | the tab you use now |
| **workflow** | the programmer, in advance | a script that calls a model twice |
| **agent** | the model, at run time | pi, in your terminal, in 20 minutes |

<!-- pause -->

An agent is a **delegation**. You set the objective; it chooses the means. You do not observe the means unless you build the means of observing them.

That is not a new problem. It is your discipline's oldest one — with a colleague who works in seconds, never gets tired, and is confidently wrong roughly as often as it is right.

<!-- speaker_note: 0:25–0:27. The principal-agent framing is worth exactly one sentence — do not milk it. The useful corollary is that monitoring is a cost, and the tools that lower it (git, tests, read-only mode, a referee agent) are what the second half of the class is about. -->

<!-- end_slide -->

6 — Skills
===

A **skill** is a folder with a text file in it.

```text
data-check/
  SKILL.md        <- name, a description, the procedure
  references/     <- optional, read only when needed
```

- the harness shows the model only the **name and the one-line description**
- the model asks for the full text **when a task matches**
- so a hundred skills cost you almost no tokens until one is used

<!-- pause -->

It is the onboarding binder for a colleague who starts from zero every morning.

<!-- speaker_note: 0:27–0:29. Concrete example they will type — "before using a column, print the column names". A skill is procedural memory that survives the amnesia, and unlike a chat prompt it is a file, so it is reviewable, committable, and shareable. That is the whole of the hype in one sentence. -->

<!-- end_slide -->

Your four dials
===

| dial | the question | what you touch |
|---|---|---|
| **model** | who does the work? | `/model`, and what it costs |
| **context** | what does it know? | `AGENTS.md`, `@file`, `/new` |
| **tools** | what may it do? | `--tools`, read-only |
| **skills** | which procedure? | `.agents/skills/` |

<!-- pause -->

Notice what is **not** on this list: the model's intelligence. You do not control it, and it is rarely your binding constraint.

<!-- speaker_note: 0:29–0:30. This table is the plan of the hands-on hour — four sections, four dials. Tell them so. -->

<!-- end_slide -->

Where it breaks — data work
===

<!-- pause -->

**1. The column that was not there.** It writes `df["income"]` from memory. The column is `annual_income`. Best case it crashes; worst case it answers about something else.

<!-- pause -->

**2. The statistic that should not exist.** Ask for "the correlation between region and income" and you will usually get a number. `region` is categorical. The number is meaningless, and it is formatted beautifully.

<!-- pause -->

**3. The silent step.** In a five-step pipeline, step three dropped 40% of the rows. Nothing crashed. The final table is clean, plausible, and wrong.

<!-- speaker_note: 0:30–0:32 — CUT candidate if late, keep 1 and 3. These three are the drills of the hands-on hour, so announce them as such. Rule to give them out loud — a number you have not seen come out of a command is a rumour. -->

<!-- end_slide -->

Where it breaks — the honest list
===

- **hallucination is not rare** — it is the normal behaviour of a system optimised to always produce a plausible continuation
- **it never says "I do not know"** unless you make room for it to
- **it agrees with you** — tell it the coefficient looks wrong and it will find a reason
- **it is not reproducible** — same prompt, same data, different code tomorrow
- **a discrepancy is a finding, not a bug** — and an agent asked to "fix" one will smooth it away

<!-- speaker_note: 0:32–0:34. For anyone going near replication or a thesis — the requirement is not "do not use it", it is "pin everything, log everything, verify against something you did not generate". Mention the optional replication track on the site. -->

<!-- end_slide -->

So what is it actually good for
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

**Good**

- boilerplate, glue, plotting
- translating code between languages
- reading an unfamiliar codebase
- the tedious 80% of data cleaning
- explaining an error message
- writing the tests you avoid writing

<!-- column: 1 -->

**Bad**

- deciding what the question is
- identification, causality, judgement
- anything you cannot check
- long unmonitored autonomy
- being trusted about its own work

<!-- reset_layout -->

<!-- pause -->

The job that disappears is typing. The job that grows is **specifying and verifying**.

<!-- speaker_note: 0:34–0:36 — CUT candidate. Careful not to oversell either column. If asked about jobs, the honest answer is that nobody knows, and that the students who can specify precisely and verify cheaply are the ones this does not replace. -->

<!-- end_slide -->

Now you drive
===

In the terminal, with the university's own models, in a git repository you can always undo.

1. watch the loop, once
2. **model** — the catalogue, and what each one costs you
3. **context** — break the data, watch it lie, write the rules, watch it recover
4. **tools** — an agent that physically cannot delete your files
5. **skills** — write one, use it
6. **two agents** — one writes, one is paid to find the fault

<!-- pause -->

Open the class plan on the site. Type everything yourself.

<!-- speaker_note: 0:36. Hand over to the site page — sessions/practice-agents. Remind them of the warning box — never start an agent in the home folder. Check that everyone is in ~/agent-lab with a clean git status before starting section 2. -->

<!-- end_slide -->
