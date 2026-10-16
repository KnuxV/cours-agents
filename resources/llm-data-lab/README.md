# llm-data-lab

Small experiments with the Unistra language models: what can an LLM do
with data? Each script is one idea, runs in under a minute, and prints
a score when we know the right answers.

The big idea: an LLM turns **unordered data** (text, names, scanned
pages) into **ordered data** (labels, codes, columns), with **no
training examples**, because it already knows the language. Without
an LLM, most of these tasks need hundreds of hand-labelled examples
and a trained model. With one, a prototype takes a paragraph.

## Get it

```bash
# WSL / Mac Terminal / Linux / Git Bash / Codespaces
cd ~
git clone https://github.com/KnuxV/cours-agents.git     # already cloned? instead: cd ~/cours-agents && git pull
cp -r ~/cours-agents/resources/llm-data-lab ~/llm-data-lab
cd ~/llm-data-lab
uv sync
export UNISTRA_API_KEY="sk-XXXX"   # your own key, from Session 3
```

If `git pull` refuses and mentions *stash*, you changed files inside the course repository: run `git stash -u` then `git pull` again (`git stash pop` brings your changes back).

`uv sync` creates `.venv/` and installs pycountry into it. No `sudo`, nothing outside the folder. Everything else uses the Python standard library.

No git, or the network is down? Download `llm-data-lab.zip` from the course site (session list, "LLMs for data"), unzip it in your home folder, then `cd ~/llm-data-lab` and `uv sync`.

Then run one experiment:

```bash
uv run python 03_relevance.py
```

or all of them (their output is saved in `results/`):

```bash
uv run python run_all.py
```

`results/` already holds the output of a run made while preparing
the class (qwen3, October 2026), so you can compare yours with it.

## The experiments

| Script | What it shows |
|---|---|
| `01_thesis_labels.py` | Label research abstracts: which SDG, which technology, which impact (3 chained steps) |
| `02_two_passes.py` | Pass 1 casts a wide net, pass 2 checks each label |
| `03_relevance.py` | Yes/no filter: is this paper about the labour market? |
| `04_normalise.py` | Messy country names to ISO codes: rules first, the LLM for the rest |
| `05_same_firm.py` | Is "Total SA" the same firm as "TotalEnergies SE"? |
| `06_summaries.py` | One-line summaries, checked by a second model (LLM as judge) |
| `07_extract.py` | A French job ad to a JSON record (contract, remote, salary, city) |
| `08_synthetic.py` | The model writes fake job ads with known labels, then finds the labels back |
| `09_text_to_table.py` | Six sentences with misspelled or nicknamed countries ("la perfide Albion") to a clean table of ISO codes and amounts |
| `10_read_table.py` | A scanned table (image) to CSV, checked cell by cell |
| `11_agent_nobel.py` | An agent with 4 tools searches Wikipedia for 3 Nobel economists |
| `12_your_turn.py` | **A template for your own classification**: change the labels, the question and the CSV |

The model is set in `llm.py` (`MODEL = "qwen3"`). The data is in `data/`.

## Try this

From easy to harder:

0. Open `12_your_turn.py` and classify something of your own: change `LABELS`, `QUESTION` and `DATA`.
1. Change `MODEL` in `llm.py` to `mistral-small` and run the same script. Same score?
2. In `03_relevance.py`, ask another question ("Is this paper about finance?") and change the labels in `data/titles.csv`.
3. Add your own messy names to `data/countries.csv` or firm pairs to `data/firm_pairs.csv`.
4. In `07_extract.py`, add a key to extract (for example `"experience_years"`).
5. Run `08_synthetic.py` with harder ads: ask the model to never write the contract type.
6. In `11_agent_nobel.py`, add a laureate, or give the agent a new tool (a plain Python function plus its description).

## Sources

The thesis abstracts in `data/thesis_abstracts.json` are simplified
paraphrases of published abstracts; the source of each is given in the
file. The scanned table, the wine exports, the job ads and the
central-bank sentences are invented.
