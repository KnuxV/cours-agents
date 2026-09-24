<!--
PORTED FROM last year's material (KnuxV/advanced_programming_python):
  exercices/02-shell/02-shell.md  — creating a CSV with echo/>/>>, head, tail, sort, cut, pipes,
      redirection, and the grades.csv questions (the questions themselves became
      exercises/shell-data.md in this port)
  lessons/01-shell-intro.md       — absolute vs relative paths, wildcards, command history,
      $OLDPWD / $_ / !!, "Pro tips for terminal productivity"
      (the apt / brew / sudo sections of that lesson are deliberately NOT ported — see INVENTORY.md)

PROPOSED DESTINATION: site/docs/reference/shell-text-tools.md
  Nav (site/mkdocs.yml, under "Reference" → "Machines and terminals"):
          - The shell as a data tool: reference/shell-text-tools.md
  Row for site/docs/reference/index.md, section "Machines and terminals":
      | [The shell as a data tool](shell-text-tools.md) | Pipes, redirection, `cut`, `sort`, `uniq`, `grep`, `wc` — and the quoting and counting traps | after [Session 0](../setup.md), used by every later session |

REWRITTEN, not pasted: no `sudo apt install tree`, no `eog`, no `micro` install; every block says
where to run it; the `wc -l` off-by-one that made last year's exercise state the wrong answer is now
a section of its own.
Every output block below was produced on this machine (GNU coreutils, bash).
-->

# The shell as a data tool

