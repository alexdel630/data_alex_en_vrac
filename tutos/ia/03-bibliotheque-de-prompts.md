# 03 — Bibliothèque de prompts

## Objectif

Disposer de prompts prêts à copier pour les tâches courantes d'un ingénieur ou chef de projet. Remplacez les éléments entre `[crochets]`. Vérifiez que les données collées sont autorisées par la politique de votre organisation (voir [06](06-securite-confidentialite-et-ethique.md)).

## Sommaire

1. [Synthèse de document](#1-synthèse-de-document)
2. [Compte rendu de réunion](#2-compte-rendu-de-réunion)
3. [Mail professionnel](#3-mail-professionnel)
4. [Cahier des charges](#4-cahier-des-charges)
5. [Analyse de risques](#5-analyse-de-risques)
6. [Revue de code](#6-revue-de-code)
7. [Explication de code](#7-explication-de-code)
8. [Génération de tests](#8-génération-de-tests)
9. [Analyse Excel](#9-analyse-excel)
10. [Préparation de présentation](#10-préparation-de-présentation)
11. [Traduction technique](#11-traduction-technique)
12. [Brainstorming](#12-brainstorming)

---

## 1. Synthèse de document

```text
Tu es un analyste rigoureux. Résume le document ci-dessous pour [public : ex. comité
de pilotage], qui dispose de [2 minutes].

Format :
- Résumé en 3 phrases
- Points clés (5 puces max)
- Décisions ou actions attendues
- Points ambigus ou manquants

Contraintes : appuie-toi uniquement sur le document. Indique la section ou page
source pour chaque point clé. Si une information n'y figure pas, ne l'invente pas.

Document :
"""
[coller le texte]
"""
```

## 2. Compte rendu de réunion

```text
À partir des notes brutes ci-dessous, rédige le compte rendu de la réunion
[objet] du [date].

Structure :
1. Participants (tels que listés dans les notes)
2. Objet de la réunion
3. Points abordés (synthèse courte par point)
4. Décisions prises
5. Tableau des actions : Action | Responsable | Échéance | Statut
6. Points ouverts / à trancher

Contraintes : ton neutre et factuel. Si un responsable ou une échéance manque,
écris [À PRÉCISER] au lieu de deviner. Ne prête à personne des propos absents des notes.

Notes :
"""
[notes]
"""
```

## 3. Mail professionnel

```text
Rédige un mail à [destinataire et fonction], relation [cordiale / formelle / tendue].
Objectif : [informer / demander / relancer / refuser / annoncer un problème].
Éléments à faire passer :
- [fait 1]
- [fait 2]
- [demande ou prochaine étape, avec date]
Ton : [factuel, courtois, ferme…]. Longueur : [100-150] mots.
Propose un objet de mail et 2 variantes de formulation pour la phrase la plus délicate.
```

## 4. Cahier des charges

```text
Tu es un ingénieur système expérimenté. J'ai besoin d'un cahier des charges pour
[produit / système / prestation].

Avant de rédiger, pose-moi jusqu'à 8 questions sur le besoin, les utilisateurs,
les contraintes (techniques, réglementaires, budget, délai) et les critères
d'acceptation. Attends mes réponses.

Ensuite, produis le plan puis le contenu :
1. Contexte et objectifs
2. Périmètre (inclus / exclus)
3. Exigences fonctionnelles (ID, description, priorité MoSCoW, critère de vérification)
4. Exigences non fonctionnelles (performance, sécurité, maintenabilité…)
5. Contraintes et hypothèses
6. Livrables et jalons
7. Critères de recette

Contraintes : exigences mesurables et vérifiables. Valeurs inconnues → [À DÉFINIR].
```

## 5. Analyse de risques

```text
Contexte du projet :
"""
[objectif, périmètre, planning, équipe, technologies, parties prenantes]
"""

Identifie les principaux risques (15 max) sous forme de tableau :
ID | Risque (cause → événement → conséquence) | Catégorie (technique, planning,
ressources, fournisseur, réglementaire…) | Probabilité (1-4) | Impact (1-4) |
Criticité | Mesure de prévention | Plan de repli | Signal d'alerte

Puis : les 3 risques prioritaires et pourquoi, et les risques que j'aurais pu
oublier compte tenu du contexte. Les cotations sont des propositions à valider.
```

## 6. Revue de code

```text
Tu es un développeur senior [langage]. Fais une revue du code ci-dessous.

Contexte : [rôle du code, contraintes, version du langage/framework].

Classe tes remarques par gravité : BLOQUANT / IMPORTANT / SUGGESTION.
Examine : bugs et cas limites, sécurité (injections, validation des entrées,
secrets), gestion d'erreurs, performance, lisibilité, testabilité.
Pour chaque remarque : ligne concernée, problème, correction proposée.
Ne réécris pas tout le fichier. Si quelque chose est correct, ne l'invente pas comme problème.

"""
[code ou diff]
"""
```

## 7. Explication de code

```text
Explique ce code à [un ingénieur qui connaît Python mais pas ce projet /
un débutant / un chef de projet non développeur].

1. Ce que fait le code en 3 phrases
2. Déroulé pas à pas des parties importantes
3. Entrées, sorties, effets de bord (fichiers, réseau, base de données)
4. Hypothèses implicites et points fragiles
5. Questions que je devrais poser à l'auteur

"""
[code]
"""
```

## 8. Génération de tests

```text
Écris des tests unitaires [framework : pytest, JUnit, Jest…] pour la fonction
ci-dessous.

Couvre : cas nominal, cas limites (vide, nul, valeurs extrêmes, types inattendus),
cas d'erreur attendus. Un test = un comportement, avec un nom explicite.
N'appelle aucune ressource externe (réseau, base) : utilise des doubles de test.
Commence par la liste des cas que tu vas tester, puis le code.
Si le comportement attendu est ambigu pour un cas, signale-le au lieu de choisir.

"""
[code + spécification ou docstring]
"""
```

## 9. Analyse Excel

```text
Voici un extrait d'un tableau [description : ex. suivi des heures par lot] avec
ses en-têtes. Colonnes : [liste et signification].

"""
[coller quelques dizaines de lignes, données anonymisées]
"""

1. Décris la structure et signale les anomalies de données (vides, doublons,
   formats incohérents).
2. Propose les formules Excel (en français ou anglais : [préciser]) pour calculer
   [indicateur], avec explication.
3. Propose 3 analyses ou graphiques pertinents pour [objectif].
Ne fais pas de calculs de tête sur les données : donne les formules pour que je
les calcule dans le tableur.
```

## 10. Préparation de présentation

```text
Je dois présenter [sujet] à [public] pendant [durée]. Objectif : [obtenir une
décision / informer / convaincre].
Messages clés : [1, 2, 3].
Matière disponible :
"""
[notes, chiffres, rapport]
"""

Propose :
1. Un fil narratif en une phrase
2. Le plan diapositive par diapositive (titre-message, contenu, visuel suggéré)
   pour [8-10] diapos max
3. Les 5 questions difficiles probables et des éléments de réponse
Chaque titre de diapo doit être une affirmation, pas un thème.
```

## 11. Traduction technique

```text
Traduis le texte suivant du [français] vers l'[anglais] pour [public : ex.
ingénieurs d'un partenaire industriel].

Contraintes :
- Respecte ce glossaire : [terme source → terme cible]
- Conserve le formatage, les unités, les références et identifiants tels quels
- Ne traduis pas le code, les noms de variables ni les messages d'erreur
- Signale à la fin les termes ambigus et tes choix de traduction

"""
[texte]
"""
```

## 12. Brainstorming

```text
Problème : [description]. Contraintes : [budget, délai, technique, organisationnelles].

1. Propose 15 idées variées, des plus classiques aux plus audacieuses, en une
   ligne chacune.
2. Regroupe-les par familles.
3. Pour les 3 plus prometteuses : avantages, inconvénients, premier test simple
   pour valider l'idée en moins d'une semaine.
4. Joue l'avocat du diable sur la meilleure idée.
```

---

## Pièges

- Copier un prompt sans adapter le contexte : le résultat reste générique.
- Coller des données personnelles ou confidentielles « parce que le prompt le demande ».
- Utiliser la sortie sans relecture (CR, mail, traduction envoyés tels quels).
- Laisser le modèle inventer des responsables, dates ou valeurs : imposez `[À PRÉCISER]`.

## Checklist

- [ ] J'ai remplacé tous les `[crochets]`.
- [ ] Les données collées sont autorisées et anonymisées si nécessaire.
- [ ] J'ai relu et vérifié la sortie avant de l'utiliser.
- [ ] J'ai adapté et enregistré ma version du prompt si elle est meilleure.
