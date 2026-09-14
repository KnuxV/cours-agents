---
title: Why Git?
sub_title: "Keeping track of a project that keeps changing"
author: Kevin Michoud — Université de Strasbourg
---

<!-- speaker_note: After s0-intro.md. About 20–25 minutes; 15 if examples are brief, 30 if expanded. Talk only. No audience tasks or live demos. SPEC Session 1; Task 02 format shortened at the instructor's request. Sources in research/s1-git.md and research/s1-git-motivation.md. -->

A familiar example
===

```text
report.docx
report_final.docx
report_final_v2.docx
report_final_REALLY.docx
```

**The filename is trying to tell the history.**

<!-- speaker_note: 0:00–0:01. Familiar workaround. Which version was sent? What changed? Rhetorical examples, no audience question. Motivation from Software Carpentry and the final-file example in research/s1-git-motivation.md. -->

<!-- end_slide -->

Why not a USB stick?
===

A USB stick carries a **copy**.

It does not explain:

- what changed;
- why it changed;
- how to combine two people's edits.

<!-- speaker_note: 0:01–0:02. Monday copy on laptop. Tuesday copy on USB. Both edited. Copying a folder is useful; comparing and combining versions is still your job. Backups remain useful with Git. -->

<!-- end_slide -->

Why not Google Drive?
===

Drive shares files. Google Docs supports shared editing.

**Version history already exists.**

Git adds a workflow for a whole code project:

**named checkpoints, experiments, reviewed changes.**

<!-- speaker_note: 0:02–0:04. Drive is useful for shared documents. A code change may span several files that belong together. Git groups that change, explains it, and combines separate work. Google file-history source https://support.google.com/drive/answer/2409045 . Comparison framing from Happy Git, cited in the research. -->

<!-- end_slide -->

A project is more than one file
===

```text
Read the data → Clean the data → Make a chart → Write the report
```

One change can affect every step.

**The files need to work together.**

<!-- speaker_note: 0:04–0:05. Example from either discipline. Rename a data column; cleaning script and chart script both need updating. Keeping only one updated file can break the project. Which set of files produced the submitted result? -->

<!-- end_slide -->

Now imagine Linux
===

**Millions of lines of code.**

**Thousands of contributors.**

Changes happening in parallel.

The challenge is keeping everyone's work together.

<!-- speaker_note: 0:05–0:07. Linux kernel, the core of an operating system. Different people fix bugs and add hardware support. Research's scale example; broad orders of magnitude only. Git was created for Linux development in 2005. Source Pro Git, A Short History of Git, cited in research/s1-git-motivation.md. -->

<!-- end_slide -->

Git keeps the project's history
===

**Version control** means recording versions as a project changes.

With Git, we can:

- keep checkpoints;
- understand changes;
- try alternatives;
- combine work.

<!-- speaker_note: 0:07–0:08. Same needs for one student or a large team. Later, the collaborator may be an agent. Git is free software. Source Pro Git, About Version Control, in research/s1-git-motivation.md. -->

<!-- end_slide -->

The project and its memory
===

A **repository**, or **repo**, is a project with Git history.

```text
Your project
├── Files you work on
└── Saved history
```

You keep working with ordinary files.

<!-- speaker_note: 0:08–0:09. Familiar project folder. Git stores its records in a hidden .git folder. Choose which files to track. Especially useful for text such as Python and notes; large datasets and private data need separate decisions. -->

<!-- end_slide -->

A checkpoint is a commit
===

A **commit** is a saved snapshot of the tracked project.

```text
First version → Fix missing values → Add the chart
```

Each checkpoint has an author, a date, and a message.

<!-- speaker_note: 0:09–0:10. Snapshot of tracked files together. Message explains the change. History connects checkpoints. Useful messages describe a purpose. Author metadata is a record, not proof. Source Pro Git, What is Git?, in research/s1-git.md. -->

<!-- end_slide -->

You choose when to take the snapshot
===

**Edit** the files.

**Select** the changes that belong together.

**Commit** that checkpoint with a message.

Saving a file in your editor is only the first step.

