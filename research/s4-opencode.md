# Research note — Session 4: OpenCode

Verified 2026-08-28 against [opencode.ai/docs](https://opencode.ai/docs/), the live JSON schema (`https://opencode.ai/config.json`) and a local install of **OpenCode 1.18.22**. Status legend: VERIFIED / UNVERIFIED / WRONG.

## 1. Claims check

| Claim in SPEC (Session 4) | Status | Evidence |
|---|---|---|
| Install `curl -fsSL https://opencode.ai/install \| bash` (WSL/Mac) | VERIFIED | Listed first on [opencode.ai/docs](https://opencode.ai/docs/); URL answers (307 → script). Alternatives: `npm i -g opencode-ai`, `brew install anomalyco/tap/opencode`, `pacman -S opencode`. |
| "Documented fallbacks for Git Bash" | **WRONG as written** | Docs: Windows has **no native support**; "use WSL". Windows package managers exist (`scoop install opencode`, `choco install opencode`) but Git Bash operation is untested and unsupported. Fallback for Windows-without-WSL must be **Codespaces**, not Git Bash. |
| `~/.config/opencode/opencode.json` with custom provider block | VERIFIED | Global config path confirmed ([config docs](https://opencode.ai/docs/config/)); project `opencode.json` merges over it. Instructor's existing global config already works with `unistra/coder`. |
| `@ai-sdk/openai-compatible`, `baseURL`, `{env:...}` key | VERIFIED | [providers docs](https://opencode.ai/docs/providers/) custom-provider example: `"npm": "@ai-sdk/openai-compatible"`, `"options": {"baseURL": …, "apiKey": "{env:VAR}"}`, `"models": {"id": {"name": …, "limit": {"context": N, "output": M}}}`. `{file:~/.secrets/key}` also supported. |
| Explicit `limit` block | VERIFIED (schema) | Schema: `limit` = `{context: number, output: number}` — **both required** when `limit` is present; optional `input`. Model entries also accept `tool_call: boolean`, `reasoning: boolean`, `options`, `temperature`, `variants`. Values: `context` from s3 note (262144 / 131072 / 128000 / 32768); `output` UNVERIFIED. |
| The loop observed: model → tool call → execution → feedback | VERIFIED live | `opencode run --pure "Count the files … create count.txt …"` with `model: unistra/coder`, permissions allow: transcript showed `$ ls -1 \| wc -l` → `3` → `← Write count.txt` → answer `3`; file created. Headless `opencode run` works; TUI not exercised. |
| Permissions: `edit`/`bash` as ask/allow/deny, whitelists, hard blocks | VERIFIED | [permissions docs](https://opencode.ai/docs/permissions/) + schema `PermissionConfig`. Keys: `read, edit, glob, grep, list, bash, task, external_directory, todowrite, question, webfetch, websearch, lsp, doom_loop, skill`, plus `"*"`. Value = `"allow"\|"ask"\|"deny"` or an object of glob → action, e.g. `"bash": {"*": "ask", "git *": "allow", "rm *": "deny"}`; **last matching rule wins**. Defaults: most `allow`; `doom_loop`, `external_directory` = `ask`; `.env` files denied. Per-agent override under `agent.<name>.permission`. |
| `AGENTS.md` standing instructions | VERIFIED | [rules docs](https://opencode.ai/docs/rules/): project `AGENTS.md` (walks up to root), global `~/.config/opencode/AGENTS.md`; `CLAUDE.md` used as fallback; `/init` generates one; `"instructions": ["file.md", "glob/*.md"]` adds more. |
| Subagents: same/different model, own context, restricted tools | VERIFIED | [agents docs](https://opencode.ai/docs/agents/). Schema `AgentConfig`: `description` (required), `mode: "primary"\|"subagent"\|"all"`, `model`, `prompt` (string or `{file:./prompts/x.txt}`), `permission`, `temperature`, `top_p`, `steps`, `hidden`, `disable`, `color`. **`tools: {write:false}` is deprecated** → use `permission: {edit: "deny", bash: "deny"}`. Markdown form: `.opencode/agents/<name>.md` (project) or `~/.config/opencode/agents/<name>.md` (global) with YAML front matter. Built-ins: `build`, `plan` (primary, Tab to switch); `general`, `explore`, `scout` (subagents). Invoke with `@name` in the prompt. `subagent_depth` config exists. |
| Grill/build pattern, reviewer, research agent | VERIFIED (feasible) | All expressible: grill = `mode: primary`, `permission: {edit: {"*": "deny", "SPEC.md": "allow"}, bash: "deny"}`; build = `mode: primary`, default perms, prompt "implement exactly SPEC.md, stop when silent"; reviewer = `mode: subagent`, `edit: deny`, `bash: {"*": "deny", "git diff*": "allow", "pytest*": "allow"}`. Whether `coder` *follows* a "refuse vague answers, one question at a time" prompt reliably: UNVERIFIED — rehearse. |
| Compaction / clean context | VERIFIED (feature exists) | `compaction` key in schema; OpenCode summarizes on overflow. Claim "long polluted sessions degrade mid-size models" is supported qualitatively by [Anthropic — Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). |
| Claude Code demo by instructor (4.5) | n/a | Instructor-side; nothing to verify. |
| Empirical A/B/C exercise counts spec violations and test failures | UNVERIFIED (design) | No literature specific to grill/build; closest evidence is Brodeur et al. (AI-led ≪ human/AI-assisted; see replication note) and [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (pass@k / pass^k — use pass^k for the "reliability" framing). |

## 2. Best deeper-dive resources

1. [OpenCode docs — Config](https://opencode.ai/docs/config/), [Agents](https://opencode.ai/docs/agents/), [Permissions](https://opencode.ai/docs/permissions/), [Rules](https://opencode.ai/docs/rules/) — primary source; the schema moves, and `https://opencode.ai/config.json` is the ground truth for what a field is called this week.
2. [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — workflows vs agents, "augmented LLM"; the vocabulary for 4.2–4.4 in 20 minutes.
3. [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — the argument for compact written state over long transcripts (SPEC 4.3).
4. [agents.md](https://agents.md/) + [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) — what goes in `AGENTS.md` and why "verify" beats "be careful".
5. *Ambitious:* [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Jan 2026; graders, pass@k vs pass^k, capability vs regression evals) and [SWE-bench](https://www.swebench.com/) / [Terminal-Bench](https://www.tbench.ai/) for how agent reliability is actually measured.

(Also live: [12-factor agents](https://github.com/humanlayer/12-factor-agents) and [Simon Willison on "agents"](https://simonwillison.net/2025/Sep/18/agents/) — good one-liners for the ladder recap.)

## 3. Pedagogical risks

- **Schema drift**: `tools:` → `permission:` and `maxSteps` → `steps` deprecations happened recently; a config copied from a blog post fails silently or warns. Mitigation: ship `resources/opencode/opencode.json` with `"$schema": "https://opencode.ai/config.json"` and re-validate the week before class; pin the version students install (`opencode upgrade v1.18.22`, exists as a CLI target).
- **Permission prompts in headless/`run` mode**: with `bash: "ask"`, `opencode run` behaviour is UNVERIFIED (I tested with allow). Mitigation: teach the TUI for 4.2; use `run` only with explicit allows.
- **Tool-calling reliability of `coder` under classroom load**: single-shot tests were clean; long multi-step sessions untested. Mitigation: rehearse the grill/build exercise end-to-end once (spec already says so); keep `qwen3` as an alternate `model` in the same provider block.
- **Fallback to `ministral`** (see s3 note): a mid-session silent downgrade would wreck the agent loop (32k context). Mitigation: set `limit.context` conservatively? No — it doesn't prevent server-side fallback; ask DNUM.
- **Windows students without WSL** cannot do Session 4 at all. Mitigation: Codespaces image with OpenCode preinstalled (a `devcontainer.json` in the course repo).
- **`AGENTS.md` ignored**: students expect magic; the model with a 3B-active MoE may not follow long rule files. Mitigation: the "instructions that route through verification" rule (SPEC 4.3) — make one rule, test it, show the diff.

## 4. Suggested spec edits

- 4.1: « documented fallbacks for Git Bash » → « Windows without WSL: GitHub Codespaces (OpenCode has no native Windows support) ».
- 4.1: « explicit `limit` block » → « explicit `limit` block (`context` **and** `output` required) using the served limits from research/s3-api.md ».
- 4.1: add « Pin the version: `opencode upgrade v1.18.22` (or current) so the class shares one schema. »
- 4.4: « restricted tools » → « restricted permissions (`permission:` — the `tools:` field is deprecated) ».
- 4.4: add « Subagent definitions as markdown in `.opencode/agents/*.md`, committed to the student repo » (nicer to diff/grade than JSON).
- 4.4, empirical exercise: add « Report pass^k over 3 runs, not one run » — 1 run of a stochastic system tells nothing; three runs at T=0 is cheap.
- Known risks: add « OpenCode `run` with `ask` permissions untested; TUI is the classroom path. »
