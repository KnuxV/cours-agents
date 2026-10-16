"""Talk to the Unistra models: everything the experiments need, in one file.

- `ask()` sends one prompt and returns the text of the answer.
- `ask_json()` does the same and parses the answer as JSON.
- `chat()` is the raw call, used by the agent loop (it needs tools).

The key is read from the environment variable `UNISTRA_API_KEY`.
"""
import base64
import json
import os
import re
import urllib.error
import urllib.request

API_URL = "https://conversation.ia.unistra.fr/api/chat/completions"
# changez de modèle ici : qwen3, mistral-small, gemma, coder, ministral, gpt-oss
MODEL = "qwen3"


def chat(
    messages: list[dict], model: str = MODEL, tools: list[dict] | None = None, temperature: float = 0
) -> dict:
    """Send a list of messages, return the assistant's message (a dict)."""
    payload: dict = {"model": model, "messages": messages, "temperature": temperature}
    if tools:
        payload["tools"] = tools
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {os.environ['UNISTRA_API_KEY']}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.load(response)["choices"][0]["message"]
    except urllib.error.HTTPError as error:
        # le serveur explique souvent pourquoi il refuse : on affiche son message
        raise RuntimeError(f"{error} {error.read().decode()[:500]}") from None


def ask(
    prompt: str,
    system: str | None = None,
    model: str = MODEL,
    temperature: float = 0,
    image: str | None = None,
) -> str:
    """One prompt in, the text of the answer out. `image` is the path of a PNG or JPEG."""
    content: str | list[dict] = prompt
    if image:
        # une image voyage dans le message, encodée en texte (base64)
        kind = "png" if image.endswith(".png") else "jpeg"
        with open(image, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/{kind};base64,{data}"}},
        ]
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": content})
    text = chat(messages, model=model, temperature=temperature).get("content") or ""
    # certains modèles « réfléchissent » à voix haute entre <think> et </think> : on l'enlève
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()


def ask_json(prompt: str, system: str | None = None, model: str = MODEL, temperature: float = 0):
    """Like ask(), but parse the answer as JSON (a list or a dict)."""
    text = ask(prompt, system=system, model=model, temperature=temperature)
    # le modèle entoure parfois son JSON de ```json ... ``` : on garde ce qu'il y a entre
    start = min((i for i in (text.find("["), text.find("{")) if i != -1), default=0)
    end = max(text.rfind("]"), text.rfind("}")) + 1
    return json.loads(text[start:end])
