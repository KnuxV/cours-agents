"""Ask an LLM whether a review is positive or negative.

The network call lives in ask_llm(). Everything else is our own code,
and our own code is what the tests check (see tests/test_labeler.py).
"""
import json
import os
import urllib.request

API_URL = "https://conversation.ia.unistra.fr/api/chat/completions"


def ask_llm(prompt):
    """Send one prompt to the Unistra API and return the text of the answer."""
    payload = {"model": "coder", "messages": [{"role": "user", "content": prompt}]}
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {os.environ['UNISTRA_API_KEY']}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)["choices"][0]["message"]["content"]


def label_review(text):
    """Return "pos", "neg" or "unknown" for one review."""
    answer = ask_llm(f"Is this review positive or negative? Answer with one word.\n\n{text}")
    word = answer.strip().strip(".!").lower()
    if word in {"positive", "positif"}:
        return "pos"
    if word in {"negative", "négatif", "negatif"}:
        return "neg"
    return "unknown"
