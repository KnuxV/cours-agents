"""Label research abstracts three times: SDG, technology, impact.

The three steps are chained: the impact question uses the answers of
the first two. Your script decides the order, so this is a workflow.

    uv run python 01_thesis_labels.py
"""
import json
import re

from llm import ask, ask_json

SDGS = open("data/sdgs.txt", encoding="utf-8").read()
ADTS = ["AI", "IOT", "COMPUTING_INFRASTRUCTURE", "BLOCKCHAIN", "ROBOTICS", "ADDITIVE_MANUFACTURING"]

# trois consignes, un paragraphe chacune
SDG_PROMPT = """Which United Nations Sustainable Development Goals does this research abstract relate to?
Count a goal only when what the paper studies bears on it, not when it is a passing mention.
The goals:
{sdgs}
Abstract: {abstract}
Answer with the codes only, for example: SDG3, SDG10. Answer NONE if there are none."""

ADT_PROMPT = """Which of these advanced digital technologies does this research involve?
AI (artificial intelligence, machine learning, big data), IOT (Internet of Things, sensors),
COMPUTING_INFRASTRUCTURE (cloud, data centres, 5G), BLOCKCHAIN (blockchain, cryptocurrencies),
ROBOTICS, ADDITIVE_MANUFACTURING (3D printing).
A word used in another sense, like an electrical power transformer, does not count.
Abstract: {abstract}
Answer with the codes only, for example: AI, ROBOTICS. Answer NONE if there are none."""

IMPACT_PROMPT = """This research involves {adts}. For each of these goals: {sdgs},
does the technology help the goal (positive), harm it (negative), both (mixed),
or does the abstract not say (unclear)? Judge from the abstract only.
Abstract: {abstract}
Answer with JSON, for example: {{"SDG3": "positive", "SDG10": "unclear"}}"""


def codes(text: str, allowed: list[str]) -> list[str]:
    """Keep only the codes from the allowed list, whatever the answer looks like."""
    found = re.findall(r"\b[A-Z][A-Z0-9_]*\b", text.upper())
    return [code for code in dict.fromkeys(found) if code in allowed]


def label(abstract: str) -> dict:
    """Run the three steps on one abstract."""
    all_sdgs = [line.split()[0] for line in SDGS.splitlines()]
    sdgs = codes(ask(SDG_PROMPT.format(sdgs=SDGS, abstract=abstract)), all_sdgs)
    adts = codes(ask(ADT_PROMPT.format(abstract=abstract)), ADTS)
    impact = {}
    # l'étape 3 dépend des deux premières : c'est l'enchaînement (prompt chaining)
    if sdgs and adts:
        impact = ask_json(IMPACT_PROMPT.format(adts=", ".join(adts), sdgs=", ".join(sdgs), abstract=abstract))
    return {"sdg": sdgs, "adt": adts, "impact": impact}


if __name__ == "__main__":
    papers = json.load(open("data/thesis_abstracts.json", encoding="utf-8"))
    for paper in papers:
        result = label(paper["abstract"])
        print(f"=== {paper['id']}: {paper['title']}")
        print(f"  SDG    : {result['sdg']}   (expected {paper['expected']['sdg']})")
        print(f"  ADT    : {result['adt']}   (expected {paper['expected']['adt']})")
        print(f"  impact : {result['impact'] or 'no technology found, nothing to score'}")
