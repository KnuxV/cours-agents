<!--
PORTED FROM last year's material (KnuxV/advanced_programming_python):
  exercices/02-shell/02-shell.md — the "Shell Commands Exercise" questions on grades.csv
  exercices/02-shell/grades.csv  — the data file (50 students, 11 columns)

PROPOSED DESTINATION: site/docs/exercises/shell-data.md
  Nav (site/mkdocs.yml, under "✏️ Exercises" → "Terminal"):
          - 0.2 The grades file — pipes and columns: exercises/shell-data.md
  Row for site/docs/exercises/index.md, "Terminal" table:
      | 0.2 | [The grades file: pipes and columns](shell-data.md) | `cut`, `sort`, `uniq`, `grep`, `wc`, pipes and redirection on a real CSV | 30 min |
  DATA FILE: research/old-site-port/files/grades.csv must be moved to site/docs/files/grades.csv
  for the `curl -LO` line below to work.

FIXED WHILE PORTING: last year's statement said the answer to question 1 was 49. It is 50 — the
file's last line has no trailing newline, so `wc -l` under-counts (see the lesson, §5.1). Every
answer in the solutions below was computed on the real file with GNU coreutils.
-->

# 0.2 — The grades file: pipes and columns

Lesson: [The shell as a data tool](../reference/shell-text-tools.md) · [All exercises](index.md)

**Goal:** answer twelve questions about a real CSV without opening a single notebook — and meet, on the way, the counting trap that made last year's answer to question 1 wrong.

## The data

```bash title="Ubuntu window (WSL), Terminal (Mac), Linux terminal, Git Bash or Codespace terminal"
cd ~
mkdir -p shell-demo
cd shell-demo
curl -LO https://knuxv.github.io/cours-agents/files/grades.csv
head -2 grades.csv
```

```text
FirstName,LastName,Algèbre1,Algèbre2,Algèbre3,Analysis1,Analysis2,Analysis3,Dissertation1,Dissertation2,Commentaire1,Commentaire2
Alice,Martin,12,14,13,11,13,10,17,16,18,17
```

Eleven data columns: two names, then three Algèbre marks, three Analysis marks, two Dissertation marks and two Commentaire marks. Out of 20, as usual. Remember that `cut` counts fields, so `Algèbre1` is field **3** and `Commentaire1` is field **11** — write the header out on paper if it helps.

!!! tip "How to work"
    Build every pipeline one stage at a time and look at the output before adding the next `|`. If a command produces nothing, remove the last stage and look again. `pwd` if you are not sure where you are.

## Warm-up

1. **How many students are in the class?** Beware: there is a trap here, and two methods that disagree. Find both and decide which one is telling the truth.
2. Show the **first three students** with all their marks, without the header line.
3. Save **every first name** to a file called `first_names.txt`.
4. Print **first and last names only**, without the header, sorted alphabetically.

## Columns and subjects

5. Extract the **three Algèbre columns** and save them to `algebra_grades.csv`.
6. Who are the **five best students in `Algèbre1`**? Show first name, last name and the mark.
7. Extract the **two Dissertation columns**.
8. List the students **sorted by `Commentaire1`, lowest first**, showing the name and that mark.

## Searching and counting

9. Print the first names that **start with `A`**, without duplicates.
10. Build a file with the names and the **first mark of each subject** (fields 1, 2, 3, 6, 9, 11).
11. Sort every student **by last name** and save the result to `students_by_lastname.csv`.
12. How many **distinct first names** are there? How many distinct **last names**? What does the difference tell you?

## Challenge

13. Create two files: `math_students.csv` with the students whose `Algèbre1` is 16 or more, and `lit_students.csv` with those whose `Dissertation1` is 16 or more. How many are in each? How many are in **both**?

**Done when** you can answer questions 1, 6 and 12 out loud, and `ls` shows the five files you were asked to create.

