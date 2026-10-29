# 05 — Ligne de commande : PowerShell et bash

## Objectif

Être à l'aise dans un terminal : naviguer, manipuler des fichiers, chercher, enchaîner des commandes, écrire un petit script, et passer de **PowerShell** (Windows) à **bash** (Linux, macOS, Git Bash, serveurs) grâce à une table d'équivalences.

## Prérequis

- Windows : PowerShell est déjà installé ; Git Bash est fourni avec Git pour Windows.
- Aucune connaissance préalable.

## Pourquoi la ligne de commande ?

- Beaucoup d'outils n'existent qu'en ligne de commande (git, pip, pytest...).
- C'est **reproductible** : une commande se copie dans une doc ou un script.
- C'est le seul accès à la plupart des serveurs.

## Se repérer

```powershell
pwd                      # où suis-je ? (Get-Location)
ls                       # que contient ce dossier ? (Get-ChildItem)
cd C:\Projets\outil      # aller dans un dossier
cd ..                    # remonter d'un niveau
cd ~                     # dossier personnel
```

Astuces universelles : **Tab** complète les noms, **↑** rappelle les commandes précédentes, **Ctrl+C** interrompt une commande, `cls` / `clear` efface l'écran.

Chemins : **absolu** (`C:\Projets\outil`, `/home/alex/outil`) ou **relatif** au dossier courant (`.\donnees`, `../outil`). Mettez des guillemets si le chemin contient des espaces : `cd "C:\Mes documents"`.

## Table des équivalences PowerShell / bash

| Action | PowerShell | bash |
|--------|-----------|------|
| Dossier courant | `Get-Location` (`pwd`) | `pwd` |
| Lister | `Get-ChildItem` (`ls`, `dir`) | `ls -la` |
| Lister récursivement | `Get-ChildItem -Recurse` | `find . -type f` / `ls -R` |
| Changer de dossier | `Set-Location` (`cd`) | `cd` |
| Créer un dossier | `New-Item -ItemType Directory -Force rapports` (`mkdir`) | `mkdir -p rapports` |
| Créer un fichier vide | `New-Item notes.txt` | `touch notes.txt` |
| Afficher un fichier | `Get-Content notes.txt` (`cat`) | `cat notes.txt` |
| Début / fin d'un fichier | `Get-Content f.log -TotalCount 10` / `-Tail 10` | `head -n 10 f.log` / `tail -n 10 f.log` |
| Suivre un log en direct | `Get-Content f.log -Wait -Tail 10` | `tail -f f.log` |
| Copier | `Copy-Item a.txt b.txt` (`cp`) | `cp a.txt b.txt` |
| Copier un dossier | `Copy-Item src dst -Recurse` | `cp -r src dst` |
| Déplacer / renommer | `Move-Item a.txt b.txt` (`mv`) | `mv a.txt b.txt` |
| Supprimer un fichier | `Remove-Item a.txt` (`rm`) | `rm a.txt` |
| Supprimer un dossier | `Remove-Item dossier -Recurse` | `rm -r dossier` |
| Chercher du texte | `Select-String -Pattern "erreur" *.log` | `grep "erreur" *.log` |
| Chercher un fichier par nom | `Get-ChildItem -Recurse -Filter *.xlsx` | `find . -name "*.xlsx"` |
| Compter les lignes | `(Get-Content f.txt).Count` | `wc -l f.txt` |
| Variable d'environnement | `$env:PATH` | `$PATH` |
| Définir une variable (session) | `$env:MODE = "test"` | `export MODE=test` |
| Où est un programme ? | `Get-Command python` | `which python` |
| Écrire dans un fichier | `"texte" \| Out-File f.txt -Encoding utf8` | `echo "texte" > f.txt` |
| Ajouter à un fichier | `"texte" \| Add-Content f.txt` | `echo "texte" >> f.txt` |
| Enchaîner si succès | `cmd1; if ($?) { cmd2 }` (PowerShell 7 : `cmd1 && cmd2`) | `cmd1 && cmd2` |
| Aide | `Get-Help Copy-Item -Examples` | `man cp` / `cp --help` |

