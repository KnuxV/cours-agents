# Research note — Session 0: environment setup

Verified 2026-08-28 against live sources. Status legend: VERIFIED / UNVERIFIED / WRONG.

## 1. Claims check

| Claim in SPEC (Session 0) | Status | Evidence |
|---|---|---|
| Windows: `wsl --install` in admin PowerShell, reboot, create Ubuntu user | VERIFIED | [MS Learn: Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) — one command, installs Ubuntu on WSL 2 by default, restart required, username/password prompted on first launch. Prerequisite: Windows 10 2004+ (build 19041) or Windows 11. |
| Current WSL install behaviour | VERIFIED | WSL is now shipped as its own package (latest release 2.7.12, 2026-08-18, [github.com/microsoft/WSL/releases](https://github.com/microsoft/WSL/releases)); `wsl --update` updates it independently of Windows. |
| Known WSL failure modes | VERIFIED (modes) / UNVERIFIED (rates) | From [MS troubleshooting page](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting): `0x80370102` = virtualization disabled in BIOS/UEFI or "Virtual Machine Platform" feature off (the #1 student-laptop case); `0x80070003` = distro must live on the system drive; `0x8007019e` = WSL optional component not enabled; install hanging at 0.0% → `wsl --install --web-download -d Ubuntu`; "no installed distributions" after a clean 24H2 install ([MS Q&A](https://learn.microsoft.com/en-us/answers/questions/2190233/wsl-distro-fails-to-install-windows-11-24h2)); WSL 2 cannot run inside VirtualBox; corporate VPN breaks networking. **No published failure-rate statistics exist**; plan on the BIOS-virtualization case being the common one. |
| Mac: nothing to install | VERIFIED | macOS ships `curl`, `uname`, `git` (git triggers an Xcode Command Line Tools prompt on first use — expect a 5–10 min download; note this in setup.md). |
| Deliverable command `uname -a && curl --version \| head -1` | VERIFIED with caveat | Works in WSL Ubuntu, macOS Terminal and Git Bash. **It does not work in PowerShell** (`uname` absent). The instructions must say "inside the Ubuntu window", not "in PowerShell". |
| Fallback: Git Bash + Scoop | VERIFIED (exists) / UNVERIFIED (course viability) | [gitforwindows.org](https://gitforwindows.org/) ships bash + curl; [scoop.sh](https://scoop.sh/) can install `jq`, `uv`, `presenterm`, `opencode`. But OpenCode docs state Windows has **no native support; WSL recommended** ([opencode.ai/docs](https://opencode.ai/docs/)). Git Bash should be a Session 1–3 fallback only; Session 4 on Git Bash is untested. |
| Windows has `curl` natively | VERIFIED | Since Windows 10 1803 ([MS DevBlog](https://devblogs.microsoft.com/commandline/tar-and-curl-come-to-windows/)) — a student can curl the API from PowerShell even if WSL fails (note: PowerShell aliases `curl` to `Invoke-WebRequest`; use `curl.exe`). |
| Fallback: GitHub Codespaces | VERIFIED | Free plan: 120 core-hours + 15 GB-month per month ([billing docs](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)); [quickstart](https://docs.github.com/en/codespaces/getting-started/quickstart). Extra quota for students via [GitHub Education](https://education.github.com/pack): page live, exact Codespaces bonus UNVERIFIED. |
| Unistra key: log in → Profil → Réglages → Compte → generate key (`sk-...`) | VERIFIED | Unistra doc [7_1API.html](https://documentation.unistra.fr/DNUM/Intelligence_artificielle/guide_complet_IA/co/7_1API.html): « Profil → Réglages → Compte → Afficher ou Générer une nouvelle clé », eye icon to reveal, copy button. Base URL given there: `https://conversation.ia.unistra.fr/api`, models at `/api/models`. Warning quoted: « Ne stockez jamais votre clé API dans du code source visible publiquement ». |
| One key per account / regeneration invalidates old key | UNVERIFIED | Stated for Open WebUI generally ([Open WebUI API keys doc](https://docs.openwebui.com/features/authentication-access/api-keys/), page live); not tested on Unistra. Matters if a student leaks a key: regenerate = rotate. |
| Students (M2) have access to the platform | UNVERIFIED | Docs describe SSO login for university accounts; I could not confirm student (vs staff) eligibility. **Check before publishing setup.md.** |
| Light terminal practice (mv, cp, ls, pwd) | n/a | Content decision; resources below. |

## 2. Best deeper-dive resources

1. [The Missing Semester of Your CS Education (MIT)](https://missing.csail.mit.edu/) — lecture 1 (shell) + 2 (shell tools) are the best 2 hours of terminal onboarding in existence; free videos + notes.
2. [Software Carpentry: The Unix Shell](https://swcarpentry.github.io/shell-novice/) — workshop-tested for researchers who have never opened a terminal; the exact audience.
3. [MS Learn: Best practices for setting up a WSL dev environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment) — username/password step, Windows Terminal, where to keep files (inside the Linux filesystem, not `/mnt/c`).
4. [GitHub Codespaces quickstart](https://docs.github.com/en/codespaces/getting-started/quickstart) — the lifeboat, 10 minutes to a working terminal in a browser.
5. *Ambitious:* [Julia Evans — "Oh shit, git!"](https://ohshitgit.com/) is for S1, but her free zine excerpts on the shell are linked from the Missing Semester page; pair with `man` pages as a habit.

## 3. Pedagogical risks

- **BIOS virtualization off** (error 0x80370102): needs a reboot into UEFI settings; impossible to fix remotely over a forum. Mitigation: the setup page must show the Task Manager → Performance → "Virtualization: Enabled/Disabled" check *first*, before `wsl --install`, and the install clinic must be scheduled with hardware in the room.
- **Locked-down / managed laptops** (no admin rights) cannot run `wsl --install`. Mitigation: Codespaces path, documented as a first-class option not a shameful fallback.
- **Old Windows 10 builds** (< 19041) fail silently on `wsl --install`. Mitigation: ask students to post `winver` output with their deliverable.
- **PowerShell confusion**: the deliverable command fails in PowerShell, so students will post errors that aren't errors. Mitigation: screenshot of the Ubuntu window in setup.md; say "the window whose prompt ends in `$`".
- **Key hygiene on day 0**: students will paste `sk-...` keys into the forum. Mitigation: deliverable is the `uname`/`curl` output only; the key check is `echo $UNISTRA_API_KEY | cut -c1-6` (prints `sk-XXX…`), never the key.
- **Xcode CLT download on Macs** eats the first 10 minutes of Session 1 if not done at home. Mitigation: add `git --version` to the Mac deliverable.

## 4. Suggested spec edits

- Session 0, Windows bullet: `- Windows: install WSL (...)` → add « Before installing: open Task Manager → Performance → CPU and confirm "Virtualization: Enabled"; if Disabled, enable it in BIOS/UEFI or come to the clinic. »
- Session 0 deliverable: change `Post output of uname -a && curl --version | head -1` → « Post output of `uname -a && curl --version | head -1`, run **inside the Ubuntu window** (Windows) or Terminal (Mac); Mac also `git --version` ».
- Session 0 fallbacks: `Git Bash + Scoop` → « Git Bash + Scoop (Sessions 1–3 only; OpenCode is not supported natively on Windows — Session 4 requires WSL or Codespaces) ».
- Session 0, key bullet: add « Never post the key. Deliverable for the key is `echo $UNISTRA_API_KEY | cut -c1-6`. »
- Add to Known risks: « Student (not staff) eligibility for conversation.ia.unistra.fr API keys — confirm with DNUM before Session 0. »
