---
name: cdc-maker
description: >
  Cree des cahiers des charges structures avec decoupage taches, dependances et assignation executeurs.
  Detecte le stack technique du projet automatiquement.
  Declenche avec "cahier des charges", "CDC", "specs projet", "decoupage taches", "plan de dev".
argument-hint: "[sujet-ou-feature]"
effort: high
allowed-tools: Read Write Edit Glob Grep Bash WebSearch WebFetch
---

# CDC Maker — Createur de Cahiers des Charges

Tu crees des cahiers des charges professionnels, structures et actionnables.
Tu detectes le stack du projet, analyses la documentation existante,
decoupe en taches avec dependances, et assigne chaque tache a un executeur.

## References disponibles

Charge ces fichiers a la demande selon l'etape en cours :

| Fichier | Quand le lire |
|---------|---------------|
| [references/methodology.md](references/methodology.md) | Etape 3 : structurer le CDC |
| [references/task-breakdown-patterns.md](references/task-breakdown-patterns.md) | Etape 4 : decouper les taches |
| [references/stack-detection.md](references/stack-detection.md) | Etape 2 : detecter le stack |

## Agents disponibles

| Agent | Quand l'utiliser |
|-------|------------------|
| [agents/analyzer.md](agents/analyzer.md) | Etape 2 : analyser le projet |
| [agents/planner.md](agents/planner.md) | Etape 4 : decouper en taches |
| [agents/generator.md](agents/generator.md) | Etape 5 : generer les fichiers |

## Workflow (8 etapes)

### Etape 1 — Cadrer le perimetre

Si `$ARGUMENTS` est fourni, utilise-le comme sujet du CDC.
Sinon, demande : "CDC pour quel projet ou quelle feature ?"

Determine le scope :
- **Projet complet** : CDC global (toutes les phases, de zero a production)
- **Feature majeure** : CDC feature (1 feature, ses sous-taches, son integration)
- **Module** : CDC module (1 bloc technique isole)

Verifie si un CDC existe deja :
- Chercher `docs/cahier-des-charges*/` ou `docs/cdc-*/`
- Si oui, proposer : mettre a jour ou creer un complement

### Etape 1bis — Recueillir les invariants non-negociables

AVANT de decouper, demande explicitement les **contraintes transverses** du commanditaire — celles qui
doivent tenir partout : fidelite d'un chiffre source (ex. « le spend doit correspondre a ce qui a vraiment
ete depense »), regle d'identite/dedup, mono-definition d'une mesure, perimetre legal/PII.

Chaque invariant recueilli devient, dans le CDC :
- soit un **test de reconciliation NOMME** la ou la donnee permet de le verifier
  (ex. `assert_no_spend_lost` : Σ alloue + Σ residuel = source au centime) ;
- soit une **LIMITE explicite, scopee et datee** si la donnee ne peut structurellement pas le satisfaire.

JAMAIS un invariant relegue en simple « Risque » ni rendu optionnel. Liste-les en tete du `_index.md`
(section **Invariants non-negociables**) et trace chacun jusqu'a une tache + un livrable verifiable.

### Etape 2 — Analyser le projet ET mesurer le terrain

**Detection automatique du stack** :

Lis ces fichiers dans l'ordre (stopper des qu'on a assez d'info) :

1. `CLAUDE.md` (racine projet) — vision, stack, conventions
2. `package.json` — dependencies frontend/backend
3. `supabase/config.toml` — si Supabase
4. `firebase.json` — si Firebase
5. `app.json` ou `app.config.js` — si Expo/React Native
6. `vite.config.*` ou `next.config.*` — si web
7. `docker-compose.yml` — si containerise
8. `.claude/skills/` — skills existants
9. `docs/` — documentation existante

Charge [references/stack-detection.md](references/stack-detection.md) pour le mapping stack → executeurs.

**Inventorier la documentation existante** :

Lister tout ce qui existe dans `docs/` avec un `Glob("docs/**/*.md")`.
Ces documents sont des inputs pour le CDC — les referencer, pas les dupliquer.

