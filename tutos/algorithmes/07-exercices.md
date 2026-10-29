# 07 — Exercices

## Objectif

Mettre en pratique les tutos 01 à 06 avec 10 exercices de difficulté croissante. Essayez **avant** d'ouvrir la solution : cliquez sur « Solution » pour la déplier.

## Prérequis

- Python installé ([02 — Python premiers pas](../logiciel/02-python-premiers-pas.md)).
- Les tutos [01](01-complexite.md) à [06](06-algorithmes-gloutons.md) de ce dossier.

Conseil : pour chaque exercice, écrivez d'abord 2 ou 3 tests (`assert`) puis la fonction. Donnez aussi la complexité de votre solution.

| # | Exercice | Notions | Niveau |
|---|----------|---------|--------|
| 1 | Maximum d'une liste | boucle, cas limite | facile |
| 2 | Fréquence des mots | dictionnaire | facile |
| 3 | Palindrome | deux indices | facile |
| 4 | Premier doublon | ensemble | facile |
| 5 | Fusion de deux listes triées | deux indices, O(n) | moyen |
| 6 | Deux montants dont la somme vaut un budget | dictionnaire | moyen |
| 7 | Première occurrence (dichotomie) | recherche dichotomique | moyen |
| 8 | Les k plus gros postes de dépense | tas | moyen |
| 9 | Plus court chemin dans une grille | BFS | difficile |
| 10 | Rendu de monnaie avec le minimum de pièces | programmation dynamique | difficile |

---

### Exercice 1 — Maximum d'une liste

Écrire `maximum(t)` sans utiliser `max()`. Lever `ValueError` si la liste est vide.
Exemple : `maximum([4, -2, 17, 8])` renvoie `17`.

<details>
<summary>Solution</summary>

```python
def maximum(t):
    if not t:
        raise ValueError("liste vide")
    m = t[0]                 # pas 0 : la liste peut ne contenir que des négatifs
    for x in t[1:]:
        if x > m:
            m = x
    return m

print(maximum([4, -2, 17, 8]))  # 17
```

Complexité O(n).
</details>

### Exercice 2 — Fréquence des mots

`frequences(texte)` renvoie un dictionnaire `{mot: nombre}`, sans tenir compte des majuscules.
Exemple : `"Le chat et le chien"` donne `{'le': 2, 'chat': 1, 'et': 1, 'chien': 1}`.

<details>
<summary>Solution</summary>

```python
def frequences(texte):
    compte = {}
    for mot in texte.lower().split():
        compte[mot] = compte.get(mot, 0) + 1
    return compte

print(frequences("Le chat et le chien"))
# {'le': 2, 'chat': 1, 'et': 1, 'chien': 1}
```

Complexité O(n). En pratique : `collections.Counter(texte.lower().split())`.
</details>

### Exercice 3 — Palindrome

`est_palindrome(s)` ignore espaces, ponctuation et majuscules.
Exemple : `"Engage le jeu que je le gagne"` donne `True`.

<details>
<summary>Solution</summary>

```python
def est_palindrome(s):
    s = "".join(c.lower() for c in s if c.isalnum())
    g, d = 0, len(s) - 1
    while g < d:
        if s[g] != s[d]:
            return False
        g += 1
        d -= 1
    return True

print(est_palindrome("Engage le jeu que je le gagne"), est_palindrome("Python"))  # True False
```

Complexité O(n). Version courte : `return s == s[::-1]`.
</details>

### Exercice 4 — Premier doublon

`premier_doublon(t)` renvoie le premier élément qui apparaît une deuxième fois, ou `None`.
Exemple : `["P1", "P7", "P3", "P7", "P1"]` donne `"P7"`.

<details>
<summary>Solution</summary>

```python
def premier_doublon(t):
    vus = set()
    for x in t:
        if x in vus:
            return x
        vus.add(x)
    return None

print(premier_doublon(["P1", "P7", "P3", "P7", "P1"]))  # P7
```

Complexité O(n) grâce au `set` (une double boucle serait O(n²)).
</details>

### Exercice 5 — Fusion de deux listes triées

`fusion_triees(a, b)` renvoie une liste triée en O(len(a) + len(b)), sans `sorted()`.

<details>
<summary>Solution</summary>

```python
def fusion_triees(a, b):
    i = j = 0
    res = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i]); i += 1
        else:
            res.append(b[j]); j += 1
    return res + a[i:] + b[j:]

print(fusion_triees([1, 4, 9], [2, 3, 10, 12]))  # [1, 2, 3, 4, 9, 10, 12]
```

C'est l'étape de fusion du tri fusion.
</details>

### Exercice 6 — Deux montants pour un budget

