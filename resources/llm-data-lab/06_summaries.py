"""One-line summaries, then a second model checks them (LLM as judge).

The judge is itself a measurement: read a few of its verdicts
yourself before trusting it on thousands of rows.

    uv run python 06_summaries.py
"""
import json

from llm import ask

SUMMARY = """Summarise this research abstract in one sentence of at most 20 words.
Abstract: {abstract}"""

JUDGE = """Here is an abstract and a one-sentence summary of it.
Abstract: {abstract}
Summary: {summary}
Does the summary say anything that the abstract does not support? Answer "OK" if it is faithful,
or "PROBLEM: " followed by what is wrong."""


if __name__ == "__main__":
    papers = json.load(open("data/thesis_abstracts.json", encoding="utf-8"))
    for paper in papers:
        summary = ask(SUMMARY.format(abstract=paper["abstract"]))
        # un autre modèle relit : il ne partage pas forcément les mêmes erreurs
        verdict = ask(JUDGE.format(abstract=paper["abstract"], summary=summary), model="mistral-small")
        print(f"=== {paper['id']} ({len(paper['abstract'].split())} words)")
        print(f"  summary : {summary}")
        print(f"  judge   : {verdict}")
