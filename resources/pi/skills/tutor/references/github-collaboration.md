# GitHub: remotes, forks, pull requests

Course pages: <https://knuxv.github.io/cours-agents/sessions/s1/> section 6 (publishing the course repository) and <https://knuxv.github.io/cours-agents/sessions/s1-collab/> (remotes, clone vs fork, pull requests, issues, CI).

## The mental model the course uses

- Git runs on the student's machine; GitHub is one place where a copy of the repository lives. `origin` is just the conventional name for that copy: `git remote -v` shows the address behind the name.
- `git push` sends commits to the remote, `git pull` brings the remote's new commits back. Only commits travel: uncommitted work stays local.
- **Clone** is a copy on your machine. **Fork** is a copy on GitHub under your account, which you then clone. You can always push to your fork; you send changes back to the original through a **pull request**: a proposal to merge one branch into another, with a discussion and a review attached.
- A fork conventionally gets a second remote, `upstream`, pointing at the original.

## Course conventions

- The student's course repository is `agent-lab`, in their home folder, published at `https://github.com/<username>/agent-lab`.
- HTTPS addresses, with login through the GitHub CLI: `gh auth login` → GitHub.com → HTTPS → authenticate Git: Yes → login with a web browser. On Git Bash the first `git push` opens a browser sign-in instead. In Codespaces nothing is needed.
- The GitHub repository is created **empty** (no README, no `.gitignore`, no licence), then `git remote add origin <url>` and `git push -u origin main`.
- University Linux desktops have no `sudo`: `gh` is unpacked into `~/.local` (S1 section 6.2, Linux tab).

## Usual stumbles

| What the student sees | Where to point them |
|---|---|
| `git push` asks for a username and password | GitHub refuses account passwords from git. Was `gh auth login` done? (setup breakage, give it directly: S1 section 6.2) |
| `remote: Permission to KnuxV/... denied` (403) | `git remote -v`: whose repository is `origin`? They cloned the original instead of their fork |
| `! [rejected] main -> main (fetch first)` | The remote has commits they do not have. Where could those come from (a README ticked at creation, an edit on the website)? Then `git pull --no-rebase origin main` |
| `fatal: remote origin already exists` | `git remote -v` shows the current address; `git remote set-url origin <url>` changes it |
| `fatal: 'origin' does not appear to be a git repository` | `git remote -v` is empty: the remote was never added |
| `src refspec main does not match any` | `git log`: is there a commit yet? `git branch`: is the branch called `master`? |
| Their work is not on the GitHub page after `git push` | `git status`: was it committed? Which branch was pushed, and which one is the page showing? |
| Pull request says "can't automatically merge" | Same conflict as a local merge: merge `main` into the branch locally, resolve, push |

## Exercises

- **1.1 Your course repository on GitHub.** Done when `https://github.com/<username>/agent-lab` shows their files and at least four commits, `git status` says `working tree clean`, and `git log --oneline` lists the same commits as the GitHub page.
- **2.3 part A.** Fork `KnuxV/password-generator` with the **Fork** button, clone *the fork* into the home folder (not inside `agent-lab`), `uv sync`. Check with `git remote -v`: `origin` must contain the student's username.
- **Optional practice of pull requests:** GitHub Skills, "Introduction to GitHub" (<https://github.com/skills/introduction-to-github>): a bot guides branch → commit → pull request → merge.
