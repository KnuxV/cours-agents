"""One call: which named entities are in this text? Asked twice.

1. Raw: the question alone. The answer is readable, but it is prose:
   nothing a script can build a table from.
2. Constrained: the same question, plus the format we want (JSON with
   five keys). Now the answer is data, and we can check it against the
   list we expect.

The two paragraphs are invented.

    uv run python 00_entities.py
"""
import json

from llm import ask, ask_json

TEXT = """In March 2025, Claire Martin, chief economist at Crédit Agricole, told Le Monde that the
European Central Bank would cut its rates twice before the summer. She expects inflation in
France to fall below 2 % by the end of the year.

In Strasbourg, the Grand Est region announced a 40 million euro plan to support small firms hit
by the energy crisis. The plan was presented by its president, Thomas Weber, on 14 April."""

RAW = """What are the named entities in this text?
Text: {text}"""

# la même question, plus le format qu'on veut en sortie
CONSTRAINED = RAW + """
Answer with JSON only, with the keys "person", "organisation", "place", "date" and "amount",
each holding a list of the entities exactly as written in the text."""

EXPECTED = {
    "person": ["Claire Martin", "Thomas Weber"],
    "organisation": ["Crédit Agricole", "Le Monde", "European Central Bank", "Grand Est region"],
    "place": ["France", "Strasbourg"],
    "date": ["March 2025", "14 April"],
    "amount": ["2 %", "40 million euro"],
}


if __name__ == "__main__":
    print("=== 1. raw call")
    print(ask(RAW.format(text=TEXT)))
    print("\n=== 2. constrained call")
    found = ask_json(CONSTRAINED.format(text=TEXT))
    print(json.dumps(found, ensure_ascii=False))
    # on compare sans tenir compte des majuscules
    for key, want in EXPECTED.items():
        got = {str(x).lower() for x in found.get(key, [])}
        missing = [w for w in want if w.lower() not in got]
        extra = sorted(got - {w.lower() for w in want})
        print(f"  {key:<12} missing: {missing or '-'}   extra: {extra or '-'}")
