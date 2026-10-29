# Modèles administratifs (Excel)

Classeurs générés par `build.py` (Python 3 + openpyxl) : `python build.py`.
Toutes les données sont **fictives** (« Votre Société », « Client A », identifiants à zéro) : à remplacer.
Cellules bleu clair = saisie ; le reste est calculé par de vraies formules Excel.
Chaque onglet est prêt à imprimer en A4 (zone d'impression définie, 1 page de large).

| Fichier | Contenu |
|---|---|
| `devis.xlsx` | Lignes désignation / quantité / unité / PU HT / remise % / TVA (liste), total HT, TVA par taux (SUMIFS), TTC, date de validité calculée, cadre « Bon pour accord ». |
| `facture.xlsx` | Idem + n° de facture, échéance = date + délai (Paramètres), acompte déduit, reste à payer, mentions légales (paiement, pénalités de retard, indemnité forfaitaire 40 €, SIRET, TVA, RCS, capital). |
| `suivi_temps.xlsx` | Saisie (date, personne, projet, tâche, heures) avec listes ; synthèse projet × mois et par personne pour l'année choisie ; tableau croisé personne × projet. |
| `notes_de_frais.xlsx` | Saisie (date, catégorie, description, km, HT, taux TVA, TVA, TTC, justificatif) ; indemnités km = km × taux du barème paramétrable ; totaux par catégorie, avance, net à rembourser, cadre de validation. |

## Onglet « Paramètres »
Infos société (noms définis `Soc_Nom`, `Soc_SIRET`, …), liste des taux de TVA (20 / 10 / 5,5 / 0 %),
délai de paiement, validité du devis, listes personnes/projets/tâches/catégories, barème kilométrique.

## À savoir
- Le barème kilométrique fourni est un **exemple** : le mettre à jour avec le barème officiel de l'année. La part fixe « b » de la tranche 5 001–20 000 km n'est pas répartie par trajet.
- Les mentions légales sont un gabarit indicatif, à faire valider selon votre situation (franchise de TVA, autoliquidation, etc.).
- Un message d'alerte s'affiche si une ligne utilise un taux de TVA ou une catégorie absente des listes.
- Ne pas modifier les classeurs à la main si vous comptez relancer `build.py` : ils sont écrasés.