**Mesurer le terrain (data/warehouse)** : si un MCP de donnees / acces warehouse est **detecte ET
accessible** (BigQuery, Supabase…), execute des requetes d'agregat (COUNT/LIMIT, jamais `SELECT *`)
pour mesurer non seulement l'etat **courant** mais aussi le **plafond atteignable** des couvertures /
volumetries qui **dimensionnent les decisions**. Raison : un CDC data qui fige une ambition sur un chiffre
non re-mesure se trompe de grain (ex. mesurer « couverture campagne 8,6 % aujourd'hui » SANS mesurer le
plafond accessible ~75-79 % sous-dimensionne le livrable). Reporte chaque chiffre **date** dans le Brief.

**Output** : Brief projet structure :
```
PROJET : [nom]
STACK : [frontend] + [backend] + [infra]
INVARIANTS NON-NEGOCIABLES : [liste — chacun = test nomme OU limite scopee]
DOCS EXISTANTES : [liste fichiers docs/]
SKILLS EXISTANTS : [liste skills .claude/skills/]
CHIFFRES MESURES (le AAAA-MM-JJ) : [valeur — requete — date — [actuel | plafond atteignable]]
CONVENTIONS : [langue, nommage, structure]
```

### Etape 3 — Structurer le CDC

Charge [references/methodology.md](references/methodology.md).

Definir les sections du CDC selon le scope :

**CDC Projet Complet** (7 sections) :
1. Contexte & Vision
2. Perimetre Fonctionnel (MVP vs V2+)
3. Architecture Technique
4. Specifications detaillees par module
5. Planning & Phases
6. Criteres de Succes (KPIs)
7. Risques & Mitigations

**CDC Feature** (5 sections) :
1. Contexte & Objectif
2. Specifications Fonctionnelles
3. Specifications Techniques
4. Taches & Dependances
5. Criteres de Succes

**CDC Module** (4 sections) :
1. Objectif
2. Specifications
3. Taches
4. Validation

Pour chaque section, noter les sources d'information :
- Docs existantes → reference directe (pas de copie)
- Recherche web necessaire → lancer WebSearch
- Input utilisateur necessaire → poser la question

### Etape 4 — Decouper les taches

Charge [references/task-breakdown-patterns.md](references/task-breakdown-patterns.md).

**Principes de decoupage** :

1. **1 tache = 1 livrable verifiable**
   Raison : une tache sans livrable est incontrolable.

2. **Identifier les dependances AVANT de lister les taches**
   Raison : l'ordre d'execution decoule des dependances, pas de l'intuition.

3. **Maximiser le parallelisme**
   Raison : les taches sans dependance mutuelle se font en parallele.

4. **Assigner un executeur a chaque tache**
   Raison : une tache sans proprietaire n'avance pas.

**Process** :

```
Pour chaque module/feature :
  1. Lister les taches brutes (brain dump)
  2. Pour chaque tache → definir le livrable verifiable
  3. Pour chaque tache → identifier les dependances (quoi doit etre fait avant)
  4. Regrouper en phases (taches sans dependance = meme phase)
  5. Pour chaque tache → assigner l'executeur optimal
  6. Calculer le chemin critique (chaine de dependances la plus longue)
```

**Format tache** :

| Champ | Description |
|-------|-------------|
| ID | Identifiant unique (ex: 1.3) |
| Tache | Description courte et actionnable |
| Executeur | Skill Cowork, agent SYM, Claude Code direct, ou manuel |
| Dependances | IDs des taches pre-requises |
| Livrable | Ce qu'on peut verifier a la fin |
| Priorite | P0 (bloquant) → P4 (nice-to-have) |

**Assignation executeurs** (adapter au stack detecte) :

| Type de travail | Executeur type |
|----------------|----------------|
| Schema/migration DB | Agent DB specialise (sym-db-migration, etc.) |
| Policies/securite DB | Agent DB SQL (sym-db-sql, etc.) |
| Types/interfaces | Agent frontend core (sym-fe-core, etc.) |
| Skill interactif (CRUD, monitoring) | Skill Cowork custom |
| Orchestration multi-agents | Skill Cowork custom (effort: high) |
| Script one-shot | Claude Code direct |
| Templates/contenu | Claude Code direct |
| Tache recurrente | Tache planifiee (`/schedule`) |
| UI/dashboard web | Agent UI (sym-fe-ui-vue, sym-fe-ui-react, etc.) |
| Audit securite | Agent securite (sym-security) |
| Integration cross-layer | Agent integration (sym-integ) |

