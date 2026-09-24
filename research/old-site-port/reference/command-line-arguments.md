<!--
PORTED FROM last year's material (KnuxV/advanced_programming_python):
  lessons/07-arguments/071-argv_argparse.md — what a CLI is, anatomy of a command, sys.argv, its limits,
      argparse basics, actions, types, choices, mutually exclusive groups, argument groups
  lessons/07-arguments/072-advanced.md      — subcommands, config files + env vars + flags precedence,
      verbosity levels, dry-run, interactive confirmation, output formats, exit codes, "structure for testing",
      the quick-reference tables.  (Note: that file also contains a verbatim duplicate of 071 from its
      line ~954 on; only the first half is unique.)
  KnuxV/slides_cours_git "Part 11 - arguments.md" — the terser classroom version of the same material
  exercices/09-password_generator/instructions.md — the sys.argv-then-argparse two-part exercise and the
      xkcd 936 framing (see INVENTORY.md: merged into the existing exercise 2.3 rather than re-ported)

PROPOSED DESTINATION: site/docs/reference/command-line-arguments.md
  Nav (site/mkdocs.yml, under "Reference"):
      - Python and quality:
          - Command-line arguments, in depth: reference/command-line-arguments.md
  Row for site/docs/reference/index.md, section "Python and quality":
      | [Command-line arguments, in depth](command-line-arguments.md) | `sys.argv`, the whole of `argparse`, subcommands, exit codes, and how to test a command line | [Session 2 — §5](../sessions/s2.md#5-from-a-notebook-cell-to-a-script-with-arguments) |
  Inbound link to add later: sessions/s2.md §5.3 already links last year's lesson on GitHub —
  repoint that sentence at this page.

REWRITTEN, not pasted: `python script.py` → `uv run script.py`; every command has a
"where to run it" title; the examples are new (a word counter and a note keeper) because last
year's `convert image.jpg` and Flask examples assume tools the room does not have.
Every output block below was produced on this machine (uv 0.12.10, CPython 3.12.14).
-->

# Command-line arguments, in depth

Introduced in [Session 2, §5](../sessions/s2.md#5-from-a-notebook-cell-to-a-script-with-arguments), which gets you as far as one positional argument and two options. This page is the rest: everything `argparse` does, subcommands, exit codes, and how to write a command line a test can call.

Why it is worth more than it looks. A notebook has no interface: to change a parameter you edit a cell. A script with arguments has one, and an interface is what makes code usable by things that are not you sitting at a keyboard — a loop over 200 files, a scheduler at 3 a.m., a colleague who does not open notebooks, a CI job, and an agent whose only way to act on the world is to run commands. `--help` is the documentation you did not have to write, and exit codes are how the caller learns whether it worked.

## 1. Anatomy of a command

```text
uv run report.py sales.csv --top 3 --product tea -v
   │        │         │        │  │      │       │
   │        │         │        │  │      │       └── flag: present or absent, no value
   │        │         │        │  └──────┴────────── option and its value
   │        │         │        └────────────────────  option name (long form)
   │        │         └─────────────────────────────  positional argument
   │        └───────────────────────────────────────  the program being run
   └────────────────────────────────────────────────  how we run it in this course
```

Vocabulary, because the words are used loosely everywhere else:

- A **positional argument** is identified by *where* it is. Usually required. `sales.csv` above.
- An **option** starts with `-` or `--` and takes a value: `--top 3`.
- A **flag** starts with `-` or `--` and takes no value; it is on or off: `-v`, `--dry-run`.

One dash introduces the short form (one letter, `-v`); two dashes the long form (`--verbose`). Most tools offer both for the same thing. Conventions worth respecting because everyone already knows them:

| Flag | Means |
|---|---|
| `-h`, `--help` | Show usage and exit |
| `-v`, `--verbose` | Say more about what you are doing |
| `-q`, `--quiet` | Say less |
| `-o`, `--output` | Where to write the result |
| `-n`, `--dry-run` | Say what you *would* do, change nothing |
| `-f`, `--force` | Skip the confirmation |
| `-r`, `--recursive` | Go into subfolders too |

You have been using these for two sessions: `git commit -m`, `ls -a`, `curl -o`, `uv run --with`.

## 2. `sys.argv`: the raw material

Python hands every script the words it was called with, as a list of strings:

```python title="show_args.py"
import sys

print("argv[0] is", sys.argv[0])
print("the rest is", sys.argv[1:])
print("types:", [type(a).__name__ for a in sys.argv[1:]])
```

```bash title="Ubuntu window (WSL), Terminal (Mac), Linux terminal, Git Bash or Codespace terminal"
uv run show_args.py hello 42 --top 3
```

```text
argv[0] is show_args.py
the rest is ['hello', '42', '--top', '3']
types: ['str', 'str', 'str', 'str']
```

Three facts to take away. `sys.argv[0]` is the script itself, so your arguments start at index 1. **Everything is a string** — `42` arrived as `'42'`. And `argparse` has not been invented yet as far as this list is concerned: `--top` and `3` are two unrelated words.

For a script with one obvious argument, that is enough:

```python title="total.py"
import sys

numbers = [float(a) for a in sys.argv[1:]]
print(sum(numbers))
```

```bash title="Any terminal"
uv run total.py 1 2 3.5
uv run total.py 1 two
```

```text
6.5
```

```text
Traceback (most recent call last):
  File "/home/you/total.py", line 3, in <module>
    numbers = [float(a) for a in sys.argv[1:]]
               ^^^^^^^^
ValueError: could not convert string to float: 'two'
```

And there is the problem. A user typo produced a traceback: eleven lines about the internals of your program, no statement of what was expected, and an exit code of 1 that says only "something raised". Everything you would add by hand to fix that — checking the count, converting types, printing a usage line, handling `-v`, supporting `--output x` — is a hundred lines of string manipulation that every script would reinvent slightly differently.

That is the entire argument for `argparse`. Use `sys.argv` when the script takes zero or one obvious argument and you are the only user. Use `argparse` the moment there is a second one.

## 3. `argparse` in four ideas

```python title="the skeleton"
import argparse

parser = argparse.ArgumentParser(description="What this program does.")   # 1
parser.add_argument("filename", help="file to process")                   # 2
parser.add_argument("--top", type=int, default=3, help="how many rows")   # 2
args = parser.parse_args()                                                # 3
print(args.filename, args.top)                                            # 4
```

1. A **parser** describes what the command accepts.
2. Each `add_argument` adds one. No dash → positional; dashes → option or flag.
3. `parse_args()` reads the real command line, validates it, and on any problem prints a usage message and **exits**.
4. The result is an object whose attributes are your old notebook constants. `args.top` is an `int` because you said `type=int`.

Three things arrive free and are the reason this is not worth writing yourself: `--help`, type validation, and a clean exit code on misuse.

## 4. A worked example with everything in it

```python title="wordcount.py"
"""Count things in a text file. Usage: uv run wordcount.py FILE [options]"""
import argparse
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """Describe the command line. Kept separate so tests can inspect it."""
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Count lines, words or characters in a text file.",
        epilog="Example: uv run wordcount.py notes.txt --unit words --top 3",
    )
    parser.add_argument("path", type=Path, help="the text file to read")
    parser.add_argument(
        "--unit",
        choices=["lines", "words", "chars"],
        default="words",
        help="what to count (default: %(default)s)",
    )
    parser.add_argument(
        "--top", type=int, metavar="N", help="also show the N most frequent words"
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="WORD",
        help="a word to leave out; repeat the option for several words",
    )
    noise = parser.add_mutually_exclusive_group()
    noise.add_argument(
        "-v", "--verbose", action="count", default=0, help="say more (-vv says even more)"
    )
    noise.add_argument("-q", "--quiet", action="store_true", help="print only the number")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command. Returns the process exit code."""
    args = build_parser().parse_args(argv)

    if not args.path.exists():
        print(f"wordcount: no such file: {args.path}", file=sys.stderr)
        return 1

    text = args.path.read_text(encoding="utf-8")
    words = [w for w in text.split() if w.lower() not in {i.lower() for i in args.ignore}]
    counts = {"lines": len(text.splitlines()), "words": len(words), "chars": len(text)}

    if args.verbose:
        print(f"reading {args.path} ({len(text)} characters)", file=sys.stderr)
    if args.verbose > 1:
        print(f"ignoring {args.ignore or 'nothing'}", file=sys.stderr)

    if args.quiet:
        print(counts[args.unit])
    else:
        print(f"{counts[args.unit]} {args.unit}")

    if args.top:
        frequency: dict[str, int] = {}
        for word in words:
            frequency[word.lower()] = frequency.get(word.lower(), 0) + 1
        for word, n in sorted(frequency.items(), key=lambda pair: -pair[1])[: args.top]:
            print(f"{n:>4}  {word}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Make a file to count:

```bash title="Any terminal"
printf 'the quick brown fox\njumps over the lazy dog\nthe dog sleeps\n' > notes.txt
```

### 4.1 What it does

```bash title="Any terminal"
uv run wordcount.py notes.txt
uv run wordcount.py notes.txt --unit lines
uv run wordcount.py notes.txt --top 3
uv run wordcount.py notes.txt --top 3 --ignore the --ignore dog
uv run wordcount.py notes.txt -q
uv run wordcount.py notes.txt -vv
```

```text
12 words
```
```text
3 lines
```
```text
12 words
   3  the
   2  dog
   1  quick
```
```text
7 words
   1  quick
   1  brown
   1  fox
```
```text
12
```
```text
reading notes.txt (59 characters)
ignoring nothing
12 words
```

### 4.2 The help you did not write

```bash title="Any terminal"
uv run wordcount.py --help
```

```text
usage: wordcount [-h] [--unit {lines,words,chars}] [--top N] [--ignore WORD]
                 [-v | -q]
                 path

Count lines, words or characters in a text file.

positional arguments:
  path                  the text file to read

options:
  -h, --help            show this help message and exit
  --unit {lines,words,chars}
                        what to count (default: words)
  --top N               also show the N most frequent words
  --ignore WORD         a word to leave out; repeat the option for several
                        words
  -v, --verbose         say more (-vv says even more)
  -q, --quiet           print only the number

Example: uv run wordcount.py notes.txt --unit words --top 3
```

Everything in there came from arguments you already had to write: `prog`, `description`, `epilog`, each `help=`, each `choices`, each `metavar`. `%(default)s` inside a help string is substituted with the actual default, so the help cannot drift from the code. `[-v | -q]` on the usage line is the mutually exclusive group announcing itself.

### 4.3 The validation you did not write

```bash title="Any terminal"
uv run wordcount.py notes.txt --unit sentences
uv run wordcount.py notes.txt -q -v
```

```text
usage: wordcount [-h] [--unit {lines,words,chars}] [--top N] [--ignore WORD]
                 [-v | -q]
                 path
wordcount: error: argument --unit: invalid choice: 'sentences' (choose from lines, words, chars)
```

```text
usage: wordcount [-h] [--unit {lines,words,chars}] [--top N] [--ignore WORD]
                 [-v | -q]
                 path
wordcount: error: argument -v/--verbose: not allowed with argument -q/--quiet
```

Both exit with code **2**, print to standard error, and produce no traceback. Compare with the eleven-line `ValueError` of section 2. Nothing in `main()` checks any of this.

## 5. The `add_argument` options worth knowing

**`action`** — what happens when the argument appears:

```python
parser.add_argument("--verbose", action="store_true")         # flag → True/False
parser.add_argument("--no-cache", action="store_false", dest="cache")  # flag → False
parser.add_argument("--include", action="append", default=[])  # repeatable → list
parser.add_argument("-v", action="count", default=0)           # -vvv → 3
parser.add_argument("--version", action="version", version="1.0")
```

`store_true` and `append` cover most needs; `count` gives you verbosity levels for free.

**`type`** — any callable that takes a string and returns something, or raises:

```python
parser.add_argument("--top", type=int)
parser.add_argument("--rate", type=float)
parser.add_argument("path", type=Path)       # pathlib.Path — then use path.exists()


def positive_int(value: str) -> int:
    """An int that must be > 0 — a custom type, for argparse to call."""
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return number


parser.add_argument("--n", type=positive_int)
```

Raising `argparse.ArgumentTypeError` gives the same clean `error:` line as a built-in type. This is the place to put validation: it happens before your code runs, and the message is about the *user's* input rather than your internals.

**`choices`** — a closed set, checked for you and printed in `--help`.

**`default`** — the value when the option is absent. Choose defaults that make the bare command do the most useful thing.

**`required=True`** on an option — legal, and occasionally right (a `--config` with no sensible default), but if it is always required, consider making it positional.

**`nargs`** — how many values:

```python
parser.add_argument("files", nargs="+")     # one or more  → a list
parser.add_argument("files", nargs="*")     # zero or more → a list, possibly empty
parser.add_argument("--out", nargs="?", default="-")  # optional value
```

**`metavar`** and **`dest`** — cosmetics with teeth. `metavar="N"` is the placeholder shown in the help; `dest="output_file"` is the attribute name on `args`. Long options with a dash become underscores automatically: `--dry-run` is `args.dry_run`.

**Groups** — `parser.add_argument_group("processing options")` only changes how `--help` is laid out; `parser.add_mutually_exclusive_group()` changes what is legal.

## 6. Subcommands: the shape of `git` and `uv`

Once a tool does several different things, options stop scaling: `--add`, `--list`, `--delete` with different required arguments each. The answer is a **subcommand**, which is a second parser:

```python title="notes.py"
"""A two-subcommand tool, in the shape of git or uv. Usage: uv run notes.py add|list ..."""
import argparse
from pathlib import Path

STORE = Path("notes.txt")


def cmd_add(args: argparse.Namespace) -> int:
    """Append one note to the store."""
    with STORE.open("a", encoding="utf-8") as handle:
        handle.write(args.text + "\n")
    print(f"added: {args.text}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """Print the stored notes, newest last."""
    if not STORE.exists():
        print("no notes yet")
        return 0
    lines = STORE.read_text(encoding="utf-8").splitlines()
    for number, line in enumerate(lines[-args.limit :], start=1):
        print(f"{number}. {line}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="notes", description="A tiny note keeper.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    add = subcommands.add_parser("add", help="store a new note")
    add.add_argument("text", help="the note itself")
    add.set_defaults(handler=cmd_add)

    listing = subcommands.add_parser("list", help="show stored notes")
    listing.add_argument("--limit", type=int, default=5, help="how many to show (default: %(default)s)")
    listing.set_defaults(handler=cmd_list)

    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

```bash title="Any terminal"
uv run notes.py --help
uv run notes.py add "read SPEC.md"
uv run notes.py add "run pytest"
uv run notes.py list --limit 1
uv run notes.py list
uv run notes.py
uv run notes.py list --help
```

```text
usage: notes [-h] {add,list} ...

A tiny note keeper.

positional arguments:
  {add,list}
    add       store a new note
    list      show stored notes

options:
  -h, --help  show this help message and exit
```
```text
added: read SPEC.md
```
```text
added: run pytest
```
```text
1. run pytest
```
```text
1. read SPEC.md
2. run pytest
```
```text
usage: notes [-h] {add,list} ...
notes: error: the following arguments are required: command
```
```text
usage: notes list [-h] [--limit LIMIT]

options:
  -h, --help     show this help message and exit
  --limit LIMIT  how many to show (default: 5)
```

Each subcommand has its own arguments and its own `--help`. The pattern that keeps `main()` short is `set_defaults(handler=...)`: each subparser remembers which function implements it, and `main` just calls `args.handler(args)`. One function per subcommand, each returning an exit code — and each testable on its own.

## 7. Three patterns you will actually reuse

**Verbosity, with `count`.** `-v` prints progress, `-vv` prints detail, neither pollutes the output you might be piping somewhere. Progress messages go to **standard error** (`file=sys.stderr`), results to standard output — that is how `uv run wordcount.py notes.txt -vv > out.txt` can put `12 words` in the file and still show you the progress on screen.

**`--dry-run`, the flag that saves your data.** For anything that deletes, overwrites or uploads:

```python
parser.add_argument("-n", "--dry-run", action="store_true",
                    help="show what would happen, change nothing")
...
for path in doomed:
    if args.dry_run:
        print(f"would delete {path}")
    else:
        path.unlink()
```

Write the dry-run branch *first*. This is also the single most useful thing to ask of a script an agent wrote for you: run it with `--dry-run`, read the list, then run it for real.

**Where a setting comes from.** A mature tool reads the same setting from several places, with a fixed precedence — **command line beats environment variable beats configuration file beats built-in default**:

```python
import os

parser.add_argument(
    "--model",
    default=os.environ.get("COURSE_MODEL", "coder"),
    help="model to use (default: $COURSE_MODEL, or coder)",
)
```

You already live with this: your `UNISTRA_API_KEY` is an environment variable ([Session 2, §6](../sessions/s2.md#6-environment-variables-where-secrets-live)), and in Session 4 `pi` takes `--model` on the command line while reading the rest from `~/.pi/agent/models.json`. Secrets belong in the environment and **never** as a command-line argument: anything you type is in your shell history and visible in the process list.

## 8. A `main()` that can be tested

Look again at the two examples above: both define `main(argv: list[str] | None = None)` and both pass `argv` to `parse_args`. That one habit is what makes a command line testable.

`parse_args(None)` reads the real `sys.argv`; `parse_args(["notes.txt", "--top", "2"])` reads the list you give it. So a test can call your program the way a user would, without a subprocess:

```python title="tests/test_wordcount.py"
from wordcount import main


def test_counts_words(tmp_path, capsys):
    notes = tmp_path / "notes.txt"
    notes.write_text("one two three\n", encoding="utf-8")
    exit_code = main([str(notes)])
    assert exit_code == 0
    assert capsys.readouterr().out == "3 words\n"


def test_missing_file_returns_1(capsys):
    assert main(["nowhere.txt"]) == 1
    assert "no such file" in capsys.readouterr().err
```

```bash title="Any terminal, inside the project"
uv run --with pytest pytest -q
```

```text
..                                                                       [100%]
2 passed in 0.01s
```

(`tmp_path` and `capsys` are explained in [testing, §7](testing.md#7-fixtures-the-setup-written-once); an empty `conftest.py` at the project root is what lets `tests/` import `wordcount`.)

Two rules follow. **`main` returns, it does not `sys.exit()`** — returning an integer is testable, exiting kills the test runner. And **`main` prints nothing it cannot be asked to be quiet about** — the `-q` flag exists so that another program can consume your output.

## 9. Exit codes

Every process ends with a number. `0` means success; anything else means failure. Your shell keeps the last one in `$?`:

```bash title="Any terminal"
uv run wordcount.py absent.txt
echo $?
```

```text
wordcount: no such file: absent.txt
```
```text
1
```

The convention this page follows, and the one `git`, `grep` and `uv` follow:

| Code | Meaning |
|---|---|
| `0` | It worked |
| `1` | It ran and failed — file missing, no data, the thing you asked for is not there |
| `2` | You called it wrongly — `argparse` produces this one by itself |

Why it matters even though you never look at it: `command-a && command-b` only runs the second if the first returned 0; a CI job is red when any step returns non-zero; and an agent decides what to do next from that number plus the text on standard error. A script that prints `ERROR: something went wrong` and exits 0 is a script that lies to everything downstream of it.

## 10. When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| `error: the following arguments are required: path` | A positional argument is missing | It is required by definition; give it, or add `nargs="?"` and a default |
| `error: unrecognized arguments: --to 3` | Typo in an option name | `--help` lists the real ones |
| `error: argument --top: invalid int value: 'two'` | `type=int` did its job | Pass a number |
| `AttributeError: 'Namespace' object has no attribute 'dry-run'` | Dashes become underscores | `args.dry_run` |
| A value is a string when you wanted a number | No `type=` on that argument | Add `type=int` / `type=float` |
| Arguments with spaces are split | The shell splits on spaces before Python sees anything | Quote them: `--product "green tea"` |
| `--ignore` only keeps the last value | Default `action` overwrites | `action="append"` |
| Your script eats an option meant for `uv` | Everything after the script name belongs to the script | `uv run script.py --help` is your help; `uv run --help` is uv's |
| A filename starting with `-` is read as an option | Ambiguous by design | `uv run script.py -- -weird-name.csv` (`--` ends the options) |
| The script cannot be tested without a subprocess | `main()` reads `sys.argv` directly | Give `main` an `argv` parameter (§8) |

## 11. Cheat sheet

| Line | Effect |
|---|---|
| `p = argparse.ArgumentParser(description=..., epilog=...)` | Create the parser; both strings appear in `--help` |
| `p.add_argument("path")` | Required positional |
| `p.add_argument("path", nargs="+")` | One or more positionals, as a list |
| `p.add_argument("--top", type=int, default=3)` | Option with a type and a default |
| `p.add_argument("--csv", action="store_true")` | Flag, `False` unless given |
| `p.add_argument("-v", action="count", default=0)` | `-vvv` → `3` |
| `p.add_argument("--inc", action="append", default=[])` | Repeatable option → list |
| `p.add_argument("--fmt", choices=["json", "csv"])` | Closed set, validated |
| `p.add_argument("--n", type=positive_int)` | Custom validation, via `ArgumentTypeError` |
| `p.add_mutually_exclusive_group()` | Two options that cannot both appear |
| `sub = p.add_subparsers(dest="command", required=True)` | Subcommands |
| `sub.add_parser("add").set_defaults(handler=cmd_add)` | One function per subcommand |
| `args = p.parse_args(argv)` | Parse; `None` means the real command line |
| `help="... (default: %(default)s)"` | Show the actual default in the help |
| `print(..., file=sys.stderr)` | Progress and errors, so results stay pipeable |
| `raise SystemExit(main())` | `main`'s return value becomes the exit code |

## 12. Going further

1. [Python HOWTO — Argparse Tutorial](https://docs.python.org/3/howto/argparse.html) — the official incremental introduction; start here if section 3 went too fast.
2. [Python docs — `argparse`](https://docs.python.org/3/library/argparse.html) — the complete reference for every keyword in section 5.
3. [Command Line Interface Guidelines](https://clig.dev/) — why the conventions in section 1 exist, and what makes a command line pleasant to use. Short, opinionated, worth an evening.
4. Last year's full version of this material: [`sys.argv` and argparse](https://github.com/KnuxV/advanced_programming_python/blob/main/lessons/07-arguments/071-argv_argparse.md) and [advanced patterns](https://github.com/KnuxV/advanced_programming_python/blob/main/lessons/07-arguments/072-advanced.md) — written for `python script.py` and `pip`; read the commands with `uv run` in mind.
5. Practice: [exercise 2.2](../exercises/argparse-script.md) (a third argument on `report.py`) and [exercise 2.3](../exercises/password-generator.md) (two new options on someone else's project, on two branches).
