---
name: revue-de-code
description: Relire un diff, une branche ou des fichiers et produire une revue de code priorisée (bugs, sécurité, performance, lisibilité). À utiliser quand l'utilisateur demande une revue, un avis sur son code, ou si c'est prêt à merger.
---

# Revue de code

## Méthode

1. Lis le contexte : but du changement (message de commit, ticket, description de la merge
   request), fichiers touchés, conventions du projet (README, fichiers d'instructions, code voisin).
2. Lis **tout** le diff, puis le code appelant et appelé quand c'est nécessaire pour juger.
3. Cherche dans cet ordre :
   - **Correction** : logique fausse, cas limites (vide, nul, zéro, très grand), erreurs non
     gérées, concurrence.
   - **Sécurité** : injections, secrets en clair, entrées non validées, droits.
   - **Données** : migrations, compatibilité, pertes possibles.
   - **Performance** : boucles coûteuses, requêtes répétées, allocations inutiles.
   - **Maintenance** : nommage, duplication, complexité, tests manquants.
4. Pour chaque problème, **vérifie** qu'il est réel (scénario concret) avant de le signaler.

## Format

Classe par gravité : 🔴 bloquant, 🟠 important, 🟡 suggestion.

```markdown
🔴 `fichier.py:42` — <problème en une phrase>
Scénario : <entrée ou état> → <mauvais résultat>
Correction proposée : <code ou explication courte>
```

Termine par : ce qui est bien fait (brièvement), ce que tu n'as pas pu vérifier, et un verdict
(prêt / prêt après corrections / à retravailler). Pas de remarques de style que le linter du
projet couvre déjà.