### Etape 5 — Generer les fichiers

Creer la structure dans `docs/cahier-des-charges/` (ou `docs/cdc-[feature]/` si feature).

**Structure CDC Projet Complet** :
```
docs/cahier-des-charges/
├── _index.md              # Index avec liens + resume executif
├── 01-vision.md           # Contexte, vision, objectifs
├── 02-perimetre.md        # Features MVP vs V2+, user stories
├── 03-architecture.md     # Stack, schemas, integrations
├── 04-specs-[module].md   # 1 fichier par module (si > 1)
├── 05-planning.md         # Phases, waves, timeline
├── 06-taches.md           # Decoupage complet avec executeurs
├── 07-kpis.md             # Criteres de succes, metriques
└── sources.md             # Docs referencees + recherches
```

**Structure CDC Feature** :
```
docs/cdc-[feature]/
├── _index.md
├── 01-specs.md
├── 02-taches.md
├── 03-recette.md      # OBLIGATOIRE si le CDC livre un outil/produit utilisable
└── sources.md
```

**`03-recette.md` — la recette scenarisee** (obligatoire des que le CDC livre un outil,
une UI, un MCP, une API — tout ce qu'un utilisateur final manipulera) :
- un scenario bout-en-bout NUMEROTE, de l'installation/premier contact jusqu'au nettoyage,
  couvrant TOUTES les capacites livrees ;
- chaque etape = une action + un critere **PASS/FAIL verifiable sur pieces** (jamais
  « ca marche » — un compte, un statut, un octet mesure) ;
- la **regle d'iteration** : chaque friction devient un constat date (format F*),
  un correctif, puis la recette se REJOUE INTEGRALEMENT depuis l'etape 0 (un correctif
  peut casser l'amont) — jusqu'a PASS integral ;
- les artefacts de test portent un prefixe dedie (ex: zz_test_) et leur nettoyage est
  une etape obligatoire meme en cas d'echec du run ;
- la recette est tracee comme **tache P0 finale** du tableau de taches, et si un
  dogfood/une recette anterieure existe, chaque constat qu'elle a produit est trace en
  tache ou limite scopee (jamais un simple « risque »).

**Regles de generation** :
- Chaque fichier < 300 lignes (sinon decouper)
- Table des matieres si > 100 lignes
- Jamais dupliquer le contenu d'un doc existant → reference avec lien
- Sources citees dans chaque fichier
- Diagrammes ASCII pour dependances et architecture

**`_index.md`** doit contenir :
```markdown
# [Nom] — Cahier des Charges

> [Resume executif en 2-3 phrases]

## Stack detecte
[Frontend] + [Backend] + [Infra]

## Phases
| Phase | Description | Taches | Effort |
|-------|-------------|--------|--------|

## Index
| Fichier | Contenu |
|---------|---------|

## Documentation referencee
- [doc1.md](chemin) — ce qu'on en utilise
```

**`06-taches.md`** (le coeur du CDC) doit contenir :
- Tableau complet ID | Tache | Executeur | Dependance | Livrable | Priorite
- Diagramme de dependances ASCII
- Waves d'execution (groupes parallelisables)
- Estimation effort par phase
- Chemin critique identifie

### Etape 6 — Auditer

Executer `python ${CLAUDE_SKILL_DIR}/scripts/cdc-audit.py [chemin]` si disponible.

⚠️ **Le score de `cdc-audit.py` est INDICATIF** (presence de vocabulaire + checks structurels), **PAS un
gate de veracite** : il ne sait pas si un chiffre est faux, fantome ou non source, ni si un invariant du
commanditaire est reellement teste. Un CDC peut scorer haut tout en portant des chiffres non mesures. Le
script **n'est pas branche en CI**. Apres le score, fais TOUJOURS une passe manuelle : (1) chaque chiffre
dimensionnant est-il **date + source** (mesure / a valider) ? (2) chaque invariant non-negociable est-il
trace en **test nomme ou limite scopee** ? (3) un chiffre depasse-t-il un total connu (signal de chiffre fantome) ?
(4) si le CDC livre un outil utilisateur : `03-recette.md` existe-t-elle, avec criteres PASS/FAIL et regle
« friction → correctif → rejouer depuis l'etape 0 » ? (5) si un dogfood/une recette anterieure a produit des
constats : chacun est-il trace en tache (table de traçabilite) ou en limite explicitement scopee ?

Sinon, appliquer manuellement :

| Check | Poids |
|-------|-------|
| `_index.md` avec resume executif | 3 |
| Stack detecte et documente | 2 |
| Toutes taches ont un executeur assigne | 3 |
| Toutes taches ont un livrable verifiable | 3 |
| Dependances documentees | 2 |
| Waves parallelisables identifiees | 2 |
| KPIs mesurables | 2 |
| Fichiers < 300 lignes | 1 |
| Sources/docs referencees (pas dupliquees) | 2 |

Score /20 :
- 18+ : CDC professionnel
- 14-17 : Bon, ajustements mineurs
- < 14 : Retravailler

### Etape 7 — Generer le pack de lancement

Objectif : traduire les waves d'execution (Etape 4) en prompts prets a coller, pour que l'utilisateur
sache EXACTEMENT quoi lancer — sans jamais avoir a le redemander. Le LAUNCH.md contient DEUX modes.

#### Mode A — Orchestrateur autonome (a generer EN PREMIER, c'est le mode recommande)

UN SEUL prompt, a coller dans UN chat avec le modele le plus capable disponible (fable/opus).
Principe economique : le modele cher NE PRODUIT PAS — il decide, verifie et journalise ; tout le
mecanique part en subagents sonnet, les relectures adversariales en opus. Le prompt DOIT contenir :

1. **Lecture d'etat d'abord** : lire `docs/cdc-[feature]/.executed/journal.md` s'il existe (reprendre
   exactement ou il s'arrete), puis les fichiers du CDC dans l'ordre (invariants → specs → taches → recette).
2. **Mission par waves** : executer W0→Wn ; une wave ne s'ouvre que si la gate de sortie de la
   precedente est VERIFIEE SUR PIECES (tests, CI, requetes, PR mergee) — jamais supposee.
3. **Verification apres CHAQUE tache** : controler le livrable du tableau de taches avant de la
   marquer faite ; en echec → correctif → re-verification, en boucle, sans passer a la suite.
4. **Delegation par modele** : sonnet = mecanique (edits, tests, endpoints, docs), opus = relectures/
   verdicts, orchestrateur = arbitrages et diagnostics.
5. **Decisions autonomes journalisees** : l'orchestrateur tranche SEUL tous les arbitrages delegues
   (les lister nominativement avec leurs garde-fous NON negociables), justification dans le journal.
6. **Arrets obligatoires** : la liste FERMEE des seuls cas ou il s'arrete et demande a l'utilisateur
   (perte de donnees, secrets/credentials, operations destructives globales, actions UI humaines).
7. **Recette en boucle** : jouer `03-recette.md` ; chaque friction = constat date → correctif →
   REJOUER depuis l'etape 0 ; jusqu'a PASS integral.
8. **Journal** : apres chaque tache/gate/run, mettre a jour `.executed/journal.md` (horodatage, statut,
   commits/PRs, decisions) — le chat est relancable a volonte, l'etat vit hors contexte.
9. **Regles de securite du repo** (git add explicite, builds serialises, secrets jamais commites) et
   la clause : le CDC gagne sur le prompt ; le TERRAIN qui contredit le CDC = arret + journal.

Terminer par la liste « ce qui reste chez l'utilisateur en Mode A » (GO initial, actions UI, arrets,
revue a posteriori du journal).

