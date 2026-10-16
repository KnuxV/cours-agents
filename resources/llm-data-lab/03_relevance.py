"""Yes/no filter: is this paper about the labour market? Scored against our own labels.

Zero examples given to the model: it already knows what a labour market is.

    uv run python 03_relevance.py
"""
import csv

from llm import ask

PROMPT = """Is this economics paper about the labour market (jobs, wages, employment, hiring)?
Title: {title}
Answer with one word: yes or no."""


if __name__ == "__main__":
    rows = list(csv.DictReader(open("data/titles.csv", encoding="utf-8")))
    correct = 0
    for row in rows:
        answer = ask(PROMPT.format(title=row["title"])).lower().strip(" .")
        # liste fermée : toute autre réponse compte comme une erreur
        if answer not in ("yes", "no"):
            answer = f"INVALID ({answer[:20]})"
        ok = answer == row["about_labour_market"]
        correct += ok
        print(f"  {'OK ' if ok else 'BAD'} {answer:>4}  {row['title'][:75]}")
    print(f"accuracy: {correct}/{len(rows)}")
