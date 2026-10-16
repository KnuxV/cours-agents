"""Deduplication: do two names refer to the same company?

String similarity says "Total SA" and "TotalEnergies SE" are different,
and "Crédit Agricole" and "Crédit Mutuel" are close. The model knows better.

    uv run python 05_same_firm.py
"""
import csv
from difflib import SequenceMatcher

from llm import ask

PROMPT = """Do these two names refer to the same company (possibly renamed or abbreviated)?
A: {a}
B: {b}
Answer with one word: yes or no."""


if __name__ == "__main__":
    rows = list(csv.DictReader(open("data/firm_pairs.csv", encoding="utf-8")))
    correct = 0
    for row in rows:
        answer = ask(PROMPT.format(a=row["name_a"], b=row["name_b"])).lower().strip(" .")
        # pour comparer : la ressemblance des lettres, de 0 à 1
        letters = SequenceMatcher(None, row["name_a"].lower(), row["name_b"].lower()).ratio()
        ok = answer == row["same"]
        correct += ok
        print(f"  {'OK ' if ok else 'BAD'} {answer:>3}  letters {letters:.2f}  {row['name_a']} / {row['name_b']}")
    print(f"accuracy: {correct}/{len(rows)}")
