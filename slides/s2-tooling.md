---
title: Python, pour de vrai
sub_title: "scripts, modules, paquets — et les arguments qui en font des outils"
author: Kevin Michoud — Université de Strasbourg
---

<!-- speaker_note: Session 2 (SPEC Session 2 — outillage Python). Environ 60 minutes de diapos + démo live tapée avec la salle, puis l'exercice argparse (password generator, exercice 2.3 du site). Cinq étapes — lancer un script, ajouter un import, importer un paquet externe, uv, les arguments. Les variables d'environnement ne sont PAS dans ce deck, elles ouvrent la séance suivante. Toutes les commandes ont été exécutées et leur sortie est collée telle quelle (uv 0.12.10, pandas 3.0.6, CPython 3.12.14). Deck en français à la demande de l'instructeur ; le site reste en anglais. -->

Aujourd'hui
===

Cinq étapes, un projet qui grandit :

1. lancer un **script**
2. ajouter un **import** → script, module, bibliothèque
3. importer le paquet de **quelqu'un d'autre** → ça échoue
4. un **gestionnaire de paquets** : `uv`
5. les **arguments** → votre script devient un outil

<!-- pause -->

Ensuite, vous étendez un vrai programme.

<!-- speaker_note: 0:00–0:02. Présenter ça comme une échelle — chaque étape fait quelque chose que l'étape précédente ne pouvait pas faire. Dire à voix haute qu'ils tapent avec moi, et que tout est sur le site s'ils décrochent. -->

<!-- end_slide -->

D'abord, un dossier de travail
===

Tout le monde dans le même dossier, sinon on se perd.

```bash
mkdir ~/demo-python
cd ~/demo-python
pwd
```

```text
/home/<votre-login>/demo-python
```

**Restez dans ce dossier toute la première partie.**

<!-- speaker_note: 0:02–0:04. Attendre que tout le monde y soit — deux commandes, mais c'est la source de la moitié des blocages ensuite ("mon fichier n'existe pas"). Rappeler cd ~ pour revenir, et ls pour vérifier. Sur les postes de l'université le home est un dossier réseau, donc ce qu'on écrit ici les suit d'un poste à l'autre. Avertissement important — sur Windows avec Git Bash il n'y a pas encore de Python. Ceux-là regardent les étapes 1 à 3 et tapent à partir de l'étape 4, où uv installe Python pour eux. Ne pas perdre dix minutes à installer Python maintenant. -->

<!-- end_slide -->

Étape 1 — Un script
===

```python
# greet.py
def greet(name):
    return f"Hello, {name}!"

print(greet("Strasbourg"))
print(greet("A330"))
```

Le lancer — dans le terminal, depuis `~/demo-python` :

```bash
python3 greet.py
```

```text
Hello, Strasbourg!
Hello, A330!
```

<!-- speaker_note: 0:04–0:07. Taper le fichier en direct (nano ou VS Code) et le lancer. Un seul point — Python lit le fichier de haut en bas et exécute tout ce qu'il y trouve. Les deux print sont au niveau principal, donc ils s'exécutent. Un fichier qu'on lance comme ça s'appelle un SCRIPT. -->

<!-- end_slide -->

Étape 2 — Quatre mots
===

| Mot | Ce que c'est |
|---|---|
| **script** | un fichier qu'on *lance* |
| **module** | un fichier qu'on *importe* |
| **paquet** (*package*) | un dossier de modules qu'on importe |
| **bibliothèque** (*library*) | des modules écrits par *quelqu'un d'autre*, installés |

<!-- pause -->

Le même fichier peut être un script **et** un module.

<!-- speaker_note: 0:07–0:09. Ils vont croiser ces quatre mots dans chaque message d'erreur et chaque tutoriel. Insister sur le mot paquet — il désigne aussi "ce qu'on installe depuis PyPI", le mot est surchargé, le contexte décide. La dernière ligne est la question de la diapo suivante. -->

<!-- end_slide -->

Vous allez voir ça partout
===

```python
def main():
    print("Bonjour")


if __name__ == "__main__":
    main()
```

Ces deux lignes sont dans presque tous les scripts Python que vous ouvrirez.

