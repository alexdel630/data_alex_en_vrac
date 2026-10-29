# Modèles d'ingénierie

Gabarits à remplir (texte d'aide en *italique gris* entre crochets à remplacer).

| Fichier | Contenu |
|---|---|
| `cahier_des_charges.docx` | Page de garde, historique des versions, sommaire automatique, 12 sections (contexte → glossaire), exigences MoSCoW |
| `revue_de_conception.docx` | Compte rendu de revue : participants, checklist, points ouverts, décision GO / GO sous réserves / NO-GO, signatures |
| `tracabilite_exigences.xlsx` | Exigence → conception → test → statut ; listes déroulantes, couverture calculée, synthèse % validé par priorité (COUNTIFS) |
| `amdec.xlsx` | Fiche AMDEC (G/O/D 1-10, criticité G×O×D colorée, actions, criticité résiduelle), barèmes, seuils modifiables, synthèse |

## Régénérer

```bash
python build.py
```

Dépendances : `openpyxl`, `python-docx`.

## Notes

- Sommaire Word : clic droit sur le sommaire > *Mettre à jour les champs* (ou F9).
- Seuils AMDEC par défaut : 100 (à surveiller) et 200 (action obligatoire), modifiables dans l'onglet *Seuils*.
- Les formules Excel sont calculées à l'ouverture dans Excel (pas de valeurs mises en cache).
