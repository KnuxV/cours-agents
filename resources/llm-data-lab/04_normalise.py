"""Messy country names -> ISO codes. Rules first, the LLM only for what rules miss.

pycountry knows the official names and codes. What it can't match
(French names, nicknames) goes to the model, and the model's answer
is checked against pycountry's list: no invented codes.

    uv run python 04_normalise.py
"""
import csv

import pycountry

from llm import ask

PROMPT = """What is the ISO 3166-1 alpha-3 code of this country: "{raw}"?
Answer with the three-letter code only, or UNKNOWN."""


def by_rule(raw: str) -> str | None:
    """Exact match on pycountry's names and codes, or None."""
    try:
        return pycountry.countries.lookup(raw.strip()).alpha_3
    except LookupError:
        return None


def by_llm(raw: str) -> str:
    """Ask the model, then check the code exists."""
    code = ask(PROMPT.format(raw=raw)).strip().upper()[:7]
    return code if pycountry.countries.get(alpha_3=code) else f"INVALID ({code})"


if __name__ == "__main__":
    rows = list(csv.DictReader(open("data/countries.csv", encoding="utf-8")))
    correct, sent_to_llm = 0, 0
    for row in rows:
        code, how = by_rule(row["raw"]), "rule"
        if code is None:
            code, how = by_llm(row["raw"]), "LLM "
            sent_to_llm += 1
        ok = code == row["iso3"]
        correct += ok
        print(f"  {'OK ' if ok else 'BAD'} {how}  {row['raw']!r:28} -> {code}")
    print(f"correct: {correct}/{len(rows)}  (rules: {len(rows) - sent_to_llm}, LLM: {sent_to_llm})")
