"""An agent: the model decides which tool to call next, in a loop.

Task: for 3 Nobel economists, find where they got their PhD and their
age at the prize. The model has 4 tools (search Wikipedia, read a page,
compute an age, save a row). Every tool call is printed as it happens.
The answers are known, so the run is scored at the end.

    uv run python 11_agent_nobel.py              # with qwen3
    uv run python 11_agent_nobel.py mistral-small
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

from llm import MODEL, chat

WIKI = "https://en.wikipedia.org/w/api.php"
# Wikipedia veut savoir qui l'appelle
USER_AGENT = "llm-data-lab/0.1 (course example, Universite de Strasbourg)"
MAX_STEPS = 15
# les pages déjà lues sont gardées ici : la démo peut se rejouer sans réseau
CACHE_FILE = "data/wiki_cache.json"

TASK = (
    "For each of these Nobel economics laureates: Esther Duflo, Jean Tirole, Claudia Goldin. "
    "Find the university where they got their PhD and their age on the day the prize was "
    "announced (Duflo 2019-10-14, Tirole 2014-10-13, Goldin 2023-10-09). Search Wikipedia, "
    "read the page, compute the age with the age tool, then call save_row once per person. "
    "Do not guess: if you could not read it in a page, save 'unknown'. "
    "When all three are saved, reply DONE."
)

# les bonnes réponses, plusieurs façons d'écrire la même université
EXPECTED = {
    "Duflo": (("MIT", "Massachusetts Institute of Technology"), "46"),
    "Tirole": (("MIT", "Massachusetts Institute of Technology"), "61"),
    "Goldin": (("Chicago",), "77"),
}

try:
    CACHE: dict[str, dict] = json.load(open(CACHE_FILE, encoding="utf-8"))
except FileNotFoundError:
    CACHE = {}


def wiki(params: dict) -> dict:
    """Call the Wikipedia API (cached, polite, retries when told to slow down)."""
    url = f"{WIKI}?{urllib.parse.urlencode(params | {'format': 'json'})}"
    if url not in CACHE:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        for wait in (2, 5, 10, None):
            time.sleep(0.5)  # pas plus de 2 requêtes par seconde
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    CACHE[url] = json.load(response)
                break
            except urllib.error.HTTPError as error:
                if error.code != 429 or wait is None:  # 429 = « trop de requêtes »
                    raise
                time.sleep(wait)
        json.dump(CACHE, open(CACHE_FILE, "w", encoding="utf-8"))
    return CACHE[url]


# --- les outils : des fonctions Python ordinaires ---

def wikipedia_search(query: str) -> str:
    """Titles of the 3 best Wikipedia matches."""
    hits = wiki({"action": "query", "list": "search", "srsearch": query, "srlimit": 3})["query"]["search"]
    return "\n".join(hit["title"] for hit in hits) or "no results"


def wikipedia_page(title: str) -> str:
    """Plain text of a page, cut to 6000 characters."""
    pages = wiki({"action": "query", "prop": "extracts", "explaintext": 1, "titles": title, "redirects": 1})
    return next(iter(pages["query"]["pages"].values())).get("extract", "page not found")[:6000]


def age_at(birth_date: str, event_date: str) -> str:
    """Age in whole years between two dates written YYYY-MM-DD."""
    # fromisoformat refuse "25 October 1972" ou "1972-13-45" : l'erreur repart au modèle
    birth = date.fromisoformat(birth_date)
    event = date.fromisoformat(event_date)
    # True (= 1) if the birthday has not come yet that year
    before = (event.month, event.day) < (birth.month, birth.day)
    return str(event.year - birth.year - before)


SAVED: dict[str, dict] = {}


def save_row(name: str, phd_institution: str, age_at_prize: str) -> str:
    """Store the result for one person."""
    SAVED[name] = {"phd": phd_institution, "age": str(age_at_prize)}
    return f"saved {name}"


TOOLS_PY = {f.__name__: f for f in (wikipedia_search, wikipedia_page, age_at, save_row)}


def describe(name: str, description: str, /, **params: str) -> dict:
    """A tool as the model sees it: a name, what it does, its parameters."""
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "required": list(params),
                       "properties": {p: {"type": "string", "description": d} for p, d in params.items()}},
    }}


TOOLS = [
    describe("wikipedia_search", "Search English Wikipedia; returns page titles.", query="search words"),
    describe("wikipedia_page", "Plain text of a Wikipedia page.", title="exact page title"),
    describe("age_at", "Age in years between two dates.", birth_date="YYYY-MM-DD", event_date="YYYY-MM-DD"),
    describe("save_row", "Save the result for one laureate.", name="full name",
             phd_institution="university, or 'unknown'", age_at_prize="number, or 'unknown'"),
]


def run(model: str) -> None:
    """The whole agent: a loop around tool calls, with a step cap."""
    messages: list[dict] = [{"role": "user", "content": TASK}]
    for step in range(1, MAX_STEPS + 1):
        reply = chat(messages, model=model, tools=TOOLS)
        messages.append(reply)
        calls = reply.get("tool_calls") or []
        if not calls:  # aucun outil demandé : le modèle a décidé d'arrêter
            print(f"[{step}] model: {(reply.get('content') or '').strip()[:100]}")
            break
        for call in calls:
            name, args = call["function"]["name"], {}
            try:
                args = json.loads(call["function"]["arguments"] or "{}")
                result = TOOLS_PY[name](**args)
            except Exception as error:  # l'erreur est renvoyée au modèle, qui peut réagir
                result = f"tool error: {error}"
            print(f"[{step}] {name}({json.dumps(args, ensure_ascii=False)}) -> {result[:60]!r}")
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
    else:
        print(f"stopped: {MAX_STEPS} steps reached")

    score = 0
    for person, (schools, age) in EXPECTED.items():
        row = next((r for n, r in SAVED.items() if person in n), None)
        ok = bool(row) and any(s.lower() in row["phd"].lower() for s in schools) and row["age"] == age
        score += ok
        print(f"  {'OK ' if ok else 'BAD'} {person}: {row}")
    print(f"score {score}/3, {step} steps")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else MODEL)
