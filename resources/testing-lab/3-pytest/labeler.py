"""Ask an LLM whether a review is positive or negative.

The network call lives in ask_llm(). Everything else is our own code,
and our own code is what the tests check (see tests/test_labeler.py).
"""
import json
import os
import urllib.request

API_URL = "https://conversation.ia.unistra.fr/api/chat/completions"


def ask_llm(prompt: str) -> str:
    """Send one prompt to the Unistra API and return the text of the answer."""
    # le message envoyé au modèle, dans le format attendu par l'API
    payload = {"model": "coder", "messages": [{"role": "user", "content": prompt}]}
    # la requête : l'adresse, le message en JSON, et la clé lue dans une variable d'environnement
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {os.environ['UNISTRA_API_KEY']}",
            "Content-Type": "application/json",
        },
    )
    # on envoie, on lit la réponse JSON et on en extrait le texte écrit par le modèle
    with urllib.request.urlopen(request) as response:
        return json.load(response)["choices"][0]["message"]["content"]


def label_review(text: str) -> str:
    """Return "pos", "neg" or "unknown" for one review."""
    # on pose la question au modèle : c'est le seul appel réseau
    answer = ask_llm(f"Is this review positive or negative? Answer with one word.\n\n{text}")
    # on nettoie la réponse : espaces, point final, majuscules ("Negative." devient "negative")
    word = answer.strip().strip(".!").lower()
    # on traduit la réponse en une de nos trois étiquettes
    if word in {"positive", "positif"}:
        return "pos"
    if word in {"negative", "négatif", "negatif"}:
        return "neg"
    # toute autre réponse (une phrase, un autre mot) : on ne devine pas
    return "unknown"