<!-- pause -->

**Pourquoi ?**

<!-- speaker_note: 0:09–0:11. Poser la question et ne pas y répondre. Dire qu'on l'explique dans dix minutes, et qu'à la fin de l'heure uv va générer ces lignes tout seul. Demander qui l'a déjà recopié sans savoir pourquoi — beaucoup de mains. C'est le seul cargo cult qu'on démonte aujourd'hui. -->

<!-- end_slide -->

Un fichier devient deux
===

```python
# tools.py
def greet(name):
    return f"Hello, {name}!"

print("tools.py démarre")
```

```python
# use.py
from tools import greet

print(greet("Kevin"))
```

**Qu'affiche `python3 use.py` ?**

<!-- speaker_note: 0:11–0:14. Vraie question à la salle, attendre des réponses avant de lancer. Presque tout le monde répond une seule ligne, Hello Kevin. Deux fichiers seulement, et rien de mystérieux dedans — le print de tools.py est là uniquement pour qu'on le voie apparaître là où on ne l'attend pas. -->

<!-- end_slide -->

La surprise
===

```bash
python3 use.py
```

```text
tools.py démarre
Hello, Kevin!
```

<!-- pause -->

**`import` exécute le fichier.** De haut en bas, une fois, avant de vous rendre quoi que ce soit.

<!-- speaker_note: 0:14–0:17. La première ligne est celle que personne n'a demandée — on n'a jamais lancé tools.py. Importer n'est pas "aller chercher une fonction", c'est exécuter ce fichier en entier. C'est la chose la plus utile de la demi-heure, elle explique tous les "pourquoi mon script affiche ça ?" de leur vie. -->

<!-- end_slide -->

`__name__` — qui me lance ?
===

Chaque fichier Python a une variable `__name__`. Mettons-la dans `tools.py` :

```python
print("__name__ =", __name__)
```

| Ce qu'on lance | tools.py affiche |
|---|---|
| `python3 tools.py` — on le lance | `__name__ = __main__` |
| `python3 use.py` — on l'importe | `__name__ = tools` |

<!-- pause -->

Le fichier peut donc **savoir** dans quel cas il se trouve.

<!-- speaker_note: 0:17–0:19. Remplacer le print de tools.py par celui-ci et lancer les deux, dans cet ordre. __main__ est le seul mot magique de la journée, rien d'autre à mémoriser. Quand on l'importe, __name__ prend le nom du fichier sans le .py. -->

<!-- end_slide -->

La correction, et la réponse
===

```python
# tools.py
def greet(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print("tools.py démarre")
```

```bash
python3 tools.py     # tools.py démarre
python3 use.py       # Hello, Kevin!      (et rien d'autre)
```

**Les définitions en haut. Les actions derrière le `if`.**

<!-- speaker_note: 0:19–0:22. Taper la correction en direct et relancer les deux. Boucler avec la diapo "vous allez voir ça partout" — c'était ça, la réponse. Dire la règle en une phrase — un fichier doit pouvoir être importé sans danger, l'importer ne doit RIEN faire. C'est une convention, pas une règle du langage ; Python ne l'impose pas. -->

<!-- end_slide -->

Pourquoi ça compte, au-delà du rangement
===

Du code qu'on peut **importer** est du code qu'on peut :

- **tester** — un fichier de test importe votre fonction et la vérifie
- **réutiliser** — dans le script suivant, par un collègue
- **appeler** — depuis un programme qui n'est pas vous

<!-- pause -->

À la séance 4, ce programme sera un **agent**.

<!-- speaker_note: 0:22–0:23. Court. Un agent vérifie son travail en important et en exécutant ; un script de 300 lignes où tout est au niveau principal ne peut pas être vérifié, seulement relu. Ne pas développer ici, c'est le boulot de la séance 4. -->

<!-- end_slide -->

Étape 3 — Le code des autres
===

Certains modules sont livrés avec Python :

```bash
python3 -c "import random; print('random ok')"
```

```text
random ok
```

`-c` = "exécute ce code tout de suite". Un script d'une ligne, sans créer de fichier.

La plupart, non :

```bash
python3 -c "import pandas"
```

