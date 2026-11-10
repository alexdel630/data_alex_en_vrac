---
name: gestion-de-configuration-gitlab-dvc
description: Mettre en place ou appliquer la gestion de configuration d'un projet avec GitLab, Git et DVC (Data Version Control) - identification des articles, versionnement du code et des données/modèles/gros fichiers, maîtrise des modifications par merge request, baselines par tags, CI GitLab, audit et reproductibilité. À utiliser quand l'utilisateur parle de gestion de configuration, de versionner des données ou de gros fichiers, de DVC, de baseline, de release ou de traçabilité sur GitLab.
---

# Gestion de configuration avec GitLab, Git et DVC

**Principe** : Git versionne le code, la configuration et de petits fichiers « pointeurs » ;
DVC stocke les gros fichiers (données, modèles, assets binaires) dans un stockage distant et
garde dans Git leur empreinte (hash). Un commit Git identifie donc **exactement** une version du
code **et** des données.

Avant d'agir, lis l'existant : `README`, `.gitlab-ci.yml`, `.dvc/config`, `dvc.yaml`, fichiers
`*.dvc`, `.gitignore`, branches et tags (`git branch -a`, `git tag`). Respecte les conventions en
place. **Ne lance jamais** d'opération destructive (`dvc gc`, `git push --force`, suppression de
tag ou de branche protégée) sans accord explicite.

## 1. Les 4 activités et leur traduction outillée

| Activité (ISO 10007) | Outil | Mise en œuvre |
|---|---|---|
| **Identification** des articles de configuration | Git + DVC | Arborescence claire, conventions de nommage, chaque artefact versionné (code dans Git, gros fichiers via `.dvc`). |
| **Maîtrise des modifications** | GitLab | Issue « demande de modification » → branche → merge request → revue et approbation → merge. Branches protégées. |
| **Enregistrement de l'état** | Git tags, GitLab Releases, `CHANGELOG.md` | Chaque baseline = un tag annoté + une release qui liste le contenu et les changements. |
| **Audit de configuration** | CI GitLab + DVC | Depuis un tag : `git checkout` + `dvc pull` + `dvc repro` doivent reproduire l'état livré. |

## 2. Mise en place (une fois par dépôt)

```bash
pip install "dvc[s3]"          # ou dvc[ssh], dvc[azure], dvc[gs] selon le stockage
dvc init
git add .dvc .dvcignore
git commit -m "Initialiser DVC"

# Stockage distant (exemple S3 ou MinIO interne)
dvc remote add -d stockage s3://mon-bucket/mon-projet
dvc remote modify stockage endpointurl https://minio.exemple.interne   # si S3 compatible
git add .dvc/config
git commit -m "Configurer le stockage DVC"
```

**Identifiants du stockage : jamais dans Git.**
- En local : `dvc remote modify --local stockage access_key_id …` (écrit dans
  `.dvc/config.local`, ignoré par Git) ou variables d'environnement (`AWS_ACCESS_KEY_ID`,
  `AWS_SECRET_ACCESS_KEY`).
- En CI : variables GitLab **masquées** et **protégées** (Settings → CI/CD → Variables).

## 3. Versionner des données, des modèles ou des gros fichiers

```bash
dvc add donnees/brutes              # crée donnees/brutes.dvc et l'ajoute au .gitignore
git add donnees/brutes.dvc donnees/.gitignore
git commit -m "Ajouter le jeu de données brut v1"
dvc push                            # envoie les fichiers vers le stockage
git push
```

Règle d'or : **`dvc push` avant (ou avec) `git push`**. Sinon le commit pointe vers des
données que personne d'autre ne peut récupérer.

Récupérer : `git pull` puis `dvc pull`. Revenir à une version : `git checkout <tag>` puis
`dvc checkout` (ou `dvc pull` si les fichiers ne sont pas en cache local).

## 4. Pipelines reproductibles

```bash
dvc stage add -n preparer \
  -d scripts/preparer.py -d donnees/brutes \
  -o donnees/preparees \
  python scripts/preparer.py

dvc stage add -n entrainer \
  -d scripts/entrainer.py -d donnees/preparees -p params.yaml:entrainement \
  -o modeles/modele.pkl -M metriques.json \
  python scripts/entrainer.py

dvc repro                           # ne relance que les étapes dont une dépendance a changé
git add dvc.yaml dvc.lock params.yaml metriques.json
git commit -m "Pipeline préparation + entraînement"
dvc push
```

- `dvc.yaml` décrit le pipeline ; `dvc.lock` fige les empreintes exactes : **les deux vont dans Git**.
- Comparer à la branche principale : `dvc params diff main`, `dvc metrics diff main`.

