# Modèles de présentation

Fichiers générés par `build.py` (python-pptx), en formes natives PowerPoint, sans image :

- `modele_presentation.pptx` (16:9, 12 diapos) : titre, sommaire, séparateur de partie, texte + visuel, 3 blocs, 4 chiffres clés, frise 5 étapes, comparaison, citation, organigramme, tableau, conclusion/contact.
- `kit_schemas.pptx` (10 diapos) : matrice 2×2, entonnoir, cycle, pyramide, chevrons, roadmap, Venn 3, arbre de décision, SWOT, avant/après.

## Changer la charte
Modifier les constantes en tête de `build.py` (`PRINCIPAL`, `ACCENT`, `GRIS`, `FOND`, `NUANCES`, `POLICE`), puis :

```
python build.py
```

Les deux .pptx sont régénérés (attention : écrasés, faites une copie avant de les remplir).

## Conseils d'usage
- Dupliquer la diapo voulue, remplacer le texte gabarit ; garder 1 message par diapo.
- Pour copier un schéma : sélectionner ses formes, Ctrl+G (grouper), copier-coller dans votre présentation.
- Recolorer : sélectionner une forme > Format de la forme > Remplissage.
- Tailles de police prévues : titres 28, corps 14–16 ; ne pas descendre sous 12.

## Insérer les pictos
Les pictos sont dans `../../pictos/svg/<categorie>/<nom>.svg`.
PowerPoint (Microsoft 365) : Insertion > Images > Cet appareil, choisir le .svg ; puis clic droit > « Convertir en forme » pour le recolorer comme une forme native (couleur du trait = `ACCENT` ou `PRINCIPAL`). Taille conseillée : 0,4 à 0,8 po.
