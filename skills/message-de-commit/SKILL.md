---
name: message-de-commit
description: Rédiger un message de commit clair à partir des changements indexés (git diff --staged). À utiliser quand l'utilisateur demande un message de commit ou de committer.
---

# Message de commit

1. Lis `git diff --staged`, et `git log -5 --oneline` pour reprendre la convention du dépôt
   (langue, Conventional Commits ou non, longueur).
2. Si les changements mélangent plusieurs sujets sans rapport, propose de les séparer en
   plusieurs commits.
3. Rédige :
   - **Titre** : 50 à 72 caractères, sans point final, qui dit **ce que fait** le commit, au mode
     utilisé par le dépôt (impératif ou infinitif).
   - **Corps** (si utile) : **pourquoi** ce changement, ce qu'il impacte, ce qui a été écarté.
     Lignes de 72 caractères maximum.
   - Références : ticket ou issue si connu.
4. Ne décris pas le diff ligne à ligne et ne liste pas les fichiers sans raison.

Exemple :

```
Corriger le calcul de la TVA sur les remises

La remise était appliquée après la TVA, ce qui surestimait le total
TTC des devis remisés. Elle est maintenant appliquée sur le HT.

Ticket : PROJ-142
```

Montre le message et attends la validation avant de committer.
