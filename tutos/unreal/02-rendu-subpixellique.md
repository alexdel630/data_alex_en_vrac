# Rendu d'un objet subpixellique dans une image capteur (Unreal Engine 5.8)

> **Statut** : note de travail — pistes de solution, non encore implémentées ni testées en jeu.
> Toutes les approches décrites sont considérées comme valables ; le choix final dépendra des
> essais.

## 1. Le problème

Dans une simulation de capteur (par exemple un imageur infrarouge MWIR), une cible lointaine
(avion, drone) peut couvrir **moins d'un pixel**. La rastérisation d'Unreal fonctionne en « tout
ou rien » : un triangle n'écrit un pixel que s'il en recouvre le centre (ou un échantillon). Donc :

- la cible **disparaît** quand elle tombe entre deux centres de pixels ;
- elle **clignote** quand elle se déplace d'une fraction de pixel ;
- son énergie n'est **pas conservée** : un pixel touché prend la luminance pleine de la cible
  au lieu d'un mélange pondéré par la surface couverte.

Un vrai capteur, lui, **intègre l'énergie** reçue sur toute la surface de chaque pixel, à travers
la PSF (réponse impulsionnelle) de son optique.

### Cadre retenu (séance « grill me »)

| # | Décision |
|---|---|
| D1 | Objectif : rendre correctement une cible **subpixellique** dans l'image capteur d'UE 5.8. |
| D2 | Critère de succès : énergie de la cible sommée sur les pixels conservée à **±5 %** quelle que soit sa position sous-pixel, **sans scintillement** d'une image à l'autre. |
| D3 | Capteur générique paramétrable ; seuls comptent ici l'**IFOV** (150 µrad par défaut) et la **PSF** (gaussienne σ ≈ 0,6 pixel par défaut). |
| — | Hors périmètre : signature de la cible (peau, panache), bruit du capteur, calcul du fond atmosphérique. |

Piste d'interface proposée (non tranchée) : le module subpixel reçoit, par cible et par image,
une **position 3D** et un **contraste de luminance équivalent** ΔL_eq calculé ailleurs.

## 2. La physique à reproduire

Pour une cible non résolue, la contribution à un pixel vaut :

$$
\Delta L_{pixel} = \underbrace{\frac{(L_{cible} - L_{fond})\,A_{proj}\,\tau}{R^2\,\Omega_{pixel}}}_{\Delta L_{eq}}
\times \iint_{pixel} PSF(x - x_0,\, y - y_0)\,dx\,dy
$$

| Symbole | Signification |
|---|---|
| $L_{cible}, L_{fond}$ | Luminances de la cible et du fond masqué |
| $A_{proj}$ | Surface projetée de la cible vue du capteur |
| $\tau$ | Transmission atmosphérique sur le trajet |
| $R$ | Distance capteur-cible |
| $\Omega_{pixel}$ | Angle solide d'un pixel (≈ IFOV²) |
| $(x_0, y_0)$ | Position **sous-pixel** de la cible dans l'image |

Le terme $(L_{cible} - L_{fond})$ traduit que la cible **ajoute** sa luminance mais **masque**
aussi le fond. Si l'on connaît directement l'intensité de la cible $I$ (W/sr) :
$\Delta L_{eq} = I\,\tau / (R^2\,\Omega_{pixel})$.

La somme de l'intégrale de la PSF sur tous les pixels vaut 1 : c'est ce qui garantit la
conservation de l'énergie.

## 3. Les pistes de solution

### Vue d'ensemble

| # | Approche | Principe | Pour | Contre |
|---|---|---|---|---|
| A | **Sur-échantillonnage** | Rendre à N× la résolution puis réduire (moyenne par blocs ou convolution PSF) | Géométrie réelle (forme, orientation, occultations) | Coût en N² ; reste faux si la cible fait moins de 1/N pixel |
| B | **Injection analytique** | Projeter la cible et déposer son énergie via la PSF intégrée par pixel, en post-process | Exact, stable, coût négligeable, indépendant de la distance | La cible est réduite à un point (pas de forme) |
| C | **Hybride** | A (ou rendu natif) quand la cible fait plus de 2 à 3 pixels, B en dessous, fondu entre les deux | Correct à toutes les distances | Plus d'intégration ; zone de transition à valider |
| D | **Sprite à énergie conservée** | Remplacer la cible lointaine par un billboard additif toujours plus grand que quelques pixels, dont la texture est la PSF normalisée | Reste dans le pipeline de rendu standard (profondeur, occultation par les nuages) | Normalisation délicate ; dépend de la résolution |
| E | **Rendu ciblé (« tuile » haute résolution)** | Un second SceneCapture à très petit champ centré sur la cible, rendu à haute résolution, puis réduit et recollé dans l'image | Forme réelle même très loin ; coût limité à une petite zone | Plusieurs captures si plusieurs cibles ; recalage à soigner |
| F | **Path tracer / Movie Render Queue** | Nombreux échantillons spatiaux par pixel (anti-aliasing par sur-échantillonnage) | Référence physique, utile pour valider | Hors temps réel |

