# Pictos pour présentations pro

316 pictos SVG originaux, en trait (24×24, épaisseur 1,75, extrémités arrondies),
dont la couleur suit `currentColor`.

- `svg/<catégorie>/` : un fichier SVG par picto, réparti en 14 catégories
- `apercu.html` : planche d'aperçu, avec réglage de la couleur et de la taille
- `icones/` : source des tracés, un module Python par catégorie
- `build.py` : régénère `svg/` et `apercu.html` (`python build.py`)

**PowerPoint** : Insertion → Images → choisir le SVG, puis Format graphique → Contour
pour la couleur. Clic droit → « Convertir en forme » pour l'éditer.
