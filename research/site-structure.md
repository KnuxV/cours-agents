# Site structure: three kinds of page, exercises one click away, no dates

Task: fix navigation on `site/`. Students said exercises are hard to find; the instructor wants
**knowledge/reference**, **lessons/slides** and **exercises** clearly separated, and everything
keyed to a calendar date removed because the NLP and economics cohorts advance at different speeds.
Implemented in the working tree, not committed. This note is the proposal, the record of judgment
calls, and the drop-in point for the ported material from last year's site.

Scope respected: `site/` only, plus this file. `SPEC.md`, `tasks/`, `slides/`, `resources/`,
`package.json` and `research/old-site-port/` untouched. No page's prose was rewritten — what
changed is nav, titles, index/landing pages, cross-links, date lines, and short orientation
paragraphs. `sessions/s2.md`'s section numbering and anchors are untouched (only its first three
lines and its "exercises of this session" box changed, no heading).

---

## 1. The shape: three top tabs, plus Home

`navigation.tabs` is switched on, so every page of the site now carries the same four tabs in its
header. That is what makes the three kinds of page separate *and* makes exercises reachable from
anywhere in one click.

| Tab | URL | What lives there |
|---|---|---|
| Home | `/` | the pitch, the order of the sessions, the list of exercises |
| Sessions | `/sessions/` | one lesson page per session — what happens in a class |
| ✏️ Exercises | `/exercises/` | the 11 exercise pages, grouped by topic |
| Reference | `/reference/` | the durable material, not tied to a session |

Each tab is a *section index page* (`navigation.indexes`), so clicking the tab lands on a real page
rather than on the first child: `/sessions/` is the roadmap, `/exercises/` is the exercise index
(the deep link students were already given), `/reference/` is the reference hub.

### Before

```
Home
Session 0 — Setup (homework)      Lesson — Setup / Lesson — WSL, explained / ✏️ 0.1
Session 1 — Git                   Lesson — Git / Reading — S1½ / ✏️ 1.1 / ✏️ 1.2 / ✏️ 1.3 / ✏️ Extra
Session 2 — Python tooling        Lesson — Python tooling / ✏️ 2.1 … ✏️ 2.5
Session 3 — What an LLM API is    Lesson
Session 4 — pi                    Lesson
▶ Today — Fri 18 Sep              Start here — plan for today / pi — install, API connection, tutor
✏️ All exercises
Resources
Replication track (optional)
```

Eleven top-level entries, exercises interleaved with lessons, a dated section holding one cohort's
plan for one past class, and the `pi` install guide filed under that date.

### After

```
Home                                   index.md

Sessions                               sessions/index.md        (tab landing: the roadmap)
  Session 0 — Set up your machine      setup.md
  Session 1 — Git
    Lesson — Git                       sessions/s1.md
    Class plan — tutor, then three     sessions/practice-git.md
      exercises
  Session 2 — Python tooling           sessions/s2.md
  Session 3 — What an LLM API is       sessions/s3.md
  Session 4 — pi, a real harness       sessions/s4.md
  Optional — Replication track         replication.md

✏️ Exercises                           exercises/index.md       (tab landing: the index)
  Terminal
    0.1 Ten minutes in the terminal    exercises/terminal.md
  Git
    1.1 Recipe history                 exercises/recipe.md
    1.2 Scrabble — merge and conflict   exercises/scrabble.md
    1.3 Collaboration, in teams of two  exercises/collab.md
    Extra — three merges in a row      exercises/scrabble-three-merges.md
  Python tooling
    2.1 A uv project from scratch      exercises/uv-project.md
    2.2 Notebook → script with argparse exercises/argparse-script.md
    2.3 Password generator             exercises/password-generator.md
    2.4 Secret hygiene audit           exercises/secret-audit.md
    2.5 Polars vs pandas               exercises/polars-pandas.md

Reference                              reference/index.md       (tab landing: the hub)
  Machines and terminals
    WSL, explained                     reference/wsl.md
  Git
    Git as a collaboration tool        reference/git-collaboration.md
  Agents and tools
    pi — install, connect, tutor       reference/pi.md
  Files and configs                    resources.md
```

