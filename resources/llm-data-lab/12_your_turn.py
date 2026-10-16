"""Your turn: classify your own texts.

This file is a template. The example sorts central-bank sentences into
hawkish / dovish / neutral (sentences invented for the example). To
classify something else, change only the three things marked CHANGE:

1. LABELS: the closed list of answers you accept.
2. QUESTION: what you ask about each text, in one paragraph.
3. DATA: a CSV with a "text" column. Add a "label" column with your own
   answers for a few rows if you want a score.

    uv run python 12_your_turn.py
"""
import csv

from llm import ask

# CHANGE 1: the closed list of answers
LABELS = ["hawkish", "dovish", "neutral"]

# CHANGE 2: the question, one paragraph ({text} is each row)
QUESTION = """Is this sentence from a central bank hawkish (in favour of higher interest rates),
dovish (in favour of lower rates) or neutral?
Sentence: {text}"""

# CHANGE 3: your CSV, with a "text" column (and "label" if you know the answer)
DATA = "data/my_data.csv"


def classify(text: str) -> str:
    """Ask the model, and keep the answer only if it is in LABELS."""
    prompt = QUESTION.format(text=text) + f"\nAnswer with one word: {', '.join(LABELS)}."
    answer = ask(prompt).strip(" .").lower()
    return answer if answer in LABELS else f"INVALID ({answer[:20]})"


if __name__ == "__main__":
    rows = list(csv.DictReader(open(DATA, encoding="utf-8")))
    scored, correct = 0, 0
    for row in rows:
        guess = classify(row["text"])
        mark = ""
        if row.get("label"):  # on a la bonne réponse : on compte
            scored += 1
            correct += guess == row["label"]
            mark = "OK " if guess == row["label"] else "BAD"
        print(f"  {mark:3} {guess:<10} {row['text'][:80]}")
    if scored:
        print(f"accuracy: {correct}/{scored}")