### A. Sur-échantillonnage

- **SceneCapture2D** avec un render target de N×W × N×H, puis réduction dans un compute shader
  ou un matériau (moyenne de N×N pixels, ou convolution par la PSF puis décimation).
- Variante rapide : `r.ScreenPercentage` à 200–400 % avec l'anti-aliasing temporel désactivé.
- Variante hors ligne : **Movie Render Queue**, *Spatial Sample Count* élevé (16 à 64),
  *Temporal Sample Count* = 1.
- Règle : N doit être assez grand pour que la cible couvre au moins quelques sous-pixels. Pour
  une cible de 0,1 pixel, il faut N ≥ 20, donc 400 fois plus de pixels : c'est là que A atteint
  sa limite.

### B. Injection analytique (piste privilégiée pour le subpixel)

**1. Projection** (C++, à chaque image) :

```cpp
// Position sous-pixel de la cible dans l'image du capteur
FVector2D PixelPos;
const bool bVisible = UGameplayStatics::ProjectWorldToScreen(
    PlayerController, Cible->GetActorLocation(), PixelPos, /*bPlayerViewportRelative=*/true);

MID->SetVectorParameterValue("CiblePixel", FLinearColor(PixelPos.X, PixelPos.Y, 0, 0));
MID->SetScalarParameterValue("DeltaLeq", DeltaLeq);   // calculé hors du module
MID->SetScalarParameterValue("SigmaPSF", SigmaPx);    // largeur de la PSF en pixels
```

Pour un **SceneCapture2D**, il faut projeter avec la matrice de vue-projection du capture
lui-même (et non celle du viewport joueur), et tenir compte d'une éventuelle différence de
résolution.

**Occultation** : avant d'injecter, tester si la cible est cachée (relief, nuage opaque) en
comparant sa profondeur à la *SceneDepth* au pixel projeté, ou par un *line trace*.

**2. Dépôt de l'énergie** (matériau de post-process, nœud *Custom*) — PSF gaussienne intégrée
**exactement** sur chaque pixel grâce à la fonction erf :

```hlsl
// Entrées : PixelCoord (float2, centre du pixel courant en pixels), CiblePixel (float2),
//           SigmaPSF (float), DeltaLeq (float), SceneColor (float3)
float erf_approx(float x)
{
    // Abramowitz & Stegun 7.1.26, erreur < 1.5e-7
    float s = sign(x); x = abs(x);
    float t = 1.0 / (1.0 + 0.3275911 * x);
    float y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
              - 0.284496736) * t + 0.254829592) * t * exp(-x * x);
    return s * y;
}

float2 d0 = (PixelCoord - 0.5 - CiblePixel) / (SigmaPSF * 1.41421356);
float2 d1 = (PixelCoord + 0.5 - CiblePixel) / (SigmaPSF * 1.41421356);
float fx = 0.5 * (erf_approx(d1.x) - erf_approx(d0.x));
float fy = 0.5 * (erf_approx(d1.y) - erf_approx(d0.y));
return SceneColor + DeltaLeq * fx * fy;
```

Variantes :
- **PSF de diffraction** (tache d'Airy) : approximable par une gaussienne σ ≈ 0,42·λ·N / pas du
  pixel, ou tabulée.
- **PSF mesurée** : la stocker dans une texture, puis pré-intégrer ses valeurs par pixel pour un
  décalage donné (table 2D indexée par la position sous-pixel).
- **Plusieurs cibles** : tableau de positions passé en *Material Parameter Collection*, ou passe
  en compute shader (*Render Dependency Graph*) qui accumule toutes les cibles dans une texture.
- **Flou de bougé** : intégrer la PSF le long du déplacement de la cible pendant le temps
  d'intégration du capteur (somme de quelques positions intermédiaires).

### C. Hybride

- Calculer la taille projetée de la cible en pixels : $d_{px} = \text{envergure} / (R \cdot \text{IFOV})$.
- $d_{px} > 3$ : rendu géométrique normal (éventuellement sur-échantillonné, piste A ou E).
- $d_{px} < 1$ : cible masquée dans le rendu géométrique, injection analytique seule (piste B).
- Entre 1 et 3 : **fondu** linéaire entre les deux, en vérifiant que l'énergie totale reste
  continue.
- Cacher la géométrie en dessous du seuil évite de compter l'énergie deux fois (option
  *Hidden in Scene Capture* ou *Owner No See* par capture).