```text
ModuleNotFoundError: No module named 'pandas'
```

<!-- speaker_note: 0:23–0:26. random, csv, pathlib, argparse, os — bibliothèque standard, toujours là. pandas, numpy, requests, matplotlib — non. Expliquer -c en une phrase — c'est la même chose que mettre la ligne dans un fichier et lancer python3 fichier.py, en plus rapide pour une vérification. On s'en sert trois fois aujourd'hui. Cette erreur est le message le plus fréquent de la vie d'un débutant Python, et elle veut toujours dire la même chose — cette bibliothèque n'est pas installée dans le Python que je suis en train de lancer. -->

<!-- end_slide -->

`random` est un fichier sur votre disque
===

```python
import random

print(random.__name__)   # "random" : importé, donc nommé d'après son fichier
print(random.__file__)   # où ce fichier se trouve vraiment
```

```text
random
/usr/lib/python3.14/random.py
```

<!-- pause -->

Ouvrez-le : c'est du Python ordinaire, écrit par quelqu'un, 37 000 caractères.

**Rien de magique. `import` va chercher un fichier.**

<!-- speaker_note: 0:26–0:28. Boucler avec __name__ de l'étape 2 — random s'appelle random parce qu'il a été importé, exactement comme tools. Puis ouvrir le fichier en direct (less ou l'éditeur) et défiler dix secondes — la bibliothèque standard est du code lisible, pas une boîte noire. Le chemin dépend de leur version de Python, 3.12 chez l'un, 3.10 chez l'autre, donc ne pas promettre le même affichage. Si quelqu'un demande, sys n'a pas de __file__ — il est compilé dans l'interpréteur. À l'étape 4, le Python installé par uv donnera un chemin complètement différent, ce qui est exactement la question de la diapo suivante. -->

<!-- end_slide -->

Deux questions se cachent dans cette erreur
===

**Où** Python cherche-t-il les modules ?

Dans une liste fixe de dossiers : le dossier courant, puis le `site-packages` de *ce* Python.

<!-- pause -->

**Quel** Python tourne ?

```bash
which python3
python3 -c "import sys; print(sys.executable)"
```

```text
/usr/bin/python3
```

<!-- speaker_note: 0:28–0:30. Lancer les deux en direct. Sur un poste de l'université c'est un Python qu'ils ne possèdent pas et ne peuvent pas modifier — pas de sudo. "Installer une bibliothèque" veut toujours dire la même chose — la mettre dans le site-packages d'un Python précis. Tout le reste de la séance consiste à choisir lequel. -->

<!-- end_slide -->

Installer — le réflexe évident
===

```bash
pip install pandas
```

Trois choses tournent mal en route :

- **pas les droits** — le Python du poste n'est pas le vôtre (et `sudo` n'est pas une option)
- **ou pire, ça marche** — et maintenant *tous* vos projets partagent un seul jeu de versions
- **le projet A veut pandas 1.5, le projet B veut pandas 3.0** — l'un des deux casse

<!-- speaker_note: 0:30–0:33. Le lancer en direct, quoi qu'il réponde — "externally-managed-environment" (Debian/Ubuntu/université), "command not found", ou une installation réussie dans ~/.local. Les trois font le même point. NON VÉRIFIÉ — on ne sait pas lequel des trois messages donnent les postes de A330. Lire à voix haute ce qui s'affiche et avancer, la leçon ne dépend pas du libellé. -->

<!-- end_slide -->

La réponse classique
===

Un **environnement virtuel** par projet : un dossier privé, avec son Python et ses bibliothèques.

```bash
python3 -m venv .venv          # le créer
source .venv/bin/activate      # y entrer  → l'invite affiche (.venv)
pip install pandas             # installe ICI, aucun droit nécessaire
pip freeze > requirements.txt  # la liste qu'on distribue
deactivate                     # en sortir
```

<!-- pause -->

Vous croiserez ça dans tous les projets écrits avant 2024.

<!-- speaker_note: 0:33–0:35. Diapo seulement, on ne tape pas — ils doivent le reconnaître, pas le pratiquer. L'invite qui devient (.venv) est le seul repère visuel. Dire que ça résout l'isolation, et que ça la résout honnêtement. Le détail complet est sur le site, section 2. -->

