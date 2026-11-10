---
name: ecrire-des-tests
description: Écrire des tests automatisés pertinents pour une fonction, un module ou une correction de bug, avec le framework déjà utilisé par le projet. À utiliser quand l'utilisateur demande des tests, une meilleure couverture ou un test de non-régression.
---

# Écrire des tests

1. **Repère l'existant** : framework (pytest, unittest, Jest, Google Test, Unreal Automation…),
   dossier des tests, conventions de nommage, fixtures. Imite-les.
2. **Liste les comportements** à tester avant d'écrire du code :
   - cas nominal ;
   - cas limites : vide, zéro, négatif, très grand, unicode, dates (fin de mois, année bissextile) ;
   - erreurs attendues (exceptions, messages) ;
   - pour un bug : un test qui **échoue avant** la correction et passe après.
3. **Un test = un comportement**, avec un nom explicite (`test_remise_appliquee_avant_tva`).
4. Structure Arrange / Act / Assert, sans logique (boucles, conditions) dans les tests.
5. Évite les dépendances fragiles : temps réel, réseau, ordre d'exécution, aléatoire non fixé.
   Les doubles (mocks) seulement aux frontières : réseau, disque, horloge.
6. **Lance les tests** et montre le résultat. Si un test échoue, détermine si c'est le test ou le
   code qui a tort ; ne modifie jamais une assertion juste pour la faire passer.

Termine par : comportements couverts, comportements volontairement non couverts, et la commande
pour relancer les tests.
