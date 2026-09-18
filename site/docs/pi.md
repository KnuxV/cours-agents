# pi — install the agent, connect it to the university's models

[pi](https://pi.dev) is a **coding agent**: a program in your terminal that sends your request to a language model, lets the model read files and run commands in the current folder, and loops until the task is done. Session 4 takes it apart. This page gets it running early, connected to the university's own models, with a **course tutor** that helps you through the exercises without doing them for you.

It takes 10–15 minutes. **At the end you will have:**

1. `pi` installed in your home folder (no administrator rights needed);
2. pi talking to the university's LLM platform with the API key you already have — nothing to buy, nothing leaves Strasbourg;
3. the `tutor` skill (English) and its twin `tuteur` (français).

**Before you start:** you need the API key from [Session 0, section 5](setup.md#5-your-unistra-llm-api-key), stored in the environment variable `UNISTRA_API_KEY`.

!!! warning "An agent acts, it does not just talk"
    pi can create, change and delete files in the folder where you start it, and run commands there. Start it inside a **git repository** with a clean `git status` (your `agent-lab`): whatever it does, `git diff` shows it and `git restore` undoes it. That is the reason Session 1 came first. The tutor of section 5 runs in a read-only mode where it cannot change anything.

## 1. Check that your key is there

```bash title="Any terminal — new window"
echo $UNISTRA_API_KEY | cut -c1-6
```

Expected: `sk-` followed by three characters. An empty line means the key is not stored on *this* machine: redo [setup 5.2](setup.md#52-store-it-as-an-environment-variable), open a new terminal, and check again.

## 2. Install pi

pi is written in JavaScript and needs **Node.js** (version 22.19 or later) to run — Node.js is to JavaScript what `python` is to Python. On WSL, Linux and Mac the installer fetches a private copy of Node.js into your home folder when you have none. On Git Bash you install Node.js yourself first.

=== "WSL (Ubuntu) / Linux"

    This is also the tab for the **university desktops**: nothing here asks for `sudo`.

    ```bash title="Ubuntu window (WSL) or Terminal (Linux)"
    curl -fsSL https://pi.dev/install.sh | sh
    ```

    The installer asks up to three questions. Answer all three with ++y++ (then ++enter++ for the first and the last):

    1. `Pi needs Node.js 22.19.0 or newer and npm. Install them now with standalone Node.js? [Y/n]` — yes. It downloads Node.js into `~/.local/share/pi-node` (about 350 MB with pi; one or two minutes).
    2. `Choose an action: y Install Pi (default)` — press ++y++.
    3. `Add … to your PATH in ~/.bashrc now? [Y/n]` — yes. This is the same mechanism as your API key: a line added to your shell's startup file, read by every *new* terminal.

    If the first question mentions `apt` instead of `standalone Node.js`, your Ubuntu is recent enough to provide Node.js itself; it then asks for your Ubuntu password (WSL or your own laptop only). Rehearsed on a Linux machine with no Node.js and no `sudo`, 17 September 2026. TODO(verify): the same run on a university desktop in A330 and on a fresh WSL Ubuntu.

=== "Mac"

    ```bash title="Terminal (Mac)"
    curl -fsSL https://pi.dev/install.sh | sh
    ```

    Same questions as in the WSL tab; answer yes to each. If you have [Homebrew](https://brew.sh/), the installer uses it to install Node.js; otherwise it downloads a private copy into your home folder. The PATH line goes into `~/.zshrc`. TODO(verify): not rehearsed on a Mac.

=== "Git Bash"

    The installer cannot fetch Node.js on Windows, so install it first. Without administrator rights, use Scoop (from [setup, Path D](setup.md#path-d-git-bash)):

    ```powershell title="Windows PowerShell (NOT administrator)"
    scoop install nodejs-lts
    ```

    With administrator rights, the Windows installer (`.msi`, the **LTS** version) from [nodejs.org](https://nodejs.org/en/download) does the same; default options are fine.

    Then **close Git Bash, open a new one**, and:

    ```bash title="Git Bash — new window"
    node --version
    npm install -g --ignore-scripts @earendil-works/pi-coding-agent
    ```

    Expected from the first line: `v22.19.0` or later. The second is the installation itself: `npm` is to Node.js what `pip` is to Python, and `-g` installs the program for your user rather than for one project. pi then runs the model's commands through Git Bash. TODO(verify): this path follows pi's documentation (Quickstart and Windows pages) but has not been rehearsed on a Windows laptop; if it fails in class, use WSL or Codespaces.

=== "Codespaces"

    A codespace already has Node.js. Check the version, then install:

    ```bash title="Codespace terminal"
    node --version
    npm install -g --ignore-scripts @earendil-works/pi-coding-agent
    ```

    If `node --version` prints something older than `v22.19.0`, use the WSL tab's `curl` line instead. TODO(verify): Node.js version of the default codespace image.

Then the usual ritual — close the terminal, open a new one:

```bash title="Any terminal — new window"
pi --version
```

Expected: `0.85.1` or later. `pi: command not found`? See [When things go wrong](#6-when-things-go-wrong).

Reference: [pi — Quickstart](https://pi.dev/docs/latest/quickstart) · [pi on Windows](https://pi.dev/docs/latest/windows).

## 3. Connect pi to the university's models

Out of the box pi knows the commercial providers (Anthropic, OpenAI, Google…), which all need a paid key. The university's platform speaks the same protocol as OpenAI's, so pi can use it; it only needs to be told *where* it is. That goes in one file, `~/.pi/agent/models.json`:

```bash title="Any terminal"
mkdir -p ~/.pi/agent
curl -fsSL https://raw.githubusercontent.com/KnuxV/cours-agents/main/resources/pi/models.json -o ~/.pi/agent/models.json
cat ~/.pi/agent/models.json
```

The last line prints what you just downloaded:

```json title="~/.pi/agent/models.json"
--8<-- "resources/pi/models.json"
```

Read it; by Session 3 every field will be familiar.

- `baseUrl` — the address of the platform. It is the one you called with `curl` at the end of Session 0.
- `api` — the protocol to speak: OpenAI's "chat completions" format.
- `apiKey` — **not your key**: the *name* of the environment variable that holds it. pi replaces `$UNISTRA_API_KEY` by its value at the moment it calls the platform. The key itself is written in no configuration file, so this file can be shared, committed, or shown on a projector.
- `models` — the models the platform serves, and for each its **context window**: how much text (counted in *tokens*, pieces of words) it can take in at once. `coder` is an 80-billion-parameter model specialised in programming, and the first in the list, so pi uses it by default.

Now test, from the outside in:

```bash title="Any terminal"
pi --list-models
```

Expected: a table of six lines starting with `unistra   coder   262.1K`. If you read `No models available. Use /login…` instead, pi found the file but not the key: go back to section 1. Then one real request:

```bash title="Any terminal"
pi -p "Reply with one word: pong"
```

Expected, after a second or two: `pong`. `-p` means *print*: one question, one answer, no conversation. That request travelled from your terminal to a machine room in Strasbourg and back, and cost nothing.

## 4. A first conversation

```bash title="Any terminal"
cd ~/agent-lab
git status
pi
```

`git status` first: it should say `working tree clean`, so that anything the agent changes stands out afterwards. pi opens a text box at the bottom of the terminal; the line under it shows the folder, and the model in use (`coder`). Try:

```text title="Inside pi"
What is in this folder? Do not change anything.
```

Watch what happens before the answer: lines such as `ls` or `read README.md` scroll by. Those are **tool calls**: the model asked pi to look at your files, pi did it and sent the result back, and only then did the model answer. That loop is the subject of Sessions 3 and 4.

| Type this | To |
|---|---|
| your request, then ++enter++ | talk to the model |
| `!git status` | run a command yourself **and show its output to the model** |
| `@` | pick a file to mention in your message |
| `/model` | choose another model from the list |
| `/new` | start a fresh conversation (the model forgets the previous one) |
| ++esc++ | interrupt the model while it is working |
| `/quit`, or ++ctrl+c++ twice | leave pi |

Back in the terminal, `git status` and `git diff` tell you whether anything changed.

## 5. The course tutor

A **skill** is a text file of instructions that pi hands to the model when the subject comes up. The course ships two — the same tutor in two languages:

| Skill | Language | Call it with |
|---|---|---|
| `tutor` | English | `/skill:tutor` |
| `tuteur` | français | `/skill:tuteur` |

The tutor knows the exercises of Sessions 1 and 2 (Python environments with `pip`, `venv` and `uv`; branches and merges; GitHub remotes, forks and pull requests), their "Done when", and where students usually trip. Its instructions are the opposite of a chatbot's: **you drive**. You type every command and write every line; it looks at your files, explains what is on your screen, and gives **one hint at a time** — first a question, then the concept and the section to reread, then the shape of the command, and the exact answer only once you have tried.

### 5.1 Install it

```bash title="Any terminal"
pi install git:github.com/KnuxV/cours-agents
pi list
```

pi clones the course repository into `~/.pi/agent/git/` and loads the skills it contains. `pi list` should show `git:github.com/KnuxV/cours-agents`. When the tutor is improved during the course, `pi update --extensions` fetches the new version.

### 5.2 Use it

Start pi in **read-only mode**, from the folder of the exercise:

```bash title="Any terminal, inside the exercise's folder"
pi --tools read,grep,find,ls
```

`--tools` is the list of what the model may do. With these four it can read and search your files, and nothing else: no editing, no commands. Then call the tutor and say where you are:

=== "English"

    ```text title="Inside pi"
    /skill:tutor I am on exercise 2.1. git status shows hundreds of files under .venv.
    ```

=== "Français"

    ```text title="Dans pi"
    /skill:tuteur Je suis sur l'exercice 2.1. git status affiche des centaines de fichiers dans .venv.
    ```

It will often ask you to run something and show it the result. That is what the `!` prefix is for: `!git status` runs the command and puts the output in the conversation, so that both of you read the same screen.

Three habits that make it useful:

1. **Give it the exact text.** Paste the error message, or rerun the command with `!`. "It doesn't work" cannot be debugged, by a human or by a model.
2. **Try each hint, and show what came back.** The tutor climbs one step per answer. Insisting only moves it up one step; what unlocks the exact answer is an attempt, even a failed one, pasted into the conversation. A failed attempt is information, and it is usually where the explanation you needed starts.
3. **End on the check.** The exercise is finished when its "Done when" passes and you can say in one sentence what the problem was — not when the tutor says so.

!!! note "It is a model, not the teacher"
    The tutor can be wrong, and a mid-size model sometimes forgets its instructions in a long conversation: if it starts handing out full solutions or rambling, `/new` and call the skill again. When it contradicts the course pages, the course pages win — and tell us, so that we fix the skill.

The skill is a plain text file, and reading it is a good preview of Session 4: [`tutor/SKILL.md`](https://github.com/KnuxV/cours-agents/blob/main/resources/pi/skills/tutor/SKILL.md) · [`tuteur/SKILL.md`](https://github.com/KnuxV/cours-agents/blob/main/resources/pi/skills/tuteur/SKILL.md).

## 6. When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| `pi: command not found` right after installing | PATH is read when a terminal starts | Open a new terminal. Still nothing: `tail -3 ~/.bashrc` (`~/.zshrc` on Mac) should show a line under `# Pi`; if not, rerun the installer and answer yes to the PATH question |
| Installer: `Unsupported operating system for automatic Node.js install` | You are in Git Bash | Follow the Git Bash tab: Node.js first, then `npm install` |
| Installer: `Pi requires Node.js 22.19.0 or newer. Found v18…` | An older Node.js is already installed | Own laptop: update Node.js ([nodejs.org](https://nodejs.org/en/download)). Otherwise come and see us |
| `No models available. Use /login…` | `UNISTRA_API_KEY` is not set in this window | Section 1 |
| `pi --list-models` complains about `models.json` | The download was cut, or the file was edited into invalid JSON | Rerun the `curl` line of section 3 |
| `401 status code (no body)` | The variable is set, but the key in it is wrong or was regenerated | [Setup 5.1](setup.md#51-generate-the-key): copy the key again, fix the line in `~/.bashrc`, new terminal |
| pi starts on a model that is not `coder`, or asks you to log in | Another provider's key exists on your machine | `/model`, choose `coder`, then ++ctrl+s++ in that list to make it the default |
| `/skill:tutor` is not offered when you type `/` | The package is not installed, or pi was already running when you installed it | `pi list`; then restart pi, or `/reload` |
| `pi install` fails with a git error | No network, or `git` missing | `git --version`; retry on another network (eduroam sometimes blocks less than a phone hotspot, sometimes more) |
| The tutor answers in the wrong language | The model picked the other skill | Call the one you want explicitly: `/skill:tutor` or `/skill:tuteur` |
| Answers stop mid-sentence or turn incoherent after a long session | The conversation has filled the model's context window | `/new` |

## Going further (optional)

- **A key that is not even in `~/.bashrc`.** In `models.json`, an `apiKey` that starts with `!` is a *command* whose output is the key, which lets a password manager hold it: `"!security find-generic-password -ws unistra"` on a Mac (Keychain), `"!secret-tool lookup application pi provider unistra"` on a Linux desktop (GNOME Keyring). The environment variable is what the course uses; this is what you would do on a machine you share.
- **Uninstall.** `npm uninstall -g @earendil-works/pi-coding-agent` removes the program; your settings and conversations stay in `~/.pi/agent/` until you delete that folder. The private Node.js, if the installer fetched one, is the folder `~/.local/share/pi-node`.
- pi's own documentation is installed with it; ask pi: `pi -p "Where is your documentation folder? List its files."`
