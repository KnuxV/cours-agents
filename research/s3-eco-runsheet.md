# Run-sheet — "Meet the agent" (economics cohort, 2h)

Built 2026-09-25, two hours before the class. Deck: `slides/s3-agents-intro.md`. Student page: `site/docs/sessions/practice-agents.md`. Exercises: `site/docs/exercises/agent-lab.md`. Demo files: `resources/agent-lab/`.

**Relation to SPEC.md (read this once).** SPEC's Session 3 is the raw `curl` session and Session 4 is pi. This class is neither: it explains the Session 3 mechanics *at talking speed* (30 min of slides, no curl typing) and then does a reduced Session 4 hands-on (four dials, no permission-gate extension, no subagent extension, no empirical A/B/C exercise). Nothing here removes anything from the spec — the curl session and the full pi session still have all their material. It is an instructor decision about ordering for one cohort, recorded rather than resolved silently.

---

## 0. Rehearse before the room fills (10 minutes, do not skip)

Everything below was written against pi **0.87.1** docs shipped in the install (`~/.local/share/mise/installs/pi/0.87.1/pi/docs/`) and against `research/s3-api.md`'s live endpoint tests of 2026-08-28. Nothing was run against the endpoint while this was written (no `UNISTRA_API_KEY` in that shell); item 2 has since been settled live by the instructor. Check the rest yourself, in this order:

1. `pi -p "Reply with one word: pong"` — endpoint alive, key in the environment.
2. **Settled live by the instructor, 2026-09-25 — the thinking dial does not exist on these models.** ++shift+tab++ and `/thinking` report that the model does not support thinking, on every university model, not only `coder`. ++ctrl+t++ does work (it collapses and expands thinking blocks in the transcript). **The hands-on was rewritten around this**: the refusal *is* the demo. Reasoning is a property of the model you chose, not a switch — you pick it at `/model`, and you pay for it in `/session`. Do not fight it in front of the room.
   *Optional, 2 minutes, if you want the dial back on `gpt-oss`:* pi's model definition carries a `reasoning` boolean (see the model object in the installed `docs/rpc-commands.md`), and the Unistra endpoint accepted `reasoning_effort: "high"` on `gpt-oss` on 2026-08-28. Adding `"reasoning": true` to that model's entry in `~/.pi/agent/models.json` should make `/thinking` offer levels and send `reasoning_effort`. **UNVERIFIED — never tested against this endpoint.** `qwen3` uses a different mechanism (`chat_template_kwargs.enable_thinking`), which pi has no way to send through `openai-completions`; do not expect that one to work at all.
3. Run the whole data step once yourself (section 4 below) so you know whether `coder` writes a working `make_survey.py` on the first try today. If it does not, use `resources/agent-lab/make_survey.py` (tested, stdlib only, 1000 rows).

**Known classroom risks** (all from `research/s3-api.md`):

- **Silent fallback to Ministral 3B.** LiteLLM falls back `coder → ministral` when the 80B is overloaded. Thirty students hammering it at once is untested. Symptom: "the model got dumb", 32k context, worse tool calls. Mitigation: keep prompts short, and if the room's answers degrade together, say what is happening — it is a good lesson about infrastructure you do not control.
- **401 says "Your session has expired … Please sign in again."** Students will reload the website. It means the key is missing or wrong in *this terminal*.
- **pi does not ask before running a command or editing a file.** There is no approval popup. Students coming from Claude Code or Copilot expect one. Say this out loud before section 2, and make git the answer.

---

## 1. Timing

| | minutes | what |
|---|---|---|
| 0:00 | 5 | arrive, `cd ~/agent-lab`, `pi -p "…pong"` while you talk |
| 0:05 | 30 | the deck — 19 slides, cut marks in the notes |
| 0:35 | 45 | hands-on, six sections, the site page open on the projector |
| 1:20 | 5 | break / stragglers |
| 1:25 | 30 | exercises started in the room, you circulate |
| 1:55 | 5 | wrap, what to hand in |

If you start late, the deck cuts to 22 minutes (drop "Where it breaks — data work" and "So what is it actually good for", both marked CUT in the speaker notes). The hands-on cuts from the bottom: section 8 (two agents) first, then section 6 (tools).

---

## 2. The hands-on, step by step

The student page has the same steps with more prose. This is your version, with the failure lines.

**Say first:** "pi will not ask your permission. It reads, writes and runs. That is why we are in a git repository, and why you never start it in your home folder."

### (1) A room to work in — 4 min

```bash
mkdir ~/agent-lab && cd ~/agent-lab && git init
pi -p "Reply with one word: pong"
```

Wait for the whole room. `No models available` → the key is not in this terminal.

### (2) Watch the loop — 4 min

`pi`, then: *What is in this folder? Change nothing.*

Point at the `ls` line scrolling past before the answer. **"That is the slide with the arrows. The model asked, pi did it, pi sent the result back."** Then `/session` — show the token count and remind them it is the invoice.

### (3) Dial one — the model — 6 min

`/model` → read the catalogue out loud (coder 80B, qwen3, gemma, gpt-oss, mistral-small, ministral — same API, different trade-offs). Pick `gpt-oss`, ask the pens-and-notebooks puzzle from the deck, and let the reasoning appear. ++ctrl+t++ collapses and expands it; `/session` shows what it cost.

Then try `/thinking` **on purpose**, and let it refuse. That is the teaching moment, not a glitch — none of the university's models declare thinking support to pi, so there is no level to set. Back to `coder`.

**The line:** "Reasoning is not a button. It is a post-training choice you make at `/model`, and you pay for it in tokens. The coder model does not think out loud at all, and it will still beat gpt-oss over the next twenty minutes, because it was trained to call tools."

### (4) A dataset — 6 min

