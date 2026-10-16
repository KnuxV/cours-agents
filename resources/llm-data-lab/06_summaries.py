"""Summaries with a limit, then a judge with explicit criteria.

1. The summary must fit in 120 characters. That rule needs no judge:
   the script counts.
2. A second model (the judge) checks what a script cannot: three
   questions written in advance, each answered yes or no with a reason.
   The judge is itself a measurement: read some of its verdicts yourself.

    uv run python 06_summaries.py
"""
import json

from llm import ask, ask_json

MAX_CHARS = 120

SUMMARY = """Summarise this research abstract in one sentence of at most {max_chars} characters.
Abstract: {abstract}"""

JUDGE = """You check a one-sentence summary of a research abstract.
Abstract: {abstract}
Summary: {summary}
Answer three questions:
- "main_finding": does the summary state the paper's main finding?
- "unsupported": does the summary claim anything the abstract does not support?
- "topic_clear": would a reader know what the paper studies?
Answer with JSON only: {{"main_finding": "yes" or "no", "unsupported": "yes" or "no",
"topic_clear": "yes" or "no", "why": "one short sentence"}}"""


if __name__ == "__main__":
    papers = json.load(open("data/thesis_abstracts.json", encoding="utf-8"))
    for paper in papers:
        summary = ask(SUMMARY.format(max_chars=MAX_CHARS, abstract=paper["abstract"]))
        # la longueur, c'est le script qui la vérifie : pas besoin d'un modèle
        length = "OK" if len(summary) <= MAX_CHARS else "TOO LONG"
        # le reste, un autre modèle le vérifie, sur des critères écrits à l'avance
        verdict = ask_json(JUDGE.format(abstract=paper["abstract"], summary=summary), model="mistral-small")
        print(f"=== {paper['id']}: {paper['title']}")
        print(f"  abstract ({len(paper['abstract'])} chars): {paper['abstract']}")
        print(f"  summary  ({len(summary)} chars, {length}): {summary}")
        print(f"  judge    : {json.dumps(verdict, ensure_ascii=False)}")
