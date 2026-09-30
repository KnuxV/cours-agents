# T.1 — Fix the code

Lesson: [Testing your code with pytest](../reference/testing.md) · class plan: [Testing with pytest](../sessions/testing.md) · [All exercises](index.md)

**Goal:** read pytest's failure messages until they tell you where the bug is, fix the code, and discover that a green test suite only covers what someone thought of testing.

**Time:** 15 minutes, plus 10 for the bonus.

## The setup

`exo1-fix/text_stats.py` holds six small functions for text statistics: counting words, normalizing a string, the type–token ratio, the most frequent words, the change between two ratings, the mean sentence length. `exo1-fix/tests/test_text_stats.py` says what each one should do. **The tests are right. The code is not.**

If you do not have the lab yet, follow [Before the class starts](../sessions/testing.md#before-the-class-starts-get-the-code).

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
cd ~/testing-lab/exo1-fix
uv run pytest
```

```text
========================= 8 failed, 3 passed in 0.03s ==========================
```

## What to do

1. Fix `text_stats.py` until `uv run pytest` shows no failure. **Do not change the tests.**
2. Work one bug at a time. `uv run pytest -x` stops at the first failure; `uv run pytest --lf` reruns only the tests that failed last time.
3. For each failure, read three things before you open the code: the **name** of the test, the **line** of the `assert`, and the two **values** pytest prints — what the code returned on the left, what the test expected on the right.

There are eight failing tests but only five bugs: some bugs break two tests.

!!! tip "Hints, if you are stuck"
    - `"".split(" ")` and `"".split()` do not return the same thing. Try both in `uv run python`.
    - `sorted()` sorts from smallest to largest unless you ask otherwise.
    - A list slice `[:n]` already stops before index `n`.
    - The rating went **from** `before` **to** `after`.

## Bonus: the bug no test catches

When everything is green, one function is still wrong. Try it:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces — inside exo1-fix"
uv run python -c "from text_stats import mean_sentence_length; print(mean_sentence_length('Ça va ? Oui. Très bien !'))"
```

Three sentences — « Ça va », « Oui », « Très bien » — of 2, 1 and 2 words: the answer should be 5 / 3, about `1.67`. What does it print, and why did the test suite not notice?

1. Write the test that shows the bug, in `tests/test_text_stats.py`. Run it: it must fail. (Use `pytest.approx` — `5 / 3` is not a round number.)
2. Fix `mean_sentence_length`. Hint: `re.split(r"[.!?]", text)` splits on any of the three characters.
3. Run the whole suite: everything green, including your new test.

## When you are done

`uv run pytest` shows **12 passed** — the eleven original tests and yours — and you can say, for each of the six bugs, which test found it.

## Solution

The solution is on the `solutions` branch of the course repository, in `resources/testing-lab/exo1-fix/`:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
git -C ~/cours-agents fetch
git -C ~/cours-agents switch solutions
```

Come back to the lessons with `git -C ~/cours-agents switch main`.