<!-- end_slide -->

Ce qui reste sans réponse
===

- **quel Python ?** `python3` est 3.10 ici, 3.14 là. Le `requirements.txt` n'en dit rien.
- **quelles versions exactes ?** `pandas>=2.0` aujourd'hui n'est pas `pandas>=2.0` l'an prochain. Et vos bibliothèques ont des bibliothèques.
- **avez-vous activé ?** Oubliez une fois, installez dans le mauvais Python, perdez une heure.

<!-- pause -->

Pour un scientifique, ce n'est pas une question de rangement. **Un résultat que personne ne peut relancer, vous compris dans six mois, est une affirmation, pas un résultat.**

<!-- speaker_note: 0:35–0:37. Pour la salle d'économie — les revues et les data editors exigent maintenant que le paquet de réplication fige son environnement. Pour la salle de TAL — même problème avec la version d'un tokenizer. Pour les deux salles — "ça marche sur ma machine" n'est pas un résultat. -->

<!-- end_slide -->

Étape 4 — `uv`
===

Un seul outil. Il installe des Python, crée l'environnement, résout les versions, les fige, et lance votre code.

**Installation — sans `sudo`, dans `~/.local/bin` :**

```bash
# poste Linux, WSL, Mac, Codespaces
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows : PowerShell (pas administrateur), puis uv s'utilise depuis Git Bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Puis **fermez le terminal et ouvrez-en un nouveau** → `uv --version`

Détail par plateforme, et dépannage si ça coince :

```text
knuxv.github.io/cours-agents/sessions/s2/#3-install-uv
```

<!-- speaker_note: 0:37–0:40. Le lien est à l'écran, les y envoyer et ne pas lire les onglets à voix haute — la page a un onglet par plateforme et un tableau de dépannage. Ceux qui lisent les diapos sur le site cliquent directement. Le rituel du nouveau terminal est celui de la séance 0 — l'installeur modifie la config du shell, que seuls les nouveaux terminaux relisent. Attendre ici que les mains soient baissées ; rien de ce qui suit ne marche sans uv. -->

<!-- end_slide -->

`uv init`
===

Dans **votre dépôt de cours** :

```bash
cd ~/agent-lab
uv init --no-package --python 3.12
```

```text
Initialized project `agent-lab`
```

Trois nouveaux fichiers :

```text
.python-version    pyproject.toml    main.py
```

<!-- speaker_note: 0:40–0:42. --python 3.12 fige l'interpréteur — sans ça uv prend le plus récent qu'il trouve, différent sur chaque machine. --no-package donne la disposition simple, un fichier à la racine, au lieu d'un paquet src/ avec un système de build. uv voit le .git de la séance 1 et ne crée pas un second dépôt. Ceux qui n'ont pas de dépôt de cours — un mkdir ~/agent-lab suffit pour aujourd'hui. -->

<!-- end_slide -->

Ouvrez `main.py`
===

```python
# main.py
def main():
    print("Hello from agent-lab!")


if __name__ == "__main__":
    main()
```

**`uv` vient d'écrire l'étape 2 pour vous.**

<!-- speaker_note: 0:42–0:43. Rappel gratuit — exactement le motif de la question posée il y a trente minutes, généré par l'outil, parce que c'est simplement à quoi ressemble un fichier Python. Dix secondes, puis on avance. -->

<!-- end_slide -->

`uv run` — l'environnement apparaît
===

```bash
uv run main.py
```

```text
Using CPython 3.12.14
Creating virtual environment at: .venv
Hello from agent-lab!
```

<!-- pause -->

- `.venv` est le même genre de dossier qu'avant — avec un Python privé en **3.12**
- vous n'**activez jamais** rien : `uv run` veut dire "lance ça dans l'environnement du projet"
- vous ne le **committez jamais**

<!-- speaker_note: 0:43–0:46. Le premier lancement télécharge aussi CPython 3.12, environ 33 Mo — avec trente machines sur le réseau de la salle ça prend une minute, les prévenir avant qu'ils paniquent. Montrer ls .venv/bin — les mêmes activate, python et pip que l'environnement classique. Le piège de l'activation disparaît parce que l'outil s'en charge. -->

<!-- end_slide -->

`uv add` — déclarer une dépendance
===

```bash
uv add pandas
```

```text
Resolved 6 packages in 177ms
Installed 4 packages in 81ms
 + numpy==2.5.3
 + pandas==3.0.6
 + python-dateutil==2.9.0.post0
 + six==1.17.0
