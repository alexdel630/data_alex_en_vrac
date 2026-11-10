---
name: compte-rendu-reunion
description: Transformer des notes brutes ou une transcription de réunion en compte rendu structuré avec décisions et tableau d'actions. À utiliser quand l'utilisateur fournit des notes de réunion ou demande un CR, un compte rendu ou un récapitulatif de réunion.
---

# Compte rendu de réunion

1. Identifie : objet, date, participants (et absents si mentionnés), ordre du jour.
2. Pour chaque sujet : contexte en 1 à 2 phrases, points clés, **décision** s'il y en a une.
3. Extrais **toutes** les actions : qui, quoi, pour quand. Si le responsable ou l'échéance
   manque, écris « à définir » ; n'invente jamais.
4. Signale séparément les désaccords non tranchés et les questions ouvertes.
5. Reste factuel : pas d'interprétation, pas de jugement, pas de citation nominative de propos
   sensibles.

## Format

```markdown
# Compte rendu — <objet> — <date>
**Participants** : … | **Absents** : …

## Décisions
- …

## Points abordés
### <sujet>
…

## Actions
| # | Action | Responsable | Échéance |
|---|---|---|---|

## Points ouverts
- …

**Prochaine réunion** : …
```

Termine en listant ce qui était ambigu dans les notes et mérite une vérification.
