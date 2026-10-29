# 04 — VS Code efficace

## Objectif

Faire de Visual Studio Code un environnement de travail confortable pour Python : bonnes extensions, raccourcis Windows essentiels, débogueur, terminal intégré et Git intégré.

## Prérequis

- VS Code installé (https://code.visualstudio.com ou `winget install Microsoft.VisualStudioCode`).
- Python installé ([02 — Python premiers pas](02-python-premiers-pas.md)).
- Git installé ([01 — Git et GitHub](01-git-et-github.md)).

## Premier réflexe : ouvrir un dossier, pas un fichier

**Fichier > Ouvrir le dossier** (ou `code .` dans un terminal) : VS Code connaît alors tout le projet (recherche, Git, venv, débogage).

## Extensions utiles

Installation : `Ctrl+Shift+X`, puis recherche par nom.

| Extension | Éditeur | Utilité |
|-----------|---------|---------|
| Python | Microsoft | exécution, venv, tests, débogage (installe aussi Pylance et Python Debugger) |
| Pylance | Microsoft | autocomplétion, vérification de types |
| Ruff | Astral | style et formatage automatique |
| Jupyter | Microsoft | notebooks `.ipynb` |
| French Language Pack | Microsoft | interface en français |
| GitLens | GitKraken | qui a modifié quelle ligne, historique |
| Rainbow CSV | mechatroner | lisibilité des CSV |
| Markdown All in One | Yu Zhang | aperçu et raccourcis Markdown |
| Markdown Preview Mermaid Support | Matt Bierner | affiche les diagrammes mermaid dans l'aperçu |
| Error Lens | Alexander | affiche les erreurs directement sur la ligne |

N'installez que ce dont vous avez besoin : trop d'extensions ralentissent l'éditeur. N'installez que des extensions d'éditeurs reconnus (beaucoup de téléchargements, éditeur vérifié).

## Choisir l'interpréteur Python (venv)

`Ctrl+Shift+P` > **Python: Select Interpreter** > choisissez celui du dossier `.venv`. VS Code l'active ensuite automatiquement dans les nouveaux terminaux.

## Raccourcis Windows essentiels

| Raccourci | Action |
|-----------|--------|
| `Ctrl+Shift+P` | **Palette de commandes** (tout est accessible ici) |
| `Ctrl+P` | Ouvrir un fichier par son nom |
| `Ctrl+Maj+F` | Rechercher dans tout le projet |
| `Ctrl+F` / `Ctrl+H` | Rechercher / remplacer dans le fichier |
| `Ctrl+ù` | Afficher / masquer le terminal (clavier AZERTY ; `` Ctrl+` `` en QWERTY) |
| `Ctrl+B` | Afficher / masquer la barre latérale |
| `Ctrl+:` | Commenter / décommenter (AZERTY ; `Ctrl+/` en QWERTY) |
| `Alt+↑` / `Alt+↓` | Déplacer la ligne |
| `Maj+Alt+↓` | Dupliquer la ligne |
| `Ctrl+D` | Sélectionner l'occurrence suivante (multi-curseurs) |
| `Alt+clic` | Ajouter un curseur |
| `F2` | Renommer un symbole partout |
| `F12` / `Alt+F12` | Aller à la définition / l'afficher en aperçu |
| `Maj+Alt+F` | Formater le document |
| `Ctrl+Espace` | Forcer l'autocomplétion |
| `Ctrl+\` | Diviser l'éditeur |
| `Ctrl+K Ctrl+S` | Liste de tous les raccourcis (personnalisables) |

Les raccourcis peuvent varier selon la disposition du clavier : en cas de doute, cherchez la commande dans `Ctrl+K Ctrl+S`.

## Le débogueur

Plus efficace que des `print` partout.

1. Cliquez dans la marge à gauche d'un numéro de ligne : un **point d'arrêt** rouge apparaît.
2. `F5` > **Python Debugger: Current File**.
3. Le programme s'arrête sur la ligne. Panneau de gauche : variables locales, expressions surveillées, pile d'appels.

| Touche | Action |
|--------|--------|
| `F5` | Démarrer / continuer jusqu'au prochain point d'arrêt |
| `F10` | Ligne suivante (sans entrer dans les fonctions) |
| `F11` | Entrer dans la fonction appelée |
| `Maj+F11` | Sortir de la fonction |
| `Maj+F5` | Arrêter |

Astuces : clic droit sur un point d'arrêt > **Modifier le point d'arrêt** pour un point conditionnel (`lot == "Peinture"`) ; la **console de débogage** permet d'évaluer des expressions pendant la pause.

Pour enregistrer une configuration (arguments, dossier de travail), créez `.vscode/launch.json` :

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Synthèse des lots",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/src/total_lots.py",
      "args": ["--fichier", "donnees/lots.xlsx"],
      "cwd": "${workspaceFolder}",
      "console": "integratedTerminal"
    }
  ]
}
```

## Le terminal intégré

- `Ctrl+ù` ouvre un terminal **dans le dossier du projet**, venv activé.
- Le `+` crée un nouveau terminal ; la flèche à côté choisit le shell (PowerShell, Git Bash, Invite de commandes).
- Définir le shell par défaut : `Ctrl+Shift+P` > **Terminal: Select Default Profile**.
- Clic sur un chemin `fichier.py:12` dans une erreur : ouvre le fichier à la bonne ligne (`Ctrl+clic`).

## Git intégré

Icône **Contrôle de code source** (`Ctrl+Maj+G`) :

1. Les fichiers modifiés apparaissent ; un clic montre le **diff** côte à côte.
2. `+` sur un fichier = `git add`.
3. Message dans la zone de texte, puis **Valider** (`Ctrl+Entrée`) = `git commit`.
4. **Synchroniser** = `git pull` puis `git push`.
5. Nom de branche en bas à gauche : cliquer pour changer ou créer une branche.
6. En cas de conflit, VS Code propose *Accepter la modification actuelle / entrante / les deux*, ou un **éditeur de fusion** à trois volets.

Gardez un œil sur la ligne de commande : savoir ce que font ces boutons ([01 — Git](01-git-et-github.md)) évite les surprises.

## Réglages utiles

`Ctrl+,` ouvre les paramètres. Quelques réglages recommandés (`settings.json`) :

```json
{
  "editor.formatOnSave": true,
  "files.autoSave": "onFocusChange",
  "editor.rulers": [88],
  "files.trimTrailingWhitespace": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "python.testing.pytestEnabled": true
}
```

Avec `python.testing.pytestEnabled`, l'icône **Tests** (fiole) liste et lance vos tests pytest, y compris en mode débogage.

## Pièges courants

- **Mauvais interpréteur** : `ModuleNotFoundError` alors que la bibliothèque est installée. Vérifiez l'interpréteur affiché en bas à droite.
- **Ouvrir un fichier isolé** au lieu du dossier : pas de Git, pas de venv détecté.
- **Exécuter avec le bouton ▶ depuis un autre dossier** : les chemins relatifs (`donnees/lots.xlsx`) ne sont pas trouvés. Utilisez `pathlib` relativement à `__file__` ou réglez `cwd`.
- **Commiter `.vscode/` avec des réglages personnels** : ne partagez que ce qui sert à toute l'équipe (`launch.json`, `extensions.json`).
- **Extensions non fiables** : une extension a accès à vos fichiers ; restez sur des éditeurs connus.

## Pour aller plus loin

- Documentation officielle : *Python in VS Code*, *Debugging*.
- Fichier `.vscode/extensions.json` pour recommander des extensions à l'équipe.
- Extension **Remote - SSH / WSL / Dev Containers** pour travailler sur un serveur ou sous Linux.
- Suite : [05 — Ligne de commande](05-ligne-de-commande.md).
