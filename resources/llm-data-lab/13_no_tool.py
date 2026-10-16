"""Why give the model a tool for counting? Ask it without one.

The agent in 11 computes ages with a tool. Is the tool needed? Here the
same kind of questions (letters, arithmetic, dates) go to two models with
no tool at all, and Python gives the right answer to compare with.

A model reads text in chunks (tokens), not letter by letter, and it writes
a number digit by digit without computing it. So it is often right, and
sometimes wrong, with the same confidence.

    uv run python 13_no_tool.py
"""
import re
import time
from datetime import date

from llm import ask

MODELS = ["qwen3", "mistral-small"]

SENTENCE = "The Grand Est region announced a plan to support small firms hit by the energy crisis."
NUMBERS = [482, 1937, 75, 3061, 228, 914, 6502, 47, 1385, 799, 2614, 53, 8120, 336, 4471]


def age(birth: str, event: str) -> int:
    """The same computation as the age_at tool in 11."""
    b, e = date.fromisoformat(birth), date.fromisoformat(event)
    return e.year - b.year - ((e.month, e.day) < (b.month, b.day))


# (question, right answer computed by Python)
QUESTIONS: list[tuple[str, int]] = [
    ('How many times does the letter "r" appear in "strawberry"?', "strawberry".count("r")),
    ('How many times does the letter "s" appear in "Mississippi"?', "Mississippi".count("s")),
    (f'How many times does the letter "n" appear in this sentence: "{SENTENCE}"', SENTENCE.lower().count("n")),
    ("What is 7 × 8?", 7 * 8),
    ("What is 48271 × 9365?", 48271 * 9365),
    (f"What is the sum of these numbers: {', '.join(map(str, NUMBERS))}?", sum(NUMBERS)),
    ("How old was someone born on 1972-10-25 on 2019-10-14?", age("1972-10-25", "2019-10-14")),
    ("How old was someone born on 1990-10-15 on 2026-10-14?", age("1990-10-15", "2026-10-14")),
    ("How many days are there from 1972-10-25 to 2019-10-14?",
     (date(2019, 10, 14) - date(1972, 10, 25)).days),
]


def as_number(answer: str) -> int | None:
    """The first number in the answer, with "1,234" or "1 234" read as 1234."""
    cleaned = re.sub(r"(?<=\d)[ , ](?=\d{3}\b)", "", answer)
    found = re.search(r"-?\d+", cleaned)
    return int(found.group()) if found else None


if __name__ == "__main__":
    right = {m: 0 for m in MODELS}
    for question, truth in QUESTIONS:
        print(f"=== {question}")
        print(f"  {'python':<14} {truth}")
        for model in MODELS:
            start = time.time()
            answer = ask(question + "\nAnswer with the number only.", model=model)
            seconds = time.time() - start
            got = as_number(answer)
            right[model] += got == truth
            mark = "OK " if got == truth else "BAD"
            print(f"  {model:<14} {got}  {mark} ({seconds:.0f} s)")
    print()
    for model in MODELS:
        print(f"{model}: {right[model]}/{len(QUESTIONS)} right")