## 5. Organisation GitLab

- **Branches** : `main` protégée (pas de push direct), branches courtes `feature/…`, `fix/…`,
  éventuellement `release/x.y` pour la maintenance.
- **Merge requests** : modèle de description (objet, issue liée, impact données, tests),
  approbation obligatoire, pipeline vert obligatoire, `CODEOWNERS` pour les dossiers sensibles
  (`dvc.yaml`, `params.yaml`, `.gitlab-ci.yml`).
- **Issues** : modèle « Demande de modification » (description, justification, impact, articles
  concernés, décision). Labels : `type::évolution`, `type::anomalie`, `statut::…`.
- **Baselines** : tags annotés protégés, nommés selon SemVer (`v1.2.0`) ou par jalon
  (`BL-CDR-2026-11`). Une GitLab Release par tag, avec les notes de version.

```bash
git tag -a v1.2.0 -m "Baseline v1.2.0 : données v3, modèle entraîné, specs v1.4"
git push origin v1.2.0
```

## 6. CI GitLab

```yaml
# .gitlab-ci.yml
stages: [verifier, reproduire, livrer]

default:
  image: python:3.12
  before_script:
    - pip install --quiet "dvc[s3]"
    # AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY : variables CI/CD masquées et protégées

verifier-donnees:
  stage: verifier
  script:
    - dvc pull                     # échoue si un commit pointe vers des données non poussées
    - dvc status                   # affiche les écarts entre pipeline et espace de travail
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

reproduire:
  stage: reproduire
  script:
    - dvc pull
    - dvc repro
    - git diff --exit-code dvc.lock   # le pipeline committé doit être à jour
    - dvc metrics diff $CI_DEFAULT_BRANCH --md >> rapport.md || true
  artifacts:
    paths: [rapport.md]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

livrer:
  stage: livrer
  script:
    - dvc pull
    - echo "Baseline $CI_COMMIT_TAG vérifiée"
  rules:
    - if: $CI_COMMIT_TAG
```

Adapte : image, extras DVC selon le stockage, temps de calcul (`reproduire` peut être réservé
aux MR qui touchent `dvc.yaml`, `params.yaml` ou `scripts/` avec `rules: changes:`).

## 7. Audit d'une baseline

```bash
git clone <dépôt> audit && cd audit
git checkout v1.2.0
dvc pull
dvc status                          # doit être propre
dvc repro --dry                     # aucune étape ne doit être à relancer
```

Rapport d'audit : tag, commit, liste des articles (`git ls-files` + fichiers `.dvc`),
empreintes (`dvc.lock`), résultat des vérifications, écarts.

## 8. Cas des gros fichiers binaires (Unreal, CAO…)

- DVC convient aux données, modèles et assets **générés ou rarement modifiés**.
- Les fichiers binaires **édités par plusieurs personnes** (`.uasset`, `.umap`, maquettes CAO) ne
  se fusionnent pas : il faut du **verrouillage**. DVC n'en propose pas ; préfère Git LFS avec le
  verrouillage de fichiers GitLab (ou Perforce pour les grosses équipes Unreal).

## 9. Pièges

| Piège | Conséquence | Parade |
|---|---|---|
| Oublier `dvc push` | Les autres ne peuvent pas récupérer les données. | Job CI `dvc pull` sur chaque MR. |
| Committer `.dvc/config.local` ou des clés | Fuite d'identifiants. | `.gitignore`, variables CI masquées, révocation immédiate en cas de fuite. |
| Modifier `dvc.lock` à la main | Empreintes incohérentes. | Toujours passer par `dvc repro` ou `dvc commit`. |
| `dvc gc` mal paramétré | Suppression de versions encore référencées. | Ne jamais le lancer sans `--all-commits`/`--all-tags` réfléchis et accord explicite. |
| Tags non protégés | Une baseline peut être déplacée. | Protected tags dans GitLab. |
| Données ajoutées directement dans Git | Dépôt énorme, lent. | Seuil de taille et revue en MR ; `dvc add` au-delà de quelques Mo. |

## Livrable attendu

Selon la demande : commandes exécutées avec leur résultat, fichiers créés ou modifiés
(`.gitlab-ci.yml`, `dvc.yaml`, modèles d'issue/MR, `CHANGELOG.md`), et une liste de ce qui reste
à faire côté GitLab dans l'interface (branches et tags protégés, variables CI, approbations),
que l'utilisateur doit régler lui-même s'il n'y a pas d'accès API.