```

`pyproject.toml` dit maintenant :

```toml
dependencies = [
    "pandas>=3.0.6",
]
```

<!-- speaker_note: 0:46–0:48. pandas télécharge environ 10 Mo et numpy 16 Mo par machine — même avertissement réseau. Relever le "Installed 4 packages" alors qu'ils n'en ont nommé qu'un — pandas tire numpy, python-dateutil et six. Personne ne pourrait maintenir cette liste à la main, c'est tout l'intérêt de la diapo sur le reçu. -->

<!-- end_slide -->

Et l'import marche
===

```bash
uv run python -c "import pandas; print(pandas.__version__)"
```

```text
3.0.6
```

**L'erreur de l'étape 3 est réparée** — pour ce projet, et seulement pour ce projet.

<!-- speaker_note: 0:48–0:49. Fermer la boucle ouverte à l'étape 3. Demander ce qui se passe si je lance python3 -c "import pandas" tout court dans le même dossier — toujours ModuleNotFoundError, la bibliothèque est dans .venv, pas dans le Python du système. Le lancer, ça vaut les quinze secondes. -->

<!-- end_slide -->

Le souhait et le reçu
===

| Fichier | Dit | Vous |
|---|---|---|
| `pyproject.toml` | "j'ai besoin de pandas, 3.0.6 ou plus" | l'écrivez (via `uv add`) |
| `uv.lock` | "au 25 septembre 2026 c'était pandas 3.0.6 **et** numpy 2.5.3, python-dateutil, six, ces fichiers exacts, ces empreintes" | ne l'éditez jamais, le committez toujours |

<!-- pause -->

Le reçu, c'est ce qui rend le résultat reproductible l'an prochain.

<!-- speaker_note: 0:49–0:51. Montrer head -20 uv.lock — versions, URLs, empreintes sha256. Ne pas le lire. L'empreinte est la promesse — les mêmes octets, ou une erreur. C'est l'exigence "tout figer" du parcours réplication. -->

<!-- end_slide -->

L'autre moitié — `uv sync`
===

Le projet de quelqu'un d'autre, ou le vôtre sur une autre machine :

```bash
git clone https://github.com/KnuxV/password-generator.git
cd password-generator
uv sync
```

```text
Using CPython 3.12.14
Creating virtual environment at: .venv
Resolved 8 packages in 0.45ms
Installed 6 packages in 18ms
 + pytest==9.1.1
 + zxcvbn==4.5.0
 ...
```

**Deux commandes et ça tourne.** Pas d'archéologie du README, pas de chasse aux versions.

<!-- speaker_note: 0:51–0:54. C'est exactement ce qu'ils font dans l'exercice dans vingt minutes, donc le faire sur un vrai clone. uv sync lit .python-version et uv.lock — il récupère ce Python s'il manque et reconstruit .venv à l'identique. uv run le fait implicitement aussi ; sync est la forme explicite qu'on met dans un README. -->

<!-- end_slide -->

Committer le projet, pas l'environnement
===

```bash
git status --short
```

```text
?? .python-version
?? pyproject.toml
?? uv.lock
?? main.py
```

<!-- pause -->

`.venv` n'est **pas** dans cette liste — le `.gitignore` s'en charge.

Si vous le voyez : ajoutez `.venv/` au `.gitignore` **avant** de committer.

<!-- speaker_note: 0:54–0:56. Committer les quatre fichiers en direct, pousser. .venv pèse des centaines de mégaoctets, dépend de la machine, et se reconstruit en quelques secondes depuis le lockfile — le committer est l'erreur classique du débutant et c'est pénible à défaire. uv dépose aussi un .gitignore à l'intérieur de .venv, deuxième filet. -->

<!-- end_slide -->

Étape 5 — Les arguments
===

`report.py`, première version :

```python
CSV_FILE = "sales.csv"      # on modifie ici…
TOP = 3                     # …et ici, puis on relance
```

<!-- pause -->

Très bien pour une personne, une fois. Impossible :

- de le lancer sur dix fichiers dans une boucle
- de le programmer chaque nuit
- de le donner à quelqu'un qui ne modifiera pas votre code
- de le **tester** — par un collègue, ou par un agent

<!-- speaker_note: 0:56–0:58. Ils reconnaissent tous l'habitude des constantes en haut du fichier. La forme professionnelle de la même chose est un script avec des arguments — les valeurs quittent le fichier pour la ligne de commande. Relever aussi que "modifier le fichier pour changer un paramètre" veut dire qu'il faut un humain à chaque exécution. -->

<!-- end_slide -->

L'outil de base — `sys.argv`
===

```python
import sys

