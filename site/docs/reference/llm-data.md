# Using an LLM on your own data

The [LLMs for data](../sessions/index.md#llms-for-data) class showed eleven small experiments: labelling abstracts, matching firm names, reading a scanned table, an agent searching Wikipedia. This page opens them up. It explains what each piece of code does, so that you can point the same recipe at your own CSV file instead of ours.

Everything quoted here comes from the class folder, `resources/llm-data-lab` in the course repository. The outputs quoted come from its `results/` folder, a real run on the Unistra models. If you do not have it yet:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
cd ~
git clone https://github.com/KnuxV/cours-agents.git     # already cloned? instead: cd ~/cours-agents && git pull
cp -r ~/cours-agents/resources/llm-data-lab ~/llm-data-lab
cd ~/llm-data-lab
uv sync
```

No git, or the network is down? Download [llm-data-lab.zip](../files/llm-data-lab.zip), unzip it in your home folder, then `cd ~/llm-data-lab` and `uv sync`.

The repository also contains a template script for classifying your own data. Read this page first: the template uses every idea below.

## 1. One API call, seen from Python

[Session 3](../sessions/s3.md) sent requests to the university's endpoint with `curl`. The file `llm.py` sends the very same request from Python. Nothing else in the repository talks to the model: every script goes through it.

A request is a block of JSON sent to `https://conversation.ia.unistra.fr/api/chat/completions`. It names the model, gives the conversation so far as a list of messages, and sets the temperature:

```json
{
  "model": "qwen3",
  "messages": [
    {"role": "user", "content": "Is this economics paper about the labour market? ... Answer with one word: yes or no."}
  ],
  "temperature": 0
}
```

Two headers travel with it: `Authorization: Bearer <your key>`, which says who you are, and `Content-Type: application/json`, which says the body is JSON. This is how `chat()` in `llm.py` builds them:

```python title="llm.py (excerpt)"
payload: dict = {"model": model, "messages": messages, "temperature": temperature}
request = urllib.request.Request(
    API_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {os.environ['UNISTRA_API_KEY']}",
        "Content-Type": "application/json",
    },
)
with urllib.request.urlopen(request, timeout=300) as response:
    return json.load(response)["choices"][0]["message"]
```

The answer is also JSON. The text you want sits at `choices[0].message.content`; next to it, `usage` counts the tokens you spent:

```json
{
  "choices": [
    {"message": {"role": "assistant", "content": "yes"}, "finish_reason": "stop"}
  ],
  "usage": {"prompt_tokens": 41, "completion_tokens": 1, "total_tokens": 42}
}
```

(The token counts above are illustrative.) Most scripts call `ask()` rather than `chat()`. It takes a prompt, builds the one-message list, calls `chat()`, and returns only the text. It also removes any `<think>…</think>` passage, where some models reason aloud before answering. The model is chosen in one place, `MODEL = "qwen3"` at the top of `llm.py`; the other IDs are `coder`, `gpt-oss`, `mistral-small`, `ministral` and `gemma`.

## 2. Your key, in your terminal

`llm.py` reads the key from the environment variable `UNISTRA_API_KEY`; the key is never written in the code. [Setup, section 5.2](../setup.md#52-store-it-as-an-environment-variable) stored it in your shell's startup file so that it survives a new window. To set it for the current window only, pick your shell:

=== "Linux / WSL / Git Bash / Codespaces (bash)"

    ```bash title="Linux terminal, Ubuntu window (WSL), Git Bash, or Codespace terminal"
    export UNISTRA_API_KEY="sk-XXXX"
    ```

=== "Mac (zsh)"

    ```bash title="Mac Terminal"
    export UNISTRA_API_KEY="sk-XXXX"
    ```

=== "fish"

    Some Linux users run the `fish` shell instead of `bash` (`echo $SHELL` ends in `fish`). Its syntax is different:

    ```fish title="Linux terminal running fish"
    set -x UNISTRA_API_KEY "sk-XXXX"
    ```

    `set -Ux UNISTRA_API_KEY "sk-XXXX"` keeps it for every future fish window as well.

Replace `sk-XXXX` with your own key, keeping the quotes. To check that the variable is there **without printing it** (a key that appears on screen ends up in screenshots and shared logs):

```bash title="Linux / Mac Terminal / WSL / Git Bash (bash or zsh)"
test -n "$UNISTRA_API_KEY" && echo "key is set" || echo "key is MISSING"
```

```fish title="Linux terminal running fish"
set -q UNISTRA_API_KEY && echo "key is set" || echo "key is MISSING"
```

Never paste the key into a script, a notebook or a file you commit. [Session 2, section 6.4](../sessions/s2.md#64-why-the-key-never-goes-in-the-code) explains what to do if that happens.

## 3. The recipe: a closed list of answers

Nearly every experiment follows the same five steps. They are what turns free text from the model into a column you can count.

1. **Decide the list of allowed answers** before writing the prompt: `yes`/`no`, four contract types, a list of codes.
2. **Write a short prompt** that gives the item, asks one question, and ends with the exact answer format.
3. **Set the temperature to 0**, so that the model picks its most likely answer instead of varying for the sake of it. `llm.py` does this by default.
4. **Check every answer against the list.** Anything else is marked as invalid, never silently kept.
5. **Score against rows you labelled yourself** before trusting it on the rest.

`03_relevance.py` is the whole recipe in under thirty lines. The prompt ends with the format:

```python title="03_relevance.py (excerpt)"
PROMPT = """Is this economics paper about the labour market (jobs, wages, employment, hiring)?
Title: {title}
Answer with one word: yes or no."""
```

and every answer is checked before it is scored:

```python title="03_relevance.py (excerpt)"
answer = ask(PROMPT.format(title=row["title"])).lower().strip(" .")
# liste fermée : toute autre réponse compte comme une erreur
if answer not in ("yes", "no"):
    answer = f"INVALID ({answer[:20]})"
ok = answer == row["about_labour_market"]
```

When the answer is a list of codes, a model does not always use the format you asked for. In our runs, `qwen3` sometimes answered with a JSON dictionary when asked for a comma-separated list. So `01_thesis_labels.py` does not parse the answer at all: it picks out every word that looks like a code and keeps only those on the allowed list.

```python title="01_thesis_labels.py (excerpt)"
def codes(text: str, allowed: list[str]) -> list[str]:
    """Keep only the codes from the allowed list, whatever the answer looks like."""
    found = re.findall(r"\b[A-Z][A-Z0-9_]*\b", text.upper())
    return [code for code in dict.fromkeys(found) if code in allowed]
```

`SDG3, SDG10`, `{"codes": ["SDG3", "SDG10"]}` and `The answer is SDG3 and SDG10.` all give `["SDG3", "SDG10"]`, and an invented code such as `SDG42` is dropped. `04_normalise.py` applies the same idea to country codes: the model's answer is accepted only if `pycountry` knows the code.

## 4. Getting a table out

A model can return several values at once if you ask for a format a program can read: JSON for one record, CSV for a table. Ask for it explicitly ("Answer with JSON only, using these keys: …", "Answer with the CSV only"), then parse it, then check it.

For JSON, `ask_json()` in `llm.py` tolerates the most common wrapping (the model surrounding its answer with a ```` ```json ```` fence or a sentence): it keeps the text between the first `[` or `{` and the last `]` or `}`, then parses it.

```python title="llm.py (excerpt)"
start = min((i for i in (text.find("["), text.find("{")) if i != -1), default=0)
end = max(text.rfind("]"), text.rfind("}")) + 1
return json.loads(text[start:end])
```

`07_extract.py` uses it to turn a French job ad into a record. A real output:

```text
{"job": "data analyst", "contract": "CDI", "remote": true, "salary_min": 42000, "city": "Strasbourg"}
```

Parsing is not checking. The script then compares each field with the expected value; in your own work, check at least that every key is present and that each value has the right type and range.

For CSV, the trap is the header. `09_text_to_table.py` asks for "a CSV table with the header country,exports_bn_eur". In our run the model returned the six data rows **without** the header line:

```text
USA,4.1
GBR,1.9
DEU,1.2
```

Code that blindly drops the first line would have lost the United States. The scripts therefore keep only lines that contain a comma, and remove the header only if it is actually there:

```python title="09_text_to_table.py (excerpt)"
rows = list(csv.reader(line for line in text.strip("`\n").splitlines() if "," in line))
# la ligne d'en-tête est enlevée seulement si le modèle l'a écrite
rows = [row for row in rows if row[0].strip().lower() != "country"]
```

Then count: the right number of rows, the right number of columns in each, numbers where numbers are expected.

## 5. Sending an image

An image travels inside the message, written out as text (base64 encoding) in a `data:` URL. `ask()` does this when you give it the path of a PNG or JPEG file:

```python title="llm.py (excerpt)"
if image:
    # une image voyage dans le message, encodée en texte (base64)
    kind = "png" if image.endswith(".png") else "jpeg"
    with open(image, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    content = [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/{kind};base64,{data}"}},
    ]
```

The message content is then a list of two parts, the text and the image, instead of a single string. Not every model reads images; `10_read_table.py` uses `gemma`:

```python title="10_read_table.py (excerpt)"
text = ask(PROMPT, model="gemma", image="data/scanned_table.png")
```

On our invented scan of an agricultural yearbook, `gemma` copied all 24 cells correctly (`cells correct: 24/24`). The script checks cell by cell against a truth file you typed yourself, the same way as section 4. Do that on a few pages of your own scans before running hundreds: a misread digit in a number looks perfectly plausible.

## 6. Agents: a loop, tools, and a step cap

In every script so far, *your* code decides what happens next. In `11_agent_nobel.py`, the model decides: it is given a task and four tools, and at each step it either asks for a tool call or answers. You met this loop with `curl` in [Session 3](../sessions/s3.md), where you played the harness by hand; here twenty lines of Python play it.

A **tool** is two things: an ordinary Python function, and a description of it that the model reads (its name, what it does, its parameters).

```python title="11_agent_nobel.py (excerpt)"
from datetime import date

def age_at(birth_date: str, event_date: str) -> str:
    """Age in whole years between two dates written YYYY-MM-DD."""
    birth = date.fromisoformat(birth_date)
    event = date.fromisoformat(event_date)
    before = (event.month, event.day) < (birth.month, birth.day)
    return str(event.year - birth.year - before)

TOOLS = [
    describe("wikipedia_search", "Search English Wikipedia; returns page titles.", query="search words"),
    describe("age_at", "Age in years between two dates.", birth_date="YYYY-MM-DD", event_date="YYYY-MM-DD"),
    ...
]
```

The model never runs anything. It only replies with the name of a tool and its arguments; the loop runs the function and sends the result back as a `tool` message. When the model replies without a tool call, it has decided to stop.

```python title="11_agent_nobel.py (excerpt)"
for step in range(1, MAX_STEPS + 1):
    reply = chat(messages, model=model, tools=TOOLS)
    messages.append(reply)
    calls = reply.get("tool_calls") or []
    if not calls:  # aucun outil demandé : le modèle a décidé d'arrêter
        break
    for call in calls:
        ...
        result = TOOLS_PY[name](**args)
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
```

Three habits matter:

- **Cap the steps.** `MAX_STEPS = 15`. Without a cap, a confused model can loop for as long as you pay for it.
- **Give the model arithmetic and lookups as tools.** The age is computed by `age_at`, not by the model. The model only turns "25 October 1972" into `1972-10-25`; `date.fromisoformat` refuses anything else, and the loop sends that error back to the model, which can try again. Strictly, the model would get most ages right on its own; `13_no_tool.py` asks it letter counts, multiplications and dates with no tool, and scores it against Python. "Most" is the problem: a tool is right every time.
- **Read the trace.** Every tool call is printed. Our run took five steps: three searches, three page reads, three `age_at` calls, three `save_row` calls (several per step), then `DONE`, and scored 3/3. A correct final table reached by a wrong path is luck; the trace is how you tell.

```text
[3] age_at({"birth_date": "1972-10-25", "event_date": "2019-10-14"}) -> '46'
[4] save_row({"name": "Esther Duflo", "phd_institution": "Massachusetts Institute of Technology", "age_at_prize": "46"}) -> 'saved Esther Duflo'
[5] model: DONE
```

Tool calling depends on the model. While preparing this class, `gpt-oss` answered the agent's request with an HTTP 400 error; the cause is unknown (a one-tool test in August had worked). `qwen3` and `mistral-small` are the ones to start with:

```bash title="Linux / Mac Terminal / WSL / Git Bash — inside llm-data-lab"
uv run python 11_agent_nobel.py mistral-small
```

## 7. Many rows: loop, save, rerun

On your own data the shape of the program is always the same: read the CSV, call the model once per row, write the answer next to the row. Three precautions turn a demo into something you can leave running:

- **Start with a small sample.** Run on 20 rows, read every answer, fix the prompt, then run on everything.
- **Save as you go.** Write each answer to the output file as soon as it arrives. If the script stops at row 3,000 (network, laptop lid, an error), you lose nothing, and a rerun skips the rows already done.
- **Be polite to the server.** Pause briefly between calls, and if the server answers HTTP 429 ("too many requests"), wait and retry. `11_agent_nobel.py` does exactly this with Wikipedia in its `wiki()` function. Whether the Unistra platform enforces a rate limit or a quota is UNVERIFIED: tests in August saw none, but the platform is shared with the whole university.

A sketch, built on `03_relevance.py`. Save it as `label_all.py` inside `llm-data-lab` and adapt the names in capitals:

```python title="label_all.py"
"""Label every row of a CSV, saving each answer as soon as it arrives."""
import csv
import os
import time

from llm import ask

PROMPT = """Is this economics paper about the labour market (jobs, wages, employment, hiring)?
Title: {title}
Answer with one word: yes or no."""
ALLOWED = ("yes", "no")
IN_FILE, OUT_FILE = "data/titles.csv", "labels.csv"
SAMPLE: int | None = 20  # set to None to run on every row


def ask_politely(prompt: str) -> str:
    """ask(), but wait and retry when the server says 'too many requests' (HTTP 429)."""
    for wait in (5, 30, 120):
        try:
            return ask(prompt)
        except RuntimeError as error:
            if "429" not in str(error):
                raise
            time.sleep(wait)
    return ask(prompt)


if __name__ == "__main__":
    rows = list(csv.DictReader(open(IN_FILE, encoding="utf-8")))[:SAMPLE]
    first_run = not os.path.exists(OUT_FILE)
    done: set[str] = set()
    if not first_run:
        done = {row["title"] for row in csv.DictReader(open(OUT_FILE, encoding="utf-8"))}
    with open(OUT_FILE, "a", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        if first_run:
            writer.writerow(["title", "answer"])
        for row in rows:
            if row["title"] in done:
                continue  # already answered in an earlier run
            answer = ask_politely(PROMPT.format(title=row["title"])).lower().strip(" .")
            writer.writerow([row["title"], answer if answer in ALLOWED else "INVALID"])
            out.flush()  # on disk now, not at the end
            time.sleep(0.5)
```

```bash title="Linux / Mac Terminal / WSL / Git Bash — inside llm-data-lab"
uv run python label_all.py
```

Run it twice: the second run should make no new calls. To start again from scratch, delete `labels.csv`.

## 8. Does it work? Measure it

A prompt that gives sensible answers on the five rows you looked at is not a result. Before using a column the model produced, measure it:

1. **Hand-label 50 to 100 rows**, chosen at random, *before* looking at the model's answers (otherwise you will tend to agree with it). Include the hard cases you know exist.
2. **Compute the accuracy** on those rows: the share of answers that match yours. For yes/no questions, also count the two kinds of error separately: a filter that says "no" to everything can still score well when most rows are "no".
3. **Read every disagreement.** Some are model errors; some show that your own category was ambiguous. Both are worth knowing, and the second kind is fixed in the prompt, not in the model.
4. **Rerun after every change** of prompt or model (`MODEL` in `llm.py`), on the same labelled rows, and compare.

The class experiments use 3 to 21 rows each. Scores such as `accuracy: 10/10` show that the method can work, not how often it fails: with ten rows, one error in fifty would usually go unseen.

Using a second model to check the first, as `06_summaries.py` does with `mistral-small` reading `qwen3`'s summaries, is called **LLM as judge**. It is useful for things you cannot score with a list, such as whether a summary is faithful. But the judge is itself a measurement, with its own errors: in our run it answered `OK` to all three summaries. Read a sample of its verdicts yourself, exactly as in step 3, before trusting it on thousands of rows.

Finally, keep a record of what produced each column: the model ID, the prompt, the date. The same model name can change behind the scenes on a shared platform; the course's research notes report fallback chains in the platform's error messages that can route a request to the smaller `ministral` model, and whether this happens silently for API keys is UNVERIFIED. Your hand-labelled rows are how you would notice.
