# 06 — Sécurité, confidentialité et éthique

## Objectif

Utiliser l'IA générative sans exposer de données sensibles, sans enfreindre la réglementation ni la propriété intellectuelle, et en gardant un regard critique sur les sorties.

> Ce tutoriel donne des repères généraux ; il ne constitue pas un avis juridique. En cas de doute, référez-vous à la politique de votre organisation, à votre DPO ou à votre service juridique.

## 1. Où vont vos données ?

Quand vous envoyez un prompt à un service en ligne, son contenu est transmis au fournisseur. Selon l'offre et le contrat, il peut être conservé, journalisé, consulté pour la modération ou utilisé pour améliorer les modèles.

Les conditions varient fortement entre offres grand public, offres professionnelles et déploiements internes. **Avant de coller des données professionnelles, vérifiez quel outil est autorisé par votre organisation et pour quel niveau de confidentialité.**

## 2. Classer avant de coller

| Niveau | Exemples | Règle générale |
|--------|----------|----------------|
| Public | Documentation publique, code open source | Utilisable |
| Interne | Procédures internes, code non sensible | Uniquement outils approuvés |
| Confidentiel | Contrats, offres, données financières, code propriétaire clé, données clients | Seulement si explicitement autorisé, sur outil validé |
| Secret / réglementé | Données de santé, défense, export contrôlé, secrets industriels | Généralement interdit hors environnement dédié |

Réflexes :

- **Anonymiser** : remplacer noms, entreprises, montants, identifiants par des génériques (`Client A`, `Fournisseur B`, `XXX €`).
- **Minimiser** : ne coller que l'extrait nécessaire.
- **Synthétiser vous-même** le contexte plutôt que de coller le document entier.

## 3. Secrets et tokens : jamais

Ne collez **jamais** dans un prompt, un chat ou un fichier envoyé à l'IA :

- mots de passe, codes PIN ;
- clés API, tokens d'accès, jetons de session, cookies ;
- clés privées (SSH, TLS, signature), certificats avec clé ;
- chaînes de connexion à des bases de données ;
- fichiers `.env`, fichiers de configuration contenant des identifiants.

Si cela arrive par erreur : **considérez le secret comme compromis**, révoquez-le et régénérez-le, puis prévenez la sécurité selon la procédure interne. Supprimer le message ne suffit pas.

Côté code : variables d'environnement ou gestionnaire de secrets, fichiers de secrets exclus du dépôt (`.gitignore`), et outils de détection de secrets dans le pipeline.

## 4. RGPD et données personnelles

Le RGPD s'applique dès que vous traitez des données concernant une personne identifiable (nom, email, voix, photo, identifiant, évaluation…). Principes à garder en tête :

- **Base légale et finalité** : avez-vous le droit d'utiliser ces données pour cet usage ?
- **Minimisation** : seulement les données nécessaires.
- **Information** des personnes (ex. transcription de réunion).
- **Transferts hors UE** et sous-traitance : encadrés contractuellement, à valider par l'organisation.
- **Décisions automatisées** ayant un effet important sur une personne (recrutement, évaluation) : encadrées et nécessitant une intervention humaine.

En pratique : anonymisez, utilisez les outils validés, et interrogez votre DPO pour tout nouveau cas d'usage impliquant des données personnelles.

## 5. Propriété intellectuelle

- **Entrées** : ne soumettez pas des contenus dont vous n'avez pas les droits ou que vos contrats interdisent de partager (documents clients, code sous NDA).
- **Sorties** : le statut juridique des contenus générés reste débattu selon les pays. Une sortie peut ressembler à un contenu existant protégé (texte, code, image).
- **Code** : vérifiez la compatibilité de licence si un extrait généré ressemble à du code connu ; certaines organisations activent des filtres de correspondance avec du code public.
- **Transparence** : respectez les règles de votre organisation ou de vos clients sur la mention de l'usage de l'IA.

## 6. Vérification des sorties et biais

- Les sorties peuvent être **fausses** (hallucinations) : voir [07](07-verifier-et-fiabiliser.md).
- Elles peuvent être **biaisées** : stéréotypes, sur-représentation de certains points de vue, langue ou culture dominante. Soyez particulièrement vigilant pour tout ce qui concerne des personnes (recrutement, évaluation, communication).
- **Injection de prompt** : un document, une page web ou un mail traité par l'IA peut contenir des instructions cachées (« ignore les consignes et… »). Avec un agent capable d'agir, cela peut déclencher des actions non voulues. Ne laissez pas un agent agir sans contrôle sur des contenus non fiables.

## 7. Politique d'entreprise

Avant d'utiliser l'IA au travail, renseignez-vous sur :

- les outils autorisés et leurs conditions (comptes professionnels, déploiement interne) ;
- les niveaux de données autorisés pour chaque outil ;
- les usages interdits ;
- les règles de mention ou de traçabilité ;
- le contact en cas d'incident.

S'il n'existe pas de politique, demandez-en une plutôt que d'utiliser des outils personnels non validés (« shadow AI »).

## 8. AI Act (règlement européen sur l'IA) : repères généraux

Le règlement européen sur l'intelligence artificielle, adopté en 2024, s'applique progressivement. Il suit une **approche par les risques** :

- **Pratiques interdites** (par exemple certaines formes de manipulation ou de notation sociale).
- **Systèmes à haut risque** (par exemple dans certains usages liés à l'emploi, aux infrastructures critiques, à l'éducation) : obligations renforcées de gestion des risques, documentation, supervision humaine, qualité des données.
- **Obligations de transparence** : par exemple informer qu'on interagit avec une IA, signaler certains contenus générés.
- **Modèles d'IA à usage général** : obligations spécifiques pour leurs fournisseurs.
- Une obligation générale de **maîtrise de l'IA** (*AI literacy*) pour les organisations qui déploient ces systèmes : former les personnes concernées.

Pour un utilisateur, l'impact concret dépend du cas d'usage : un assistant de rédaction n'a pas les mêmes obligations qu'un outil de tri de candidatures. Les détails et le calendrier d'application relèvent de votre service juridique.

## Pièges

- Coller un document client entier « juste pour gagner du temps ».
- Utiliser un compte personnel gratuit pour des données de l'entreprise.
- Partager une capture d'écran contenant un token ou une adresse interne.
- Croire que supprimer la conversation efface les données côté fournisseur.
- Utiliser l'IA pour évaluer ou trier des personnes sans cadre ni contrôle humain.
- Faire traiter des contenus externes par un agent ayant des droits étendus.

## Checklist

- [ ] L'outil utilisé est autorisé par mon organisation pour ce niveau de données.
- [ ] Les données sont minimisées et anonymisées.
- [ ] Aucun secret (mot de passe, clé, token, `.env`) dans le prompt ou les fichiers joints.
- [ ] J'ai les droits sur les contenus que je soumets.
- [ ] Les données personnelles sont traitées conformément au RGPD (DPO consulté si nouveau cas).
- [ ] La sortie est vérifiée et ses biais éventuels examinés.
- [ ] Je connais la procédure en cas de fuite.
