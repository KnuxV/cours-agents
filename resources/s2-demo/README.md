# Code de la démo — séance 2 (outillage Python)

Tout ce qui est tapé au tableau pendant la séance 2, un dossier par étape.
Les fichiers sont exactement ceux des diapos (`slides/s2-tooling.md`).

Pour les récupérer :

```bash
git clone https://github.com/KnuxV/cours-agents.git
cd cours-agents/resources/s2-demo
```

| Dossier | Étape de la séance | Ce qu'il montre |
|---|---|---|
| `01-script/` | 1 — un script | Python lit le fichier de haut en bas et exécute tout ce qu'il trouve |
| `02-import/` | 2 — la surprise | `import` **exécute** le fichier importé : `use.py` affiche une ligne que personne n'a demandée |
| `03-main/` | 2 — la correction | la même paire de fichiers avec `if __name__ == "__main__":` : importer `tools.py` ne fait plus rien |
| `04-arguments/` | 5 — les arguments | le même programme en trois versions : valeurs codées en dur → `sys.argv` → `argparse` |

## Les lancer

```bash
# 1 — un script
cd 01-script
python3 greet.py            # Hello, Strasbourg! / Hello, A330!
```

```bash
# 2 — la surprise : deux lignes, alors qu'on n'a lancé que use.py
cd 02-import
python3 use.py              # tools.py démarre / Hello, Kevin!
```

```bash
# 2 — la correction : plus rien ne s'échappe à l'import
cd 03-main
python3 tools.py            # tools.py démarre
python3 use.py              # Hello, Kevin!
```

### 5 — les arguments, en trois versions

Le même calcul, trois façons de lui donner ses valeurs. `pandas` est nécessaire,
donc on passe par `uv`.

```bash
cd 04-arguments
```

**`report_1_variables.py`** — les valeurs sont dans le fichier. Pour changer de CSV ou
de nombre de régions, on édite le code et on relance.

```bash
uv run --with pandas report_1_variables.py
```

**`report_2_argv.py`** — les valeurs viennent du terminal, mais tout est à notre charge :
le message d'usage, la valeur par défaut, la conversion en nombre.

```bash
uv run --with pandas report_2_argv.py                 # message d'usage, code de sortie 1
uv run --with pandas report_2_argv.py sales.csv 2
uv run --with pandas report_2_argv.py sales.csv deux  # ValueError + traceback
```

**`report.py`** — avec `argparse`. L'aide, les valeurs par défaut, les types et les
messages d'erreur sont fournis.

```bash
uv run argv_demo.py sales.csv --top 2                  # ce que le terminal donne vraiment
uv run --with pandas report.py --help
uv run --with pandas report.py sales.csv --top 2
uv run --with pandas report.py sales.csv --product tea
uv run --with pandas report.py sales.csv --top deux    # erreur propre, code de sortie 2
```

Comparez les deux dernières lignes des deux blocs ci-dessus : la même faute de frappe
donne un traceback Python d'un côté, et de l'autre une ligne lisible avec le code de
sortie que les autres programmes savent interpréter.

Dans la séance, `report.py` tourne dans un projet `uv` (`uv init`, `uv add pandas`, puis
`uv run report.py …`). Le `--with pandas` ci-dessus est le raccourci qui évite de créer
un projet juste pour relire le code à la maison.

`sales.csv` : neuf lignes inventées, colonnes `region, product, units, unit_price`.

## Vérifié

Toutes les sorties ci-dessus ont été produites sur cette machine le 24 septembre 2026
(CPython 3.12.14, pandas 3.0.6, uv 0.12.10).
