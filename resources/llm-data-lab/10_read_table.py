"""Read a scanned table: an image in, a CSV out, checked cell by cell.

gemma reads images. For old printed statistics this can replace the
OCR step and the cleaning that follows it.

    uv run python 10_read_table.py
"""
import csv

from llm import ask

PROMPT = """This is a scanned page of a statistical yearbook. Copy the table as CSV
with the header arrondissement,ble,houblon,tabac. Write numbers without spaces.
Answer with the CSV only."""


if __name__ == "__main__":
    text = ask(PROMPT, model="gemma", image="data/scanned_table.png")
    print(text)
    lines = [line for line in text.strip("`\n").splitlines() if "," in line]
    # la ligne d'en-tête est enlevée seulement si le modèle l'a écrite
    got = [row for row in csv.reader(lines) if row[0].strip().lower() != "arrondissement"]
    truth = list(csv.reader(open("data/scanned_table_truth.csv", encoding="utf-8")))[1:]
    # on compare case par case
    cells = sum(len(row) for row in truth)
    correct = sum(
        g.strip() == t for got_row, truth_row in zip(got, truth) for g, t in zip(got_row, truth_row)
    )
    print(f"cells correct: {correct}/{cells}")
