# 2.3 — Fork and extend the password generator

Lesson: [Session 2 — Python tooling](../sessions/s2.md) · [All exercises](index.md)

**Goal:** install a project you did not write with one command, read a real `argparse` program, and add two options to it — one branch per option.

The project is [github.com/KnuxV/password-generator](https://github.com/KnuxV/password-generator): a command-line tool that prints a strong password, either **memorable** (random English words: `Stubbed Congress Tiptop`) or **random** (mixed characters: `aB3$cD9#eF2@`). One dependency (`zxcvbn`, a strength estimator), a small test suite, and the three project files from [S2 §4](../sessions/s2.md#4-a-project-from-scratch).

**Part A — fork and install (10 min).** You will push your work, so you need your own copy on GitHub: a **fork** ([Git as a collaboration tool, §2](../reference/git-collaboration.md#2-clone-vs-fork)). On the repository page, click **Fork** → **Create fork**. Then clone *your* fork — in your home folder, not inside `agent-lab`:

```bash title="Any terminal"
cd ~
git clone https://github.com/YOUR-USERNAME/password-generator.git
cd password-generator
uv sync
```

`uv sync` prints `Using CPython 3.12.x`, `Creating virtual environment at: .venv`, then `Installed 6 packages` — the exact versions from `uv.lock`. That was the installation. Now use it:

```bash title="Any terminal, inside password-generator"
uv run strong_password.py --help
uv run strong_password.py -t memorable -l 5
uv run strong_password.py -t random -l 16
uv run strong_password.py -t words
uv run compute_crack_time.py
uv run pytest
```

Expected: a help message with two options; a five-word password; a sixteen-character one; a refusal (`invalid choice: 'words' (choose from memorable, random)`); a comparison of the two kinds with a crack-time estimate; `13 passed`.

**Part B — read the code (10 min, together).** Open `strong_password.py` and answer, in your own words:

1. `cat pyproject.toml`, `cat .python-version`, `head -20 uv.lock`: which file says *what the project asked for*, which says *what it got*, which says *which Python*? Why is `pytest` under `[dependency-groups] dev` and not with `zxcvbn`?
2. In `main()`: which argument is **required**, which has a **default**? What does `choices=` buy you (you saw it with `-t words`)? Where does `args.length` end up?
3. Follow the value: `args.type` → `TypePassword(args.type)` → `StrongPassword(...)` → `generate()` → `generate_memorable()`. Which line joins the words with a space?
4. Where does the word list come from, and why `Path(__file__).parent` rather than just `"data/eff_large_wordlist.txt"`? (Try: `cd ~` then `uv run --project password-generator password-generator/strong_password.py -t memorable`.)
5. In `tests/test_memorable_password.py`, what does `test_has_spaces` assert? Keep it in mind for part C.

**Part C — two options, two branches (20 min).** Each option gets its own branch, merged into `main` before the next one starts (S1 §5, case 1: fast-forward).

1. `git switch -c separator`. Add an option `-s` / `--separator`: what goes *between* the words of a memorable password. Allowed values: `-`, a space, `_`, `.`, `/` (`choices=`); default: a space, so that nothing changes for existing users. Three places to touch: `parser.add_argument(...)`, the `StrongPassword` constructor (a new parameter *with a default*), and the `" ".join(...)` line. Check:

    ```bash title="Any terminal, inside password-generator"
    uv run strong_password.py -t memorable -l 4 -s -
    uv run strong_password.py -t memorable -l 4 --separator "_"
    uv run strong_password.py -t memorable -l 4 -s ,
    uv run pytest
    ```

    Expected: four words joined by `-` (`Earful-Afraid-Sapling-Helpful`), then by `_`, a refusal for `,`, and still `13 passed` — the default did not move. (To pass a space: `-s " "`, with the quotes — shell quoting, S2 §9.) Commit, `git switch main`, `git merge separator`.

2. `git switch -c numbers`. Add a **flag** `-n` / `--numbers` (`action="store_true"`, no value): when present, every word of a memorable password gets one random digit appended — `Wildlife1 Synthesis5 Useable1 Facecloth3`. Hint: `secrets.choice(DIGITS)` is already imported; the flag is ignored for `random` passwords, which have digits anyway. Same three places. Check `-l 4 -n`, then `-l 4 -s - -n`, then `uv run pytest`. Commit, switch to `main`, merge.

3. `git push`. Your fork on GitHub now carries both features on `main`.

**Done when** `uv run strong_password.py --help` documents four options, `uv run strong_password.py -t memorable -l 4 -s - -n` prints something like `Decode9-Rebuild2-Squirt4-Paper9`, `uv run pytest` passes, and `git log --oneline` on GitHub shows your two commits.

*Stretch:* add one test per option in `tests/` (a `-` separator → `password.count("-") == 3` for four words; `numbers=True` → `any(c.isdigit() for c in password)`). Then redo part C the hard way: both branches off the *same* commit, merged one after the other — Git reports conflicts in every place both branches touched; resolve them as in S1 §5, case 3.

??? note "Solution"
    Both options, as they look once the two branches are merged. The constructor:

    ```python
    def __init__(
        self, length: int, type_p: TypePassword, separator: str = " ", numbers: bool = False
    ):
        self.length = length
        self.type_p = type_p
        self.separator = separator
        self.numbers = numbers
    ```

    `generate_memorable`:

    ```python
    words = [secrets.choice(WORD_LIST) for _ in range(self.length)]
    if self.numbers:
        words = [word + secrets.choice(DIGITS) for word in words]
    return self.separator.join(words)
    ```

    The parser, before `args = parser.parse_args()`, and the call that follows it:

    ```python
    parser.add_argument(
        "-s",
        "--separator",
        choices=["-", " ", "_", ".", "/"],
        default=" ",
        help="character between words (memorable only); default: a space",
    )
    parser.add_argument(
        "-n",
        "--numbers",
        action="store_true",
        help="add a digit after each word (memorable only)",
    )
    args = parser.parse_args()

    generator = StrongPassword(
        length=args.length,
        type_p=TypePassword(args.type),
        separator=args.separator,
        numbers=args.numbers,
    )
    ```

    `--help` then lists `-s {-, ,_,.,/}` — the space in the choices makes the usage line ugly; `metavar="SEP"` on that `add_argument` tidies it. The rehearsed sequence: `separator` branch → 13 passed → fast-forward merge; `numbers` branch → 13 passed → fast-forward merge; `--help` shows four options.
