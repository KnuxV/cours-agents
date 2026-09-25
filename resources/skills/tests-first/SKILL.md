---
name: tests-first
description: Writing a test before writing or changing code, and running it. Use when asked to add a function, fix a bug, refactor, or when a change needs proof that it works — in Python with pytest.
---

# Tests first

A change is not finished because it looks right. It is finished when something that failed now passes.

## Order of work

1. **Write the assertion first.** Before touching the code, write the smallest test that fails for the reason the user described. Show it failing — paste the real `pytest` output, including the error line.
2. **Write the least code that makes it pass.** No extra features, no speculative options.
3. **Run the whole suite**, not just the new test: `uv run pytest -q`. Paste the real output. A test you have not run is a claim, not a test.
4. **Then, and only then**, refactor — with the suite green before and after.

## Writing the test

- One behaviour per test, named for the behaviour: `test_rejects_negative_length`, not `test_2`.
- Arrange, act, assert — in that order, with a blank line between them.
- Prefer exact values to loose checks. `assert result == 7`, not `assert result > 0`.
- For a bug, the test reproduces the bug report, using the user's own numbers where they gave any.
- Cover the edges the user did not mention: empty input, zero, a negative, a duplicate, the wrong type.

## Never

- Never change a test so that failing code passes. If a test is wrong, say so out loud and explain why before touching it.
- Never report a suite as passing without the output that shows it.
- Never add a test that asserts nothing, or that only checks the code ran without raising.
