# 04 — Coder avec un assistant IA

## Objectif

Utiliser un assistant ou un agent de code pour gagner du temps **sans perdre la maîtrise** du code : découper, contextualiser, relire, tester, et garder un filet de sécurité.

## 1. Les types d'outils

| Type | Fonctionnement | Usage typique |
|------|----------------|---------------|
| Complétion dans l'éditeur | Suggère la suite de la ligne ou du bloc | Code répétitif, boilerplate |
| Chat (dans l'éditeur ou à part) | Vous posez une question, il répond avec du code | Explication, petite fonction, débogage |
| **Agent de code** | Lit le dépôt, modifie plusieurs fichiers, lance des commandes et des tests | Fonctionnalité complète, refactoring, migration |

Un agent est puissant car il **agit** : il peut écrire des fichiers, exécuter des commandes, installer des dépendances. Il exige donc plus de garde-fous.

## 2. Découper la tâche

Les agents réussissent mieux des tâches **petites, précises et vérifiables**.

- Mauvais : « Ajoute la gestion des utilisateurs à l'application. »
- Mieux :
  1. « Propose un plan pour ajouter un modèle `User` (nom, email, rôle) avec migration. N'écris pas de code. »
  2. « Implémente l'étape 1 du plan, avec les tests. »
  3. « Ajoute l'endpoint de création avec validation de l'email. »

Règle pratique : une étape = un changement que vous pouvez relire en quelques minutes et valider par un test.

## 3. Donner le contexte

L'assistant ne connaît pas vos conventions ni vos intentions. Indiquez :

- l'**objectif** et le **pourquoi** de la modification ;
- les **fichiers concernés** (et ceux à ne pas toucher) ;
- les **contraintes** : version du langage, bibliothèques autorisées, style, performance ;
- le **critère de fin** : « les tests existants passent + nouveau test pour le cas X » ;
- pour un bug : message d'erreur complet, étapes de reproduction, comportement attendu vs observé.

### Les fichiers d'instructions projet

Beaucoup d'outils lisent automatiquement un fichier d'instructions placé à la racine du dépôt (par exemple `CLAUDE.md`, `AGENTS.md`, ou un fichier d'instructions propre à l'outil ; le nom dépend de l'outil, vérifiez sa documentation). Il évite de répéter le contexte à chaque session.

Exemple de contenu :

```markdown
# Instructions pour l'assistant

## Projet
API Python 3.12 (FastAPI) de gestion des essais du banc B2.

## Commandes
- Installer : `pip install -e .[dev]`
- Tests : `pytest -q`
- Lint : `ruff check .`

## Conventions
- Typage obligatoire, docstrings en français.
- Pas de nouvelle dépendance sans le demander.
- Toute nouvelle fonction publique a un test.

## Interdits
- Ne jamais modifier `migrations/` existantes.
- Ne jamais écrire de secret dans le code : utiliser les variables d'environnement.
```

Gardez-le court, factuel et à jour ; c'est de la documentation vivante.

## 4. Relire et tester

Le code généré **compile souvent et semble juste**, ce qui rend les erreurs plus insidieuses.

- Relisez chaque diff comme celui d'un collègue junior talentueux mais pressé.
- Vérifiez que les fonctions et bibliothèques appelées **existent vraiment** (hallucinations d'API fréquentes).
- Exigez des tests, et vérifiez que les tests testent quelque chose (un test qui ne peut pas échouer ne sert à rien).
- Méfiez-vous des agents qui « font passer les tests » en modifiant les tests ou en ajoutant des cas particuliers.
- Lancez vous-même les tests, le linter et l'application.
- Si vous ne comprenez pas un passage, demandez une explication ; si vous ne pouvez pas l'expliquer vous-même, ne le fusionnez pas.

## 5. Git comme filet de sécurité

- Travaillez sur une **branche dédiée**, jamais directement sur la branche principale.
- **Committez avant** de lancer l'agent : vous pourrez revenir en arrière.
- Faites des **petits commits** après chaque étape validée.
- Utilisez `git diff` pour relire précisément ce qui a changé.
- Passez par une **revue de pull request** comme pour du code humain.
- Pour annuler des modifications non voulues, privilégiez les commandes réversibles et vérifiez ce qu'elles font avant de les lancer.

## 6. Encadrer les permissions d'un agent

- Limitez les commandes qu'il peut exécuter sans confirmation.
- Refusez les commandes destructrices ou qui touchent hors du projet.
- Ne lui donnez pas accès aux secrets de production.
- Travaillez si possible dans un environnement isolé (conteneur, machine de dev, copie du dépôt).
- Relisez toute dépendance qu'il propose d'ajouter (nom exact, réputation, maintenance) : des paquets malveillants aux noms proches de paquets connus existent.

## Exemple de session réussie

1. « Lis `src/import_csv.py` et explique son fonctionnement. Ne modifie rien. »
2. « Le fichier plante si une ligne a moins de colonnes. Écris d'abord un test qui reproduit le bug. »
3. « Corrige le bug avec un changement minimal ; les lignes invalides sont journalisées et ignorées. »
4. Relecture du diff, `pytest`, commit.

## Pièges

- Demander une énorme fonctionnalité d'un coup et recevoir un diff de 2 000 lignes impossible à relire.
- Accepter du code qu'on ne comprend pas.
- API ou options inventées, versions de bibliothèques obsolètes.
- Secrets écrits en dur dans le code ou collés dans le chat.
- Suppression ou affaiblissement de tests pour « les faire passer ».
- Dérive du périmètre : l'agent « améliore » des fichiers qu'on ne lui a pas demandé de toucher.
- Licences : du code généré peut ressembler à du code existant sous licence ; respectez la politique de votre organisation.

## Checklist

- [ ] Je suis sur une branche dédiée, avec un commit propre avant de commencer.
- [ ] La tâche est découpée en étapes vérifiables.
- [ ] J'ai donné objectif, fichiers, contraintes et critère de fin.
- [ ] Le fichier d'instructions projet existe et est à jour.
- [ ] J'ai relu tout le diff et je le comprends.
- [ ] Les tests passent chez moi et couvrent le changement.
- [ ] Aucun secret dans le code, l'historique ou le chat.
- [ ] Les nouvelles dépendances ont été vérifiées.