print("all arguments:", sys.argv)
```

```bash
uv run argv_demo.py sales.csv --top 2
```

```text
all arguments: ['argv_demo.py', 'sales.csv', '--top', '2']
```

**Une liste de chaînes.** La position 0 est le script lui-même.

<!-- speaker_note: 0:58–1:00. Trois minutes, en direct. C'est tout ce que le terminal donne à un programme — des mots. Le reste est votre travail, ce qui est la diapo suivante. --top et 2 sont deux éléments distincts, et la chaîne "2" n'est pas le nombre 2. -->

<!-- end_slide -->

Pourquoi `argv` pourrit
===

Avec `sys.argv`, c'est **vous** qui écrivez :

- le texte d'aide — et qui le maintenez en phase avec le code
- le `int("2")`, et le message d'erreur quand c'est `"two"`
- "l'argument 3, c'est le fichier de sortie ou l'option ?"

```python
if len(sys.argv) > 2 and sys.argv[2] == "--loud":
    ...
```

<!-- speaker_note: 1:00–1:01. Montrer cette diapo comme une motivation, pas comme quelque chose à apprendre. Tout le monde écrit ça une fois, puis découvre argparse. Garder sys.argv pour un script d'une ligne avec un seul argument. Démo qui vaut trente secondes — resources/s2-demo/04-arguments contient le même programme en trois versions ; lancer report_2_argv.py sales.csv deux donne un ValueError avec traceback, et deux diapos plus loin report.py sales.csv --top deux donne une ligne lisible et le code de sortie 2. La même faute de frappe, deux qualités de message. -->

<!-- end_slide -->

`argparse` — quatre idées
===

```python
import argparse

parser = argparse.ArgumentParser(description="Revenue per region from a sales CSV.")
parser.add_argument("csv_file", help="path to the CSV")
parser.add_argument("--top", type=int, default=3, help="how many regions (default: 3)")
args = parser.parse_args()

print(args.csv_file, args.top)
```

1. un **parseur** — ce que la commande accepte
2. un argument **positionnel** — obligatoire, identifié par sa place
3. une **option** — commence par `--`, facultative, avec un `type` et un `default`
4. **`parse_args()`** — `args.top` est votre ancien `TOP`

<!-- speaker_note: 1:01–1:04. Le taper en direct dans report.py, autour du code de la diapo précédente, dans un main() derrière le if __name__ == "__main__". Bibliothèque standard, aucun uv add nécessaire. Le corps de la fonction ne change pas — seules les deux constantes disparaissent. -->

<!-- end_slide -->

Gratuit — la documentation
===

```bash
uv run report.py --help
```

```text
usage: report.py [-h] [--top TOP] [--product PRODUCT] csv_file

Revenue per region from a sales CSV.

positional arguments:
  csv_file           path to the CSV (columns: region, product, units,
                     unit_price)

options:
  -h, --help         show this help message and exit
  --top TOP          how many regions to show (default: 3)
  --product PRODUCT  keep only this product (default: all)
