# 02 — Bien rédiger ses prompts

## Objectif

Écrire des demandes claires qui produisent un résultat exploitable dès le premier ou deuxième essai, et savoir itérer efficacement.

## 1. La structure en 5 blocs

| Bloc | Question | Exemple |
|------|----------|---------|
| **Rôle** | Quel point de vue adopter ? | « Agis comme un ingénieur qualité expérimenté en aéronautique. » |
| **Contexte** | Quelle est la situation, pour qui ? | « Projet de refonte d'un banc de test, équipe de 6, livraison en mars. » |
| **Tâche** | Que faut-il produire exactement ? | « Rédige la section "Exigences de performance" du cahier des charges. » |
| **Format** | Sous quelle forme ? | « Tableau : ID, exigence, critère de validation, priorité. 10 lignes max. » |
| **Contraintes** | Ce qu'il faut respecter / éviter | « Exigences mesurables uniquement. N'invente pas de valeurs : mets [À DÉFINIR]. » |

Le rôle est le bloc le moins important ; le **contexte** et le **format** font la plus grande différence.

### Gabarit

```text
Rôle : tu es [expertise].
Contexte : [situation, public, enjeux, ce qui existe déjà].
Tâche : [verbe d'action + livrable précis].
Format : [structure, longueur, ton, langue].
Contraintes : [à respecter, à éviter, que faire en cas d'incertitude].
Données :
"""
[texte, tableau, code…]
"""
```

Délimitez les données (`"""`, balises `<document>…</document>`, blocs de code) pour séparer clairement instructions et contenu.

## 2. Exemples avant / après

### Mail

- **Avant** : « Écris un mail pour le retard. »
- **Après** : « Rédige un mail au client (directeur technique, relation cordiale mais exigeante) pour annoncer un retard de 2 semaines sur le lot 3, dû à une non-conformité fournisseur. Propose une nouvelle date (15 mai) et une mesure compensatoire (point hebdo). Ton factuel, sans excuses excessives, 150 mots max. »

### Synthèse

- **Avant** : « Résume ce document. »
- **Après** : « Résume ce rapport d'audit pour un comité de direction qui a 2 minutes. Format : 3 constats principaux, 3 risques, 3 recommandations, chacun en une phrase. Indique la page source de chaque point. »

### Code

- **Avant** : « Corrige mon code. »
- **Après** : « Cette fonction Python doit retourner la moyenne glissante sur 7 jours, mais renvoie des NaN sur les premiers jours. Voici le code et un exemple d'entrée/sortie attendue. Explique la cause, puis propose une correction minimale sans changer la signature. »

## 3. Donner des exemples (few-shot)

Montrer 1 à 3 exemples du résultat attendu est souvent plus efficace qu'une longue description.

```text
Classe chaque retour client en : BUG, DEMANDE, QUESTION, AUTRE.

Exemples :
"L'export PDF plante depuis la mise à jour" → BUG
"Ce serait bien d'avoir un mode sombre" → DEMANDE
"Comment changer mon mot de passe ?" → QUESTION

À classer :
"""
[liste]
"""
```

Variez les exemples : sinon le modèle copie leur forme trop fidèlement.

## 4. Demander de poser des questions

Pour une tâche floue ou importante, inversez le processus :

```text
Avant de répondre, pose-moi les questions nécessaires (5 max) pour
bien comprendre mon besoin. Attends mes réponses avant de produire quoi que ce soit.
```

Très utile pour : cahier des charges, plan de projet, stratégie de test, présentation.

## 5. Autres techniques utiles

- **Demander un plan d'abord** : « Propose d'abord le plan, je valide, puis tu rédiges. »
- **Faire raisonner par étapes** : « Analyse étape par étape avant de conclure. »
- **Autoriser l'incertitude** : « Si tu n'es pas sûr, dis-le et indique ce qu'il faudrait vérifier. »
- **Demander une critique** : « Liste les 5 faiblesses principales de ce document. Sois direct. »
- **Fixer la longueur** : « 200 mots », « 5 puces », « une page ».
- **Préciser le public** : « pour un non-spécialiste », « pour un expert sécurité ».

## 6. Itérer

Le premier résultat est rarement le bon. Itérez de façon ciblée :

1. Identifiez ce qui ne va pas (fond, forme, longueur, ton).
2. Donnez une consigne précise : « Garde la structure, mais raccourcis la partie 2 de moitié et supprime le jargon. »
3. Si la conversation part dans tous les sens, **repartez de zéro** avec un prompt amélioré intégrant ce que vous avez appris.
4. Quand un prompt marche bien, **sauvegardez-le** (voir [03](03-bibliotheque-de-prompts.md)).

## Pièges

- Prompt trop court qui laisse le modèle deviner le contexte.
- Prompt-fleuve où la consigne principale se perd : mettez la tâche clairement, au début ou à la fin.
- Consignes contradictoires (« détaillé » et « court »).
- Formulations négatives seules (« ne sois pas vague ») : préférez la consigne positive (« donne des chiffres et des exemples »).
- Croire qu'il existe une formule magique : la qualité vient du contexte et de l'itération.
- Coller des données confidentielles pour « donner du contexte » (voir [06](06-securite-confidentialite-et-ethique.md)).

## Checklist

- [ ] La tâche commence par un verbe d'action et décrit un livrable précis.
- [ ] Le contexte (public, enjeu, existant) est donné.
- [ ] Le format et la longueur sont fixés.
- [ ] Les données sont délimitées.
- [ ] J'ai indiqué quoi faire en cas d'incertitude.
- [ ] Pour une tâche floue, j'ai demandé au modèle de me poser des questions.
- [ ] J'ai sauvegardé le prompt s'il est réutilisable.