Les alias (`ls`, `cat`, `rm`...) existent dans PowerShell mais **n'acceptent pas les options bash** : `rm -rf dossier` échoue, il faut `Remove-Item dossier -Recurse -Force`.

## Le pipe `|`

On enchaîne des commandes : la sortie de l'une devient l'entrée de la suivante.

**bash** fait circuler du **texte** :

```bash
# Les 5 fichiers les plus gros du dossier
ls -S | head -n 5
# Nombre de lignes contenant "ERREUR" dans un log
grep "ERREUR" app.log | wc -l
```

**PowerShell** fait circuler des **objets** (avec des propriétés) :

```powershell
# Les 5 fichiers les plus gros
Get-ChildItem | Sort-Object Length -Descending | Select-Object -First 5 Name, Length
# Fichiers Excel modifiés depuis 7 jours
Get-ChildItem -Recurse -Filter *.xlsx |
    Where-Object LastWriteTime -gt (Get-Date).AddDays(-7)
# Lire un CSV et filtrer (séparateur ; courant dans les fichiers français)
Import-Csv lots.csv -Delimiter ";" | Where-Object { [double]$_.Montant -gt 50000 }
```

## Un petit script

Renommer tous les PDF d'un dossier en les préfixant par la date du jour.

PowerShell (`renommer.ps1`) :

```powershell
$date = Get-Date -Format "yyyy-MM-dd"
foreach ($f in Get-ChildItem -Path . -Filter *.pdf) {
    Rename-Item -Path $f.FullName -NewName "$date`_$($f.Name)" -WhatIf
}
```

`-WhatIf` affiche ce qui **serait** fait sans rien modifier : retirez-le une fois satisfait. Le `` ` `` avant `_` empêche PowerShell de lire `$date_` comme un nom de variable. Lancement : `.\renommer.ps1`.

bash (`renommer.sh`) :

```bash
#!/usr/bin/env bash
set -euo pipefail                 # s'arrête à la première erreur
date=$(date +%Y-%m-%d)
for f in *.pdf; do
    [ -e "$f" ] || continue       # aucun PDF : on ne fait rien
    echo mv -- "$f" "${date}_$f"  # retirer "echo" pour exécuter vraiment
done
```

Lancement : `bash renommer.sh` (ou `chmod +x renommer.sh` puis `./renommer.sh`).

## Lancer Python depuis le terminal

```powershell
python script.py --fichier donnees\lots.xlsx   # lancer un script avec un argument
python -c "print(2 ** 10)"                      # exécuter une ligne
python -m http.server 8000                      # serveur web de test sur le dossier courant
```

## Pièges courants

- **Espaces dans les chemins** sans guillemets : la commande voit plusieurs arguments.
- **`\` contre `/`** : Windows accepte les deux dans PowerShell, bash n'accepte que `/`. Git Bash écrit `C:\Users` sous la forme `/c/Users`.
- **Suppression définitive** : `rm` / `Remove-Item` **ne passent pas par la corbeille**. Vérifiez avec `ls` (ou `-WhatIf`) avant.
- **Exécution de scripts bloquée** sous PowerShell : `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (pour votre utilisateur uniquement). Ne désactivez pas la protection globalement.
- **Encodage** : Windows PowerShell 5.1 écrit en UTF-16 avec `>` (PowerShell 7 écrit en UTF-8) ; précisez `-Encoding utf8` pour les fichiers lus par d'autres outils.
- **Copier-coller une commande trouvée sur Internet** sans la comprendre, surtout avec `sudo`, `rm -rf` ou `iex` / `curl ... | bash`.

## Pour aller plus loin

- Installer **PowerShell 7** (`winget install Microsoft.PowerShell`) : plus moderne, `&&` et `||` disponibles.
- **Windows Terminal** : onglets PowerShell, Git Bash et WSL dans une seule fenêtre.
- **WSL** (Windows Subsystem for Linux) pour un vrai Linux sous Windows.
- Outils modernes : `rg` (ripgrep), `fd`, `jq` (JSON).
- Suite : [06 — Architecture logicielle](06-architecture-logicielle.md).
