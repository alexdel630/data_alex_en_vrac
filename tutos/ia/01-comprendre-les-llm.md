# 01 — Comprendre les LLM

## Objectif

Comprendre, sans mathématiques, comment fonctionne un grand modèle de langage (LLM), pour savoir **quand lui faire confiance, quand s'en méfier et comment l'utiliser au mieux**.

## 1. Qu'est-ce qu'un LLM ?

Un LLM (*Large Language Model*) est un programme entraîné sur de très grandes quantités de textes (et souvent de code, d'images…) pour **prédire la suite la plus plausible d'un texte**. À partir de votre message, il génère une réponse morceau par morceau.

Conséquences pratiques :

- Il produit du texte **plausible**, pas nécessairement **vrai**.
- Il ne « consulte » pas une base de faits : il s'appuie sur des régularités apprises, plus éventuellement des documents ou outils que vous lui fournissez (recherche web, fichiers, exécution de code).
- Sa connaissance a une **date limite** liée à son entraînement. Ce qui est plus récent lui est inconnu, sauf accès à des outils de recherche.

Un **assistant** (interface de chat), un **copilote** (intégré à un éditeur ou à une suite bureautique) ou un **agent** (qui enchaîne des actions : lire des fichiers, lancer des commandes) reposent tous sur un LLM, avec plus ou moins d'outils autour.

## 2. Les tokens

Le modèle ne lit pas des mots mais des **tokens** : des fragments de texte (un mot court, un morceau de mot, une ponctuation). Ordre de grandeur : un mot français ≈ 1 à 2 tokens.

Les tokens comptent parce que :

- les **limites** de taille (entrée et sortie) s'expriment en tokens ;
- les **coûts** des API sont généralement calculés au token ;
- certaines tâches « caractère par caractère » (compter des lettres, inverser un mot) sont difficiles pour un modèle qui voit des fragments.

## 3. La fenêtre de contexte

La **fenêtre de contexte** est la quantité de texte que le modèle peut prendre en compte à un instant donné : vos instructions, l'historique de la conversation, les documents joints et sa réponse.

- Au-delà, les éléments les plus anciens sont tronqués ou résumés : le modèle « oublie ».
- Même dans la limite, une information noyée dans un très long contexte peut être moins bien exploitée.
- Le modèle n'a **pas de mémoire entre conversations** sauf fonctionnalité explicite de mémoire. Ne supposez pas qu'il se souvient d'hier.

**Bonne pratique** : pour une nouvelle tâche, ouvrez une nouvelle conversation et redonnez le contexte utile, de façon condensée.

## 4. Les hallucinations

Une **hallucination** est une réponse fausse présentée avec assurance : référence bibliographique inventée, fonction de bibliothèque qui n'existe pas, article de norme imaginaire, chiffre fabriqué.

Situations à risque :

- questions très pointues ou de niche ;
- demandes de références, citations, URL, numéros d'articles de loi ou de norme ;
- calculs longs « de tête » ;
- questions sur des événements récents ;
- questions qui présupposent quelque chose de faux (« Pourquoi la norme X impose-t-elle Y ? »).

Réduire le risque : fournir les sources, demander de citer les passages, autoriser explicitement « je ne sais pas », vérifier (voir [07](07-verifier-et-fiabiliser.md)).

## 5. Ce qu'un LLM fait bien / mal

| Fait plutôt bien | Fait plutôt mal ou de façon non fiable |
|------------------|----------------------------------------|
| Reformuler, résumer, changer de ton | Garantir l'exactitude de faits précis |
| Structurer des idées en plan, tableau, liste | Calculs exacts sans outil de calcul |
| Produire un premier jet (mail, doc, code) | Connaître votre contexte interne sans qu'on le lui donne |
| Expliquer un concept ou du code | Raisonner sur des données qu'il n'a pas vues |
| Traduire, y compris technique | Citer des sources exactes de mémoire |
| Proposer des options, des idées, des contre-arguments | Prendre une décision à votre place |
| Écrire et corriger du code courant | Code critique (sécurité, temps réel) sans revue |
| Repérer incohérences et oublis dans un texte | Être constant : deux essais peuvent différer |

## 6. Autres caractéristiques utiles

- **Non-déterminisme** : la même question peut donner des réponses différentes. Pratique pour explorer, gênant pour la reproductibilité.
- **Complaisance** : le modèle a tendance à aller dans votre sens. Demandez explicitement une critique.
- **Sensibilité à la formulation** : un prompt flou donne une réponse générique.
- **Multimodalité** : en 2026, beaucoup de modèles lisent des images, PDF ou tableaux ; la qualité d'extraction varie, vérifiez les chiffres extraits.

## Exemples concrets

- *Bon usage* : « Voici le compte rendu brut de réunion ci-dessous. Résume les décisions et actions sous forme de tableau. » → le modèle travaille sur **vos** données.
- *Usage risqué* : « Quelle est la valeur limite imposée par la norme XYZ pour… ? » → réponse plausible mais à vérifier systématiquement dans le texte officiel.

## Pièges

- Prendre un ton assuré pour un gage d'exactitude.
- Croire que le modèle « sait » ce qui se passe dans votre entreprise.
- Poursuivre une conversation interminable : le contexte se dégrade.
- Lui demander de compter, calculer ou trier de gros volumes sans outil.
- Confondre « l'IA l'a dit » avec « c'est vérifié ».

## Checklist

- [ ] Je sais que la réponse est plausible, pas garantie.
- [ ] J'ai fourni les données et documents nécessaires plutôt que de compter sur sa mémoire.
- [ ] J'ouvre une nouvelle conversation pour une nouvelle tâche.
- [ ] Je vérifie tout fait, chiffre, référence ou citation qui compte.
- [ ] J'utilise un outil (tableur, script) pour les calculs exacts.
