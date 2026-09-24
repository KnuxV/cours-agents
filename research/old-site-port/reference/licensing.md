<!--
PORTED FROM last year's material (KnuxV/slides_cours_git):
  "Part 14 - licensing.md" (850 lines) — why licences matter, the default all-rights-reserved state,
  MIT / Apache 2.0 / GPL v3 / AGPL / Unlicense, copyright vs patents, licence compatibility,
  the free-software vs open-source split, who actually writes open source, the service model,
  "open source AI", and how to add a LICENSE on GitHub.
  "Part 15 - exam.md" — licence choice was worth 1 point of last year's mark, with a justification.

PROPOSED DESTINATION: site/docs/reference/licensing.md
  Nav (site/mkdocs.yml, under "Reference"):
      - Publishing and sharing:
          - Choosing a licence: reference/licensing.md
  Row for site/docs/reference/index.md (new section "Publishing and sharing"):
      | [Choosing a licence](licensing.md) | What the absence of a LICENSE file means, the four families, what you may and may not mix, and what "open" means for a model | not taught in a session — read it before publishing anything |

CUT ON PURPOSE (see REPORT.md): every monetary figure and market-share percentage of the original
deck (Red Hat revenue, the IBM acquisition price, "44.7 % of GitHub", kernel contributor counts,
"94 % of Chromium commits"). They are plausible and widely repeated but were not checked against a
primary source for this page, and AGENTS.md rule 2 forbids guessing. The structural arguments they
illustrated are kept.

NOT LEGAL ADVICE — the page says so itself.
-->

# Choosing a licence

Not taught in any of the four sessions, and the shortest page on this site that can change what happens to your work. Read it once before you make a repository public — including the repository you build in [Session 1](../sessions/s1.md).

!!! warning "Not legal advice"
    This page is a working understanding written by a programmer, not a lawyer. It is enough to choose sensibly for a course project or a research repository. For anything with money, an employer or a thesis embargo attached, ask someone qualified — your laboratory or your university's legal service.

## 1. The default is "nobody may use this"

Push code to a public GitHub repository with no `LICENSE` file and you have published something everybody can *read* and nobody may legally *use*. Copyright is automatic: the moment you write the file, you hold the exclusive right to copy, modify and distribute it. Visibility is not permission. "It is on GitHub" grants no more than "it is in a library".

This surprises people, and it has consequences that are practical rather than theoretical:

- A classmate who wants to build on your project cannot, strictly speaking, do so.
- A company will not touch it — their compliance process rejects unlicensed dependencies automatically.
- Your future self, at another institution, may have to renegotiate with a co-author to reuse it.
- A journal or data editor asking for a replication package will ask what licence it is under.

A licence is how you say yes, once, in writing, to everybody, in advance. **A `LICENSE` file is the difference between publishing and merely uploading.** GitHub's own explanation of the default state is [choosealicense.com — No permission](https://choosealicense.com/no-permission/).

## 2. The one decision behind all of them

Every licence in common use answers the same question: **if somebody improves my code, must their version stay open too?**

- **No** → a **permissive** licence. Take it, change it, sell it, keep your changes secret; just keep my copyright notice. MIT, BSD, Apache 2.0.
- **Yes** → a **copyleft** licence. You may do all of that, *provided* that whatever you distribute stays under the same licence. GPL, AGPL.

Permissive maximises adoption: anybody can use your work anywhere, including in a closed product. Copyleft maximises the commons: your work cannot be absorbed into something the public cannot see. Neither is more ethical than the other; they optimise different things. The whole zoo below is variations on that answer.

## 3. The four you need to recognise

### MIT — the permissive default

Around twenty lines. Do anything, including commercial and closed-source use; keep the copyright notice and the licence text; the author gives no warranty and accepts no liability.

Used by a very large share of what you `uv add` — NumPy, pandas and matplotlib are under permissive licences (BSD, in their case, which is MIT with the words rearranged). **Choose MIT when you want your code used, full stop.** For a course project, a teaching repository, a small library or a replication package, this is almost always the right answer.

