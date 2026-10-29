# Modèles de gestion de projet

Gabarits prêts à remplir (données d'exemple anonymisées : « Personne A », « Projet A »).
Charte : en-têtes bleu nuit #1F2A44 / texte blanc, accent #2F6FED, police Calibri.
Chaque classeur commence par un onglet « Mode d'emploi ».

## Régénérer

```
python build.py
```
Requiert Python 3 avec `openpyxl` et `python-docx`. Les fichiers sont recréés à côté du script (écrasés).

## Fichiers

| Fichier | Contenu |
|---|---|
| `registre_risques.xlsx` | Onglet **Risques** (ID, description, cause, conséquence, catégorie, propriétaire, probabilité 1-5, impact 1-5, criticité P×I colorée, niveau, statut, plan d'action, échéance en rouge si dépassée). **Matrice** 5×5 comptant les risques non clos par case (NB.SI.ENS). **Synthèse** par niveau, statut et catégorie. |
| `matrice_raci.xlsx` | Tâches × 6 personnes, listes R/A/C/I. Colonne **Contrôle** : OK si exactement un A et au moins un R, sinon ligne en rouge avec le motif. Bloc **Charge par personne** (nombre de R, A, C, I, total ; plus chargé en orange). |
| `tableau_de_bord_projets.xlsx` | **Projets** : phase, priorité, météo (Soleil/Nuage/Orage), avancement % (barre), budgets, écart, % consommé, indicateur (Maîtrisé/Dérive/Dépassement). **Synthèse** : totaux, avancement moyen et pondéré, répartition météo, graphique budget prévu vs consommé. |
| `suivi_actions_reunions.xlsx` | **Réunions** (journal) et **Actions** (n°, réunion — liste issue du journal, action, responsable, échéance, statut, retard en jours via AUJOURDHUI()). Retards en rouge, échéances < 7 jours en orange, filtres automatiques. |
| `compte_rendu_reunion.docx` | Modèle Word : en-tête/pied, cartouche, participants, ordre du jour, points abordés, décisions, tableau des actions, prochaine réunion. |

## Notes
- Toutes les valeurs calculées sont de vraies formules Excel (écrites en anglais dans le script, affichées en français par Excel).
- Les plages de formules et de listes sont pré-étendues (200 risques, 40 tâches RACI, 50 projets, 300 actions).
- Le graphique du tableau de bord couvre les 4 projets d'exemple : étendre sa plage si vous ajoutez des projets.