`deux_sommes(t, cible)` renvoie les indices `(i, j)` de deux montants dont la somme vaut `cible`, ou `None`. Visez O(n).
Exemple : `deux_sommes([120, 450, 300, 80], 380)` donne `(2, 3)`.

<details>
<summary>Solution</summary>

```python
def deux_sommes(t, cible):
    vus = {}                          # montant -> indice
    for i, x in enumerate(t):
        if cible - x in vus:
            return vus[cible - x], i
        vus[x] = i
    return None

print(deux_sommes([120, 450, 300, 80], 380))  # (2, 3)
```

Complexité O(n) au lieu de O(n²) avec deux boucles.
</details>

### Exercice 7 — Première occurrence par dichotomie

Dans une liste triée pouvant contenir des doublons, renvoyer l'indice de la **première** occurrence de `cible` (ou `-1`) en O(log n).

<details>
<summary>Solution</summary>

```python
def premiere_occurrence(t, cible):
    g, d, res = 0, len(t) - 1, -1
    while g <= d:
        m = (g + d) // 2
        if t[m] >= cible:
            if t[m] == cible:
                res = m               # on mémorise et on continue à gauche
            d = m - 1
        else:
            g = m + 1
    return res

print(premiere_occurrence([1, 2, 2, 2, 5, 7], 2))  # 1
print(premiere_occurrence([1, 3], 2))              # -1
```

Équivalent standard : `bisect.bisect_left`.
</details>

### Exercice 8 — Les k plus gros postes de dépense

`k_plus_gros(depenses, k)` renvoie les k couples `(poste, montant)` les plus élevés, du plus grand au plus petit.

<details>
<summary>Solution</summary>

```python
import heapq

def k_plus_gros(depenses, k):
    return heapq.nlargest(k, depenses.items(), key=lambda kv: kv[1])

print(k_plus_gros({"Acier": 52000, "Beton": 31000, "Etudes": 18000, "Grue": 45000}, 2))
# [('Acier', 52000), ('Grue', 45000)]
```

Complexité O(n log k), plus rapide que trier tout (O(n log n)) quand k est petit.
</details>

### Exercice 9 — Plus court chemin dans une grille

Une grille de chaînes : `.` = libre, `#` = obstacle. Départ en haut à gauche, arrivée en bas à droite, déplacements haut/bas/gauche/droite. Renvoyer le nombre minimal de pas, ou `-1`.

```text
..#.
.#..
....
#.#.
```

Réponse attendue : `6`.

<details>
<summary>Solution</summary>

```python
from collections import deque

def plus_court_grille(g):
    h, l = len(g), len(g[0])
    file = deque([(0, 0, 0)])         # ligne, colonne, distance
    vus = {(0, 0)}
    while file:
        i, j, d = file.popleft()
        if (i, j) == (h - 1, l - 1):
            return d
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < h and 0 <= b < l and g[a][b] == "." and (a, b) not in vus:
                vus.add((a, b))
                file.append((a, b, d + 1))
    return -1

print(plus_court_grille(["..#.", ".#..", "....", "#.#."]))  # 6
```

BFS : le premier passage sur l'arrivée est forcément le plus court. Complexité O(h × l).
</details>

### Exercice 10 — Rendu de monnaie optimal

Avec des pièces quelconques, renvoyer le **nombre minimal** de pièces pour faire `montant`, ou `-1` si impossible. Rappel : le glouton échoue pour `6` avec `[1, 3, 4]`.

<details>
<summary>Solution</summary>

```python
def min_pieces(montant, pieces):
    INF = float("inf")
    M = [0] + [INF] * montant         # M[s] = nb minimal de pièces pour faire s
    for s in range(1, montant + 1):
        for p in pieces:
            if p <= s and M[s - p] + 1 < M[s]:
                M[s] = M[s - p] + 1
    return M[montant] if M[montant] != INF else -1

print(min_pieces(6, [1, 3, 4]))  # 2  (3 + 3)
print(min_pieces(7, [2, 4]))     # -1 (impossible)
```

Programmation dynamique, complexité O(montant × nombre de pièces).
</details>

---

## Pièges courants

- Oublier les **cas limites** : liste vide, un seul élément, éléments tous égaux, valeurs négatives.
- Lire la solution trop vite : vous apprendrez davantage en restant bloqué 15 minutes.
- Ne tester que l'exemple de l'énoncé.

## Pour aller plus loin

- Transformez chaque exercice en tests `pytest` ([03 — Bonnes pratiques](../logiciel/03-bonnes-pratiques-code.md)).
- Plateformes d'entraînement : France-IOI (en français), Advent of Code, LeetCode, Codewars.
