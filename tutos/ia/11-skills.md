# 11 — Les skills : apprendre des savoir-faire à son assistant

## Objectif

Comprendre ce qu'est un **skill** (compétence), installer des skills existants et écrire les
siens pour que l'assistant applique **vos** méthodes de travail de façon répétable.

**Prérequis** : [02 — Bien rédiger ses prompts](02-bien-rediger-ses-prompts.md),
[04 — Coder avec un assistant IA](04-coder-avec-un-assistant-ia.md).

## 1. Le principe

Un skill est un **dossier** contenant un fichier `SKILL.md` : des instructions détaillées pour
une tâche précise (faire un compte rendu, une revue de code, une analyse de risques…), et
éventuellement des fichiers annexes (modèles, scripts, exemples).

```
grill-me/
├── SKILL.md          # obligatoire : en-tête + instructions
├── modele.md         # optionnel : gabarit utilisé par le skill
└── scripts/          # optionnel : scripts que l'agent peut exécuter
```

Le `SKILL.md` commence par un en-tête YAML :

```markdown
---
name: compte-rendu-reunion
description: Transformer des notes brutes en compte rendu avec décisions et actions. À utiliser quand l'utilisateur fournit des notes de réunion ou demande un CR.
---

# Compte rendu de réunion
1. …
```

### Chargement progressif

L'assistant ne lit au départ que le **nom** et la **description** de chaque skill installé (quelques
dizaines de mots). Quand votre demande correspond à une description, il charge le reste du
fichier, puis les annexes si nécessaire. On peut donc installer beaucoup de skills sans
encombrer le contexte.

### Skill, prompt, MCP : la différence

| | Prompt | Skill | Serveur MCP |
|---|---|---|---|
| **Apporte** | Une demande ponctuelle | Un **savoir-faire** réutilisable | Un **accès** à un outil ou à des données |
| **Forme** | Texte tapé | Dossier avec `SKILL.md` | Programme qui tourne |
| **Exemple** | « Résume ce texte » | « Voici comment on fait un CR chez nous » | « Voici comment lire et écrire dans GitLab » |

Skills et MCP se combinent : un skill « gestion de configuration » peut expliquer la méthode,
et un serveur MCP GitLab donner les moyens d'agir.

Le format a été publié comme **standard ouvert** (« Agent Skills ») fin 2025, et plusieurs
assistants le prennent en charge en 2026. Vérifiez la documentation du vôtre pour
l'emplacement des dossiers.

## 2. Les skills de ce dépôt

Le dossier [`skills/`](../../skills/README.md) contient des skills prêts à installer :

| Skill | Usage |
|---|---|
| `grill-me` | L'assistant vous interroge **une question à la fois**, avec sa réponse recommandée, jusqu'à ce que votre plan n'ait plus de zone d'ombre. Idéal avant de lancer un projet, une spec ou une décision importante. |
| `compte-rendu-reunion` | Notes brutes → CR structuré avec tableau d'actions. |
| `revue-de-code` | Revue priorisée (bloquant / important / suggestion) avec scénarios concrets. |
| `message-de-commit` | Message de commit qui explique le pourquoi. |
| `ecrire-des-tests` | Tests utiles avec cas limites, dans le framework du projet. |
| `redaction-specs` | Spécifications avec exigences testables et critères d'acceptation. |
| `analyse-de-risques` | Registre des risques coté probabilité × impact. |
| `gestion-de-configuration-gitlab-dvc` | Gestion de configuration avec GitLab, Git et DVC : identification, merge requests, baselines par tags, CI, audit. |

### Exemple : une séance « grill me »

> **Vous** : Grill me sur mon projet de migration de nos plannings Excel vers un outil web.
>
> **Assistant** : Je reformule : vous voulez remplacer les fichiers Gantt Excel par un outil web
> partagé pour toute l'équipe, c'est bien ça ?
>
> **Vous** : Oui.
>
> **Assistant** : Première question, la plus structurante : qu'est-ce qui doit être vrai dans
> 6 mois pour que ce soit un succès ? **Ma recommandation** : « tous les projets actifs sont
> dans l'outil et le reporting mensuel est produit sans Excel », parce que c'est mesurable et
> que ça force la reprise de l'existant. Ça vous convient ?

Une question par message, une recommandation à chaque fois : on avance vite, et chaque
décision est tracée dans la synthèse finale.

## 3. Installer un skill

Copiez le **dossier** entier dans le répertoire de skills de votre outil. Exemple avec Claude Code :

| Portée | Emplacement |
|---|---|
| Tous vos projets | `~/.claude/skills/<nom>/SKILL.md` |
| Un projet, partagé avec l'équipe via Git | `.claude/skills/<nom>/SKILL.md` |

```bash
cp -r skills/grill-me ~/.claude/skills/
```

Ensuite, le skill se déclenche quand votre demande correspond à sa description, ou à la
demande (par exemple en tapant `/grill-me`).

## 4. Écrire un bon skill

1. **Une tâche précise** par skill. « Tout sur la qualité » est trop large ; « revue de code » est bien.
2. **La description fait tout le travail de déclenchement** : dites **ce que fait** le skill et
   **quand l'utiliser**, avec les mots que vous employez vraiment (« CR », « compte rendu »,
   « récap de réunion »).
3. **Des étapes numérotées**, des critères vérifiables, et le **format de sortie** attendu.
4. **Ce qu'il ne faut pas faire** : inventer une échéance, committer sans validation, lancer une
   commande destructive…
5. **Court** : quelques centaines de lignes au maximum. Mettez les longs modèles ou références
   dans des fichiers annexes que le skill cite.
6. **Testez-le** sur 3 ou 4 cas réels, puis corrigez les instructions là où l'assistant a dévié.

## 5. Sécurité

Un skill peut contenir des instructions **et des scripts** que l'agent exécutera. Avant
d'installer un skill trouvé en ligne :

- lisez entièrement le `SKILL.md` et les scripts ;
- méfiez-vous des instructions qui demandent d'envoyer des données, de télécharger et exécuter
  du code, ou de désactiver des confirmations ;
- préférez les sources de confiance (votre équipe, éditeurs officiels) et versionnez vos skills
  dans Git pour suivre leurs modifications.

## Pièges courants

- Description vague : le skill ne se déclenche jamais, ou au mauvais moment.
- Skill trop long qui répète ce que le modèle sait déjà.
- Deux skills aux descriptions qui se chevauchent : l'assistant hésite.
- Copier seulement `SKILL.md` alors que le skill référence des fichiers annexes.

## Checklist

- [ ] Le skill fait une seule chose, décrite clairement dans `description`.
- [ ] Les étapes et le format de sortie sont explicites.
- [ ] Les interdits (actions destructives, inventions) sont écrits.
- [ ] Testé sur des cas réels.
- [ ] Relu entièrement avant installation s'il vient d'ailleurs.
- [ ] Versionné dans Git.
