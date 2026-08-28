# Research note — Session 1: Git

Verified 2026-08-28. Status legend: VERIFIED / UNVERIFIED / WRONG.

## 1. Claims check

| Claim in SPEC (Session 1) | Status | Evidence |
|---|---|---|
| Content available in `~/Codebase/fake-website-to-teach-git/` | VERIFIED | Exists locally: `docs/`, `exercises/`, `practice-site/`, `MISSION.md`, `NOTES.md`, `RESOURCES.md`. `RESOURCES.md` already contains a curated, previously-verified source list (Pro Git chapters, Software Carpentry episodes, GitHub docs) — reuse it rather than re-deriving. |
| init, add, commit, log, diff; snapshots mental model | VERIFIED | Canonical treatment: [Pro Git §1.3 "What is Git?"](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F) (snapshots, not differences). Page live. |
| Branching lightly; clone/push/pull with GitHub | VERIFIED | [Pro Git: Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging); GitHub account creation is free, no card. `git push -u origin main` requires a credential helper on first push — HTTPS + Git Credential Manager opens a browser login (WSL Ubuntu: GCM is **not** installed by default; students must either install it or use a Personal Access Token — see risks). |
| "Version control is the undo button and audit trail for agent-written code" | VERIFIED (practice) | OpenCode docs describe snapshots/undo via git internally; Cunningham's hooks post (free) argues the same for research code: [causalinf.substack.com/p/how-and-why-i-am-using-hooks-part](https://causalinf.substack.com/p/how-and-why-i-am-using-hooks-part). Anthropic's [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) recommends working in a git repo. |
| "Agents work best inside a git repo" | VERIFIED (OpenCode) | OpenCode looks for the project root via git and reads `AGENTS.md` from it ([opencode.ai/docs/rules](https://opencode.ai/docs/rules/)); tested locally: `opencode run` inside a fresh `git init` directory worked (see s4 note). |
| Exercise: create the personal course repo used in S3–S4 | n/a | Design decision; consistent with S3/S4 deliverables. |

## 2. Best deeper-dive resources

1. [Pro Git, 2nd ed.](https://git-scm.com/book/en/v2) (Chacon & Straub, free) — chapters 1–3 are the reference; point students at §2 "Git Basics" and §3.1–3.2 only.
2. [Learn Git Branching](https://learngitbranching.js.org/) — interactive commit-graph visualizer; the fastest way to make "branch = pointer" click. Do the first "Introduction Sequence" in class if time allows.
3. [Software Carpentry: Version Control with Git](https://swcarpentry.github.io/git-novice/) — peer-reviewed novice curriculum for researchers; steal its pacing (init→add→commit before any branching).
4. [Oh Shit, Git!?!](https://ohshitgit.com/) (Julia Evans / Katie Sylor-Miller) — the recovery cheat-sheet; exactly what students need after an agent commits garbage.
5. *Ambitious:* [GitHub Skills — Introduction to GitHub](https://github.com/skills/introduction-to-github) (hands-on, automated feedback, ~1h) then [How to Write a Git Commit Message](https://cbea.ms/git-commit/) — the norms an agent should be told to follow in `AGENTS.md`.

(Also live and useful: [Oh My Git!](https://ohmygit.org/), a desktop game — optional.)

## 3. Pedagogical risks

- **First push authentication** is the classic 20-minute sinkhole: GitHub rejects passwords; WSL has no credential manager by default; students end up creating PATs with the wrong scopes. Mitigation: pre-write the exact steps for one path only (recommended: `gh auth login` via GitHub CLI, or install GCM in WSL) and rehearse it on a clean WSL. Mark as TODO(verify) in the site until rehearsed.
- **`git config user.name/email` unset** → the first commit errors with a wall of text. Mitigation: make it step 1 of the exercise.
- **Line endings / CRLF warnings** on Windows (Git Bash path) confuse beginners. Mitigation: WSL path avoids it; on Git Bash choose "checkout as-is, commit as-is" during install (Software Carpentry setup episode has the installer screenshots).
- **Editor trap**: `git commit` without `-m` opens vim/nano. Mitigation: always `-m` in Session 1; set `git config --global core.editor nano` in the setup exercise.
- **Time**: 2h for init→push including account creation is tight for terminal-first-timers. Mitigation: GitHub account creation goes into Session 0 homework.

## 4. Suggested spec edits

- Session 1: « clone/push/pull with GitHub (account creation = course outcome) » → « (GitHub account creation moves to Session 0 homework; Session 1 = first push) ».
- Session 1, add bullet: « Authentication path fixed in advance: HTTPS + `gh auth login` (or GCM) — one documented path, rehearsed on clean WSL. »
- Session 1, exercise: add « configure `user.name`, `user.email`, `core.editor nano` as step 1 ».
- Session 1, agent-era bullet: add the concrete rule students will reuse in S4: « commit before letting an agent touch the repo; `git diff` is how you review what it did ».