[Session 0](../setup.md#7-ten-minutes-in-the-terminal) taught you to move around: `pwd`, `ls`, `cd`, `cp`, `mv`. This page is the next half-hour, and it is the half that makes the terminal worth the trouble: half a dozen small programs that read text, and one character — `|` — that connects them.

Why a course about agents cares. When an agent "does something" on your machine, what it does is run commands like these. Reading a model's proposed `grep … | cut … > out.csv` and knowing whether it is right, or whether it is about to overwrite your data, is the review skill of [Session 4](../sessions/s4.md). The same pipeline is also, quite often, the fastest way to answer a question about a file that would otherwise cost you a notebook and a kernel restart.

!!! note "Where this works"
    Everything on this page works in the **Ubuntu window (WSL)**, a **Mac Terminal**, a **Linux terminal**, **Git Bash** and a **Codespace terminal**. It does *not* work in Windows PowerShell, which has its own, different commands. Nothing here needs `sudo`, and nothing needs to be installed.

## 1. Make a file to play with

Two operators do all the file writing:

```bash title="Ubuntu window (WSL), Terminal (Mac), Linux terminal, Git Bash or Codespace terminal"
cd ~
mkdir -p shell-demo
cd shell-demo
echo "Name,City,Age
Alice,Paris,25
Bob,Lyon,30
Claire,Nice,22" > people.csv
echo "David,Marseille,28" >> people.csv
cat people.csv
```

```text
Name,City,Age
Alice,Paris,25
Bob,Lyon,30
Claire,Nice,22
David,Marseille,28
```

`>` sends a command's output into a file, **replacing** whatever was there. `>>` **appends**. The difference is one character and one lost afternoon, so read every `>` you type — and every `>` an agent proposes.

## 2. Looking at a file without opening it

```bash title="Any terminal, inside shell-demo"
cat people.csv        # the whole thing
head -3 people.csv    # first 3 lines (default 10)
head -1 people.csv    # just the header
tail -2 people.csv    # last 2 lines
tail -n +2 people.csv # from line 2 to the end — i.e. skip the header
```

```text
Name,City,Age
```

```text
Alice,Paris,25
Bob,Lyon,30
Claire,Nice,22
David,Marseille,28
```

`head -1` and `tail -n +2` are the two you will use constantly: one shows you the column names, the other gives you the data without them. Note the `+`: `tail -2` means "the last two", `tail -n +2` means "starting at the second".

For a file too big for the screen, `less people.csv` opens a pager — arrows and ++page-down++ to move, `/word` to search, `q` to quit. `wc` counts (section 5).

## 3. `cut`: columns

```bash title="Any terminal, inside shell-demo"
cut -d',' -f2 people.csv
```

```text
City
Paris
Lyon
Nice
Marseille
```

`-d','` says the delimiter is a comma, `-f2` says take field 2. `cut` cannot read column *names* — it counts delimiters, so you have to know that `City` is the second field. Ranges work: `-f1,3` (first and third), `-f2-` (from the second on), `-f-2` (up to the second).

!!! warning "`cut` does not understand quoted CSV"
    `Doe, John",42` — a comma inside a quoted field — will be cut in the wrong place, silently. For quick looks and clean files, `cut` is perfect. For real data with quoting, embedded newlines and encodings, use Polars ([Session 2, §7](../sessions/s2.md#7-bonus-polars-in-five-minutes)). Knowing which tool stops being appropriate is part of the skill.

## 4. Pipes: the whole idea

`command1 | command2` feeds the output of the first into the second, with no temporary file:

```bash title="Any terminal, inside shell-demo"
cut -d',' -f1 people.csv | tail -n +2 | sort -r
```

```text
David
Claire
Bob
Alice
```

Read it left to right: take the first column, drop the header, sort in reverse. Three tiny programs, none of which knows the others exist. This is the Unix idea — small tools with one job, composed at the point of use — and it is why the commands on this page have survived fifty years.

The habit that makes it painless: **build the pipeline one stage at a time**, looking at the output after each `|` you add. When something comes out wrong, remove the last stage and look again.

## 5. `sort`, `uniq`, `wc`, `grep`

**`sort`** — alphabetical by whole line by default. The options that matter:

| Option | Effect |
|---|---|
| `-r` | reverse |
| `-n` | numeric (so 10 comes after 2, not before) |
| `-t','` | fields are separated by commas |
| `-k3,3` | sort on field 3 only |
| `-u` | drop duplicates while sorting |

```bash title="Any terminal, inside shell-demo"
tail -n +2 people.csv | sort -t',' -k3,3n
```

```text
Claire,Nice,22
Alice,Paris,25
David,Marseille,28
Bob,Lyon,30
```

Write `-k3,3n` ("field 3 only, numerically"), not `-k3n` ("from field 3 to the end of the line, numerically") — the second one works until two rows have the same age.

**`uniq`** removes *adjacent* duplicate lines, which means it is almost always preceded by `sort`. `uniq -c` counts, and the combination below is the shell's `group_by`:

```bash title="Any terminal, inside shell-demo"
tail -n +2 people.csv | cut -d',' -f2 | sort | uniq -c | sort -rn
```

```text
      1 Paris
      1 Nice
      1 Marseille
      1 Lyon
```

(Four cities, one person each — on a real file this is a frequency table, highest first, in one line.)

**`grep`** keeps the lines that match:

```bash title="Any terminal, inside shell-demo"
grep 'Lyon' people.csv
grep -c ',2' people.csv
```

```text
Bob,Lyon,30
```

```text
3
```

Useful options: `-c` count instead of printing, `-i` ignore case, `-v` invert (keep the lines that do *not* match), `-n` show line numbers, `-r` search a whole directory tree. `grep -rn "TODO" .` is how you find your own loose ends; it is also, not coincidentally, one of the tools a read-only agent is given in [Session 4](../sessions/s4.md).

**`wc`** counts: `-l` lines, `-w` words, `-c` bytes.

### 5.1 The counting trap that made last year's answer wrong

`wc -l` does not count lines. It counts **newline characters** — and a file whose last line does not end with one is reported one short, silently, for ever. Make one and see:

```bash title="Any terminal, inside shell-demo"
printf 'Name,City,Age\nAlice,Paris,25\nBob,Lyon,30' > nonewline.csv
cat nonewline.csv
wc -l nonewline.csv
grep -c '' nonewline.csv
```

```text
Name,City,Age
Alice,Paris,25
Bob,Lyon,30
```
```text
2 nonewline.csv
```
```text
3
```

Three lines on screen, `wc -l` says two, `grep -c ''` says three. (`grep -c ''` counts the lines matching the empty pattern — that is, all of them, terminated or not. `awk 'END {print NR}'` does the same.)

This is not a curiosity. Last year's version of the [grades exercise](../exercises/shell-data.md) asked "how many students are in the class?" and gave 49 as the answer, computed with `tail -n +2 grades.csv | wc -l`. The file's last line has no newline, so the real number is **50** — which `grep -c ''` reports and `wc -l` does not. One student, invisible, in a file of fifty.

The lesson generalises past the shell: **a count is a claim, and a claim deserves a second method.** When two ways of counting disagree you have found something — a missing newline, a duplicated key, a filter you forgot. This is the same reflex the [shape assertions](testing.md#11-where-this-sits-in-the-bigger-picture) of a test suite automate.

## 6. Saving the result

```bash title="Any terminal, inside shell-demo"
cut -d',' -f1 people.csv | tail -n +2 | sort > names.txt
cat names.txt
```

Redirection is evaluated *before* the command runs, so `sort file.csv > file.csv` empties the file. If you need to transform a file in place, write to a new name and rename afterwards:

```bash title="Any terminal — the safe pattern"
sort people.csv > people.sorted.csv && mv people.sorted.csv people.csv
```

`&&` means "only if the first command succeeded" — which is [exit codes](command-line-arguments.md#9-exit-codes) doing their job.

## 7. Quoting, wildcards, and the two characters that bite

The shell splits your command line on spaces **before** the program sees it, and expands `*` and `?` against the filenames in the current directory. Two rules:

- **Quote anything with a space in it**: `grep "green tea" menu.csv`, `cd "My Documents"`, `--product "green tea"`.
- **Quote anything with a `*` you do not want expanded**: `python calc.py 20 "*" 3`, because bare `*` becomes the list of files in the folder.

```bash title="Any terminal — wildcards"
ls *.csv          # every file ending in .csv
ls data/*.txt     # every .txt in data/
cp *.csv backup/  # every csv into backup/
rm *.tmp          # …think first. There is no recycle bin.
```

!!! danger "`rm` is final"
    No confirmation, no trash, no undo. Before any `rm` with a wildcard, run the same pattern through `ls` first — literally replace `rm` with `ls`, look at the list, then run the `rm`. The same applies with more force to an `rm` an agent suggests: `ls` it yourself.

## 8. Typing less

| Keys / characters | Effect |
|---|---|
| ++tab++ | Complete the filename or command you started typing. Press twice for the list of possibilities |
| ++ctrl+r++ | Search backwards through your command history — type a few letters of a command you ran before |
| ++up++ / ++down++ | Previous / next command |
| `history` | The whole list, numbered |
| `!!` | The previous command, again (`!!` on its own re-runs it) |
| `$_` | The last argument of the previous command: `mkdir -p ~/project/data && cd $_` |
| `cd -` | Back to the directory you were in before (it is kept in `$OLDPWD`) |
| ++ctrl+c++ | Stop the running command |
| ++ctrl+l++ | Clear the screen |
| ++ctrl+a++ / ++ctrl+e++ | Jump to the start / end of the line |

```bash title="Any terminal — $_ and cd -"
mkdir -p /tmp/zzz && cd $_ && pwd
cd -
```

```text
/tmp/zzz
```

++ctrl+r++ is the one to learn today. It replaces remembering the long pipeline you wrote yesterday.

## 9. When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| `cut: you must specify a list of bytes, characters, or fields` | No `-f` | `cut -d',' -f2 file.csv` |
| `cut` returns the whole line | Wrong delimiter (tabs? semicolons?) | `head -1 file` and look; `-d';'` for a French-style CSV |
| Sorting puts 10 before 2 | Alphabetical sort | `sort -n`, or `-k3,3n` for one field |
| `sort -k3n` breaks on ties | It sorts from field 3 *to the end of the line* | `-k3,3n` |
| `uniq` leaves duplicates | They were not adjacent | `sort \| uniq` |
| Your file is suddenly empty | `cmd file > file` | Write to a new name, then `mv` (§6) |
| One line fewer than expected | No trailing newline; `wc -l` counts newlines | `grep -c ''` (§5.1) |
| `No such file or directory` on a name you can see | A space in the name, unquoted | Quote it, or use ++tab++ completion |
| `rm` deleted more than you meant | The wildcard matched more than you thought | There is no recovery. Next time, `ls` the pattern first (§7) |
| Accented text comes out as `Ã¨` | Encoding mismatch | The file is probably UTF-8 and something read it as Latin-1; in Python always pass `encoding="utf-8"` |
| These commands do not exist | You are in Windows PowerShell | Open the Ubuntu window, Git Bash or a Codespace terminal |

## 10. Cheat sheet

| Command | What it does |
|---|---|
| `cat f` / `less f` | Show a file / page through it |
| `head -n N f` / `tail -n N f` | First / last N lines |
| `tail -n +2 f` | Skip the header |
| `cut -d',' -f1,3 f` | Fields 1 and 3 |
| `sort -t',' -k3,3nr f` | Sort on field 3, numeric, descending |
| `sort \| uniq -c \| sort -rn` | Frequency table, most frequent first |
| `grep -i 'pattern' f` | Matching lines (`-v` invert, `-c` count, `-rn` recursive with line numbers) |
| `wc -l f` / `grep -c '' f` | Count lines (the second one is trustworthy) |
| `cmd > f` / `cmd >> f` | Write to a file / append to it |
| `cmd1 \| cmd2` | Feed the first's output into the second |
| `cmd1 && cmd2` | Run the second only if the first succeeded |
| `ls *.csv` | Wildcard: every matching filename |
| ++ctrl+r++, `!!`, `$_`, `cd -` | History and shortcuts |

## 11. Practice and going further

- **Exercise**: [the grades file](../exercises/shell-data.md) — twelve questions on a class of 50 students, answered with the commands above.
- [The Missing Semester — Shell Tools and Scripting](https://missing.csail.mit.edu/2020/shell-tools/) and [Data Wrangling](https://missing.csail.mit.edu/2020/data-wrangling/) — the MIT lectures that cover exactly this, with `sed` and `awk` for when `cut` is not enough. One hour, very high return.
- [Software Carpentry — The Unix Shell](https://swcarpentry.github.io/shell-novice/) — the same material at a gentler pace, written for researchers.
- [`explainshell.com`](https://explainshell.com/) — paste a command you do not understand and it annotates every flag. Useful on a command an agent wrote.
