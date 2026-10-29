# 08 — Automatiser avec les API

## Objectif

Comprendre le principe d'une API de LLM et écrire un premier script Python minimal, sécurisé (clé hors du code) et maîtrisé en coûts.

## 1. Principe

Une API de LLM est un service web : votre programme envoie une **requête HTTP** (généralement `POST`, en JSON) contenant :

- l'**identifiant du modèle** ;
- les **messages** (instructions système, message utilisateur, éventuellement historique) ;
- des **paramètres** : longueur maximale de réponse, température (part d'aléatoire), etc. ;
- une **clé d'API** dans un en-tête, qui vous identifie et sert à la facturation.

Le service renvoie une réponse JSON contenant le texte généré et, souvent, le nombre de tokens consommés.

Chaque fournisseur a son propre format d'URL, d'en-têtes et de JSON, et propose généralement un SDK officiel. Beaucoup de services et d'outils locaux proposent aussi un format compatible avec un format répandu de « chat completions ». **Référez-vous à la documentation de votre fournisseur** : l'exemple ci-dessous est volontairement générique.

Cas d'usage typiques : classer des tickets, résumer des documents en lot, extraire des champs de mails, générer des brouillons de rapports, enrichir un outil interne.

## 2. La clé d'API : règles

- **Jamais en dur** dans le code, jamais dans un dépôt Git, jamais dans un chat.
- Lue depuis une **variable d'environnement** ou un gestionnaire de secrets.
- Un fichier `.env` local est acceptable s'il est dans `.gitignore`.
- Une clé par projet ou environnement, avec des droits et limites de dépenses si le fournisseur le permet.
- En cas de fuite : révocation immédiate et régénération.

Définir la variable :

```bash
# Linux / macOS
export LLM_API_KEY="..."
```

```powershell
# Windows PowerShell (session courante)
$env:LLM_API_KEY = "..."
```

## 3. Exemple Python minimal générique

Prérequis : `pip install requests`.

```python
"""Appel minimal à une API de LLM au format "chat" (exemple générique).

Adaptez URL, en-têtes et structure JSON à la documentation de votre fournisseur.
Variables d'environnement attendues :
  LLM_API_KEY   : clé d'API (obligatoire, jamais dans le code)
  LLM_API_URL   : URL de l'endpoint
  LLM_MODEL     : identifiant du modèle
"""
import os
import sys

import requests


def get_config() -> tuple[str, str, str]:
    api_key = os.environ.get("LLM_API_KEY")
    api_url = os.environ.get("LLM_API_URL")
    model = os.environ.get("LLM_MODEL")
    if not api_key or not api_url or not model:
        sys.exit("Définissez LLM_API_KEY, LLM_API_URL et LLM_MODEL.")
    return api_key, api_url, model


def ask(prompt: str, system: str = "Tu es un assistant concis. Réponds en français.") -> str:
    api_key, api_url, model = get_config()

    headers = {
        # Le nom de l'en-tête dépend du fournisseur (Authorization, x-api-key...)
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "max_tokens": 500,          # plafonne la longueur, donc le coût
        "temperature": 0.2,         # faible = réponses plus stables
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    }

    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    if response.status_code == 429:
        raise RuntimeError("Quota ou limite de débit atteint : réessayez plus tard.")
    response.raise_for_status()

    data = response.json()
    # Le chemin vers le texte dépend du format de réponse du fournisseur.
    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    texte = "Le lot 3 a deux semaines de retard à cause d'une non-conformité fournisseur."
    print(ask(f"Reformule en une phrase pour un comité de pilotage :\n{texte}"))
```

Points à noter :

- la clé ne figure nulle part dans le code ;
- un `timeout` évite qu'un script reste bloqué ;
- le code HTTP 429 (trop de requêtes) est traité explicitement ;
- `max_tokens` borne le coût de chaque appel ;
- ne journalisez jamais les en-têtes (ils contiennent la clé).

## 4. Aller plus loin (proprement)

- **Réessais** avec attente croissante (*exponential backoff*) sur les erreurs temporaires (429, 5xx).
- **Sorties structurées** : demander du JSON et le valider (schéma) avant usage ; prévoir le cas où la sortie est invalide.
- **Traitement par lot** : limiter la concurrence, enregistrer l'avancement pour reprendre après une erreur.
- **Journalisation** : prompts, versions de modèle, tokens consommés, sans données sensibles.
- **Évaluation** : constituer un petit jeu d'exemples avec résultats attendus pour vérifier la qualité quand vous changez de prompt ou de modèle.
- **SDK officiel** : souvent plus simple et plus robuste que les requêtes brutes, une fois le principe compris.

## 5. Coûts et quotas (principes généraux)

- La facturation dépend en général du **nombre de tokens en entrée et en sortie**, et varie selon le modèle : les modèles les plus puissants coûtent plus cher.
- Les fournisseurs appliquent des **limites de débit** (requêtes ou tokens par minute) et parfois des plafonds de dépense.
- Les tarifs et limites changent souvent : consultez la page de tarification du fournisseur au moment de votre projet.

Bonnes pratiques :

- estimer le coût sur un petit échantillon avant de lancer un gros lot ;
- choisir le modèle le plus simple qui donne une qualité suffisante ;
- raccourcir les prompts et le contexte envoyé ;
- éviter de renvoyer un long historique inutile à chaque appel ;
- mettre en cache les résultats de requêtes identiques ;
- définir des alertes ou plafonds de dépense si disponibles.

## Pièges

- Clé d'API commitée dans Git (même supprimée ensuite, elle reste dans l'historique : révoquez-la).
- Boucle mal écrite qui envoie des milliers de requêtes et fait exploser la facture.
- Faire confiance aveuglément à une sortie JSON sans validation.
- Envoyer des données personnelles ou confidentielles via une API non validée par l'organisation.
- Exécuter directement du code ou des commandes générés par le modèle sans contrôle.
- Supposer que le comportement d'un modèle restera identique après une mise à jour du fournisseur.

## Checklist

- [ ] La clé d'API est lue depuis l'environnement ou un gestionnaire de secrets.
- [ ] `.env` et fichiers de secrets sont dans `.gitignore`.
- [ ] Timeout, gestion des erreurs et des quotas en place.
- [ ] `max_tokens` et un plafond de dépense définis.
- [ ] Coût estimé sur un échantillon avant passage à l'échelle.
- [ ] Sorties validées avant usage.
- [ ] Données envoyées conformes à la politique de l'organisation.
- [ ] Un jeu d'exemples permet de vérifier la qualité dans le temps.
