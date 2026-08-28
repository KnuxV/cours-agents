# Advanced Programming for Economists — Course Specification (Draft)

**Format:** 8h (4 × 2h) + optional research mini-module. This is the first-part of an Advanced Programming class, they will have an extra 15 hours on MCP and IA with Hugging Face later. The exam is a single presentation for the two-class. 
**Audience:** M2 students. Terminal, Programming beginners: current workflow is browser + Colab + a ChatGPT tab. They have 15 hours of experience with SQL and 20 hours of Python. They will code in Python.
**Infrastructure:** Students' own laptops. LLM access via Unistra's self-hosted platform (conversation.ia.unistra.fr), OpenAI-compatible API, free, sovereign, no personal API keys to buy.
**Repo:** builds from github.com/KnuxV/advanced_programming_python (last year materials). We create a fresh repo for this, with a fresh remote, the last year classes are mostly for the basic support.

**Course thesis:** An "AI coding agent" is not magic. It is an HTTP call in a loop, wrapped in engineering decisions (context, tools, permissions, verification). By the end, students have built that loop by hand and configured a professional harness, and can reason about when to trust it.

**Exam** A presentation in front of the class of a coding project on whatever they want, as long as they show us how they apply the concepts they will see in the class.

---

## Session 0 (homework, before Session 1): environment setup

Deliverable posted on the course forum before the first class:
- Windows: install WSL (`wsl --install` in admin PowerShell, reboot, create Ubuntu user). Post output of `uname -a && curl --version | head -1`.
- Mac: nothing to install. Post output of same command from Terminal.
- Fallbacks (documented, in order): Git Bash + Scoop; GitHub Codespaces as day-of lifeboat.
- Get a Unistra LLM API key: log in to conversation.ia.unistra.fr → Profil → Réglages → Compte → generate key (`sk-...`).
- Optional 30-min install clinic before Session 1 for forum-thread casualties.

Rationale slide for Day 1: why the terminal at all (it is the interface of every server, every agent, every data job they are aiming for).

- Exercise: some light terminal practice, it’s vital that they understand the basic commands: mv, cp, ls, pwd etc...

---

## Session 1 (2h): Git

Content is available in ~/Codebase/fake-website-to-teach-git/. It can be improved. 
- init, add, commit, log, diff; the mental model of snapshots.
- Branching lightly; clone/push/pull with GitHub (account creation = course outcome).
- Why it matters doubly in the agent era: version control is the undo button and the audit trail for agent-written code. An agent without git is a liability.
- Exercise: create the personal course repo they will use in Sessions 3-4 (agents work best inside a git repo; this is deliberate setup).

## Session 2 (2h): Python tooling

*(Content owned by existing material.)*
- `uv`: project init, venv, adding dependencies, lockfile. Why reproducibility is a scientific requirement, not a preference.
- `argparse`: turning a notebook into a script with arguments. The notebook→script transition is the industry gap this course closes.
- Environment variables: what they are, `export`, `.bashrc`, and why secrets (API keys!) never go in code. Direct setup for Session 3.
- Optional/bonus: Polars discovery (kept because it is that good).

---

## Session 3 (2h): What an LLM API actually is

**Goal:** replace "I use a chatbot" with a mechanical understanding of the request/response cycle. Everything runs in the terminal with curl against the Unistra endpoint.

### 3.1 One raw call (~30 min)
- `curl` POST to `https://conversation.ia.unistra.fr/api/chat/completions` with a JSON payload (`-d @request.json`; payload files provided, one per step).
- Anatomy of the request: `model`, `messages`, headers, the API key as env variable.
- Anatomy of the response: `choices[0].message.content`, and `usage` — **tokens are the unit of account**. What a token is (subword pieces), input vs output tokens, why cost and context limits are counted in them. (Economists: this is the price system of the whole industry.)
- Sampling parameters, minimal vital set: `temperature` (variance dial; live demo at 0 vs 1.5), `top_p`/`top_k` mentioned in one slide as "which slice of the distribution we sample from" — no more.

