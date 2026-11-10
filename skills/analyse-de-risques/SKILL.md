---
name: analyse-de-risques
description: Identifier, coter et traiter les risques d'un projet (probabilité × impact, plan d'action) au format d'un registre des risques. À utiliser quand l'utilisateur demande une analyse de risques, un registre, ou ce qui peut mal tourner.
---

# Analyse de risques

1. Récupère le contexte : objectif, planning, équipe, budget, dépendances, technologies.
2. Balaye les catégories : technique, planning, ressources humaines, budget, fournisseurs,
   réglementaire, sécurité, qualité, adoption par les utilisateurs.
3. Pour chaque risque, formule « **cause** → **événement** → **conséquence** ». Un constat
   (« on manque de temps ») n'est pas un risque.
4. Cote **probabilité** et **impact** de 1 à 5 ; criticité = P × I :
   1–4 faible, 5–9 moyen, 10–14 élevé, 15–25 critique. Justifie chaque cote en une phrase.
5. Pour les risques élevés et critiques : stratégie (éviter, réduire, transférer, accepter),
   action concrète, responsable (« à définir » si inconnu) et signal d'alerte observable.

## Format

| ID | Risque (cause → conséquence) | Catégorie | P | I | Criticité | Action | Signal d'alerte |
|---|---|---|---|---|---|---|---|

Termine par les 3 risques prioritaires et ce qui manque pour mieux les évaluer. Le classeur
`modeles/gestion-projet/registre_risques.xlsx` de ce dépôt reprend ces colonnes.
