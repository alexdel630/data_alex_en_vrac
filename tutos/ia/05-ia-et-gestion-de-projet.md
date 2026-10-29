# 05 — IA et gestion de projet

## Objectif

Identifier les usages concrets de l'IA générative dans le pilotage de projet (planning, risques, comptes rendus, reporting), avec leurs limites. L'IA fait gagner du temps sur la **mise en forme et l'analyse** ; la **décision et l'engagement** restent au chef de projet.

## 1. Cadrage

- Reformuler un besoin flou en objectifs SMART.
- Rédiger un premier jet de note de cadrage ou de charte projet.
- Lister les parties prenantes possibles et leurs attentes.
- Faire jouer le rôle d'un sponsor sceptique pour tester l'argumentaire.

Prompt type : « Voici le besoin exprimé par le client. Reformule-le en objectifs mesurables, liste les hypothèses implicites et les questions à poser avant de lancer le projet. »

## 2. Planning

Usages :

- Proposer un **WBS** (découpage en lots et tâches) à partir d'un périmètre.
- Identifier les **dépendances** et les tâches oubliées (recette, documentation, formation, mise en production).
- Rédiger des hypothèses de durée à challenger avec l'équipe.
- Produire un tableau importable dans votre outil de planning (CSV avec ID, tâche, durée, prédécesseurs).

Limites :

- Les durées proposées sont **génériques** : seules l'équipe et l'historique de vos projets donnent des estimations crédibles.
- Le modèle ne calcule pas de chemin critique fiable sur un gros planning : utilisez l'outil de planning.
- Il ignore vos contraintes réelles (congés, disponibilités, budget) si vous ne les donnez pas.

## 3. Risques

Usages :

- Générer une liste de risques initiale par catégorie (voir prompt n°5 de la [bibliothèque](03-bibliotheque-de-prompts.md)).
- Reformuler les risques en « cause → événement → conséquence ».
- Proposer des actions de prévention et des plans de repli.
- Faire une revue critique d'un registre existant : doublons, risques mal formulés, actions non assignées.

Limites : la cotation probabilité/impact est une **proposition** ; elle doit être validée en revue de risques avec les personnes qui connaissent le terrain.

## 4. Comptes rendus de réunion

Usages :

- Transformer des notes brutes en CR structuré (décisions, actions, responsables, échéances).
- Extraire les actions d'une transcription.
- Produire deux versions : détaillée pour l'équipe, synthétique pour la direction.

Limites et précautions :

- L'enregistrement ou la transcription d'une réunion suppose d'**informer les participants** et de respecter les règles internes et le RGPD.
- L'IA peut attribuer un propos à la mauvaise personne ou transformer une piste en décision : **relecture obligatoire** avant diffusion.
- Imposez `[À PRÉCISER]` quand responsable ou échéance manquent.

## 5. Reporting

Usages :

- Rédiger la météo projet hebdomadaire à partir de vos éléments bruts.
- Adapter un même état d'avancement à plusieurs publics (équipe, client, comité).
- Transformer des indicateurs en messages : « Que disent ces chiffres ? Quels points d'attention ? »
- Proposer la structure d'un tableau de bord.

Gabarit de reporting :

```text
À partir des éléments ci-dessous, rédige le point d'avancement hebdomadaire
pour [comité de pilotage].
Format : météo globale (vert/orange/rouge) avec justification en une phrase,
réalisé cette semaine, prévu semaine prochaine, risques et alertes,
décisions attendues du comité. 250 mots max.
Ne modifie aucun chiffre. N'ajoute aucune information absente des éléments.

Éléments :
"""
[avancement, indicateurs, problèmes]
"""
```

Limites : l'IA tend à **lisser** les mauvaises nouvelles et à présenter une situation plus positive. Vérifiez que la météo et les alertes reflètent la réalité. Les chiffres doivent venir de vos outils, pas du modèle.

## 6. Communication et conduite du changement

- Préparer un mail difficile (retard, refus, escalade).
- Préparer un entretien ou une négociation : arguments, objections probables.
- Rédiger une FAQ pour les utilisateurs d'un nouvel outil.

## Exemple concret

Un chef de projet colle ses notes de comité (anonymisées), demande un CR avec tableau d'actions, relit, corrige deux responsables mal attribués, puis demande une version 5 lignes pour la direction. Gain : 30 à 45 minutes, sans délégation de la responsabilité du contenu.

## Pièges

- Diffuser un CR ou un reporting non relu.
- Prendre les estimations de durée ou de coût du modèle pour des engagements.
- Coller des données contractuelles, financières ou RH sans autorisation.
- Utiliser l'IA pour éviter une conversation nécessaire avec l'équipe.
- Laisser l'IA embellir la situation du projet.

## Checklist

- [ ] Les données fournies sont autorisées et anonymisées si besoin.
- [ ] Les chiffres viennent de mes outils, pas du modèle.
- [ ] Les estimations et cotations ont été validées avec l'équipe.
- [ ] Le CR a été relu (attributions, décisions, échéances).
- [ ] Le reporting reflète fidèlement la situation, y compris les mauvaises nouvelles.
- [ ] Les participants savent si une réunion est enregistrée ou transcrite.
