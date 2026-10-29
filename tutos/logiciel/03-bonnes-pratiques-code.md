# 03 — Bonnes pratiques de code

## Objectif

Écrire du code que vos collègues (et vous dans six mois) comprennent et modifient sans peur : nommage, fonctions courtes, tests automatisés avec `pytest`, revue de code et documentation.

## Prérequis

- [02 — Python premiers pas](02-python-premiers-pas.md) (venv, pip, structure d'un script).
- [01 — Git et GitHub](01-git-et-github.md) pour la partie revue de code.

## Nommage

Un bon nom évite un commentaire. Conventions Python (PEP 8) :

| Élément | Convention | Exemple |
|---------|------------|---------|
| Variable, fonction | `snake_case` | `montant_ht`, `calculer_marge()` |
| Classe | `PascalCase` | `LotChantier` |
| Constante | `MAJUSCULES` | `TAUX_TVA` |
| Module (fichier) | `snake_case` court | `lecture_planning.py` |
| « Privé » (usage interne) | préfixe `_` | `_nettoyer_ligne()` |

```python
# À éviter
def calc(l, t):
    r = 0
    for x in l:
        r += x * t
    return r

# Mieux
def total_ttc(montants_ht: list[float], taux_tva: float) -> float:
    return sum(m * (1 + taux_tva) for m in montants_ht)
```

Conseils : des noms **prononçables** et **précis** (`date_livraison` plutôt que `d`), un verbe pour les fonctions (`charger_lots`), des booléens qui se lisent comme une question (`est_valide`, `a_des_retards`), et les unités dans le nom si ambiguïté (`duree_jours`, `poids_kg`).

## Fonctions

- **Une fonction = une responsabilité.** Si vous devez dire « et » pour la décrire, découpez-la.
- **Courte** : idéalement visible sans faire défiler (≈ 20-30 lignes).
- **Peu de paramètres** (≤ 4) ; au-delà, regroupez dans une `dataclass`.
- **Pas d'effets de bord cachés** : une fonction qui calcule ne devrait pas aussi écrire un fichier.
- **Retour anticipé** plutôt que des `if` imbriqués.

```python
from dataclasses import dataclass


@dataclass
class Lot:
    nom: str
    montant_ht: float
    avancement: float  # entre 0 et 1


def reste_a_facturer(lot: Lot) -> float:
    """Montant HT restant à facturer pour un lot."""
    if not 0 <= lot.avancement <= 1:
        raise ValueError(f"Avancement invalide pour {lot.nom} : {lot.avancement}")
    return round(lot.montant_ht * (1 - lot.avancement), 2)
```

Autres principes utiles :

- **DRY** (*Don't Repeat Yourself*) : un copier-coller répété trois fois mérite une fonction.
- **KISS** (*Keep It Simple*) : la solution la plus simple qui marche.
- **Pas de nombres magiques** : `if retard > SEUIL_ALERTE_JOURS` plutôt que `if retard > 7`.
- **Gérer les erreurs** là où l'on sait quoi en faire ; ne jamais écrire `except: pass`.

## Tests avec pytest

Un test est une fonction qui vérifie automatiquement qu'un comportement est correct. Il vous protège quand vous modifiez le code.

```powershell
python -m pip install pytest
```

Arborescence :

```text
projet/
├── chantier.py          (contient Lot et reste_a_facturer)
└── tests/
    └── test_chantier.py
```

`tests/test_chantier.py` :

```python
import pytest

from chantier import Lot, reste_a_facturer


def test_reste_a_facturer_lot_a_moitie():
    lot = Lot("Peinture", 10_000, 0.5)
    assert reste_a_facturer(lot) == 5_000


def test_lot_termine_ne_reste_rien():
    assert reste_a_facturer(Lot("Peinture", 10_000, 1.0)) == 0


@pytest.mark.parametrize("avancement", [-0.1, 1.5])
def test_avancement_invalide_leve_une_erreur(avancement):
    with pytest.raises(ValueError):
        reste_a_facturer(Lot("Peinture", 10_000, avancement))
```

Lancer les tests depuis la racine du projet :

```powershell
python -m pytest            # lance tous les fichiers test_*.py
python -m pytest -v         # détail de chaque test
python -m pytest -k invalide  # seulement les tests dont le nom contient "invalide"
```

Lancer pytest via `python -m pytest` depuis la racine ajoute ce dossier au chemin d'import : `from chantier import ...` fonctionne.

Bonnes pratiques de test :

- Un test = un comportement, avec un nom qui le décrit.
- Structure **Préparer / Agir / Vérifier** (*Arrange / Act / Assert*).
- Tester les **cas limites** : vide, zéro, valeurs négatives, bornes.
- Comparer des `float` avec `pytest.approx` : `assert 0.1 + 0.2 == pytest.approx(0.3)`.
- Les tests doivent être **rapides et indépendants** (pas d'ordre, pas de dépendance au réseau).

## Revue de code

La revue (sur une pull request GitHub) sert à **partager la connaissance** et attraper les erreurs, pas à juger la personne.

Pour l'auteur :

- PR **petite** (idéalement < 400 lignes) et centrée sur un sujet.
- Description : quoi, pourquoi, comment tester, captures si visuel.
- Relisez votre propre diff avant de demander une revue.

Pour le relecteur, check-list :

| Question | Exemple de point à relever |
|----------|----------------------------|
| Le code fait-il ce qui est demandé ? | cas oublié, mauvaise unité |
| Est-ce lisible ? | nom ambigu, fonction trop longue |
| Est-ce testé ? | cas limite non couvert |
| Y a-t-il un risque ? | secret en clair, suppression de données, entrée non validée |
| Est-ce cohérent avec le reste du projet ? | style, structure des dossiers |

Formulez des commentaires **précis et bienveillants** : « Que se passe-t-il si la liste est vide ? » plutôt que « c'est faux ». Distinguez le bloquant du facultatif (préfixe `nit:` pour un détail).

## Documentation

| Niveau | Quoi | Où |
|--------|------|----|
| Projet | à quoi ça sert, installation, utilisation, exemple | `README.md` |
| Module / fonction | ce que ça fait, paramètres, retour, erreurs | *docstring* |
| Ligne | **pourquoi** (pas *quoi*) d'un choix non évident | commentaire `#` |
| Décision | choix d'architecture et alternatives écartées | `docs/` (ADR) |

Docstring au format Google :

```python
def charger_lots(chemin: str, feuille: str = "Lots") -> list[Lot]:
    """Charge les lots d'un classeur Excel.

    Args:
        chemin: Chemin du fichier .xlsx.
        feuille: Nom de la feuille à lire.

    Returns:
        La liste des lots, dans l'ordre du fichier.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
    """
```

Outils qui automatisent la qualité :

- **ruff** : vérifie le style et les erreurs courantes, et formate (`ruff check .`, `ruff format .`).
- **mypy** : vérifie les annotations de type.
- **pre-commit** : lance ces outils automatiquement avant chaque commit.

## Pièges courants

- **Commentaires qui paraphrasent le code** (`i += 1  # incrémente i`) ou qui ne sont plus à jour.
- **Valeur par défaut mutable** : `def f(t=[])` partage la même liste entre tous les appels. Utilisez `t=None`.
- **`except Exception: pass`** : l'erreur disparaît, le bug reste.
- **Tests qui testent l'implémentation** plutôt que le comportement : ils cassent à chaque refactorisation.
- **Fichier de test nommé `test.py`** ou fonctions sans préfixe `test_` : pytest ne les trouve pas.
- **Refactoriser sans tests** : écrivez d'abord les tests, puis améliorez le code.

## Pour aller plus loin

- PEP 8 (style) et PEP 257 (docstrings).
- Livres : *Clean Code* (R. C. Martin), *The Pragmatic Programmer*.
- `pytest` : fixtures, `tmp_path` pour tester l'écriture de fichiers, couverture avec `pytest-cov`.
- Intégration continue : lancer `pytest` et `ruff` à chaque PR avec GitHub Actions.
- Suite : [04 — VS Code efficace](04-vscode-efficace.md).
