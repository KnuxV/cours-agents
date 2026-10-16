"""Two passes: first cast a wide net, then check each catch.

Pass 1 is told to be inclusive: a label it misses is lost for good.
Pass 2 looks at one label at a time and answers Y or N: it removes
the false alarms. Done for the goals (SDG) and the technologies (ADT).
Same idea as the thesis pipeline, with shorter prompts.

    uv run python 02_two_passes.py
"""
import json
import re

from llm import ask, ask_json

SDGS = open("data/sdgs.txt", encoding="utf-8").read()
SDG_NAMES = dict(line.split(" ", 1) for line in SDGS.splitlines())
ADT_NAMES = {
    "AI": "artificial intelligence, machine learning, big data",
    "IOT": "Internet of Things, connected sensors",
    "COMPUTING_INFRASTRUCTURE": "cloud, data centres, 5G",
    "BLOCKCHAIN": "blockchain, cryptocurrencies",
    "ROBOTICS": "robots",
    "ADDITIVE_MANUFACTURING": "3D printing",
}
ADT_LIST = "\n".join(f"{code} ({name})" for code, name in ADT_NAMES.items())

PASS1 = """Which {what} could this research abstract relate to?
This is a screening step: a later step checks each answer, so a label you name wrongly costs little
and a label you miss is lost. Be inclusive: name every one that could plausibly apply, even weakly,
even when the abstract describes it without using its usual name.
The list:
{options}
Abstract: {abstract}
Answer with the codes only, separated by commas."""

PASS2 = """A screening step proposed the label {code} ({name}) for this abstract. Your job is to check.
Answer Y when what the paper studies really bears on it. Answer N when the link is only a passing
mention, a word used in another sense, or a generic claim of benefit.
Abstract: {abstract}
Is {code} right for this abstract? Answer with one letter, Y or N."""

IMPACT = """This research involves {adts}. For each of these goals: {sdgs},
does the technology help the goal (positive), harm it (negative), both (mixed),
or does the abstract not say (unclear)? Judge from the abstract only.
Abstract: {abstract}
Answer with JSON, for example: {{"SDG3": "positive", "SDG10": "unclear"}}"""


def codes(text: str, allowed: dict) -> list[str]:
    """Keep only the codes from the allowed list, whatever the answer looks like."""
    found = re.findall(r"\b[A-Z][A-Z0-9_]*\b", text.upper())
    return [code for code in dict.fromkeys(found) if code in allowed]


def two_passes(abstract: str, what: str, options: str, names: dict) -> tuple[list, dict]:
    """Pass 1 proposes, pass 2 checks each proposal."""
    proposed = codes(ask(PASS1.format(what=what, options=options, abstract=abstract)), names)
    # passe 2 : une question fermée par étiquette proposée
    verdicts = {
        code: ask(PASS2.format(code=code, name=names[code], abstract=abstract)).strip()[:1].upper()
        for code in proposed
    }
    return proposed, verdicts


if __name__ == "__main__":
    papers = json.load(open("data/thesis_abstracts.json", encoding="utf-8"))
    for paper in papers:
        print(f"=== {paper['id']}: {paper['title']}")
        kept = {}
        for key, what, options, names in [
            ("sdg", "United Nations Sustainable Development Goals", SDGS, SDG_NAMES),
            ("adt", "advanced digital technologies", ADT_LIST, ADT_NAMES),
        ]:
            proposed, verdicts = two_passes(paper["abstract"], what, options, names)
            kept[key] = [code for code, v in verdicts.items() if v == "Y"]
            print(f"  {key.upper()} pass 1 (wide net) : {proposed}")
            print(f"  {key.upper()} pass 2 (check)    : {verdicts}")
            print(f"  {key.upper()} kept              : {kept[key]}   (expected {paper['expected'][key]})")
        if kept["sdg"] and kept["adt"]:
            impact = ask_json(IMPACT.format(
                adts=", ".join(kept["adt"]), sdgs=", ".join(kept["sdg"]), abstract=paper["abstract"]))
            print(f"  impact : {impact}")
