# WSL, explained

This page is for Windows users who followed [Path A](setup.md#path-a-windows-wsl). It explains what you installed, why, and the one thing that confuses everybody in the first weeks: you now have **two file systems**.

## What WSL actually is

WSL (*Windows Subsystem for Linux*) is a small, complete Linux computer running inside your Windows one. Microsoft builds it; Windows 10 and 11 ship it. The Linux it runs for us is **Ubuntu**, the most common Linux distribution.

Concretely:

- It has **its own files**, its own programs, its own user account and password. None of that is your Windows account.
- It has **no desktop**. The only thing you see of it is a terminal window — a black window with a `$` prompt. That is not a limitation for this course: the terminal is the whole point.
- It **shares** your network, your clipboard and your screen with Windows, and it can see your Windows disk (see below).
- It starts when you open the Ubuntu window and stops by itself when you close it. It uses a few hundred MB of disk and little memory while idle.

If you have used Google Colab: Colab is a Linux machine in Google's cloud that you reach through a browser. WSL is the same idea, except the machine is *your* laptop and you reach it through a terminal instead of a notebook.

## Why we use it

- **Every server is Linux.** The machines that run websites, data pipelines, model training and the coding agents you will use in Session 4 all run Linux and are driven through a terminal. Learning it on your own laptop is learning the real thing.
- **The tools of this course are made for it.** `git`, `curl`, `uv`, and OpenCode are designed for Unix-style shells. OpenCode (Session 4) does not run natively on Windows at all.
- **Same commands as your Mac classmates.** macOS is Unix underneath, so inside WSL you type exactly what they type. One set of instructions for the whole room.
- Windows has its own command language, PowerShell. It is a fine tool, but a different one; nothing in this course uses it beyond the WSL install itself.

## Vocabulary

| Word | Meaning here |
|---|---|
| **Terminal** | The window where you type commands. |
| **Shell** | The program inside the terminal that reads your commands. In Ubuntu it is `bash`; on a Mac it is `zsh`; in Windows it is PowerShell. |
| **Prompt** | What the shell prints while waiting for you: `lea@LAPTOP:~$` means user `lea`, on machine `LAPTOP`, in folder `~`. You never type it. |
| **Distribution** ("distro") | A packaged Linux: Ubuntu, Debian, Fedora… WSL can run several; we use Ubuntu. |
| **`sudo`** | "Do this as administrator". Asks for your *Linux* password; nothing shows while you type it. |

### Which window am I in?

This is the first thing to check when a command "does not exist":

| The prompt looks like | You are in | Linux commands work? |
|---|---|---|
| `lea@LAPTOP:~$` | Ubuntu (WSL) | yes |
| `PS C:\Users\Lea>` | PowerShell | no (`uname`, `ls -la`, `export` will fail or behave differently) |
| `C:\Users\Lea>` | Command Prompt (cmd) | no |

## Opening and closing it

- **Start menu → type `Ubuntu` → Enter.** Always works.
- **Windows Terminal** (preinstalled on Windows 11; on Windows 10 install it from the Microsoft Store): open it, click the small arrow ▾ next to the `+` tab, choose *Ubuntu*. You get tabs, a proper font, and reliable copy/paste. You can set Ubuntu as the default profile in its settings.
- From a PowerShell window, typing `wsl` also drops you into Ubuntu.
- To leave: type `exit` or close the window. Nothing is lost; your files stay.

Copy and paste inside the terminal: ++ctrl+shift+c++ / ++ctrl+shift+v++, or right-click to paste. Plain ++ctrl+c++ inside a terminal means "stop the running command".

## The two file systems

This is where the confusion comes from. You now have two independent folder trees on the same laptop.

**Windows** has drives with letters and backslashes:

```text
C:\Users\Lea\Documents\thesis.docx
```

**Linux** has one single tree starting at `/` ("root"), with forward slashes:

```text
/home/lea/cours-agents/note.txt
```

Two more differences that bite:

- Linux is **case-sensitive**: `Data.csv` and `data.csv` are two different files. Windows treats them as the same.
- Files whose name starts with a dot (`.bashrc`, `.git`) are **hidden** in Linux; `ls -la` shows them.

Your **home** in Linux is `/home/<your-linux-user>`, and the shell abbreviates it to `~`. `cd ~` (or just `cd`) takes you home from anywhere. Your Windows home, `C:\Users\<your-windows-name>`, is a different place — and the two user names need not match.

### The bridges between them

The two trees can see each other. Learn both directions:

| From | To reach | Type |
|---|---|---|
| Ubuntu terminal | your Windows `C:` drive | `/mnt/c/` — e.g. `ls /mnt/c/Users/Lea/Downloads` |
| Ubuntu terminal | open the *current* Linux folder in Windows Explorer | `explorer.exe .` (note the dot) |
| Windows Explorer address bar | your Linux files | `\\wsl$\Ubuntu\home\lea` (or just `\\wsl$` to browse) |

Example — you downloaded `data.csv` with the browser (it landed in Windows Downloads) and want it in your Linux project:

```bash title="Ubuntu window (WSL)"
cp /mnt/c/Users/Lea/Downloads/data.csv ~/cours-agents/
```

Replace `Lea` with your Windows user name (look at `ls /mnt/c/Users/` if unsure). Paths with spaces must be quoted: `"/mnt/c/Users/Lea/My Documents/data.csv"`. Press ++tab++ while typing a path and the shell completes it for you — it also tells you immediately if the path is wrong.

### Where to keep your work

**Inside Linux, in your home folder (`~`).** For example `~/cours-agents/`. Reasons:

- `/mnt/c` is **much slower** (every file access crosses between the two systems), and `git` behaves oddly there (file permissions and line endings differ between Windows and Linux).
- Every command on this site assumes you are in `~/...`.

Use the Windows side only to fetch things (Downloads) and to look at results (`explorer.exe .`). When you feel lost, `pwd` prints where you are.

!!! note "Two of everything"
    Because the two systems are independent, a program installed on Windows (Python from python.org, VS Code, Git for Windows) is **not** installed in Ubuntu, and vice versa. In this course everything is installed inside Ubuntu. VS Code is the one exception: it is installed on Windows and *connects* to Ubuntu (see below).

## Installing programs

Linux installs programs with a **package manager**, not by downloading `.exe` files. On Ubuntu it is `apt`:

```bash title="Ubuntu window (WSL)"
sudo apt update
sudo apt install -y jq
```

The first line refreshes the catalogue; the second installs `jq`, a small tool we will use in Session 3 to read JSON. Some tools ship their own one-line installer instead (`uv` in Session 2, OpenCode in Session 4) — those are `curl ... | sh` commands you will copy from the session pages.

## Editing files

Three options; keep the first and one of the other two:

- **`nano`**, a minimal editor inside the terminal, always present: `nano note.txt`, type, ++ctrl+o++ then ++enter++ to save, ++ctrl+x++ to leave. Its shortcuts are odd, but it is on every Linux machine you will ever log into, so know these three keys.
- **`micro`**, the same idea with the shortcuts you already know — ++ctrl+s++ save, ++ctrl+q++ quit, ++ctrl+z++ undo, ++ctrl+c++ / ++ctrl+v++ copy and paste, ++ctrl+f++ find, mouse and ++shift++-arrows to select. Install it once, then use `micro` wherever this site says `nano`:

    ```bash title="Ubuntu window (WSL)"
    sudo apt update && sudo apt install -y micro
    micro note.txt
    ```

    (Ubuntu's package is version 2.0.13; the project lives at [github.com/micro-editor/micro](https://github.com/micro-editor/micro). On a Mac: `brew install micro`.)
- **VS Code**, a real editor: install [VS Code](https://code.visualstudio.com/download) *on Windows*, then inside it install the extension named **WSL** (by Microsoft). From then on, typing `code .` in an Ubuntu terminal opens the current Linux folder in VS Code, with a built-in Ubuntu terminal at the bottom. Reference: [Get started using VS Code with WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode).

## Managing WSL itself (from PowerShell)

These are typed in a normal PowerShell window, not in Ubuntu:

| Command | What it does |
|---|---|
| `wsl --list --verbose` | Which distributions are installed and whether they are running |
| `wsl --update` | Update WSL itself (fixes many odd problems) |
| `wsl --shutdown` | Stop all Linux machines (the next Ubuntu window starts fresh) |
| `wsl --unregister Ubuntu` | **Deletes Ubuntu and every file in it.** Only for starting over; back up first. |

Forgot your Linux password? In PowerShell, `wsl -u root` opens Ubuntu as the administrator; then `passwd lea` (your Linux user name) lets you set a new one. Details in Microsoft's [set up a WSL development environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment).

## Virtualization must be enabled

WSL runs Ubuntu as a lightweight virtual machine, which needs a CPU feature that some laptops ship switched off. It is the most common install failure, and it cannot be fixed from software.

1. Press ++ctrl+shift+esc++ (Task Manager) → **Performance** → **CPU**.
2. Bottom right: **Virtualization: Enabled** or **Disabled**.

If **Disabled**: reboot into the BIOS/UEFI settings (usually a key like ++f2++, ++f10++, ++del++ or ++esc++ during startup — the exact key depends on the brand) and enable the option called *Intel VT-x*, *AMD-V*, *SVM Mode* or *Virtualization Technology*. If that is not something you want to do alone, bring the laptop to Session 1 and use [Git Bash](setup.md#path-d-git-bash) or [Codespaces](setup.md#path-c-github-codespaces-the-lifeboat) meanwhile.

## When it fails

| What you see | Meaning | What to do |
|---|---|---|
| `0x80370102` | Virtualization is off (BIOS) or the *Virtual Machine Platform* Windows feature is disabled | Check the section above. If Task Manager says *Enabled*, open Start → *Turn Windows features on or off* → tick **Virtual Machine Platform** and **Windows Subsystem for Linux** → reboot. |
| `0x8007019e` | The WSL optional component is not enabled | Same fix: tick both features, reboot, `wsl --install` again. |
| `0x80070003` | The distribution must be installed on the system drive (`C:`) | Free up space on `C:`. |
| Download stuck at `0.0%` | Store download blocked (VPN, proxy, network) | `wsl --install --web-download -d Ubuntu` in admin PowerShell. |
| "no installed distributions" after the install (typical on a fresh Windows 11 24H2) | WSL is there but Ubuntu is not | `wsl --install -d Ubuntu` in admin PowerShell. |
| `wsl --install` does nothing useful on Windows 10 | Build older than 19041 (check with ++win+r++ → `winver`) | Update Windows, or use Codespaces. |
| `uname : The term 'uname' is not recognized` | You are in PowerShell, not Ubuntu | Start → Ubuntu. |
| Anything else | | `wsl --update` in admin PowerShell, reboot, retry. Keep the exact message for Session 1. |

Known non-starters: WSL 2 cannot run inside a VirtualBox VM; some corporate VPNs break WSL networking (disconnect the VPN to test).

## Going further

- [Microsoft — Working across file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems) — the source for the bridges above, plus running Windows tools from Linux (`notepad.exe`) and Linux tools from PowerShell (`wsl ls`).
- [Microsoft — Best practices for setting up a WSL development environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment).
- [Microsoft — Troubleshooting WSL](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting).
- [The Missing Semester — The Shell](https://missing.csail.mit.edu/) — the first lecture is exactly what to watch after this page.
