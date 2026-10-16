"""From messy text to a clean table.

data/wine_exports.txt has 6 sentences, written fast, with misspelled
countries ("Etats Unix") or no name at all ("la perfide Albion"). The
model turns them into a 2-column table: ISO country code, exports in
billions of euros. Figures invented.

    uv run python 09_text_to_table.py
"""
import csv

from llm import ask

PROMPT = """Here are notes about wine exports, one sentence per country. A country may be misspelled,
or described by a nickname instead of its name.
Turn them into a CSV table with the header country,exports_bn_eur.
Write each country as its ISO 3166-1 alpha-3 code (FRA, ITA...), and the amount in billions
of euros as a number with a dot.
Notes:
{notes}
Answer with the CSV only."""


if __name__ == "__main__":
    notes = open("data/wine_exports.txt", encoding="utf-8").read()
    text = ask(PROMPT.format(notes=notes))
    print(text)
    rows = list(csv.reader(line for line in text.strip("`\n").splitlines() if "," in line))
    # la ligne d'en-tête est enlevée seulement si le modèle l'a écrite
    rows = [row for row in rows if row[0].strip().lower() != "country"]
    truth = list(csv.reader(open("data/wine_exports_truth.csv", encoding="utf-8")))[1:]
    # une ligne est juste si le pays et le montant sont justes
    correct = sum(
        got[0].strip() == want[0] and float(got[1]) == float(want[1])
        for got, want in zip(rows, truth)
    )
    print(f"rows correct: {correct}/{len(truth)}")
