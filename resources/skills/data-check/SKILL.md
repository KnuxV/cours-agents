---
name: data-check
description: Careful analysis of a tabular data file (CSV, Excel, Parquet) — checking the columns before using them, and verifying every number that is reported. Use when asked to clean, describe, aggregate, plot or model a dataset, or to compute any statistic from a file.
---

# Data check

Numbers leave this session only if you have seen them come out of code you ran.

## Before touching the data

1. Print the shape, the column names, the dtypes and the first three rows. Never write a column name from memory or from the user's message — read it from the file.
2. Print the count of missing values per column, and the number of distinct values of every non-numeric column.
3. Say in one line what the unit of observation is (one row = one what?). If you cannot tell, ask.

## While analysing

- One question, one script, one output. Write the code to a file, run it, and show the real output. Do not describe what the code "would" print.
- Choose the statistic for the type of the variable. A correlation between a categorical variable and a numeric one is not a correlation — it is a group comparison. Means of identifiers are meaningless.
- Report the number of observations behind every statistic, after dropping missing values.
- Round money to two decimals and percentages to one, and always give the unit.

## Before answering

- Re-read your own claims and, for each number, name the line of code that produced it.
- State every step where you had to guess something the data did not say.
- If a result looks surprising, say so instead of explaining it away. A discrepancy is a finding, not a bug to be smoothed over.

## Never

- Never modify or delete the raw data file. Write derived files under `out/`.
- Never invent a column, a row count or a coefficient to complete a sentence.
