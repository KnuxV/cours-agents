"""Talk to the Unistra models: everything the experiments need, in one file.

- `ask()` sends one prompt and returns the text of the answer.
- `ask_json()` does the same and parses the answer as JSON.
- `chat()` is the raw call, used by the agent loop (it needs tools).

The key is read from the environment variable `UNISTRA_API_KEY`.

How it works, in one paragraph: a model does not run on your computer.
It runs on a server at the university. To use it, Python sends an HTTP
request (the same kind of message your browser sends when it opens a
page) to an address, the API URL. The request carries your prompt and
your key, written in JSON. The server answers with JSON too, and the
model's text is inside. That is all this file does: build the request,
send it, dig the text out of the answer. It is the same request you
sent with curl in Session 3, written in Python.

Only the standard library is used (nothing to install): `urllib` sends
the request, `json` converts between Python dicts and JSON text.
"""
import base64  # turns an image (bytes) into text, so it can travel in JSON
import json  # Python dict <-> JSON text
import os  # to read the environment variable that holds the key
import re  # regular expressions, to cut the model's "thinking" out of its answer
import urllib.error
import urllib.request  # sends HTTP requests

# The address of the server. "chat/completions" is the standard path that
# OpenAI made popular; many providers (Unistra included) copy it, so this
# file would work elsewhere by changing the URL, the key and the model name.
API_URL = "https://conversation.ia.unistra.fr/api/chat/completions"

# The model used when a script does not say otherwise.
# Change it here: qwen3, mistral-small, gemma (reads images), coder, ministral, gpt-oss
MODEL = "qwen3"


def chat(
    messages: list[dict], model: str = MODEL, tools: list[dict] | None = None, temperature: float = 0
) -> dict:
    """Send a list of messages, return the assistant's message (a dict)."""
    # The request body. `messages` is the whole conversation so far, as a list:
    #   [{"role": "system", "content": "..."},     <- optional instructions
    #    {"role": "user", "content": "..."},       <- what we ask
    #    {"role": "assistant", "content": "..."},  <- what the model answered before
    #    ...]
    # The model has no memory between calls: to continue a conversation,
    # you send it again, in full, every time.
    # `temperature` controls randomness: 0 = always pick the most likely next
    # word, so the same prompt gives (almost) the same answer. Good for data.
    payload: dict = {"model": model, "messages": messages, "temperature": temperature}
    if tools:
        # Descriptions of functions the model may ask us to run (see 11_agent_nobel.py).
        # The model never runs them itself: it answers "please call this one".
        payload["tools"] = tools
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),  # dict -> JSON text -> bytes
        headers={
            # The key proves who you are. It is read from the environment,
            # never written in the code: this file can be shared safely.
            # If the variable is missing, Python stops here with KeyError: 'UNISTRA_API_KEY'.
            "Authorization": f"Bearer {os.environ['UNISTRA_API_KEY']}",
            "Content-Type": "application/json",  # "the body is JSON"
        },
    )
    try:
        # Send it and wait for the answer (at most 300 seconds: big models can be slow).
        with urllib.request.urlopen(request, timeout=300) as response:
            # The answer looks like this (shortened):
            #   {"choices": [{"message": {"role": "assistant", "content": "USA"}}],
            #    "usage": {"prompt_tokens": 52, "completion_tokens": 1}, ...}
            # We keep only the message. When the model wants a tool, its
            # message has "tool_calls" instead of (or as well as) "content".
            return json.load(response)["choices"][0]["message"]
    except urllib.error.HTTPError as error:
        # The server refused (401: bad key, 404: unknown model, 429: too many
        # requests, 400: something it did not like in the request). It usually
        # says why in its answer, so we show that message instead of hiding it.
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
        # An image travels inside the message, written as text (base64), in a
        # "data URL". Only models that can see accept it (gemma here).
        kind = "png" if image.endswith(".png") else "jpeg"
        with open(image, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        # With an image, the content becomes a list of parts: the text, then the image.
        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/{kind};base64,{data}"}},
        ]
    # A conversation of one or two messages: the optional system instruction, then our prompt.
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": content})
    text = chat(messages, model=model, temperature=temperature).get("content") or ""
    # Some models "think out loud" before answering, between <think> and </think>.
    # Useful to read when debugging, but not part of the answer: we cut it out.
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()


def ask_json(prompt: str, system: str | None = None, model: str = MODEL, temperature: float = 0):
    """Like ask(), but parse the answer as JSON (a list or a dict)."""
    text = ask(prompt, system=system, model=model, temperature=temperature)
    # Even when asked for "JSON only", models often wrap it:
    #   Here is the result: ```json {"person": [...]} ```
    # So we keep what lies between the first [ or { and the last ] or }.
    start = min((i for i in (text.find("["), text.find("{")) if i != -1), default=0)
    end = max(text.rfind("]"), text.rfind("}")) + 1
    # If the model wrote something that is not valid JSON, this line fails
    # with json.JSONDecodeError: print `text` to see what it really answered.
    return json.loads(text[start:end])
