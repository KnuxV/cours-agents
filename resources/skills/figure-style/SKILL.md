---
name: figure-style
description: House style for charts and figures made with matplotlib — what to plot, how to label it, and what to check before saving. Use when asked to plot, chart, visualise or produce a figure from data.
---

# Figure style

A figure is an argument. If a reader cannot say what it claims within five seconds, it has failed.

## Before plotting

State in one line what the figure is meant to show, and check the variable types support it: a category goes on a discrete axis, a continuous variable on a continuous one, time on the x axis.

## The rules

- **Label every axis**, with the unit in parentheses: `Annual income (€)`, `Experience (years)`.
- **Say n.** Put the number of observations in the title or a corner note, after dropping missing values.
- Sort categorical bars by value, not alphabetically, unless the order means something.
- Start a bar chart's axis at zero. A line chart need not.
- No legend when one line is enough; label the line directly instead.
- Default to a single colour. Use a second only when it encodes something, and never encode with colour alone.
- Thousands separators on tick labels; money to two decimals, shares to one.

## Saving

Write to `out/<name>.png` at `dpi=150` with `bbox_inches="tight"`. Never overwrite a figure from a different question — give it a new name.

## After saving

Report the file path, the n behind the figure, and one sentence stating what the figure shows. If the pattern is surprising, say that it is surprising rather than explaining it away.
