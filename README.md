# data_alex_en_vrac

Dépôt de données et fichiers de travail divers.

## Contenu

### `Gantt_lots.xlsx`

Modèle de planning de projet organisé par lots, sur la période 09/2026 → 02/2028.
Les données sont anonymisées (« Personne A », « Client A », « Projet A »…) : c'est un
gabarit à remplir, pas un planning réel.

| Onglet | Rôle |
|---|---|
| `Gantt` | Diagramme de Gantt : une ligne par tâche, charge mensuelle en heures |
| `Équipe` | Charge par personne et par mois |
| `Projets` | Synthèse par projet (tâches, charge, avancement) |
| `Financement` | Sources de financement, budget vs. affecté, niveau de certitude |
| `Répartition` | Ventilation des heures de chaque tâche par source de financement |
| `Pointage` | Saisie des heures réellement consommées (une ligne = un pointage) |
| `Suivi` | Comparaison référentiel figé (planning) vs. suivi vivant (pointages) |

**Utilisation** : saisir le planning dans `Gantt`, les sources dans `Financement`,
la ventilation dans `Répartition`, puis les heures au fil de l'eau dans `Pointage`.
Les onglets `Équipe`, `Projets` et `Suivi` se calculent automatiquement.

### `pictos/`

Bibliothèque de 316 pictos SVG pour présentations, rangés en 14 catégories.
Voir [`pictos/README.md`](pictos/README.md).

### `modeles/`

Modèles prêts à remplir (Excel, Word, PowerPoint), régénérables avec le `build.py` de chaque dossier.

| Dossier | Contenu |
|---|---|
| [`presentation/`](modeles/presentation) | Modèle de présentation 16:9 (12 diapos) et kit de schémas (matrice 2×2, entonnoir, SWOT, roadmap…) |
| [`gestion-projet/`](modeles/gestion-projet) | Registre des risques, matrice RACI, tableau de bord projets, suivi des actions, compte rendu de réunion |
| [`ingenierie/`](modeles/ingenierie) | Cahier des charges, traçabilité des exigences, AMDEC, revue de conception |
| [`administratif/`](modeles/administratif) | Devis, facture, suivi des temps, notes de frais |

### `tutos/`

Tutoriels en français : logiciel (Git, Python, VS Code, architecture…), algorithmes
(complexité, tris, graphes, programmation dynamique, exercices) et travail avec l'IA
(prompts, sécurité, agents de code, API), Unreal Engine (rendu réaliste). Voir [`tutos/README.md`](tutos/README.md).
