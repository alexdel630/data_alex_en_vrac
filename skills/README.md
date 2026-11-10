# Skills pour assistants IA

Compétences prêtes à installer dans un assistant compatible avec le format **Agent Skills**
(un dossier par skill, contenant un fichier `SKILL.md`). Explications complètes dans le tuto
[11 — Les skills](../tutos/ia/11-skills.md).

| Skill | Quand l'utiliser |
|---|---|
| [`grill-me`](grill-me/SKILL.md) | Se faire challenger sur un plan, une question à la fois, jusqu'à ce que tout soit clair. |
| [`compte-rendu-reunion`](compte-rendu-reunion/SKILL.md) | Notes brutes → compte rendu avec décisions et actions. |
| [`revue-de-code`](revue-de-code/SKILL.md) | Revue priorisée d'un diff ou d'une branche. |
| [`message-de-commit`](message-de-commit/SKILL.md) | Message de commit clair à partir des changements indexés. |
| [`ecrire-des-tests`](ecrire-des-tests/SKILL.md) | Tests utiles, cas limites, non-régression. |
| [`redaction-specs`](redaction-specs/SKILL.md) | Cahier des charges et exigences testables. |
| [`analyse-de-risques`](analyse-de-risques/SKILL.md) | Registre des risques coté P × I avec plan d'action. |
| [`gestion-de-configuration-gitlab-dvc`](gestion-de-configuration-gitlab-dvc/SKILL.md) | Gestion de configuration avec GitLab, Git et DVC : baselines, MR, CI, audit. |

## Installation

Copiez le **dossier** du skill (pas seulement le fichier) dans le répertoire de skills de votre
outil. Exemple avec Claude Code :

- pour tous vos projets : `~/.claude/skills/<nom-du-skill>/SKILL.md` ;
- pour un seul projet (partagé avec l'équipe via Git) : `.claude/skills/<nom-du-skill>/SKILL.md`.

Les autres assistants compatibles ont leur propre emplacement : voir leur documentation.

```bash
cp -r skills/grill-me ~/.claude/skills/
```

Le skill se déclenche ensuite automatiquement quand votre demande correspond à sa description,
ou à la demande (par exemple `/grill-me` dans Claude Code).

## Crédits

L'idée du skill « grill me » a été popularisée par Matt Pocock. La version de ce dépôt est une
réécriture originale en français.