#### Mode B — Pack par tache (reprises ciblees)

**Pour chaque tache de la Wave 1** (sans dependance) dont l'executeur est "Claude Code direct" :

```markdown
### Tache [ID] — [nom]

Lis le CDC complet : @[chemin vers le fichier taches du CDC]

Tu es l'executeur de la tache [ID] : [nom].
Dependances : aucune (Wave 1)
Perimetre strict : ne touche QUE les fichiers listes pour cette tache dans le CDC.
Critere de fin : [critere de verification copie depuis le tableau de taches]

Demarre en Plan Mode : explore les fichiers concernes, propose un plan technique,
attends la validation avant d'editer quoi que ce soit.
```

**Pour une tache dont l'executeur est un agent SYM** (ex: sym-db-migration) :

```markdown
### Tache [ID] — [nom]

Use [agent-sym] pour : [tache], en lisant @[chemin CDC] (tache [ID]).
Critere de fin : [critere de verification]
```

**Pour une tache "Skill Cowork custom"** → ne pas generer de prompt de lancement, noter plutot :
*"Skill a creer d'abord via /skill-maker avant de pouvoir lancer cette tache."*

**Pour une tache "Tache planifiee"** → noter : *"A configurer via /schedule, pas un chat a lancer."*

**Repeter pour chaque wave**, avec un marqueur explicite et la regle d'attente entre waves :

