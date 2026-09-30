# T.2 — Test first: `parse_number`

Lesson: [Testing your code with pytest](../reference/testing.md) · class plan: [Testing with pytest](../sessions/testing.md) · [All exercises](index.md)

**Goal:** build a small function by writing each test *before* the code that makes it pass, and decide — in writing — when the function is good enough.

**Time:** 15 minutes in class for steps 1–4; finish at home.

## The function

Numbers written the French way do not convert with `float()`:

```pycon
>>> float("1 234,56")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: could not convert string to float: '1 234,56'
```

You will write `parse_number(text)` in `exo2-tdd/french_numbers.py`, so that `parse_number("1 234,56")` returns `1234.56`. You need it as soon as you read a CSV file exported from a French spreadsheet.

## The method: red, green, clean

This way of working is called **test-driven development** (TDD). Repeat, one test at a time:

1. **Red** — write one test. Run it and watch it fail. A test you have never seen fail may not be testing anything.
2. **Green** — write the *least* code that makes it pass. Not the code for the next step: only this one.
3. **Clean** — tidy the code if it needs it. Run the tests again: still green.

Then the next test. Do not write all the tests at once, and do not write the whole function at once: the exercise is the rhythm.

## Start

If you do not have the lab yet, follow [Before the class starts](../sessions/testing.md#before-the-class-starts-get-the-code).

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
cd ~/testing-lab/exo2-tdd
uv run pytest
```

The first test is already written, and it fails: `parse_number` only raises `NotImplementedError`. That is step 1's red. Make it green, then carry on.

## The steps

Each step is one test (or one `parametrize`d test) added to `tests/test_french_numbers.py`.

| Step | Test | Notes |
|---|---|---|
| 1 | `"12"` → `12.0` | already written |
| 2 | `"12,5"` → `12.5` | the decimal comma |
| 3 | `"1 234,56"` → `1234.56` | the space between thousands. Compare floats with `pytest.approx` |
| 3b | `"1 234,56"` → `1234.56` | French spreadsheets and word processors often put a **no-break space** (` `) or a **narrow no-break space** (` `) there instead of an ordinary one. They look the same on screen |
| 4 | `"-3,2"` → `-3.2`, `"  7 "` → `7.0` | a sign, and spaces around the number. Use `@pytest.mark.parametrize` |
| 5 | `""`, `"abc"` → `ValueError` | use `with pytest.raises(ValueError):`. Write the test first — you may find it already passes. Why? |
| 6 | `"1.234,56"`? `"1,234.56"`? | see below |

## Step 6: when is it good enough?

`"1.234,56"` is how German writes one thousand two hundred and thirty-four and a bit; `"1,234.56"` is how English writes the same number. What should `parse_number` do with them: accept them, refuse them, guess?

There is no right answer, but there must be *an* answer, written as a test. Decide, write the test, make it pass. Then ask the same question about `"12,5 %"` and `"1 234,56 €"`.

!!! note "What 'good enough' means"
    Good enough is: the cases your data actually contains, plus the cases that must be refused. Your tests are the written specification of the function. Every decision you made is in them, and it is checked again every time you run `uv run pytest`.

## When you are done

Every step has at least one test, all tests pass, and you can explain your step 6 decision in one sentence.

## Solution

The solution — the tests in the order they were written, and a ten-line function — is on the `solutions` branch of the course repository, in `resources/testing-lab/exo2-tdd/`:

```bash title="WSL / Mac Terminal / Linux / Git Bash / Codespaces"
git -C ~/cours-agents fetch
git -C ~/cours-agents switch solutions
```

It chose to refuse both foreign formats. Come back with `git -C ~/cours-agents switch main`.
