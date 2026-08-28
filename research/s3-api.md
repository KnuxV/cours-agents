# Research note — Session 3: What an LLM API actually is

All endpoint claims below were **tested live on 2026-08-28** with the instructor's key (`$UNISTRA_API_KEY`, `$UNISTRA_BASE_URL=https://conversation.ia.unistra.fr/api`). Test payloads are described so Task 03 can reproduce them. Status legend: VERIFIED / UNVERIFIED / WRONG.

## 1. Claims check

### Endpoint and stack
| Claim | Status | Evidence |
|---|---|---|
| Endpoint `https://conversation.ia.unistra.fr/api/chat/completions`, OpenAI-compatible | VERIFIED | POST with `{"model","messages"}` + `Authorization: Bearer sk-…` → HTTP 200, standard `chat.completion` object. Documented by Unistra ([7_1API.html](https://documentation.unistra.fr/DNUM/Intelligence_artificielle/guide_complet_IA/co/7_1API.html): base URL `https://conversation.ia.unistra.fr/api`). Front-end is **Open WebUI** ([API reference](https://docs.openwebui.com/reference/api-endpoints/): `POST /api/chat/completions`, `GET /api/models`), which proxies through **LiteLLM** to **vLLM 0.25.1** (response `system_fingerprint: "vllm-0.25.1-tp2-…"`; error bodies say `litellm.… Hosted_vllmException`). |
| Model list at `/api/models` | VERIFIED | `GET $UNISTRA_BASE_URL/models` → 18 entries. Chat model IDs: `coder`, `coder-qwen`, `qwen3`, `gpt-oss`, `mistral-small`, `ministral`, `gemma`, plus Open WebUI "workspace" variants `chat-gpt`, `chat-mistral`, `chat-qwen`, `chat-gemma` (chat-qwen resolves to `qwen3`), embeddings `bge-m3`, `nomic`, `qwen3-embedding`, and `glm-ocr`, `documentation-unistra`, `qcm-moodle-generator-aiken`, `talk-trainer`. **The listing does not expose context lengths** (`info.meta` only has capability flags). |
| Response has `choices[0].message.content` and `usage` | VERIFIED | `usage: {prompt_tokens, completion_tokens, total_tokens}` present on every response, including tool-call responses. |
| `temperature` 0 vs 1.5 demo | VERIFIED | `temperature: 1.5` accepted (HTTP 200). `top_p`/`top_k` not tested — vLLM supports both; UNVERIFIED that LiteLLM forwards `top_k`. |
| Streaming | VERIFIED | `"stream": true` returns SSE `data: {...chat.completion.chunk...}` lines (what OpenCode uses). |
| Rate limits | UNVERIFIED (none observed) | 20 concurrent requests → 20× HTTP 200; no `x-ratelimit-*` headers (`server: uvicorn`). A 30-student burst is untested. |
| Error shapes | VERIFIED | Bad key → **401** `{"detail":"Your session has expired or the token is invalid. Please sign in again."}` (misleading wording — students will think they must log in to the website). Malformed `messages` → **400** `{"detail":"dictionary update sequence element #0 has length 1; 2 is required"}` (a Python error, not an OpenAI-style error object). Context overflow → `{"detail":"litellm.ContextWindowExceededError: … This model's maximum context length is N tokens …"}`. |

### Models (SPEC 3.3 "local zoo")
Context lengths obtained by sending an oversized prompt and reading vLLM's error (`This model's maximum context length is N tokens`). Model identities from `/api/models` display names + Unistra's [catalogue page](https://documentation.unistra.fr/DNUM/Intelligence_artificielle/guide_complet_IA/co/2_2-catalogueModeles.html) + model cards.

| ID | Underlying model (card) | Params (total/active) | Context **as served** | Notes |
|---|---|---|---|---|
| `coder` (= `coder-qwen`) | [Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next), NVFP4 | 80B / 3B | **262,144** | Non-thinking only; "the 80B coder". Card recommends T=1.0, top_p 0.95. |
| `qwen3` | [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B), NVFP4 | 35B / 3B | **262,144** | Thinking **off by default via API** (4 completion tokens for 17×23); `"chat_template_kwargs": {"enable_thinking": true}` turns it on and returns `reasoning` in the message → the live "instruct vs reasoning" demo works on one model. |
| `gpt-oss` | [gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | 117B / 5.1B | **131,072** | Always reasons; reasoning text returned in `message.provider_specific_fields.reasoning`; `reasoning_effort: "high"` accepted. |
| `mistral-small` | [Mistral-Small-4-119B-2603](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | 119B / 6B | **128,000** (card: 256k) | Vision; `reasoning_effort` in card. |
| `ministral` | [Ministral-3-3B-Instruct-2512](https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512) | 3.4B+0.4B | **32,768** (card: 256k) | The fallback model (see risks). |
| `gemma` | [gemma-4-31B-it](https://huggingface.co/google/gemma-4-31B-it) | 30.7B dense | **262,144** | Vision; thinking mode via control tokens (not tested). |

- Max **output** tokens per model: UNVERIFIED (not probed; needed for OpenCode `limit.output`). Test: send `"max_tokens": 200000` and read the error.
- Spec's list « mistral-small, qwen3, gemma, gpt-oss, the 80B coder, ministral » — VERIFIED, all six exist. Spec should use the exact IDs.
- "Instruct vs reasoning vs agentic: same architecture, different post-training" — VERIFIED as framing; concretely demonstrable here: `qwen3` (thinking toggle), `gpt-oss` (`reasoning_effort`), `coder` (agentic, non-thinking).

### Tool calling (SPEC 3.4) — the decisive item
| Claim | Status | Evidence |
|---|---|---|
| Endpoint accepts `tools` and returns `tool_calls` | **VERIFIED on all 7 chat models** | Payload: one function `run_bash(command: string)`, `tool_choice: "auto"`, T=0, user asks "how many .md files… use the tool". Every model (`coder`, `coder-qwen`, `qwen3`, `gpt-oss`, `mistral-small`, `ministral`, `gemma`) returned `finish_reason: "tool_calls"`, `content: null`, and a well-formed `tool_calls[0].function.arguments` JSON string, e.g. `{"command": "find . -maxdepth 1 -name \"*.md\" -type f | wc -l"}`. `id` format differs by family (`chatcmpl-tool-…` for Qwen/gpt-oss/gemma; 9-char ids like `oemJ8j4rH` for Mistral). |
| Multi-turn: send back `{"role":"tool","tool_call_id":…,"content":"3\n"}` | VERIFIED (`coder`) | Second call with assistant `tool_calls` message + tool message → `finish_reason: "stop"`, `content: "There are 3 `.md` files in the current directory."` — the "students are the harness" round trip works exactly as the spec describes. |
| "Models are post-trained to emit well-formed tool calls" | VERIFIED | Qwen3-Coder-Next card: "excels in tool calling"; vLLM uses `--tool-call-parser qwen3_coder`/`qwen3_xml` and can constrain output to the schema ([vLLM tool calling docs](https://docs.vllm.ai/en/latest/features/tool_calling.html), which also documents the failure modes: malformed JSON without schema constraints, wrong argument types, parallel-call issues). |
| MCP as "USB-C for tools", separate class later | VERIFIED | [modelcontextprotocol.io intro](https://modelcontextprotocol.io/docs/getting-started/intro). OpenCode has `opencode mcp` and an `mcp` config block. |
| Statelessness demo, edited-assistant-message demo | VERIFIED (mechanism) | Standard chat-completions behaviour; nothing Unistra-specific blocks it. Reasoning models: for `gpt-oss` the prior `reasoning` need not be resent. |

## 2. Best deeper-dive resources

1. [Andrej Karpathy — Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) (3h31, free) — tokens, pretraining, post-training (SFT/RL), why "reasoning" models exist; the single best primer for 3.1–3.3. Shorter alternative: [Intro to Large Language Models (1h)](https://www.youtube.com/watch?v=zjkBMFhNj_g).
2. [Tiktokenizer](https://tiktokenizer.vercel.app/) — paste text, watch it split into tokens; the 30-second demo that makes "tokens are the unit of account" land.
3. [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) and the [Chat Completions reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) — the schema Unistra implements; the reference is what to open when a payload is rejected.
4. [vLLM — Tool calling](https://docs.vllm.ai/en/latest/features/tool_calling.html) — how the server turns model text into `tool_calls`, and why open-weight models sometimes emit malformed calls.
5. *Ambitious:* [Karpathy — Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) (2h13, code-along), then the [Berkeley Function-Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) to see tool-calling reliability measured across models.

## 3. Pedagogical risks

- **Silent fallback to a 3B model.** LiteLLM is configured with fallback chains visible in error messages: `gpt-oss → gpt-oss-ilaas → ministral`, `qwen3 → qwen3-ilaas → ministral`, `mistral-small → …-ilaas → ministral`, `gemma → …-ilaas → ministral`, `coder → ministral`. If the requested model is down or overloaded, answers may come from **Ministral 3B with a 32k context** while the response still reports the requested `model` name. In class this looks like "the model got dumb". Mitigation: show `usage`/quality checks; ask DNUM whether fallbacks are active for API keys; keep the demo prompts short enough for 32k.
- **The 401 message says "sign in again"** — students will reload the website. Mitigation: a slide "what each HTTP code means here" (401 = key wrong/unset, 400 = your JSON, 5xx = their problem).
- **Load**: 20 parallel requests were fine; 30 students × repeated tool-calling on an 80B model is untested. Mitigation: rehearse a burst test the morning of; `resources/fallback/` transcripts (Task 03) are the plan B.
- **Windows quoting**: `curl -d @request.json` is fine, but any inline `-d '{...}'` breaks in PowerShell. Mitigation: only ever `-d @file.json`; run in WSL/Git Bash.
- **`jq` not installed** on fresh WSL/Mac. Mitigation: `sudo apt install jq` / `brew install jq` in Session 0, or use `python3 -m json.tool` as fallback.
- **Reasoning tokens invisible in `content`** for `gpt-oss` — students see terse answers and a big `completion_tokens`. Mitigation: show `provider_specific_fields.reasoning` once; it is a great "you pay for thinking" moment.

## 4. Suggested spec edits

- 3.1: « `curl` POST to `https://conversation.ia.unistra.fr/api/chat/completions` » → add « (`$UNISTRA_BASE_URL/chat/completions` with `UNISTRA_BASE_URL=https://conversation.ia.unistra.fr/api`) ».
- 3.1: add « `usage` is present on every response — including tool-call responses; use it for the cost homework. »
- 3.3: replace the zoo list with exact IDs and served context: « `coder` (Qwen3-Coder-Next 80B/3B, 262k), `qwen3` (Qwen3.6-35B-A3B, 262k, thinking toggle), `gpt-oss` (120B/5B, 131k, always reasons), `mistral-small` (119B/6B, 128k), `gemma` (31B, 262k), `ministral` (3B, 32k) ».
- 3.3: add the one-payload demo « same question to `qwen3` with and without `chat_template_kwargs.enable_thinking` — compare `completion_tokens` » as the reasoning-vs-instruct evidence.
- 3.4: add « tool-calling verified on all six models; use `coder` for the exercise; `ministral` as the cheap fallback ».
- Known risks: add « LiteLLM fallback chains can silently route to `ministral` (3B, 32k) ».