`navigation.sections` is kept, so the groups inside a tab render expanded: on the Exercises tab all
eleven exercises are visible at once, under their topic.

---

## 2. Exercise discoverability

Five routes to an exercise, deliberately redundant:

1. **The ✏️ Exercises tab**, on every page of the site. One click to the index, one more to the
   exercise — and from the index's sidebar, one click straight to any of the eleven.
2. **The home page** has its own `## Exercises` section listing all eleven, grouped by topic, and
   the session table's *Exercises* column now links each one individually (it used to collapse S2's
   five into "2.1–2.5").
3. **Each session lesson page** opens with an "The exercises of this session" admonition listing its
   exercises by name. `setup.md` (Session 0) gained the same pointer to 0.1, which it did not have.
4. **The `/sessions/` roadmap** lists each session's exercises.
5. **Search** — unchanged plugin, plus `search.highlight` so a hit is highlighted on arrival.

`exercises/index.md` was rewritten as a hub (structure only — no exercise statement was touched):
grouped by topic instead of one flat table, a *What you practise* column so the topic of each one is
legible without opening it, the time, the lesson to lean on per group, and a "when you are stuck, in
this order" box (statement → lesson → tutor → hand) lifted from the old `today.md`.

**Trade-off to be aware of.** MkDocs attaches a page to its *last* nav entry, so an exercise page
cannot appear both under its session and under the Exercises tab. I chose the Exercises tab, which
is the opposite of the 2026-09-18 decision that put exercises in each session's sidebar section. The
reason: that arrangement is the one students called hard to navigate, it mixes the three kinds of
page the instructor wants separated, and it only ever showed exercises to someone already looking at
a session. The per-session listing survives as the admonition at the top of each lesson page (which
is a link students actually see in the body text, not a sidebar entry they scroll past). **Overrule
this if you prefer the sidebar grouping** — it is one nav block to move back, at the cost of the
Exercises tab becoming a flat list of eleven pages with nothing under it.

**Difficulty.** Not implemented as labels. `[core]`/`[stretch]`/`[home]` tags were deliberately
removed on 2026-09-18, so re-adding per-exercise difficulty tags (or the Material `tags` plugin,
which is the same idea with an index page) would reverse a decision without being asked to. Instead
the index says the exercises within a topic are in order of difficulty, keeps the minutes, and marks
the two optional ones the pages already call optional ("Extra — … if you are ahead"). If you want
difficulty back, the cheapest form is one extra column in `exercises/index.md` and nothing on the
exercise pages themselves.

---

## 3. De-dating

Removed from the site (nothing else on the site carried a date):

| Was | Now |
|---|---|
| `index.md` tip box "Class of Friday 18 September" | tip box "Three kinds of page, three tabs at the top" — the orientation students actually need on arrival |
| `index.md` `## Schedule` with a *When* column (4 dates + times) and "All sessions take place in room A330" | `## The four sessions, in order` with an *Order* column, and one sentence saying the site is keyed to content because two cohorts advance at different speeds, so dates and rooms are announced in class |
| `setup.md` "before Session 1 (Monday 14 September 2026)" | "before the first class" |
| `sessions/s1.md` "Monday 14 September 2026, 14:00–16:00, room A330" | "Two hours in class. The first session of four; Session 0 is the homework that comes before it." |
| `sessions/s2.md` "Friday 18 September 2026, 15:00–17:00, room A330" | "Two hours in class. The second session of four; it happens inside the repository you created in Session 1." |
| nav section "▶ Today — Fri 18 Sep" | gone |

Two date-like strings were left alone on purpose: `sessions/s2.md` §4.3 uses "on 18 September 2026
that resolved to polars 1.44.1" as the *illustration* of what a lockfile records, which is content,
not scheduling; and `reference/pi.md` records the date a rehearsal was done, which is a verification
note.

### What happened to `today.md`