### D. Sprite à énergie conservée

- Un billboard (ou une particule Niagara) en **blend additif**, dont la taille à l'écran est
  maintenue à environ 6σ de PSF, avec une texture = PSF normalisée.
- L'intensité du matériau est réglée pour que la somme des pixels vaille ΔL_eq.
- Avantage : il passe par le test de profondeur standard, donc les occultations sont gérées.
- Attention : la rastérisation du sprite lui-même réintroduit un léger aliasing ; à combiner
  avec un léger sur-échantillonnage.

### E. Tuile haute résolution centrée sur la cible

- Un second SceneCapture2D avec un champ de quelques pixels capteur, orienté vers la cible, rendu
  à haute résolution (par exemple 256×256 pour 4×4 pixels capteur).
- La tuile est réduite à la résolution du capteur (intégration par pixel + PSF) puis composée
  dans l'image principale à la bonne position sous-pixel.
- Conserve la forme réelle (ailes, orientation) même à très grande distance, pour un coût
  maîtrisé.

### F. Référence hors ligne

- Path tracer ou Movie Render Queue avec beaucoup d'échantillons spatiaux : sert de **vérité
  terrain** pour valider A à E sur quelques images.

## 4. Réglages Unreal indispensables

| Réglage | Pourquoi |
|---|---|
| SceneCapture → *Capture Source* : **SceneColor (HDR) in RGB, Inv Opacity in A** ; render target **RGBA32f** (ou 16f) | Valeurs linéaires, sans tonemapper |
| Désactiver **auto-exposition, bloom, vignette, film grain, lens flares, motion blur** | Ces effets modifient la radiométrie |
| Anti-aliasing **None** (ou FXAA), **pas de TSR/TAA** | L'accumulation temporelle étale la cible et crée des traînées |
| Désactiver le **culling par taille d'écran** : *Min Screen Size* des LOD, *Cull Distance Volumes*, *Bounds Scale* | Sinon la cible est supprimée avant d'être dessinée |
| Vérifier le **LOD** et **Nanite** à grande distance | La silhouette simplifiée change la surface projetée |
| **Large World Coordinates** (par défaut en UE5) | Précision suffisante pour des dizaines de km |
| Matériau de post-process : *Blendable Location* **avant tonemapping** | Travailler en luminance linéaire |

## 5. Plan de validation

| Test | Attendu |
|---|---|
| **Balayage sous-pixel** : déplacer la cible par pas de 0,1 pixel | Somme des pixels (moins le fond) constante à ±5 % (critère D2) |
| **Image fixe, plusieurs images** | Aucune variation d'une image à l'autre (pas de scintillement) |
| **Loi en 1/R²** | Distance doublée → signal divisé par 4 (à transmission constante) |
| **Continuité hybride** | Pas de saut d'énergie au passage du seuil de 1 à 3 pixels |
| **Comparaison à la référence** | Approches A, B, C, E comparées au rendu F sur quelques cas |
| **ΔL_eq = 1 arbitraire** | Somme mesurée = 1 : valide le module indépendamment de la physique |

## 6. Prochaines étapes proposées

1. Prototype **B** dans un niveau de test : fond uniforme, une cible, ΔL_eq = 1, balayage
   sous-pixel automatique, export CSV de la somme des pixels.
2. Prototype **A** (sur-échantillonnage ×8) sur le même scénario, pour comparaison.
3. Choisir les seuils de l'**hybride C** à partir des deux prototypes.
4. Évaluer **E** si la forme de la cible compte à moyenne distance.
5. Brancher ensuite (hors périmètre de cette note) la signature de la cible, le fond
   atmosphérique (voir [`calculs/luminance_mwir`](../../calculs/luminance_mwir)) et le bruit du
   capteur.
