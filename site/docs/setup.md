# Session 0 — Set up your machine (homework)

Do this **before Session 1 (Monday 14 September 2026)**, at home, when you have time and a stable connection. It takes 20–40 minutes if all goes well, and it is the one thing that can make Session 1 miserable if it does not. Budget for it.

**At the end you will have:**

1. a terminal that runs Linux-style commands (`ls`, `curl`, `git`…);
2. a personal API key for the university's LLM platform, stored as an environment variable.

!!! tip "How to read this page"
    - Every grey box is something to type. Use the copy button at its right edge, paste into the window named in the box title, press ++enter++.
    - A **terminal** is a window where you type commands. The **prompt** is the text it shows while waiting for you (it ends with `$` on Linux/Mac). You never type the prompt.
    - When something fails, keep the *exact* error message (screenshot or copy-paste) and bring it to Session 1. "It doesn't work" cannot be debugged; `0x80370102` can.

## 0. Which path is yours?

| Your laptop | Follow | Time |
|---|---|---|
| Windows 10 / 11, you can install software (admin rights) | [Path A — WSL](#path-a-windows-wsl) (then read [WSL, explained](wsl.md)) | 20–30 min + a reboot |
| Mac | [Path B — Terminal](#path-b-mac) | 5–15 min |
| Windows **without** admin rights (managed laptop), or WSL failed | [Path C — GitHub Codespaces](#path-c-github-codespaces-the-lifeboat) | 10 min, needs a GitHub account |
| Windows, quickest way to a working `git` + `bash` for Session 1 | [Path D — Git Bash](#path-d-git-bash) | 10 min |

Windows users: Path D (Git Bash) is the fastest way to be ready for Session 1 (git), and you can do it even if WSL is giving you trouble. Path A (WSL) is what you will need from Session 4 on, so start it early. Doing both is fine.

Everyone then does [section 5 (API key)](#5-your-unistra-llm-api-key) and [section 6 (ten minutes in the terminal)](#6-ten-minutes-in-the-terminal).

Codespaces is a real option, not a shameful one: it gives you the same Ubuntu terminal in a browser tab. If your laptop is locked down, go straight there.

## Path A — Windows (WSL)

WSL (*Windows Subsystem for Linux*) installs a small, complete Linux — Ubuntu — inside Windows. You will only ever see it as a terminal window. We use it because the tools of this course (`git`, `curl`, `uv`, the agent harness of Session 4) and every server, cloud machine and data pipeline you will meet run Linux; inside WSL you type exactly the same commands as your Mac classmates, and what you learn transfers as is. The full story — what it is, the two file systems you now have, how to manage it — is on [WSL, explained](wsl.md). Read it once the install is done.

### A1. Install

Before you start: press ++ctrl+shift+esc++ (Task Manager) → **Performance** → **CPU** and check that it says **Virtualization: Enabled**. If it says *Disabled*, read [this first](wsl.md#virtualization-must-be-enabled).

1. Click Start, type `PowerShell`, **right-click** *Windows PowerShell* → **Run as administrator**.
2. Paste, press ++enter++:

```powershell title="Windows PowerShell (Administrator)"
wsl --install
```

3. **Reboot** when asked. After the reboot an **Ubuntu** window opens by itself, finishes installing, and asks for:
    - a **username**: short, lowercase, no spaces (it is not your Windows login);
    - a **password**, twice: **nothing appears while you type** — no dots, no stars. That is normal.

### A2. Open the terminal, run the check

From now on: Start → type `Ubuntu` → open. The window shows a prompt ending in `$`. That is your terminal for the whole course.

```bash title="Ubuntu window (WSL) — the window whose prompt ends in $"
uname -a && curl --version | head -1
```

Expected output (details will differ):

```text
Linux DESKTOP-XXXX 5.15.167.4-microsoft-standard-WSL2 #1 SMP ... x86_64 GNU/Linux
curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 ...
```

!!! danger "It must be run in the Ubuntu window, not in PowerShell"
    In PowerShell the same line fails with `uname : The term 'uname' is not recognized`. That is not a WSL error — you are in the wrong window. Open **Ubuntu** from the Start menu.

Something failed? See [When it fails](wsl.md#when-it-fails) on the WSL page. Meanwhile, [Path D](#path-d-git-bash) gets you through Session 1.

## Path B — Mac

Nothing to install. macOS ships with `curl`, `uname` and `git`.

### B1. Open Terminal

Press ++cmd+space++, type `Terminal`, press ++enter++. You see a prompt ending in `%` or `$`.

### B2. Trigger the one-time developer-tools download *now*

```bash title="Terminal (Mac)"
git --version
```

The **first time**, macOS pops up a window asking to install the *Command Line Developer Tools*. Click **Install** and wait (5–10 minutes, a few GB). Do this at home: if you skip it, it eats the first ten minutes of Session 1. Then run `git --version` again; it prints something like `git version 2.39.5 (Apple Git-154)`.

### B3. The check command

```bash title="Terminal (Mac)"
uname -a && curl --version | head -1 && git --version
```

Expected output (details will differ):

```text
Darwin MacBook-Air.local 24.5.0 Darwin Kernel Version 24.5.0 ... arm64
curl 8.7.1 (x86_64-apple-darwin24.0) libcurl/8.7.1 ...
git version 2.39.5 (Apple Git-154)
```

## Path C — GitHub Codespaces (the lifeboat)

A Codespace is a small Ubuntu machine in GitHub's cloud, with a terminal in your browser. The free plan gives every GitHub account **120 core-hours per month** (a 2-core machine = 60 hours) — far more than this course needs. Use it if your laptop is managed, if WSL failed, or as the day-of backup when something breaks during class.

1. Create a [GitHub account](https://github.com/signup) if you do not have one (you will need it in Session 1 anyway).
2. Go to [github.com/codespaces](https://github.com/codespaces). In *Explore quick start templates*, click **See all**, then **Use this template** under **Blank**.
3. A Visual Studio Code editor opens in the browser. Open the terminal panel: menu ☰ → **Terminal** → **New Terminal** (or press ++ctrl+grave++).
4. You are in an Ubuntu terminal, prompt ending in `$`. Run the check command:

```bash title="Codespace terminal (browser)"
uname -a && curl --version | head -1
```

Things to know:

- A codespace **stops after 30 minutes of inactivity** by default and keeps your files; it is **deleted after 30 days** unused. TODO(verify): confirm the current defaults on the [Codespaces billing page](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) before the first class.
- Environment variables you `export` (section 5) are lost when the codespace restarts unless you put them in `~/.bashrc` — section 5 does exactly that.
- Students may get extra quota through the [GitHub Student Developer Pack](https://education.github.com/pack). TODO(verify): the exact Codespaces bonus.

Reference: [Codespaces quickstart](https://docs.github.com/en/codespaces/getting-started/quickstart) · [Creating a codespace from a template](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-from-a-template).

## Path D — Git Bash

Git Bash gives a `bash` shell with `curl` and `git` on Windows, with no admin rights and no reboot. It is the quickest way to be ready for Session 1 (git) and it works for Sessions 2–3 as well. **It is not enough for Session 4**: OpenCode has no native Windows support (its documentation recommends WSL), so plan to have WSL (Path A) or Codespaces (Path C) working by then.

1. Download and install Git for Windows from [gitforwindows.org](https://gitforwindows.org/) (default options are fine).
2. Start → type `Git Bash` → open it. Prompt ends in `$`.
3. Check:

```bash title="Git Bash"
uname -a && curl --version | head -1
```

Expected first line starts with `MINGW64_NT-10.0 ...`.

Optional — **Scoop**, a package installer that needs no admin rights (for `jq`, `uv` and other tools we will use). In a *normal* (non-administrator) PowerShell window:

```powershell title="Windows PowerShell (NOT administrator)"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

Reference: [scoop.sh](https://scoop.sh/) · [Scoop install notes](https://github.com/ScoopInstaller/Install).

!!! note "PowerShell alone can call the API, but it is not our terminal"
    Windows 10/11 ship `curl.exe`, so a raw API call from PowerShell is possible in an emergency (`curl.exe`, not `curl`, which PowerShell silently replaces with another command). Nothing else in the course assumes PowerShell.

## 5. Your Unistra LLM API key

The university runs its own LLM platform at [conversation.ia.unistra.fr](https://conversation.ia.unistra.fr/): free, hosted in Strasbourg, with an API compatible with the OpenAI format. In Session 3 you will call it from the terminal. For that you need a personal **API key** — a long string starting with `sk-` that identifies *you*.

### 5.1 Generate the key

1. Log in at [conversation.ia.unistra.fr](https://conversation.ia.unistra.fr/) with your university account.
2. Click your **profile** (bottom left) → **Réglages** (Settings) → **Compte** (Account).
3. Under *Clés API*: **Afficher** (show) or **Générer une nouvelle clé** (generate a new key). Click the eye icon to reveal it, then the copy button.

Treat the key like a password. Never paste it in a file you share, in a chat, in the forum, or in code. If it leaks, come back here and generate a new one (TODO(verify): whether regenerating invalidates the old key on the Unistra platform — it does on the underlying software, Open WebUI).

Reference: [Unistra — Utiliser l'API](https://documentation.unistra.fr/DNUM/Intelligence_artificielle/guide_complet_IA/co/7_1API.html) (French).

### 5.2 Store it as an environment variable

An **environment variable** is a named value your terminal keeps for the programs it launches. We store the key in one, so that commands can use `$UNISTRA_API_KEY` and the key itself never appears in a script. The variable must be defined in your shell's *startup file*, otherwise it disappears when you close the window. That file depends on your platform:

=== "WSL (Ubuntu) / Codespaces / Git Bash"

    ```bash title="Ubuntu window, Codespace terminal, or Git Bash"
    echo 'export UNISTRA_API_KEY="sk-XXXX"' >> ~/.bashrc
    source ~/.bashrc
    ```

=== "Mac"

    macOS's default shell is `zsh`, whose startup file is `~/.zshrc`, not `~/.bashrc`.

    ```bash title="Terminal (Mac)"
    echo 'export UNISTRA_API_KEY="sk-XXXX"' >> ~/.zshrc
    source ~/.zshrc
    ```

    If `echo $SHELL` prints `/bin/bash` instead of `/bin/zsh`, use the WSL tab's commands instead.

Replace `sk-XXXX` with your real key **before** pressing ++enter++, keeping the quotes. The `>>` appends one line to the startup file; `source` reloads it in the current window.

### 5.3 Test it — in a *new* window

Close the terminal, open a new one (this is the real test: does the key survive?), then:

```bash title="Any terminal — new window"
echo $UNISTRA_API_KEY | cut -c1-6
```

Expected: `sk-XXX` — the first six characters of your key, nothing more. If you see an empty line, the export went into the wrong file: check `echo $SHELL` and redo 5.2 in the other tab.

Now one real call to the platform, which lists the available models:

```bash title="Any terminal"
curl -s https://conversation.ia.unistra.fr/api/models -H "Authorization: Bearer $UNISTRA_API_KEY" | head -c 200
```

Expected (truncated on purpose): a block of JSON starting with

```text
{"data":[{"id":"bge-m3","object":"model","created":1677610602,"owned_by":"openai", ...
```

If instead you get `{"detail":"Your session has expired or the token is invalid. Please sign in again."}`, the key is missing or wrong in this window — the platform says "session expired" for both cases. Redo 5.2 and 5.3.

Congratulations: that was your first API call. Session 3 starts from here.

A script that runs all these checks and prints PASS/FAIL per item (`check-setup.sh`) will be linked here once it is ready. TODO(verify): link when Task 03 delivers it.

## 6. Ten minutes in the terminal

You are going to spend the whole course in this window, so make it yours now. Type each line, look at what happens. (A fuller exercise with solutions will be on the [exercises page](exercises.md).)

```bash title="Any terminal"
pwd                      # print working directory: where am I?
ls                       # list what is here
ls -la                   # ... including hidden files, with details
mkdir cours-agents       # make a directory (folder)
cd cours-agents          # change into it
pwd                      # you moved
echo "hello" > note.txt  # write the word hello into a new file
cat note.txt             # print the file
cp note.txt copy.txt     # copy
mv copy.txt renamed.txt  # move = rename
ls
rm renamed.txt           # remove (no trash, no undo)
cd ..                    # go up one level
ls
```

Habits worth acquiring on day 0:

- ++tab++ completes file and command names; press it twice to see options. Nobody types full paths.
- ++up++ recalls the previous command.
- ++ctrl+c++ interrupts a command that hangs. `clear` empties the screen. `q` quits most pagers (like `less` or `git log`).
- `--help` after a command (e.g. `ls --help`) or `man ls` (quit with `q`) shows its manual.
- Text after `#` is a comment; the shell ignores it.

Why the terminal at all? Because it is the interface of every server, every data pipeline, and every coding agent you are aiming to use. A chatbot tab is a demo; the terminal is where the work runs.

## Going further (optional)

1. [The Missing Semester of Your CS Education (MIT)](https://missing.csail.mit.edu/) — lectures 1 and 2 (the shell, shell tools): the best two hours of terminal onboarding available, free videos and notes.
2. [Software Carpentry — The Unix Shell](https://swcarpentry.github.io/shell-novice/) — written for researchers who have never opened a terminal.
3. [Microsoft — Best practices for a WSL development environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment) — Windows Terminal, where to keep files, VS Code integration.
4. [GitHub Codespaces quickstart](https://docs.github.com/en/codespaces/getting-started/quickstart).
5. [Julia Evans — Oh shit, git!](https://ohshitgit.com/) — for after Session 1, but a taste of the tone: things will go wrong and there is always a way out.