It became **`sessions/practice-git.md`**, titled *"Class plan — the tutor, then three Git
exercises"*, filed in the nav under Session 1 as "Class plan — tutor, then three exercises", with
`/today/` redirecting to it. Nothing was cut: the five pi/tutor setup steps, the three exercises with
their "lesson to lean on" pointers and their "start pi in this folder" notes, and the
"if something breaks" triage table are all still there. Only the date, the room, the times ("not
finished at 17:00" → "when the class ends") and the two uses of the word "today" changed.

This is the third of the three options in the task — a content-keyed page rather than a per-cohort
"current class" page — because its three exercises *are* Session 1's three exercises, so the page is
"the plan for the practice half of the Git class", which is true for both cohorts. It is reusable as
it stands, and it also reads correctly for a student working alone at home.

**Judgment call to overrule:** if you want a page you overwrite per cohort before each class ("what
we are doing today, room X"), this is not it — this one is meant to be stable. The cheap version of
that is a new `sessions/next-class.md` in the Sessions tab, kept to a few lines pointing into the
lesson and exercise pages, so overwriting it never destroys material. I did not create it because
there is no content for it and an empty page is worse than no page.

---

## 4. Knowledge/reference as its own section

`reference/` is a new folder and a new tab, with `reference/index.md` as its hub. Three pages moved
into it, each with a redirect from its old path:

| Old URL | New URL | Why it is reference, not a lesson |
|---|---|---|
| `/wsl/` | `/reference/wsl/` | answers "what is WSL, where are my files", consulted for weeks after Session 0 |
| `/pi/` | `/reference/pi/` | a tool install guide, used from the Git practice class onwards and studied in Session 4 — it was filed under "▶ Today", which is exactly the mislabelling the instructor described |
| `/sessions/s1-collab/` | `/reference/git-collaboration/` | it was never a class: it is the 40-minute home reading on remotes, forks, PRs, issues and CI |

`resources.md` (the files-and-configs page) is listed in the Reference tab but kept at `/resources/`;
its stub is still a stub, reworded to say what it will hold and where to look meanwhile.

The two directions of the session↔reference link are now explicit:

- **Session → reference.** `sessions/s1.md`'s exercise box names *Git as a collaboration tool* as the
  reference material the session leads to; `setup.md` sends Windows users to *WSL, explained* (as
  before); `/sessions/` names the reference page of each session; `sessions/s4.md` points at
  *pi — install, connect, tutor*.
- **Reference → session.** `reference/index.md` has an *Introduced in* column for every page, and
  each reference page's first paragraph now says which session it belongs to.

`reference/index.md` ends with a note saying the section is growing and names the material coming
from last year's site, so the page does not look thin while the port is in flight.

### Page titles changed

- `# Session 1½ — Git as a collaboration tool` → `# Git as a collaboration tool` (a reference page
  should not be numbered like a class). The three in-site references to "Session 1½" / "S1½" were
  reworded to name the page instead. Its subtitle still says it is the companion reading to
  Session 1, to do at home after it.
- `# Today — Friday 18 September` → `# Class plan — the tutor, then three Git exercises`.
- Nav labels only: "Session 3 — What an LLM API is", "Session 4 — pi, a real harness",
  "Files and configs" for `resources.md`.

The four "not built yet" stubs (`sessions/s3.md`, `sessions/s4.md`, `resources.md`,
`replication.md`) were reworded because they told students about "Task 02", which is internal
vocabulary. They now say what the page will hold and where to go meanwhile.

---

## 5. Config changes

`site/mkdocs.yml`:

- theme features added: `navigation.tabs`, `navigation.indexes`, `navigation.tracking`,
  `navigation.footer` (prev/next links at the bottom of every page — useful for a lesson read in
  order), `search.highlight`. Kept: `navigation.sections`, `navigation.top`, `toc.follow`,
  `content.code.copy`, `content.tabs.link`.
- `plugins:` block added. Because naming `plugins` disables the implicit default, `search` is listed
  explicitly alongside `redirects`.
- `redirect_maps`: `wsl.md`, `pi.md`, `sessions/s1-collab.md`, `today.md`.

`site/requirements.txt`: `mkdocs-redirects==1.2.3` added (latest on PyPI today, pinned like
`mkdocs-material`). `.github/workflows/site.yml` installs from this file, so CI picks it up with no
workflow change.

No markdown extension, no `validation:` setting and no palette changed.

---

## 6. Deliberately not done

- **No `tags` plugin, no per-exercise difficulty tags** — see §2. Tags were removed once on purpose.
- **No move of `setup.md`, `sessions/s1.md`, `sessions/s2.md` or any `exercises/*.md`.** These carry
  the deep links students have (`/setup/`, `/exercises/`, `/sessions/s2/#3-install-uv`,
  `/sessions/s2/#9-when-things-go-wrong`, and every `#21-…`-style exercise anchor). Their URLs and
  anchors are byte-identical to before.
- **No split of any long page.** `sessions/s1.md` (4.7k words) and `sessions/s2.md` (5.2k words) are
  long, and a class using s2 is imminent. Splitting them would break anchors and would be content
  work, not navigation work. A reasonable later move is to lift the cheat sheets (`s1.md` §7,
  `s2.md` §10) into a single reference page — but that must be a deliberate decision, with redirects
  for the anchors.
- **No cohort split of the site** (no `/nlp/` and `/eco/` trees). The instructor's stated problem is
  that the cohorts advance at different *speeds*, not that they read different material; two trees
  would double the maintenance and split the search index.
- **No `navigation.expand`, no `toc.integrate`, no instant navigation.** `toc.integrate` is
  incompatible with `navigation.indexes`; the others add nothing here.
- **No blog/news page** for "what we did last class". If that is wanted, it is a dated artefact and
  the instructor's own call.

---

## 7. Verification

- `cd site && uv run --with mkdocs-material==9.7.7 --with mkdocs-redirects==1.2.3 mkdocs build --strict`
  → exit 0, no MkDocs warnings. (`validation.anchors: warn` plus `--strict` means every internal
  link *and* every `#anchor` in the site is checked; the only console noise is the upstream
  "MkDocs 2.0" banner Material prints on every build, silenced with `DISABLE_MKDOCS_2_WARNING=true`.)
- Nav read back from the built HTML: four tabs (`Home`, `Sessions`, `✏️ Exercises`, `Reference`)
  pointing at `.`, `sessions/`, `exercises/`, `reference/`; the sidebar trees match §1 exactly,
  including all eleven exercises under their three topic headings.
- Old deep links: `/exercises/`, `/setup/`, `/sessions/s2/#3-install-uv`,
  `/sessions/s2/#9-when-things-go-wrong` resolve unchanged (anchors present in the built HTML);
  `/pi/`, `/wsl/`, `/today/`, `/sessions/s1-collab/` are redirect pages. mkdocs-redirects writes a
  `<script>` that carries the fragment across, so `/pi/#2-install-pi` also lands on the right
  section.
- `pymdownx.snippets` still inlines `resources/pi/models.json` into the moved `reference/pi.md`
  (`base_path` is relative to `mkdocs.yml`, so the move is harmless), and the six mermaid diagrams
  on `sessions/s1.md` still render as `class="mermaid"` blocks.
- Every internal link in the repo was re-listed after the moves and checked; no reference to
  `wsl.md`, `pi.md`, `today.md` or `s1-collab.md` is left.

---

## 8. UNVERIFIED

1. **Nothing was looked at in a browser.** The nav was read out of the generated HTML, not seen
   rendered. `navigation.tabs` changes the header on every page and the drawer on phones; page
   through the built site once (`mkdocs serve`) before deploying, especially on a narrow window.
2. **The redirects have never been served from GitHub Pages** in this repo — they are plain HTML
   files, which is as safe as it gets, but the first deploy is the proof. Until the site is
   redeployed, `/pi/` on the published site is still the old page.
3. **`mkdocs-redirects==1.2.3` has not run in CI** here, only locally under `uv`. It requires
   Python ≥ 3.10; the workflow uses 3.12.
4. Whether any student was given `/wsl/`, `/today/` or `/sessions/s1-collab/` as a deep link is
   unknown; all four old paths are redirected regardless.
5. `resources.md` claims the practice-site files and `report.py`/`sales.csv` are reachable from the
   session pages — true today (`sessions/s1.md` §4.1, `sessions/s2.md` §5.2), but that page is still
   a stub and will need rewriting when the real resource list exists.
6. Pre-existing `TODO(verify)` / `TODO:` markers on the site were left exactly as they were (forum
   link and exam rubric on the home page, the `check-setup.sh` link, the 2.4 starter repo, the pi
   install rehearsal on an A330 desktop). This task did not resolve any of them.

---

## 9. Follow-ups

### Where the ported material from last year's site lands

The port (`lessons/06-organization_packaging`, `lessons/07-arguments` and the rest of
`KnuxV/advanced_programming_python`) is **reference material**, so it goes under
`site/docs/reference/` — one file per topic, a topic name rather than a lesson number as the
filename. The nav has room for it: add a `Python` group to the Reference tab, between `Git` and
`Agents and tools`:

```yaml
      - Python:
          - Modules, packages and imports: reference/python-packaging.md
          - Command-line arguments: reference/python-arguments.md
```

Each ported page needs two things to fit the structure, both cheap:

1. a first line saying which session introduces it and what it answers, the way `reference/wsl.md`
   and `reference/git-collaboration.md` now do;
2. a row in the matching table of `reference/index.md`, with its *Introduced in* cell — and the
   "This section is growing" note at the bottom of that page removed once the port has landed.

The session pages should then point *into* it: `sessions/s2.md`'s planned §5.4–5.6 (the
script/module/library rung from the `slides/s2-tooling.md` deck) is the obvious first inbound link,
and adding it inside section 5 keeps every existing anchor — which is what the 2026-09-24 LOG entry
already planned.

### Smaller ones

- `sessions/s3.md` and `sessions/s4.md` are still stubs; when they are written, their exercises get a
  `Session 3` / `Session 4` group in the Exercises tab and a row each in `exercises/index.md` §
  "Sessions 3 and 4" (which currently says they are published with the sessions).
- Consider lifting the two cheat sheets into one `reference/git-and-python-cheatsheet.md`; needs
  redirects for `#7-cheat-sheet` and `#10-cheat-sheet`, so not done here.
- `sessions/practice-git.md`'s Part 1 (the five pi/tutor setup steps) duplicates `reference/pi.md` in
  checklist form. If a second practice class wants the same checklist, extract Part 1 into
  `reference/pi.md` as a numbered "setup checklist" section and have both class plans link it, rather
  than copying the page.
- The forum link and exam rubric on the home page are still `TODO`.
- Nothing in `slides/` was touched, so the decks still carry whatever dates they carry; the S0 deck
  deliberately has none.

### For `tasks/LOG.md` (to be written by the main session, not by this run)

Produced: `site/mkdocs.yml` restructured to four tabs with section index pages and a
`redirects` plugin; new `site/docs/sessions/index.md` and `site/docs/reference/index.md`;
`wsl.md`, `pi.md` and `sessions/s1-collab.md` moved into `reference/` (the last renamed
`git-collaboration.md`), `today.md` moved to `sessions/practice-git.md` and de-dated, all four with
redirects from their old paths; `index.md` and `exercises/index.md` reworked as landing pages;
dates removed from `index.md`, `setup.md`, `sessions/s1.md`, `sessions/s2.md`; the four
"not built yet" stubs reworded; `mkdocs-redirects==1.2.3` added to `site/requirements.txt`.
Verification and UNVERIFIED items: §7 and §8 above. Needs human review: §2 (exercises in their own
tab instead of in each session's sidebar), §3 (`today.md` recast as a stable class plan rather than
a per-cohort page), and the browser pass of item 1 in §8.
