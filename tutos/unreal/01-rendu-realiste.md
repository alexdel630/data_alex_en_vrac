# Rendu réaliste dans Unreal Engine 5

> **Objectif** : produire des images fixes ou des séquences photoréalistes avec Unreal Engine 5,
> de la configuration du projet jusqu'à l'export final.
>
> **Prérequis** : savoir naviguer dans l'éditeur, placer des acteurs, éditer un matériau simple.
>
> **Version** : écrit pour **UE 5.8** (juin 2026), valable dans l'ensemble depuis 5.4.
> Nouveautés de 5.8 utiles ici : **MegaLights** devient prêt pour la production, et un mode
> **Lumen Lite** apparaît (voir [section 4](#4-éclairage)). Si un réglage n'est pas au même
> endroit, cherche-le par son nom dans la barre de recherche des Project Settings ou du
> panneau Details.

---

## Sommaire

1. [La démarche : photographier plutôt que « rendre »](#1-la-démarche--photographier-plutôt-que--rendre-)
2. [Configurer le projet](#2-configurer-le-projet)
3. [Exposition : la base de tout](#3-exposition--la-base-de-tout)
4. [Éclairage](#4-éclairage)
5. [Matériaux PBR](#5-matériaux-pbr)
6. [Géométrie et détails](#6-géométrie-et-détails)
7. [Caméra](#7-caméra)
8. [Post-process](#8-post-process)
9. [Lumen ou Path Tracer ?](#9-lumen-ou-path-tracer-)
10. [Exporter avec Movie Render Queue](#10-exporter-avec-movie-render-queue)
11. [Pièges courants](#11-pièges-courants)
12. [Checklist finale](#12-checklist-finale)

---

## 1. La démarche : photographier plutôt que « rendre »

Une image paraît réaliste quand elle respecte ce qu'un **vrai appareil photo** verrait d'une
**vraie scène**. Trois règles guident tout le reste :

| Règle | En pratique |
|---|---|
| **Valeurs physiques** | Intensités de lumière en lux et en candelas, exposition en EV, matériaux aux albédos plausibles. |
| **Imperfection** | Rien n'est parfaitement propre, droit ou uniforme : rugosité variable, poussière, bords arrondis. |
| **Références** | Travaille à côté d'une photo de référence. Compare souvent, à la même exposition. |

L'ordre de travail recommandé :

```mermaid
flowchart LR
    A[Projet configuré] --> B[Exposition manuelle]
    B --> C[Éclairage]
    C --> D[Matériaux]
    D --> E[Caméra et cadrage]
    E --> F[Post-process léger]
    F --> G[Export MRQ]
```

On règle l'exposition **avant** l'éclairage : sinon l'exposition automatique compense
silencieusement chaque modification et on ne sait plus ce qu'on fait.

---

## 2. Configurer le projet

### Project Settings → Rendering

| Réglage | Valeur conseillée | Pourquoi |
|---|---|---|
| Dynamic Global Illumination Method | **Lumen** | Éclairage indirect temps réel. |
| Reflection Method | **Lumen** | Reflets cohérents avec l'éclairage. |
| Support Hardware Ray Tracing | **Activé** (si GPU RTX / RX 6000 ou plus) | Reflets et GI Lumen plus précis. |
| Use Hardware Ray Tracing when available | **Activé** | Fait passer Lumen en mode matériel. |
| Generate Mesh Distance Fields | **Activé** | Requis par Lumen en mode logiciel. |
| Extend default luminance range in Auto Exposure settings | **Activé** | Exposition exprimée en EV100 physiques. |
| Virtual Shadow Maps (Shadow Map Method) | **Virtual Shadow Maps** | Ombres nettes et détaillées. |
| Anti-Aliasing Method | **TSR** | Meilleure qualité temporelle en éditeur. |

Redémarre l'éditeur après ces changements (le ray tracing l'exige).

### Plugins utiles

- **Movie Render Queue** : export haute qualité (indispensable).
- **Sun Position Calculator** : place le soleil selon une date, une heure et un lieu.
- **HDRI Backdrop** : éclairage et fond à partir d'une image HDR.

### Unités

Unreal travaille en **centimètres**. Vérifie l'échelle de tes modèles importés : une porte doit
mesurer environ 200 uu. Une mauvaise échelle fausse la profondeur de champ, le flou de
mouvement et l'éclairage.

---

## 3. Exposition : la base de tout

L'exposition automatique est pratique pour jouer, mais nuisible pour une image maîtrisée.

**Dans un Post Process Volume** (cocher *Infinite Extent (Unbound)* pour qu'il couvre tout) :

| Paramètre | Valeur |
|---|---|
| Exposure → Metering Mode | **Manual** |
| Exposure → Exposure Compensation | ajuste ici |
| Apply Physical Camera Exposure | **Activé** si tu règles ouverture, vitesse et ISO sur la caméra |

### Repères d'exposition (EV100)

| Scène | EV100 approximatif |
|---|---|
| Plein soleil, ciel dégagé | 14 à 16 |
| Ciel couvert | 12 à 13 |
| Ombre extérieure lumineuse | 11 à 12 |
| Intérieur lumineux près d'une fenêtre | 7 à 9 |
| Bureau éclairé artificiellement | 6 à 8 |
| Intérieur tamisé, soirée | 4 à 6 |
| Rue éclairée de nuit | 2 à 4 |

> **Astuce** : `Show → Visualize → HDR (Eye Adaptation)` et le mode `Lit → Exposure`
> aident à lire les valeurs. Le *Pixel Inspector* (Window → Pixel Inspector) donne la luminance
> d'un pixel.

---

## 4. Éclairage

### Extérieur jour : le système ciel physique

Ajoute (ou utilise le panneau **Env. Light Mixer**, Window → Env. Light Mixer, qui crée tout d'un clic) :

| Acteur | Rôle | Réglage clé |
|---|---|---|
| **Directional Light** | Soleil | Intensité ≈ **75 000 à 120 000 lux** en plein jour ; *Atmosphere Sun Light* coché. |
| **Sky Atmosphere** | Couleur du ciel et diffusion | Laisser par défaut au début. |
| **Sky Light** | Lumière ambiante du ciel | *Real Time Capture* **activé**, Source Type = *SLS Captured Scene*. |
| **Exponential Height Fog** | Perspective atmosphérique | Densité faible ; *Volumetric Fog* pour les rayons de lumière. |
| **Volumetric Cloud** | Nuages | Optionnel ; coûteux mais très crédible. |

La température de couleur du soleil se gère via la Sky Atmosphere (l'angle du soleil colore
naturellement la lumière). Évite de teinter la Directional Light à la main en plus.

### Extérieur avec HDRI

Alternative rapide : **HDRI Backdrop** avec une image HDR (`.hdr` / `.exr`) d'au moins 8K.
Ajoute un soleil (Directional Light) aligné sur celui de la HDRI pour obtenir des ombres nettes,
car une HDRI seule donne des ombres trop douces.

### Intérieur

L'intérieur est le cas le plus difficile : la lumière entre par les ouvertures et rebondit.

- **Lumière naturelle** : soleil + Sky Light comme en extérieur. Ajoute éventuellement des
  **Rect Lights** devant les fenêtres (*portals* légers) pour renforcer la lumière qui entre.
- **Éclairage artificiel** : Point, Spot et Rect Lights en **unités physiques**.

| Source | Valeur indicative |
|---|---|
| Ampoule LED domestique | 800 lm (≈ ampoule 60 W) |
| Spot encastré | 400 à 700 lm |
| Néon / dalle de bureau | 3 000 à 4 000 lm |

Règle l'unité d'intensité de chaque lumière sur **Lumens** ou **Candelas**, jamais en
« Unitless ». Ajoute un **profil IES** (fichiers photométriques fournis par les fabricants)
pour la répartition réaliste des spots.

Températures de couleur (cocher *Use Temperature*) :

| Source | Kelvin |
|---|---|
| Bougie | 1 900 K |
| Ampoule chaude | 2 700 K |
| Blanc neutre | 4 000 K |
| Lumière du jour | 5 500 à 6 500 K |

### Réglages Lumen pour la qualité

Dans le Post Process Volume, section **Global Illumination** et **Reflections** :

| Paramètre | Aperçu | Rendu final |
|---|---|---|
| Lumen Scene Lighting Quality | 1 | 2 à 4 |
| Lumen Scene Detail | 1 | 2 à 4 |
| Final Gather Quality | 1 | 2 à 4 |
| Lumen Reflections Quality | 1 | 2 à 4 |
| Ray Lighting Mode (Reflections) | — | *Hit Lighting for Reflections* (ray tracing matériel) |
| Max Trace Distance | défaut | augmenter pour les grands espaces |

> Les murs fins (moins de 10 cm) laissent passer la lumière avec Lumen. Donne une épaisseur
> réelle aux murs, sols et plafonds.

### Lumen Lite (UE 5.8) : pas pour le rendu final

UE 5.8 ajoute **Lumen Lite**, un mode de qualité moyenne nettement plus rapide (champs
d'irradiance par sondes). Il vise le jeu à 60 images/s. Pour une image réaliste, reste sur
Lumen **haute qualité** avec ray tracing matériel ; Lumen Lite peut servir à naviguer plus
fluidement dans une scène lourde pendant la mise en place.

### MegaLights (UE 5.8) : beaucoup de lumières ombrées

**MegaLights** est prêt pour la production en 5.8, avec moins de bruit qu'en version
expérimentale. Il permet d'avoir des **centaines de lumières qui projettent des ombres**
(éclairage de bureaux, de rues, de vitrines, guirlandes) pour un coût quasi constant. C'est un
gros gain de réalisme pour les intérieurs et les scènes de nuit, où chaque source devrait
normalement avoir son ombre.

- Active-le dans les Project Settings (cherche « MegaLights »), puis dans le Post Process Volume.
- Chaque lumière peut choisir d'utiliser MegaLights ou non (option dans ses Details).
- Outils de diagnostic en 5.8 : un *Light Finder* pour repérer les lumières de la scène et un
  visualiseur de rayons pour comprendre le bruit.
- Si le projet n'utilise pas MegaLights, `r.MegaLights.Supported 0` évite la compilation de ses
  shaders.

> Vérifie le rendu final avec et sans MegaLights sur une image de test : le bruit résiduel
> dépend de la scène, et MRQ (échantillons temporels) aide à le lisser.

---

## 5. Matériaux PBR

Le rendu physique repose sur quelques entrées. Chacune a des **plages réalistes** :

| Entrée | Rôle | Valeurs plausibles |
|---|---|---|
| **Base Color** | Couleur sans éclairage (albédo) | Jamais noir pur ni blanc pur : environ **0,03 à 0,85** en linéaire. Neige ≈ 0,8, charbon ≈ 0,04. |
| **Metallic** | Métal ou non | **0 ou 1**. Les valeurs intermédiaires servent uniquement aux transitions (rouille, saleté sur métal). |
| **Roughness** | Rugosité de la surface | **C'est l'entrée qui fait le réalisme.** Jamais une valeur constante sur une grande surface. |
| **Specular** | Réflectance des non-métaux | Laisser à **0,5** dans la plupart des cas. |
| **Normal** | Détail de relief | Texture normale en espace tangent. |
| **Ambient Occlusion** | Occultation fine | Optionnel avec Lumen. |

### Textures

- Base Color en **sRGB** ; Roughness, Metallic, AO, Normal en **linéaire** (décocher *sRGB* dans
  la texture, ou utiliser la compression *Masks* pour une texture ORM).
- Les bibliothèques de matériaux scannés (Fab / Quixel Megascans, Poly Haven, ambientCG…)
  donnent des valeurs calibrées : un bon point de départ.

### Ce qui trahit un rendu 3D

| Défaut | Correction |
|---|---|
| Rugosité uniforme | Ajouter une texture de variation (taches, traces de doigts, usure). |
| Arêtes vives parfaites | Chanfreiner la géométrie, ou utiliser des normales arrondies. |
| Répétition visible des tuiles | *Macro variation*, rotation aléatoire, mélange de deux échelles de texture. |
| Couleurs trop saturées | Désaturer la Base Color. Les matériaux réels sont plus ternes qu'on ne le croit. |
| Surfaces trop propres | Decals de saleté, d'humidité ou de poussière dans les coins. |

### Matériaux spéciaux

- **Verre** : Blend Mode *Translucent*, Lighting Mode *Surface TranslucencyVolume* ou
  *Surface ForwardShading* ; activer les reflets ray tracés sur la translucidité dans le
  Post Process Volume. Avec le Path Tracer, le verre se comporte physiquement (réfraction).
- **Peau, cire, feuilles** : Shading Model *Subsurface Profile* ou *Two Sided Foliage*.
- **Peinture voiture** : Shading Model *Clear Coat*.
- **Substrate** : le système de matériaux en couches d'UE5 (verre teinté, vernis, tissus
  superposés, peinture multicouche). Il s'active dans les Project Settings et change l'éditeur
  de matériaux : décide-le en début de projet. En 5.8, Substrate gère aussi l'éclairage des
  cheveux (hair strands) et utilise un modèle de « sheen » plus précis pour les tissus.

---

## 6. Géométrie et détails

- **Nanite** : active-le sur les meshes statiques détaillés (scans, architecture). Il permet des
  millions de polygones sans perte de performance notable et améliore la précision de Lumen.
- **Végétation** : Nanite supporte la végétation dans UE5 récent. Un léger vent
  (*SimpleGrassWind*) ajoute de la vie aux séquences.
- **Densité** : une scène réaliste est **encombrée**. Câbles, petits objets, plinthes,
  interrupteurs, joints… Le vide trahit la 3D.
- **Échelle** : encore une fois, vérifie que les objets ont une taille réelle.

---

## 7. Caméra

Utilise un **Cine Camera Actor** plutôt que la caméra de l'éditeur.

| Réglage | Recommandation |
|---|---|
| Filmback | *Full Frame 35 mm* (comme un appareil photo réel). |
| Focale | 24–35 mm pour l'architecture, 50 mm « œil humain », 85–135 mm pour un portrait ou un produit. |
| Ouverture (Aperture) | f/1.8–2.8 pour un flou d'arrière-plan marqué, f/8–11 pour tout net. |
| Focus Method | *Manual* avec la pipette (*Focus Distance*) ou *Tracking* sur un acteur. |
| Hauteur | 1,50 à 1,70 m pour une vue « humaine ». |

**Architecture** : garde les verticales verticales. Caméra parfaitement à l'horizontale, ou
correction de perspective (décalage de l'objectif, réglable dans la Cine Camera via *Filmback*
/ *Lens Settings* selon la version). Une caméra inclinée fait « tomber » les murs.

**Composition** : règle des tiers, premier plan pour la profondeur, lignes directrices.
Active *Show → Grid* ou l'overlay de composition du viewport.

---

## 8. Post-process

Le post-process **finit** une image, il ne la sauve pas. Reste léger.

| Effet | Réglage conseillé |
|---|---|
| **Bloom** | Méthode *Standard*, intensité faible (≈ 0,1 à 0,3). *Convolution* pour un rendu plus physique, plus coûteux. |
| **Vignette** | 0,2 à 0,4. |
| **Chromatic Aberration** | 0 à 0,2. Au-delà, l'effet devient gadget. |
| **Film Grain** | Très léger : il casse l'aspect « trop propre ». |
| **Lens Flares** | Désactiver, sauf effet voulu. |
| **Motion Blur** | Désactivé pour une image fixe ; pour une séquence, angle d'obturateur ≈ 180°. |
| **Tonemapper / Film** | Garder le tonemapper par défaut (type ACES), ne pas pousser les sliders. |
| **Color Grading** | Petites corrections de balance des blancs et de contraste. Pour un grading poussé, exporter en EXR et étalonner dans un logiciel dédié. |

> **Balance des blancs** : `Color Grading → White Balance → Temp`. Règle-la pour que les
> blancs de la scène paraissent neutres, comme le ferait un appareil photo.

---

## 9. Lumen ou Path Tracer ?

| Critère | **Lumen** | **Path Tracer** |
|---|---|---|
| Type | Temps réel | Rendu hors ligne, progressif |
| Vitesse | Instantané à quelques secondes par image | Plusieurs secondes à minutes par image |
| Réalisme | Très bon | Référence physique (caustiques, verre, réflexions multiples) |
| Matériel | GPU récent | GPU avec ray tracing matériel |
| Usage typique | Séquences, itération, temps réel | Images fixes de haute qualité, visuels marketing |

**Activer le Path Tracer** : Project Settings → *Support Hardware Ray Tracing* et
*Path Tracing* activés, puis dans le viewport `Lit → Path Tracing`.

Réglages utiles (Post Process Volume → Path Tracing) :

| Paramètre | Valeur de départ |
|---|---|
| Max Bounces | 8 à 32 |
| Samples Per Pixel | 512 à 4 096 pour le rendu final |
| Reference Denoiser | Activé pour réduire le bruit |
| Filter Width | défaut |

Le Path Tracer ignore certains réglages propres à Lumen et ne supporte pas tous les effets
temps réel. Compare toujours une image Path Tracer avec ton rendu Lumen : c'est aussi le
meilleur moyen de **calibrer** Lumen.

---

## 10. Exporter avec Movie Render Queue

N'exporte jamais une image finale par capture d'écran du viewport. Utilise **Movie Render
Queue** (MRQ), ou **Movie Render Graph** dans les versions récentes.

### Étapes

1. Crée un **Level Sequence** contenant ta Cine Camera (même pour une image fixe : une
   séquence d'une image).
2. `Window → Cinematics → Movie Render Queue` → *+ Render* → choisis la séquence.
3. Clique sur la configuration (*Unsaved Config*) et règle :

| Section | Réglage |
|---|---|
| **Output** | Résolution (3 840 × 2 160 ou plus), nom de fichier, dossier. |
| **Anti-aliasing** | *Override Anti-Aliasing* coché ; **Spatial Sample Count** 1 à 8 et **Temporal Sample Count** 8 à 32 (le produit = qualité et temps de rendu). Pour une image fixe, privilégier les échantillons spatiaux. |
| **Anti-aliasing** | *Engine Warm Up Count* : 32 à 64 images, pour que Lumen et les particules se stabilisent. |
| **Console Variables** | Voir le tableau ci-dessous. |
| **Format** | **EXR 16 bits** pour l'étalonnage, ou PNG/JPEG pour une livraison directe. |
| **Path Tracer** | Ajouter le *Path Tracer* comme passe de rendu au lieu de *Deferred Rendering* si tu l'utilises. |

### Console variables utiles pour le rendu final

| Variable | Valeur | Effet |
|---|---|---|
| `r.ScreenPercentage` | 100 à 200 | Sur-échantillonnage interne. |
| `r.Lumen.ScreenProbeGather.RadianceCache.ProbeResolution` | 32 | GI plus fine. |
| `r.Lumen.Reflections.DownsampleFactor` | 1 | Reflets en pleine résolution. |
| `r.Shadow.Virtual.ResolutionLodBiasDirectional` | -1 à -1,5 | Ombres du soleil plus nettes. |
| `r.MotionBlurQuality` | 4 | Flou de mouvement de qualité (séquences). |
| `r.DepthOfFieldQuality` | 4 | Profondeur de champ de qualité. |

> Les noms de console variables évoluent entre versions. Si une variable n'a aucun effet,
> vérifie-la avec `help <nom>` dans la console de l'éditeur (touche ²).

### Passes séparées (compositing)

MRQ peut exporter des passes supplémentaires (*Stencil Layers*, *Object ID*, profondeur…)
pour retoucher dans Nuke, After Effects, DaVinci Resolve ou Photoshop.

---

## 11. Pièges courants

| Symptôme | Cause probable | Correction |
|---|---|---|
| L'image change de luminosité en bougeant | Exposition automatique | Metering Mode *Manual*. |
| Fuites de lumière dans les coins | Murs trop fins pour Lumen | Murs d'au moins 10 cm, géométrie fermée. |
| Taches ou scintillement dans l'éclairage indirect | Qualité Lumen faible, warm-up trop court | Monter les *Quality*, plus d'*Engine Warm Up* dans MRQ. |
| Reflets flous ou faux | Lumen en mode logiciel | Ray tracing matériel + *Hit Lighting for Reflections*. |
| Ombres floues ou crénelées | Virtual Shadow Maps mal résolues | Console variable de bias LOD, Source Angle de la lumière réaliste. |
| Image « plastique » | Rugosité uniforme, matériaux trop saturés | Textures de variation, désaturer. |
| Profondeur de champ bizarre | Mauvaise échelle de la scène | Vérifier que la scène est en centimètres réels. |
| Bruit avec le Path Tracer | Trop peu d'échantillons | Plus de *Samples Per Pixel*, activer le denoiser. |
| Rendu MRQ différent du viewport | Réglages de scalabilité différents | Vérifier *Engine Scalability* = *Cinematic* et les console variables de la config MRQ. |

---

## 12. Checklist finale

- [ ] Échelle des objets vérifiée (centimètres réels).
- [ ] Exposition manuelle, valeur EV cohérente avec la scène.
- [ ] Lumières en unités physiques (lux, lumens, candelas), températures en Kelvin.
- [ ] Murs et sols épais, sans fuite de lumière.
- [ ] Matériaux : albédos plausibles, rugosité variée, metallic à 0 ou 1.
- [ ] Arêtes chanfreinées, saleté et usure là où il faut.
- [ ] Scène assez dense en détails.
- [ ] Cine Camera Actor : focale et ouverture choisies, verticales droites.
- [ ] Post-process léger : pas de bloom excessif ni d'aberration chromatique forte.
- [ ] Comparaison avec une photo de référence et/ou un rendu Path Tracer.
- [ ] Export MRQ : résolution finale, anti-aliasing et warm-up suffisants, EXR si étalonnage.

---

## Pour aller plus loin

- La documentation officielle d'Unreal Engine : pages *Lumen Technical Details*,
  *Path Tracer*, *Movie Render Queue*, *Physical Lighting Units*.
- Les projets d'exemple gratuits d'Epic (scènes d'architecture et de démonstration), à ouvrir
  pour étudier leurs réglages.
- La photographie elle-même : comprendre le triangle ouverture / vitesse / ISO et la lecture
  de la lumière améliore davantage un rendu que n'importe quel réglage.
