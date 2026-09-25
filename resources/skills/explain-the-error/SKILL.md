---
name: explain-the-error
description: Reading a Python traceback or a shell error message with the person, instead of silently fixing it. Use when the user pastes an error, a traceback, or a command that failed and wants to understand it.
---

# Explain the error

The user pasted an error because they want to be able to read the next one alone.

## Each time

1. **Name the last line first.** The exception type and its message are the answer; everything above is the route taken to get there.
2. **Find the user's own line.** In a traceback, the lowest frame inside their files is where to look — frames inside libraries usually mean the wrong value arrived, not that the library is broken.
3. **Translate the message into plain words**, term by term: what `NoneType`, `KeyError`, `command not found`, `Permission denied` or `ModuleNotFoundError` is actually saying about the state of the machine.
4. **Say the one-sentence cause**, then the smallest fix — as a command or a line, with the reason for each part.
5. **Give the check** that proves it is fixed, and have the user run it.

## Shape

Six lines at most. No apology, no restating the whole traceback, no lecture on best practice. If the cause is genuinely ambiguous, name the two candidates and the one command that tells them apart.
