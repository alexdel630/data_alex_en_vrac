# Luminance du fond de ciel MWIR (3-5 µm) en fonction de l'altitude

Calcul de transfert radiatif avec **libRadtran 2.0.6** (`uvspec`, solveur DISORT 16 flux,
paramétrisation de bandes LOWTRAN), en alternative libre à MODTRAN.

## Hypothèses

| Paramètre | Valeur |
|---|---|
| Bande | 3-5 µm, pas de 1 nm |
| Visée | 1° au-dessus de l'horizon (`umu -0.01745`) |
| Altitudes | 0,5 ; 1 ; 2 ; 5 ; 8 ; 10 ; 12 ; 15 km |
| Atmosphère | US Standard 1976 (`afglus.dat`) |
| Aérosols | par défaut de libRadtran (rural, ~50 km de visibilité) |
| Soleil | élévation 45°, azimut de visée à 90° du soleil, spectre Kurucz 1 nm |
| Sol | albédo 0,1 |

Les contributions solaire (diffusion) et thermique (émission) sont calculées séparément puis
additionnées.

## Résultats

Voir [`resultats.md`](resultats.md) et [`luminance_mwir.png`](luminance_mwir.png). À 10 km,
la luminance intégrée vaut environ **0,032 W/(m² sr)**, dont 86 % d'émission thermique.

Contrôle : dans la bande opaque du CO₂ (4,25-4,35 µm), la luminance thermique calculée est égale
à celle du corps noir à la température de l'air local (rapport 1,00 à 1,01).

## Limites

- LOWTRAN est moins résolu que MODTRAN : écarts possibles de quelques dizaines de pourcents
  dans les bandes d'absorption.
- Une visée strictement horizontale n'est pas définie en géométrie plan-parallèle ; la
  luminance proche de l'horizon dépend fortement de l'angle exact.
- La part solaire dépend de la géométrie soleil-visée choisie.

## Reproduire

Dans WSL/Linux avec libRadtran compilé dans `~/libradtran/libRadtran-2.0.6` :

```bash
cd ~/libradtran/libRadtran-2.0.6/bin
./uvspec < solaire.inp > solaire.out
./uvspec < thermique.inp > thermique.out
python3 analyse.py
```
