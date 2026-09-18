# 0.1 — Ten minutes in the terminal

Lesson: [Session 0 — Setup](../setup.md) · [All exercises](index.md)

**Goal:** the six commands you will type a hundred times — `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv` — plus `cat`, `echo`, `rm`.

1. Follow [setup, section 7](../setup.md#7-ten-minutes-in-the-terminal) line by line.
2. Then, without looking: create a folder `sandbox` in your home, inside it a file `a.txt` containing the word `one`, copy it to `b.txt`, rename `b.txt` to `c.txt`, list the folder with details, and delete `c.txt`.
3. Expected final state: `ls sandbox` prints `a.txt` only; `cat sandbox/a.txt` prints `one`.

??? note "Solution"
    ```bash title="Any terminal"
    cd ~
    mkdir sandbox
    cd sandbox
    echo "one" > a.txt
    cp a.txt b.txt
    mv b.txt c.txt
    ls -la
    rm c.txt
    ls
    cat a.txt
    ```
