# 02 — Python : premiers pas

## Objectif

Installer Python proprement, isoler chaque projet dans un environnement virtuel, installer des bibliothèques avec pip, structurer un script, et lire/écrire des fichiers Excel avec `openpyxl` et `pandas`.

## Prérequis

- Windows 10/11 (les commandes macOS/Linux sont indiquées).
- Savoir ouvrir un terminal ([05 — Ligne de commande](05-ligne-de-commande.md)).

## Installer Python

1. Téléchargez Python 3 sur https://www.python.org/downloads/ (ou via `winget install Python.Python.3.13`).
2. Cochez **« Add python.exe to PATH »** pendant l'installation.
3. Vérifiez dans un nouveau terminal :

```powershell
python --version
py --list          # Windows : liste les versions installées (lanceur py)
```

## Environnement virtuel (venv)

Un venv est un dossier qui contient une copie isolée de Python et des bibliothèques **d'un seul projet**. Il évite les conflits de versions entre projets.

```powershell
cd C:\Projets\mon-outil
python -m venv .venv               # crée le dossier .venv
.\.venv\Scripts\Activate.ps1       # active (PowerShell)
# le prompt affiche maintenant (.venv)
deactivate                         # désactive
```

```bash
# macOS / Linux / Git Bash
python3 -m venv .venv
source .venv/bin/activate          # Git Bash sous Windows : source .venv/Scripts/activate
```

Si PowerShell refuse d'exécuter le script d'activation (« l'exécution de scripts est désactivée »), autorisez les scripts locaux pour votre utilisateur seulement :

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Ajoutez `.venv/` au `.gitignore` ([01 — Git](01-git-et-github.md)) : on ne versionne jamais un venv.

## pip : installer des bibliothèques

```powershell
python -m pip install --upgrade pip
python -m pip install openpyxl pandas
python -m pip list                       # ce qui est installé
python -m pip freeze > requirements.txt  # figer les versions
python -m pip install -r requirements.txt  # réinstaller chez un collègue
```

Écrire `python -m pip` plutôt que `pip` garantit d'utiliser le pip du Python actif.

## Structure d'un script

```python
"""Calcule le total des lots d'un chantier.

Usage : python total_lots.py
"""
from pathlib import Path          # 1. imports (bibliothèque standard, puis externes)

TAUX_TVA = 0.20                   # 2. constantes en MAJUSCULES


def montant_ttc(ht: float) -> float:   # 3. fonctions
    """Renvoie le montant TTC arrondi au centime."""
    return round(ht * (1 + TAUX_TVA), 2)


def main() -> None:               # 4. point d'entrée
    lots = {"Gros oeuvre": 120_000, "Electricite": 45_000}
    for nom, ht in lots.items():
        print(f"{nom:<12} {montant_ttc(ht):>12,.2f} EUR TTC")
    print("Dossier courant :", Path.cwd())


if __name__ == "__main__":        # 5. n'exécute main() que si on lance ce fichier
    main()
```

Le bloc `if __name__ == "__main__":` permet d'importer les fonctions depuis un autre fichier (ou un test) sans lancer le programme.

Arborescence conseillée pour un petit projet :

```text
mon-outil/
├── .venv/              (ignoré par Git)
├── .gitignore
├── README.md
├── requirements.txt
├── src/
│   └── total_lots.py
├── tests/
│   └── test_total_lots.py
└── donnees/
    └── lots.xlsx
```

## Lire et écrire Excel avec openpyxl

`openpyxl` manipule le fichier cellule par cellule : idéal pour **garder une mise en forme** ou remplir un modèle.

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font

# Écrire
wb = Workbook()
ws = wb.active
ws.title = "Lots"
ws.append(["Lot", "Montant HT"])            # ligne d'en-tête
ws.append(["Gros oeuvre", 120000])
ws.append(["Electricite", 45000])
ws["A1"].font = ws["B1"].font = Font(bold=True)
ws["A4"] = "Total"
ws["B4"] = "=SUM(B2:B3)"                    # formule Excel (calculée à l'ouverture dans Excel)
wb.save("lots.xlsx")

# Lire
wb = load_workbook("lots.xlsx")             # data_only=True pour lire le résultat des formules
ws = wb["Lots"]
for lot, montant in ws.iter_rows(min_row=2, max_row=3, values_only=True):
    print(lot, montant)
# Gros oeuvre 120000
# Electricite 45000
```

## Lire et écrire Excel avec pandas

`pandas` charge une feuille dans un **DataFrame** (un tableau) : idéal pour **filtrer, agréger, croiser** des données.

```python
import pandas as pd

df = pd.read_excel("lots.xlsx", sheet_name="Lots", nrows=2)   # utilise openpyxl en interne
print(df)
#            Lot  Montant HT
# 0  Gros oeuvre      120000
# 1  Electricite       45000

df["Montant TTC"] = df["Montant HT"] * 1.20
gros = df[df["Montant HT"] > 50_000]          # filtrer
print(df["Montant HT"].sum())                 # 165000

with pd.ExcelWriter("synthese.xlsx") as w:    # plusieurs feuilles
    df.to_excel(w, sheet_name="Detail", index=False)
    gros.to_excel(w, sheet_name="Gros lots", index=False)
```

| Besoin | Outil |
|--------|-------|
| Remplir un modèle mis en forme, styles, formules | `openpyxl` |
| Analyser, filtrer, agréger, fusionner des tableaux | `pandas` |
| Fichiers `.csv` | `pandas.read_csv` ou module `csv` |
| Anciens `.xls` | `pandas` + bibliothèque `xlrd` |

## Pièges courants

- **`python` ouvre le Microsoft Store** : l'installation n'a pas été ajoutée au PATH. Réinstallez en cochant la case, ou désactivez les « alias d'exécution d'application » dans les paramètres Windows.
- **Oublier d'activer le venv** : les bibliothèques s'installent dans le Python global. Vérifiez le `(.venv)` dans le prompt.
- **`PermissionError` en écrivant un `.xlsx`** : le fichier est ouvert dans Excel. Fermez-le.
- **Formules lues comme du texte** : `load_workbook(..., data_only=True)` lit la dernière valeur calculée, mais seulement si le fichier a été enregistré par Excel (un fichier créé par openpyxl n'a pas de valeur calculée : `None`).
- **Chemins Windows** : `"C:\nouveau"` contient `\n` (retour à la ligne). Utilisez `r"C:\nouveau"`, des `/`, ou `pathlib.Path`.
- **Accents mal affichés en CSV** : précisez `encoding="utf-8"` (ou `"utf-8-sig"` / `"cp1252"` pour des fichiers produits par Excel).

## Pour aller plus loin

- Tutoriel officiel Python (en français) : https://docs.python.org/fr/3/tutorial/
- Gestionnaire de projets moderne `uv` (crée venv et installe très rapidement).
- Documentation pandas « 10 minutes to pandas ».
- Suite : [03 — Bonnes pratiques de code](03-bonnes-pratiques-code.md).
