# 3.1 — Agent lab: six tasks against a dataset

Lesson: [Class plan — meet the agent](../sessions/practice-agents.md) · [All exercises](index.md)

**Goal:** get an agent to do real data work, and catch it when it is wrong. The point of every task below is the **check**, not the answer.

Work inside `~/agent-lab`, the git repository from class. Commit after every task that works. If the agent wrecks something: `git status`, then `git restore <file>`.

!!! tip "The rule for the whole page"
    A number you have not seen come out of a command is a rumour. Before you write down any result, ask yourself which line of code produced it — and if you cannot point at it, ask the agent to show you.

---

## A. Rebuild the room (10 min)

If you did not finish in class: create `~/agent-lab`, `git init`, generate `survey.csv` with an agent (or with the [fallback generator](../sessions/practice-agents.md#4-a-dataset-to-argue-about)), write the `AGENTS.md` from the class plan, and commit.

**Done when** `git log --oneline` shows at least one commit and `ls` shows `survey.csv`, `make_survey.py` and `AGENTS.md`.

## B. The column that moved (15 min)

Rename `income` to `annual_income` in `survey.csv` without telling the agent, then ask it for "average income by region".

Do it **twice**: once with `AGENTS.md` in place, once after renaming the file to `AGENTS.md.off` and running `/reload` and `/new`.

**Done when** you can write three sentences in `notes.md`: what the agent did in each case, which one you would trust, and which line of `AGENTS.md` made the difference. Restore the column afterwards (`git restore survey.csv`).

## C. Dirty data (25 min)

Make a deliberately messy copy of the data: `cp survey.csv survey_dirty.csv`, then by hand (or with `sed`) blank out a dozen `income` cells, put a few region names in capitals, and add two duplicated rows. Ask the agent to clean it into `out/survey_clean.csv`.

**Done when** this check passes — and **you** wrote the check, not the agent:

```python title="check_clean.py"
import pandas as pd
df = pd.read_csv("out/survey_clean.csv")
assert df.isna().sum().sum() == 0, "missing values remain"
assert df["region"].str.islower().all(), "region not normalised"
assert not df.duplicated().any(), "duplicates remain"
print(f"clean — {len(df)} rows")
```

Run it with `uv run --with pandas python check_clean.py`. Note how many rows you lost, and whether the agent told you it was dropping them.

## D. A regression you can grade (30 min)

Ask the agent to regress `log(income)` on years of education and `years_experience`, and to report the coefficients with their standard errors.

You have the ground truth: the data-generating process is written in the docstring of `make_survey.py` (0.11 per extra year of schooling, 0.020 per year of experience).

**Done when** you can say whether the estimated coefficients recover the true ones, and — this is the real exercise — whether the agent's *own* commentary on the results would have told you if they did not.

## E. The statistic that should not exist (20 min)

Ask, in a fresh session: *"What is the correlation between region and income?"*

`region` is a categorical variable with four values. A Pearson correlation with it is meaningless; the honest answers are group means, a plot, or an ANOVA.

**Done when** `notes.md` records what the agent produced, whether it objected, and the prompt that finally got it to say "that statistic does not apply here". If it never objects, that is your result — write that down.

## F. Your own skill, and a referee (40 min)

Write a skill of your own in `.agents/skills/<name>/SKILL.md` for a procedure you keep repeating (a chart style you always want, the checks before a regression, the shape of a results table). Six to twenty lines. The `description` line decides when it gets used — spend a minute on it.

Then open a second terminal, start a read-only agent (`pi --tools read,grep,find,ls`) with the [referee skill](../sessions/practice-agents.md#8-two-agents-opposite-jobs), and have it review the work of tasks C to E.

**Done when** the referee returns at least one `[FAIL]` line that you agree with, and you have decided whether to fix it or to argue with it.

---

## Hand in

`~/agent-lab` pushed to GitHub, containing: `AGENTS.md`, `.agents/skills/` with your own skill, the scripts, `out/`, and `notes.md` with your observations from B, D and E. Honest failure analysis scores better than a clean story.