<!-- speaker_note: 0:10–0:11. Selection is called staging. Fix the cleaning rule and its explanation together; leave an unfinished chart for later. Git does not automatically record every keystroke. No command names needed yet. -->

<!-- end_slide -->

See exactly what changed
===

A **diff** shows the difference between versions.

```diff
-The meeting is on Monday.
+The meeting is on Tuesday.
```

Red / `-` = removed. Green / `+` = added.

<!-- speaker_note: 0:11–0:12. Same sentence; one day changed. Red removes the old line. Green adds the new line. Git shows a replacement as removal plus addition. Works with ordinary text as well as code. -->

<!-- end_slide -->

Return to a known version
===

Monday: the script worked.

Tuesday: an experiment broke it.

**Monday's checkpoint is still available.**

You can inspect it or recover a saved file.

<!-- speaker_note: 0:12–0:13. Recovery needs something recorded. Git cannot promise to recover edits it never saved. Local history is not protection against losing the entire laptop; keep another copy too. -->

<!-- end_slide -->

Try an idea on a branch
===

A **branch** names a line of work.

```text
Main version     A ── B ── C
                      ╲
Experiment             D ── E
```

The experiment can develop separately.

<!-- speaker_note: 0:13–0:15. Example, try a different chart while fixing the original report. Shared starting point B. Technically a branch is a movable name pointing to a commit; Git shares the earlier history. main is our agreed baseline, not automatically a live application. -->

<!-- end_slide -->

Bring the work together
===

A **merge** combines histories.

```text
Main version     A ── B ── C ───── M
                      ╲          ╱
Experiment             D ── E ──
```

**Review the experiment before bringing it back.**

<!-- speaker_note: 0:15–0:16. M includes both lines of work. Git can combine many independent edits automatically. This picture shows a merge commit; simpler merges just advance the branch name. No merge variants to memorise. -->

<!-- end_slide -->

Sometimes a person must decide
===

Two edits to the same title:

| Alice | Sam |
|---|---|
| Annual report | September report |

A **conflict** means Git cannot combine the edits automatically.

**People decide what the title should be.**

<!-- speaker_note: 0:16–0:17. Both started from the same title and replaced it differently. Neither edit is automatically wrong. Resolve by choosing or rewriting. Even a merge without conflicts still needs checking. -->

<!-- end_slide -->

Git is not GitHub
===

**Git** keeps history on your computer.

**GitHub** hosts a shared copy online.

You can use Git offline.

Sharing online is a separate step.

<!-- speaker_note: 0:17–0:18. Git is the tool; GitHub is a hosting service. GitLab is another host. An online repository may be private. A local commit has not been uploaded. -->

<!-- end_slide -->

Sharing has three simple verbs
===

**Clone** — get your own copy, with history.

```text
Your computer       ── push ──>       Shared repository
                    <── pull ──
```

**Push** — send your commits.

**Pull** — bring back and integrate shared changes.

<!-- speaker_note: 0:18–0:19. Clone to start; pull to update an existing copy. Each person can work locally. Sharing is deliberate, unlike automatic folder synchronisation. Pull may need conflict resolution. Remote simply means another repository. -->

<!-- end_slide -->

Your next collaborator may be an AI
===

An agent can edit many files quickly.

Git helps you:

- see what it changed;
- review before accepting;
- recover a known version.

**You still need to check that the result works.**

<!-- speaker_note: 0:19–0:21. Bridge to pi in Session 4. Save a working baseline first. Read actual changes, including any commits the agent made. Run tests. Confidence in a chat message is not verification. SPEC Session 1 agent-era motivation. -->

<!-- end_slide -->

Why we use Git
===

**Remember** how the project changed.

**Experiment** from a known version.

**Collaborate** without losing track of changes.

One script or a large project: the same ideas.

Repository: https://github.com/KnuxV/cours-agents

Course website: https://knuxv.github.io/cours-agents/

<!-- speaker_note: 0:21–0:22. End the explanation here. Practical work comes separately, with the course site as reference. No terminal demonstration while this deck is displayed. -->
