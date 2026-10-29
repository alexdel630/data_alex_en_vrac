# 07 — Vérifier et fiabiliser

## Objectif

Mettre en place des réflexes et une méthode pour vérifier les sorties de l'IA avant de les utiliser, proportionnellement aux enjeux.

## 1. Proportionner l'effort

| Enjeu | Exemples | Niveau de vérification |
|-------|----------|------------------------|
| Faible | Brainstorming, brouillon personnel | Lecture rapide |
| Moyen | Mail interne, CR d'équipe, script jetable | Relecture attentive, faits clés vérifiés |
| Élevé | Livrable client, reporting direction, code en production | Vérification systématique + double lecture humaine |
| Critique | Sécurité, juridique, réglementaire, financier, santé | Validation par un expert, sources primaires obligatoires |

## 2. Checklist de vérification d'un texte

- **Faits** : chaque chiffre, date, nom, référence est-il exact et sourcé ?
- **Fidélité** : la synthèse reflète-t-elle le document source, sans ajout ni omission importante ?
- **Complétude** : manque-t-il un point clé, une exception, une condition ?
- **Cohérence** : pas de contradiction interne, totaux cohérents, unités correctes ?
- **Ton et public** : adapté au destinataire ?
- **Engagements** : le texte n'engage-t-il pas sur une date, un prix, une garantie non validés ?
- **Confidentialité** : aucune information qui ne devrait pas sortir ?

## 3. Vérifier les sources

- Demandez au modèle de **citer le passage** du document fourni qui justifie chaque affirmation, puis contrôlez-le.
- Pour les références externes (articles, normes, lois, documentation), **ouvrez la source primaire**. Une référence inventée peut avoir un titre très crédible.
- Vérifiez la **date** et la **version** des sources (normes, bibliothèques logicielles).
- Pour une recherche web faite par l'outil, vérifiez que la page citée dit bien ce qui est affirmé.

Prompt utile :

```text
Pour chaque affirmation de ta réponse, indique : la source (passage exact du
document fourni ou "connaissance générale"), et ton niveau de confiance
(élevé/moyen/faible). Liste ce que je devrais vérifier en priorité.
```

Attention : l'auto-évaluation du modèle aide à prioriser, mais **ne remplace pas** la vérification.

## 4. Vérifier les chiffres et calculs

- Refaites les calculs dans un tableur ou un script.
- Contrôlez les ordres de grandeur.
- Comparez les totaux aux données sources.
- Préférez demander au modèle une **formule** ou un **script** que vous exécutez, plutôt qu'un résultat calculé « de tête ».

## 5. Vérifier le code

- Lisez le code et faites-vous expliquer ce que vous ne comprenez pas.
- Exécutez-le sur des cas nominaux **et** des cas limites.
- Tests automatisés, linter, analyse statique, analyse de sécurité si disponibles.
- Vérifiez l'existence et la version des bibliothèques et fonctions utilisées.
- Revue par un pair pour tout code destiné à la production (voir [04](04-coder-avec-un-assistant-ia.md)).

## 6. Techniques de fiabilisation

- **Fournir les données** plutôt que compter sur la mémoire du modèle.
- **Autoriser le « je ne sais pas »** et imposer `[À VÉRIFIER]` en cas de doute.
- **Faire critiquer** : dans une nouvelle conversation, demandez une relecture critique de la sortie (« trouve les erreurs »).
- **Comparer** : posez la question deux fois ou à deux outils ; les divergences signalent les zones à vérifier.
- **Découper** : plusieurs petites questions vérifiables valent mieux qu'une grande.
- **Garder une trace** : conservez les prompts et sources utilisés pour les livrables importants.

## 7. Double lecture humaine

Pour les livrables à enjeu, une seconde personne relit **sans** avoir vu le prompt, avec la question : « Est-ce juste, complet et compréhensible ? ». Elle repère ce que l'auteur, habitué au texte, ne voit plus.

Responsabilité : ce que vous signez ou livrez vous engage, quelle que soit la part de l'IA.

## Exemple concret

Un ingénieur fait résumer un rapport d'essai de 40 pages. Il demande la page source de chaque point, vérifie les 5 valeurs numériques citées dans le rapport original, découvre qu'une tolérance a été mal recopiée (± 0,5 au lieu de ± 0,05), corrige, puis fait relire la synthèse par le responsable des essais avant diffusion.

## Pièges

- Vérifier le style mais pas le fond.
- Se fier à l'auto-évaluation du modèle (« je suis sûr à 95 % »).
- Ne vérifier que les points qui « semblent » douteux : les erreurs crédibles passent.
- Vérifier une référence via le même outil qui l'a générée.
- Abandonner la relecture humaine sous la pression du délai.

## Checklist

- [ ] J'ai évalué le niveau d'enjeu et adapté la vérification.
- [ ] Chiffres et calculs recontrôlés avec un outil.
- [ ] Références ouvertes dans leur source primaire.
- [ ] Fidélité au document source vérifiée.
- [ ] Code exécuté, testé et relu.
- [ ] Aucun engagement non validé dans le texte.
- [ ] Double lecture humaine pour les livrables à enjeu.
