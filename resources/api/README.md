# Session 3 — raw API payloads

One file per step. Send them with `curl`, from the folder that holds them:

```bash
curl -s https://conversation.ia.unistra.fr/api/chat/completions \
  -H "Authorization: Bearer $UNISTRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d @question.json | python3 -m json.tool
```

- `question.json` — one system message, one user message, `temperature: 0`. No tools.
- `question-2turns.json` — the same conversation with the assistant's reply and a follow-up, to show that history is re-sent by hand.

The endpoint, the `Authorization: Bearer` header and the response shape were tested live on 2026-08-28 (`research/s3-api.md`). `python3 -m json.tool` pretty-prints; `jq` does the same but is not installed everywhere.