### 3.2 Statelessness and context (~30 min)
- Second call: "make it faster" → the model has no idea what "it" is. **The model remembers nothing.**
- "Conversation" = resending the full history in `messages` every time. Roles: `system` (the agent's standing instructions), `user`, `assistant`.
- Demo: edit a past `assistant` message before resending — the model believes it said that. Context is constructed, not recalled.
- Consequences they now understand for free: context window limits, why long chats cost more, why "the model forgot" happens, what context engineering means.

### 3.3 Model families and training (~20 min)
- Unistra's local zoo as the concrete catalogue (mistral-small, qwen3, gemma, gpt-oss, the 80B coder, ministral) — same API, different trade-offs (size, context length, specialization).
- **Instruct vs reasoning vs agentic models**: same architecture, different post-training. Reasoning models are trained (RL) to spend tokens thinking before answering — visible chains of thought, better on math/debugging, slower and costlier. Agentic/coder models are tuned on tool-calling and multi-step software tasks. "Which model" is a real decision with a cost-performance frontier, not brand loyalty.

### 3.4 Tool calling (~40 min) — the punchline
- Add a `tools` array to the curl payload (one function: `run_bash`).
- The response contains `tool_calls`, not an answer. **The model did not run anything. It returned a request.** Someone must execute it and paste the result back as a `tool` message.
- Exercise: students ARE the harness for one round — copy the command, run it themselves, paste output back via a second curl. Tedious by design.
- Landing: models are now specifically post-trained to emit well-formed tool calls; this is what makes agents possible.
- Mention **MCP** in two slides: a standard protocol so any tool can plug into any model/harness — "USB-C for tools." Pointer: a later class is dedicated to MCP, where they build their own tool.
- Closing line: "everything in Session 4 is automating what you just did by hand — with judgment about when *not* to execute."

**Deliverable:** a working `step1.json`→`step4` sequence committed to their repo.

---

## Session 4 (2h): OpenCode — configuring a real harness

**Goal:** from raw calls to a professional agent harness, with the reliability levers made explicit. Model: Unistra's 80B coder via a custom provider config.

### 4.1 Setup (~20 min)
- Install: `curl -fsSL https://opencode.ai/install | bash` (WSL/Mac); documented fallbacks for Git Bash.
- `~/.config/opencode/opencode.json`: custom provider block pointing at the Unistra endpoint (`@ai-sdk/openai-compatible`, baseURL, `{env:...}` key, explicit `limit` block). They already understand every field from Session 3.

### 4.2 The loop, observed (~20 min)
- Run one task in the TUI, watch the cycle: model → tool call → execution → feedback → model. It is Session 3's exercise, automated.
- Permissions as the first reliability lever: `edit`/`bash` as ask/allow/deny, whitelists and hard blocks. Autonomy is a dial, not a switch.

### 4.3 Context and instruction engineering (~30 min)
- **AGENTS.md**: standing project instructions. Rule of thumb: instructions that route through verification ("run pytest after every edit") beat instructions that ask for virtue ("be careful").
- Clean context as a design principle: why long polluted sessions degrade mid-size models; fresh context + compact written state (a spec file) beats a long transcript.
- **Testing as the anchor**: the assertion-before-code rule, enforced. The most reliable component of an agent system is not a model — it is the test suite.

### 4.4 Structure: subagents and separation of powers (~40 min)
- Subagents: same or different model, own context, restricted tools. Think-only consultants (no write/edit) vs an actor that must consult.
- Live build of the **grill/build pattern**: a "grill" agent that only interrogates and writes SPEC.md (one question at a time, refuses vague answers), a "build" agent that implements exactly the spec and stops when the spec is silent. Same model, opposing incentives — principal-agent framing for an economics room.
- Optional flavors: an adversarial reviewer agent (PASS/FAIL on diffs); a research/explore agent that reads but never writes.
- The empirical exercise: same task under (A) one agent raw, (B) hand-written spec, (C) grill-then-build. Count spec violations and test failures. Result "it depends" is itself the lesson; reliability comes from structure, not model IQ.

### 4.5 Ladder recap (~10 min)
curl → (hand harness) → OpenCode → frontier harnesses (Claude Code demo by instructor). Each rung answers: what did the layer below hide from me? Open question to leave them with: when do you need to drop down a level? (Fixed workflows, compliance, budget caps.)

**Deliverable:** their repo containing opencode.json, AGENTS.md, agent definitions, and the SPEC.md + implementation from the exercise.

---

## Optional mini-module: LLM-assisted replication in economics

- Motivation: the replication crisis meets a new instrument. Walk through the Scott Cunningham-style workflow of using coding agents to reproduce published results from public data/code packages.
- What agents are good at here (re-running pipelines, translating Stata→Python/R, spotting undocumented steps) and what they are not (judging identification strategies, silently "fixing" discrepancies — a discrepancy is a finding, not a bug).
- Method requirements: pin everything (uv lockfile), log every agent action (git), verify against published tables with assertions.

**Research-track project:** pick a published paper with an available replication package; use the Session 4 harness to reproduce its main table(s); write a short memo on what reproduced, what didn't, and what the agent's role was. Grading favors honest failure analysis over clean success.

---

## Assessment (to discuss)
- Forum deliverables (setup, session artifacts in git) — participation-grade.
- Live offline debugging exam (existing commitment) — fits Session 3-4 content directly: give them a broken harness/config/loop and no internet.
- Research track: replication memo, in place of or on top of the exam?

## Known risks
- Environment setup failure (mitigated: homework + clinic + Codespaces lifeboat).
- Unistra API rate limits / downtime during class — test load beforehand; have a second provider config ready.
- The 80B coder's tool-calling reliability under classroom conditions: rehearse the Session 4 exercises end-to-end once.
