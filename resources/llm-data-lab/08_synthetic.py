"""Synthetic data: the model writes fake job ads whose labels we know,
then a classifier (the model again) has to find the labels back.

Useful to test a pipeline before you have real data. Too clean to
draw conclusions from: real ads are messier.

    uv run python 08_synthetic.py
"""
from llm import ask, ask_json

GENERATE = """Write 8 short, realistic French job ads (2 sentences each) for economics graduates:
2 CDI, 2 CDD, 2 stage, 2 alternance. Vary the wording; do not always write the contract type literally.
Answer with a JSON list of objects with keys "text" and "contract"."""

CLASSIFY = """What type of contract does this job ad offer? Ad: {text}
Answer with one word: CDI, CDD, stage or alternance."""


if __name__ == "__main__":
    # température haute : on veut de la variété
    ads = ask_json(GENERATE, temperature=0.9)
    correct = 0
    for ad in ads:
        guess = ask(CLASSIFY.format(text=ad["text"])).strip(" .")
        ok = guess.lower() == ad["contract"].lower()
        correct += ok
        print(f"  {'OK ' if ok else 'BAD'} true {ad['contract']:<10} guess {guess:<10} {ad['text'][:70]}")
    print(f"recovered: {correct}/{len(ads)}")