```markdown
## WAVE 1 — lancer ces [N] chats en parallele maintenant
[bloc prompt par tache...]

## WAVE 2 — attendre que la Wave 1 soit committee, puis lancer ces [N] chats
[bloc prompt par tache...]
```

**Output** : fichier `docs/cdc-[feature]/LAUNCH.md` (ou `docs/cahier-des-charges/LAUNCH.md` si CDC projet
complet) : Mode A (LE prompt orchestrateur) en tete, puis Mode B structure par wave. C'est l'artefact que
l'utilisateur copie-colle directement — le pack de lancement, pas juste un comptage.

### Etape 8 — Resume

```
CDC CREE
Projet : [nom]
Scope : [complet/feature/module]
Stack : [frontend] + [backend] + [infra]
Emplacement : [chemin]
Fichiers : [N] fichiers, [X] lignes total
Score : [Y]/20

Decoupage :
  [N] taches au total
  [N] phases
  [N] taches parallelisables
  Chemin critique : [N] taches sequentielles

Executeurs :
  [N] skills Cowork a creer
  [N] agents SYM a invoquer
  [N] taches Claude Code direct
  [N] taches planifiees

Pack de lancement : docs/cdc-[feature]/LAUNCH.md ([N] prompts, [N] waves)

Prochaine etape recommandee :
  Ouvrir les [N] chats de la Wave 1 (voir LAUNCH.md) — tous en parallele
```

## Regles

- Detecter le stack automatiquement — ne jamais demander ce qui est dans les fichiers
- **Un CDC data ne fige aucun dimensionnement sur un chiffre non re-mesure** quand la donnee est accessible — mesure le **potentiel** (plafond), pas seulement l'etat courant ; tout chiffre = date + tag (mesure / a valider)
- **Tout invariant transverse du commanditaire = test de reconciliation NOMME, OU limite explicite scopee** — jamais relegue en simple « Risque » ni rendu optionnel
- 1 tache = 1 livrable verifiable = 1 executeur assigne
- **CDC qui livre un outil utilisateur = recette scenarisee obligatoire** (`03-recette.md` : scenario
  numerote, criteres PASS/FAIL sur pieces, regle « friction → constat date → correctif → rejouer depuis
  l'etape 0 jusqu'a PASS integral »), tracee comme tache P0 finale
- **Tout constat d'un dogfood/d'une recette anterieure = tache tracee ou limite scopee** (table de
  traçabilite constats → taches), jamais un simple « risque »
- Referencer les docs existantes, jamais les dupliquer
- Maximiser le parallelisme dans les waves d'execution
- Toujours generer le pack de lancement (LAUNCH.md, Etape 7) avec ses DEUX modes — Mode A orchestrateur
  autonome (un prompt, verification apres chaque tache, journal, arrets fermes) en premier, Mode B pack
  par tache pour les reprises — l'utilisateur ne doit jamais redemander quoi lancer
- Adapter les executeurs au stack detecte (pas de recommandation Supabase si Firebase)
- Fichiers dans `docs/` — jamais dans `.claude/rules/`
- Format `.md` — jamais `.mdc`