Text: [opensource.org — MIT](https://opensource.org/license/mit).

### Apache 2.0 — MIT plus patents

Same permissions, longer text, one substantive addition: contributors grant you a licence to any **patents** they hold that the code implements, and the licence terminates for anyone who sues over those patents.

Which requires a detour, because the two words are constantly confused:

| | Copyright | Patent |
|---|---|---|
| Protects | *this particular expression* — your actual lines of code | *the method itself*, however you write it |
| Arises | automatically, when you write it | only by application, examination and payment |
| Means | "do not copy my code" | "do not use my method, even in your own code" |

Write a new sorting algorithm and copyright protects your implementation; a patent (in jurisdictions that grant software patents) could stop anyone from implementing the *idea* at all. Apache 2.0 exists so that using a project cannot become a patent trap. **Choose Apache 2.0 for anything you expect a company to depend on** — Android, Kubernetes and TensorFlow are under it.

Text: [apache.org — Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

### GPL v3 — copyleft

Anyone may use, study, modify and redistribute — and anyone who **distributes** a modified version must ship its source under the GPL as well. The Free Software Foundation states it as [four freedoms](https://www.gnu.org/philosophy/free-sw.html): run it for any purpose, study it, redistribute it, improve and share the improvements.

The strategic consequence is what matters to you: a company cannot take GPL code into a closed product. Some organisations therefore forbid GPL dependencies outright. That is not a bug — it is the licence working as designed. Linux, GCC and Bash are GPL.

Text and a readable summary: [gnu.org — GPL v3](https://www.gnu.org/licenses/gpl-3.0.html) and its [quick guide](https://www.gnu.org/licenses/quick-guide-gplv3.html).

### AGPL — copyleft that survives the web

The GPL was written when software was shipped on disks: its obligation is triggered by **distribution**. Run modified GPL code on your own server and let the world use it over HTTP, and you have distributed nothing — so you owe nothing. That is the "SaaS loophole", and it is how a great deal of open-source software came to power businesses that return nothing.

The **AGPL** adds one clause: if users interact with your modified version **over a network**, they are entitled to its source. It is the right choice for a web service you want to stay open, and the reason several well-known projects have relicensed in that direction. Expect it to be refused by companies even more often than the GPL.

Text: [gnu.org — AGPL v3](https://www.gnu.org/licenses/agpl-3.0.html).

### And the fifth: no rights reserved

**Unlicense** and **CC0** are dedications to the public domain: "I give up my rights, do what you like." Simpler than MIT in spirit, but public-domain dedication is not clean in every jurisdiction, which is why MIT remains the pragmatic minimum. [unlicense.org](https://unlicense.org/), [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

### The table

| Licence | Commercial use | May keep changes private | Must share source | Patent grant |
|---|---|---|---|---|
| MIT / BSD | yes | yes | no | no |
| Apache 2.0 | yes | yes | no | yes |
| GPL v3 | yes | no | yes, when distributed | yes |
| AGPL v3 | yes | no | yes, including over a network | yes |
| Unlicense / CC0 | yes | yes | no | — |

Every one of them allows commercial use. "Open source" has never meant "not for money"; it means the source travels with the program.

## 4. You cannot mix them freely

Licences compose, and copyleft propagates. If your project imports a GPL library, what you distribute is a combined work, and it must be GPL:

```python title="what the imports imply"
# myproject.py — you would like this to be MIT
import requests        # Apache 2.0 — fine
import polars          # permissive — fine
import some_gpl_lib    # GPL v3 — your distributed project must now be GPL too
```

Nothing warns you. `uv add` is not a compliance tool, and neither is an agent that adds a dependency because it solved the problem. Two habits:

- **Before adding a dependency to something you will publish, look at its licence.** It is in the repository, and PyPI shows it on the project page.
- **In a project you intend to keep permissive, treat a GPL dependency as a decision, not a detail.**

The FSF maintains the exhaustive [compatibility list](https://www.gnu.org/licenses/license-list.html); the OSI maintains the [list of approved licences](https://opensource.org/license) and the [definition](https://opensource.org/osd) they must satisfy.

## 5. How to add one

=== "On GitHub, in the browser"

    1. In the repository: **Add file → Create new file**.
    2. Type `LICENSE` as the filename. GitHub offers a licence picker as soon as you do.
    3. Choose one, review the text, commit.

    GitHub then displays the licence on the repository's front page and in its API, which is how tools discover it. The steps are documented at [docs.github.com — Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

=== "In the terminal"

    Go to [choosealicense.com](https://choosealicense.com/), pick one, copy the text into a file called `LICENSE` (no extension; `LICENSE.txt` and `LICENSE.md` are also recognised), fill in the year and your name where the text asks for them, then:

    ```bash title="Ubuntu window (WSL), Terminal (Mac), Linux terminal, Git Bash or Codespace terminal"
    cd ~/agent-lab
    # paste the licence text into LICENSE with nano or your editor
    git add LICENSE
    git commit -m "Add MIT licence"
    git push
    ```

Then say so in two more places: a **line in the README** ("Licensed under the MIT licence — see `LICENSE`") and, for an installable project, the `license` field of `pyproject.toml` ([modules and packages, §6](modules-and-packages.md#6-making-the-package-installable)), so that the metadata in the wheel agrees with the file.

!!! tip "The decision tree, when you have thirty seconds"
    | You want | Choose |
    |---|---|
    | The widest possible use, no conditions | **MIT** |
    | The same, but with patent protection for users | **Apache 2.0** |
    | Improvements to stay open | **GPL v3** |
    | The same, for something that runs as a web service | **AGPL v3** |
    | To keep control and publish nothing | *no licence* — and keep the repository private, so the situation is honest |

    For coursework, a replication package or a personal tool: MIT. Decide in a minute and move on; you can relicense later, as long as you are the only author.

## 6. Two things worth knowing beyond the choice

**Who actually writes open source, and who pays.** The romantic picture — volunteers in their spare time — is not how the big projects work. Most contributions to the Linux kernel come from engineers paid by companies (Intel, Red Hat, Google, Meta, Microsoft and others) whose business depends on Linux running well. The strategy is not charity, it is complements: Intel wants Linux to exploit Intel chips, Google wants the mobile web on its terms, cloud providers need the software their customers deploy to work. And since copyleft makes selling copies pointless, whole businesses were built on selling *service* around free software — support, certification, guaranteed patches — with Red Hat as the canonical example. For an economics room this is a textbook case of complements, standards and appropriability; for an NLP room it explains why the tooling you use is free and excellent at the same time.

!!! note "Figures deliberately absent"
    Last year's slides carried precise numbers for all of this: revenues, an acquisition price, contributor counts, percentages of commits, GitHub licence shares. They are plausible and widely repeated, but they were not checked against a primary source while writing this page, so they are not reproduced. If you want them, the annual Linux Foundation kernel reports and the projects' own statistics are the places to look.

**"Source available" is not the same as open.** A published repository whose direction one company controls entirely — all the decisions, all the infrastructure, a build nobody else can realistically perform — is open in the licence sense and closed in every practical sense. Chromium and VS Code (whose de-branded rebuild, VSCodium, exists precisely to strip what Microsoft adds) are the standard examples. The lesson is small and useful: **read the licence, then look at who decides.**

## 7. Licences and models

This is where the course and this page meet, and where the vocabulary breaks down.

A released large language model typically comes as **weights** under some licence, a **paper**, and sometimes **training code**. What is almost never released is the **training data**. Several widely used models also ship licences with conditions no OSI-approved licence has — acceptable-use clauses, or a threshold above which you must negotiate — which is why "open source model" appears in marketing and rarely survives contact with the definition. The Open Source Initiative has published an [Open Source AI Definition](https://opensource.org/ai/open-source-ai-definition) precisely because the old words did not settle the question.

Two consequences for you.

- **For your own projects**, the Unistra platform you use in [Session 3](../sessions/s3.md) sidesteps the question: it is self-hosted, so your prompts stay inside the university whatever the weights' licence says. That is a sovereignty property, not a licensing one, and it is the reason the course uses it.
- **For code an agent writes for you**, the sober position is that you are responsible for what you publish. A model trained on public code can reproduce recognisable fragments of it, and the legal landscape around that is unsettled and moving. Practically: keep your `LICENSE` file honest, do not paste licensed code you have not looked at, and say in your `justifications` or README what was generated — which is what last year's exam asked for, and a good habit regardless.

## 8. Going further

1. [choosealicense.com](https://choosealicense.com/) — GitHub's chooser: three questions, one recommendation, the full text ready to copy. Start and usually finish here.
2. [choosealicense.com — No permission](https://choosealicense.com/no-permission/) — the two paragraphs behind section 1, worth reading in full before you publish anything.
3. [OSI — the Open Source Definition](https://opensource.org/osd) and [FSF — What is free software?](https://www.gnu.org/philosophy/free-sw.html) — the two rival definitions, in the words of the two organisations. The disagreement between them is the whole of section 2.
4. [gnu.org — licence compatibility list](https://www.gnu.org/licenses/license-list.html) — the answer to "may I combine these two?", for hundreds of licences.
5. [OSI — Open Source AI Definition](https://opensource.org/ai/open-source-ai-definition) — the attempt to say what section 7 should mean.
