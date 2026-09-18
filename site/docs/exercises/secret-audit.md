# 2.4 — Secret hygiene audit

Lesson: [Session 2 — Python tooling](../sessions/s2.md) · [All exercises](index.md)

**Goal:** find a leaked secret in a repository's history and say how it should have been handled.

You are given a repository in which someone committed an API key inside a script, then "removed" it in a later commit. Produce a short text file `audit.md` in your own course repo answering:

1. In which commit did the key appear, and in which was it "removed"? (Hint: `git log -p`, `git log -S "sk-"`.)
2. Is the key still recoverable from the repository? Show the command that prints it.
3. Rewrite the offending line the right way (environment variable + `os.environ.get` + a clear failure message), and give the `.gitignore` line that protects a `.env` file.
4. What must the owner do *first* — before touching git at all?

TODO(verify): the starter repository will be published with the exercises of Task 03.

??? note "Solution sketch"
    `git log -S "sk-" --oneline` lists the commits that added or removed the string; `git show <first-hash>` prints the key — it is fully recoverable by anyone with the repository, so the answer to 4 is *regenerate the key* ([setup 5.1](../setup.md#51-generate-the-key)). The correct line is the one in [S2 §6.2](../sessions/s2.md#62-reading-them-from-python); the `.gitignore` line is `.env`.