??? note "Solutions"
    **1. How many students**

    ```bash title="Any terminal, inside shell-demo"
    tail -n +2 grades.csv | wc -l
    tail -n +2 grades.csv | grep -c ''
    ```

    ```text
    49
    ```
    ```text
    50
    ```

    **50 is the right answer.** `wc -l` counts newline characters, and the last line of this file does not end with one, so it reports one fewer. `grep -c ''` counts lines whether or not they are terminated (`awk 'END {print NR}'` agrees). Last year's statement gave 49; this is the same file and the same trap. When two counts disagree, one of them is a bug — find out which before you quote it.

    **2. The first three students**

    ```bash title="Any terminal, inside shell-demo"
    tail -n +2 grades.csv | head -3
    ```

    ```text
    Alice,Martin,12,14,13,11,13,10,17,16,18,17
    Bob,Durand,17,18,16,16,17,15,10,9,11,10
    Claire,Petit,17,18,16,16,17,18,16,18,17,16
    ```

    `tail -n +2` first (drop the header), then `head -3`. The other order — `head -3 | tail -n +2` — gives you only two students, because the header was still in the three lines.

    **3. First names to a file**

    ```bash title="Any terminal, inside shell-demo"
    tail -n +2 grades.csv | cut -d',' -f1 > first_names.txt
    head -3 first_names.txt
    ```

    **4. Names, sorted**

    ```bash title="Any terminal, inside shell-demo"
    cut -d',' -f1,2 grades.csv | tail -n +2 | sort
    ```

    **5. The Algèbre columns**

    ```bash title="Any terminal, inside shell-demo"
    cut -d',' -f3,4,5 grades.csv > algebra_grades.csv
    head -3 algebra_grades.csv
    ```

    ```text
    Algèbre1,Algèbre2,Algèbre3
    12,14,13
    17,18,16
    ```

    Keeping the header here is a deliberate choice: the file is meant to be read by a human or by Polars later, and both want the column names.

    **6. The five best in Algèbre1**

    ```bash title="Any terminal, inside shell-demo"
    tail -n +2 grades.csv | sort -t',' -k3,3nr | head -5 | cut -d',' -f1,2,3
    ```

    ```text
    Iris,Blanc,18
    Lucas,Dubois,18
    Alexandre,François,17
    Bob,Durand,17
    Claire,Petit,17
    ```

    Three things had to be right: `-t','` (the delimiter), `-k3,3nr` (field 3 **only**, numeric, reversed) and the `cut` at the *end* of the pipeline rather than the start — cutting first would have thrown away the names you want to display.

    **7. The Dissertation columns**

    ```bash title="Any terminal, inside shell-demo"
    cut -d',' -f9,10 grades.csv | head -3
    ```

    ```text
    Dissertation1,Dissertation2
    17,16
    10,9
    ```

    **8. Sorted by Commentaire1, lowest first**

    ```bash title="Any terminal, inside shell-demo"
    tail -n +2 grades.csv | sort -t',' -k11,11n | head -3 | cut -d',' -f1,2,11
    ```

    ```text
    Gabriel,Riviere,7
    Alexandre,François,8
    Arthur,Renard,8
    ```

    **9. First names starting with A**

    ```bash title="Any terminal, inside shell-demo"
    tail -n +2 grades.csv | cut -d',' -f1 | sort -u | grep '^A'
    ```

    ```text
    Adrien
    Alexandre
    Alice
    Anaïs
    Antoine
    Arthur
    ```

    `^` means "start of line", so `grep '^A'` keeps only the names that *begin* with A. Drop the `^` and you keep every name containing a capital A anywhere — on this small file the two happen to give the same list, which is exactly why the mistake survives until the file gets bigger. `sort -u` is `sort | uniq` in one command.

    **10. One mark per subject**

    ```bash title="Any terminal, inside shell-demo"
    cut -d',' -f1,2,3,6,9,11 grades.csv > first_marks.csv
    head -3 first_marks.csv
    ```

    ```text
    FirstName,LastName,Algèbre1,Analysis1,Dissertation1,Commentaire1
    Alice,Martin,12,11,17,18
    Bob,Durand,17,16,10,11
    ```

    **11. Sorted by last name**

    ```bash title="Any terminal, inside shell-demo"
    tail -n +2 grades.csv | sort -t',' -k2,2 > students_by_lastname.csv
    head -3 students_by_lastname.csv | cut -d',' -f1,2
    ```

    ```text
    Quentin,Andre
    Mélanie,Barbier
    Felix,Bernard
    ```

    The file keeps every column; the `cut` at the end of the check is only there to make the output readable on this page.

    **12. Distinct names**

    ```bash title="Any terminal, inside shell-demo"
    tail -n +2 grades.csv | cut -d',' -f1 | sort -u | grep -c ''
    tail -n +2 grades.csv | cut -d',' -f2 | sort -u | grep -c ''
    ```

    ```text
    50
    ```
    ```text
    46
    ```

    Fifty distinct first names for fifty students: every first name is unique. Only forty-six distinct last names, so four are shared — `sort | uniq -c | sort -rn` on the second field shows `Moreau`, `Martin`, `Lopez` and `Blanc` twice each. The practical consequence is the one that matters: **the last name is not a key.** If you were joining this file to another one on the name, you would silently duplicate rows — which is why a test suite for a data pipeline asserts row counts after every join ([testing, §11](../reference/testing.md#11-where-this-sits-in-the-bigger-picture)).

    **13. Specialists**

    ```bash title="Any terminal, inside shell-demo"
    tail -n +2 grades.csv | awk -F',' '$3 >= 16' > math_students.csv
    tail -n +2 grades.csv | awk -F',' '$9 >= 16' > lit_students.csv
    grep -c '' math_students.csv
    grep -c '' lit_students.csv
    tail -n +2 grades.csv | awk -F',' '$3 >= 16 && $9 >= 16' | grep -c ''
    ```

    ```text
    13
    ```
    ```text
    15
    ```
    ```text
    6
    ```

    Thirteen strong in Algèbre1, fifteen in Dissertation1, six in both. This is the one question `cut`, `sort` and `grep` cannot answer, because it needs a *comparison on a field*: `awk -F',' '$3 >= 16'` means "split on commas, print the line when field 3 is at least 16". That is the whole of awk you need today; if you find yourself wanting more of it, you have reached the point where [Polars](../sessions/s2.md#7-bonus-polars-in-five-minutes) is the better tool.

## Going further

Do the same twelve questions in Polars, in a `uv` project, and compare: which ones were shorter in the shell, which ones were shorter in Python, and at what point you stopped being sure the shell version was right. That boundary — roughly, when you need to *compute* rather than *select* — is the honest answer to "when should I leave the terminal?".
