"""Extraction (NER): a job ad in French -> a JSON record.

Without an LLM you would label hundreds of ads by hand and train a model.
Here: zero examples, one paragraph of instructions.

    uv run python 07_extract.py
"""
import json

from llm import ask_json

PROMPT = """Extract information from this job ad.
Ad: {text}
Answer with JSON only, using these keys:
"job" (the job title), "contract" (one of CDI, CDD, stage, alternance, freelance),
"remote" (true if any remote work is allowed, else false),
"salary_min" (lowest yearly gross salary in euros as a number, or null if not given),
"city"."""

SCORED = ["contract", "remote", "salary_min", "city"]


if __name__ == "__main__":
    ads = json.load(open("data/job_ads.json", encoding="utf-8"))
    correct = 0
    for ad in ads:
        record = ask_json(PROMPT.format(text=ad["text"]))
        print(f"=== {ad['text'][:60]}...")
        print(f"  {json.dumps(record, ensure_ascii=False)}")
        for key in SCORED:
            got, want = record.get(key), ad["expected"][key]
            ok = got == want or str(got).lower() == str(want).lower()
            correct += ok
            if not ok:
                print(f"  BAD {key}: got {got!r}, expected {want!r}")
    print(f"fields correct: {correct}/{len(ads) * len(SCORED)}")