```

**Construite depuis vos chaînes `help=`.** Elle ne peut pas se désynchroniser du code.

<!-- speaker_note: 1:04–1:06. C'est la diapo qui vend argparse. Tous les vrais outils en ligne de commande dans lesquels ils ont tapé --help marchent exactement comme ça. Leur programme ressemble maintenant à git et à curl. -->

<!-- end_slide -->

Gratuit — la validation
===

```bash
uv run report.py
```

```text
report.py: error: the following arguments are required: csv_file
```

```bash
uv run report.py sales.csv --top two
```

```text
report.py: error: argument --top: invalid int value: 'two'
```

<!-- pause -->

Message propre, code de sortie **2**, aucune traceback. Vous n'en avez écrit aucune ligne.

<!-- speaker_note: 1:06–1:08. Lancer les deux. Montrer qu'il n'y a pas de traceback Python — une mauvaise invocation est une erreur d'utilisateur, pas un plantage. Le code de sortie 2 est la convention Unix pour "mauvais usage", echo $? pour le montrer. Ça compte aux séances 3 et 4, où le code de sortie d'un programme est la façon dont le harnais sait si une étape a marché. -->

<!-- end_slide -->

Et le vrai résultat
===

```bash
uv run report.py sales.csv --top 2
```

```text
region
Bretagne    937.5
Alsace      828.5
Name: revenue, dtype: float64
```

```bash
uv run report.py sales.csv --product tea
```

<!-- speaker_note: 1:08–1:10. Le même programme, trois réponses différentes, aucun fichier modifié. C'est tout l'enjeu de l'étape 5. Le groupby pandas est sur le site si quelqu'un demande ; ce n'est pas le sujet du jour. Committer report.py et pousser. -->

<!-- end_slide -->

L'échelle
===

```text
un fichier qu'on lance                      →  script
un fichier qu'on importe                    →  module        ( if __name__ == "__main__" )
les modules de quelqu'un d'autre            →  bibliothèque  ( uv add )
un Python et des versions exactes, figés    →  projet        ( pyproject.toml + uv.lock )
des valeurs venues de la ligne de commande  →  outil         ( argparse )
```

**Chaque barreau fait quelque chose que celui du dessus ne pouvait pas faire.**

<!-- speaker_note: 1:10–1:12. Diapo de récapitulation. Leur demander sur quel barreau se trouve le code qu'ils écrivaient jusqu'ici. Séance suivante — la même échelle pour parler à un modèle de langue, en commençant par curl à la main. -->

<!-- end_slide -->

À vous
===

**Forkez et étendez le générateur de mots de passe.**

```bash
git clone https://github.com/KnuxV/password-generator.git
cd password-generator
uv sync
uv run strong_password.py --help
```

Lire un vrai programme `argparse`, ajouter deux options, une branche par option.

Énoncé : **site → séance 2 → exercice 2.3**

<!-- speaker_note: 1:12–1:14. Ils forkent d'abord sur GitHub et clonent LEUR fork — l'énoncé le dit, parce qu'ils poussent à la fin. Terminé quand --help documente quatre options, que pytest passe, et que les deux commits sont sur GitHub. Je circule ; le tuteur pi (--tools read,grep,find,ls) est la première ligne d'aide. -->

<!-- end_slide -->

Où tout se trouve
===

Site du cours : https://knuxv.github.io/cours-agents/

- **Séance 2** — la version complète de cette heure, installations par plateforme, dépannage
- **exercices 2.1 → 2.5** — avec les solutions
- séance suivante : les **variables d'environnement** et votre clé d'API, puis `curl`

Tout le code tapé aujourd'hui, un dossier par étape :

```bash
git clone https://github.com/KnuxV/cours-agents.git
cd cours-agents/resources/s2-demo
```

<!-- speaker_note: 1:14. Les diapos sont des amorces, le site est la référence. Les diapos elles-mêmes sont sur le site, et resources/s2-demo/ contient les fichiers de la démo avec un README qui dit comment les lancer — c'est le filet pour ceux qui ont décroché en route, mais leur dire de taper le code d'abord, c'est là que ça s'apprend. À la maison — exercice 2.1 (un projet uv depuis zéro) pour ceux qui veulent répéter, 2.5 (polars vs pandas) pour ceux qui sont en avance. Les variables d'environnement ouvrent la séance suivante — elles sont le prérequis de l'API, et sans elles la séance 3 démarre sur un 401. -->