Paste (it is on the student page):

> Write make_survey.py, using only the Python standard library, that generates survey.csv: 1000 rows, columns id, region, education, years_experience, hours_worked, income. Income should depend on education and experience, with noise. Then run it and show me the first 3 rows.

Then `!git add -A && git commit -m "baseline data"`. **The line:** "an agent without git is a liability."

Fallback if it flails twice: `resources/agent-lab/make_survey.py`.

### (5) Dial two — context — 8 min, the centrepiece

a. `/new`, then *Compute mean income by education level. Save a bar chart to out/income_by_edu.png.* — usually works.

b. Break it, in front of them, in pi: `!sed -i.bak 's/,income/,annual_income/' survey.csv` (Mac: `sed -i '' …`). Say nothing else about it.

c. `/new`, then *What is the average income by region?*

Three possible outcomes, all useful: it reads the header first (good — say why), it crashes with a `KeyError` (fine — "it wrote the name from memory"), or **it answers anyway about another column** (jackpot — stop everything and read the tool output with them).

d. Write `AGENTS.md` together — dictate it, or `cat` the example from `resources/agent-lab/AGENTS.md.example`. Then `/reload`, `/new`, same question. Compare.

**The line:** "Instructions that route through a verification work. Instructions that ask for virtue do not. Compare 'print the columns, then use them' with 'be careful'."

e. `!git restore survey.csv && rm -f survey.csv.bak`.

### (6) Dial three — tools — 4 min

`/quit`, then `pi --tools read,grep,find,ls`. Ask it to delete something. It cannot. **The line:** "This is the only hard guarantee in the room. Everything else is a request you hope it honours."

### (7) Dial four — skills — 8 min

`mkdir -p .agents/skills/data-check`, paste `resources/skills/data-check/SKILL.md`, `/reload`, then `/skill:data-check What is the income gap between master and high school, by region?`

Show them the top two lines of the file: `name` becomes the command, `description` is the routing — the model sees only those until it decides the skill applies. **The line:** "A skill is procedural memory that survives the amnesia. And because it is a file, you can review it, commit it, and give it to someone else."

### (8) Two agents — 8 min — cut this first if late

Second terminal, same folder, `.agents/skills/referee/SKILL.md` in place, then `pi --tools read,grep,find,ls` and `/skill:referee Review the analysis in this folder against survey.csv.`

**The line:** "Same model, opposite incentives, separate contexts. The referee cannot be talked round by the author's reasoning, because it never saw it. Reliability comes from structure, not from a bigger model." (This is the seed of SPEC 4.4's grill/build pattern — plant it, do not develop it.)

**Plan mode, if someone asks:** pi has none built in (GitHub issue `earendil-works/pi#97` is open; there is an example extension in `examples/extensions/plan-mode/` with `/plan` and ++ctrl+alt+p++, UNVERIFIED — never installed here). The version that needs no install: a read-only pi writes `PLAN.md`, a second pi executes it. Say that is exactly what "plan mode" is in every harness that has one.

### (9) Wrap — 2 min

Four dials on the board. Then: "The agent is a confident junior colleague with no memory of yesterday. You keep git, the tests, and the last word." Point at the exercises.

---

## 3. Questions you will get, with honest answers

- **"Will this replace us?"** — Nobody knows. What is visible is that typing shrinks and specifying-and-verifying grows. The student who can state a problem precisely and check an answer cheaply is not the one this is aimed at.
- **"Can I use it for my thesis / memoir?"** — Yes, under conditions: pin the environment, commit every step, and verify results against something the agent did not produce. A discrepancy is a finding, not a bug — and an agent told to "fix" one will smooth it away. Point at the optional replication track.
- **"Is it sending my data to OpenAI?"** — Not here. `conversation.ia.unistra.fr` is the university's own platform; the models are open-weight, served in Strasbourg. That is a real reason this course uses it.
- **"Why is it free?"** — It is not; the university pays for the GPUs. The token counter is still the honest unit even when the bill is invisible to them.
- **"Which model should I use?"** — A real decision with a cost-performance frontier, not brand loyalty. `coder` for tool work, `gpt-oss` when a hard reasoning step matters, `ministral` when the context is small and speed matters.

## 4. Optional talking points — **verify before quoting**

These did not exist in the repo's verified notes and were not checked today. Do not put a number on a slide you have not opened yourself.

- METR's 2025 randomised trial reporting that experienced open-source developers were **slower** with AI assistance while believing they were faster. Strong material for an economics room (perceived vs measured productivity). **UNVERIFIED here — check the exact figure and framing before saying it.**
- Anthropic engineering, *Building effective agents* and *Effective context engineering for AI agents* — the sources behind the "workflow vs agent" distinction and the "context rot" claim on the context-window slide. <https://www.anthropic.com/engineering/building-effective-agents>, <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- *How coding agents fail their users* (arXiv 2605.29442), a study of ~20,000 real sessions including agents deleting project directories — a citable version of the git-is-your-undo-button warning. **UNVERIFIED — the paper was found by a delegated search, not read here.**
- Ludwig, Mullainathan & Rambachan, *Large Language Models: An Applied Econometric Framework* (NBER WP 33344) — the right reference for any student who wants to use an LLM as a measurement instrument in a dissertation. **UNVERIFIED at full-text level.**

## 5. What to fix after class

- Whether the `gpt-oss` thinking block renders in pi (item 2 of the rehearsal). The answer decides how the student page's section 3 is written.
- Whether `coder` survived thirty simultaneous students, or fell back to Ministral.
- Which of the three column-drill outcomes actually happened — the student page currently presents all three as equally likely.
- If the two-agent section landed, it is the bridge to SPEC 4.4; if it did not, Session 4 needs to rebuild it from scratch.
