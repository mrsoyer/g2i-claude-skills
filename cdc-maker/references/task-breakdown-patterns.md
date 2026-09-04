# Patterns de Decoupage de Taches

## Table des Matieres

- [Principes Fondamentaux](#principes-fondamentaux)
- [Format Standard](#format-standard)
- [Patterns de Decomposition](#patterns-de-decomposition)
- [Gestion des Dependances](#gestion-des-dependances)
- [Waves d'Execution](#waves-dexecution)
- [Chemin Critique](#chemin-critique)
- [Assignation Executeurs](#assignation-executeurs)

## Principes Fondamentaux

### 1. Regle INVEST pour les taches

| Lettre | Critere | Exemple bon | Exemple mauvais |
|--------|---------|-------------|-----------------|
| **I**ndependante | Minimiser les dependances | "Creer types User" | "Faire le frontend" |
| **N**egociable | Scope ajustable | "Import CSV basique" | "Import parfait" |
| **V**aluable | Valeur livree | "CRUD personae fonctionnel" | "Setup projet" |
| **E**stimable | Effort quantifiable | "1 jour" | "Quelques jours" |
| **S**mall | Petite (1-3 jours max) | "RLS table prospects" | "Securiser la DB" |
| **T**estable | Verification possible | "Test: creer + lire personae" | "Backend OK" |

### 2. Granularite adaptee

| Scope CDC | Granularite tache | Exemple |
|-----------|-------------------|---------|
| Projet complet | 1-3 jours | "Creer schema migration toutes tables" |
| Feature | 0.5-1 jour | "Creer table campaigns + RLS" |
| Module | 1-4 heures | "Ecrire RPC calcul_reputation" |

## Format Standard

### Tableau de taches

```markdown
| ID | Tache | Executeur | Dep. | Livrable | Prio |
|----|-------|-----------|------|----------|------|
| 1.1 | Creer schema DB | sym-db-migration | - | Tables creees | P0 |
| 1.2 | RLS toutes tables | sym-db-sql | 1.1 | Policies actives | P0 |
| 1.3 | Types TypeScript | sym-fe-core | 1.1 | Fichiers .ts | P0 |
| 2.1 | Skill personae CRUD | Skill Cowork | 1.2 | /personae fonctionne | P0 |
```

### Fiche tache detaillee (optionnel, pour taches complexes)

```markdown
### Tache 3.5 — Skill newsletter-generate

**Executeur** : Skill Cowork custom (effort: high)
**Dependances** : 3.1 (agent recherche), 3.2 (agent tuto), 3.3 (agent use case)
**Livrable** : `/newsletter-generate immo paris` produit une newsletter HTML valide
**Effort** : 2 jours
**Risque** : Qualite contenu IA variable → mitigation : validation humaine

**Sous-taches** :
1. Creer SKILL.md orchestrateur
2. Creer agents/ (researcher.md, tutorial.md, assembler.md)
3. Creer templates/ (HTML base)
4. Creer scripts/validate-html.py
5. Tester sur 2 combinaisons personae x ville
```

## Patterns de Decomposition

### Pattern 1 — Par Couche Technique

```
Feature X
├── DB : schema + migration + RLS
├── Backend : API/RPC + logique metier
├── Frontend : types + hooks/composables + UI
└── Integration : wiring + tests e2e
```

Usage : Projets full-stack avec separation claire des couches.

### Pattern 2 — Par Module Fonctionnel

```
Projet
├── Module Auth : login, register, MFA, roles
├── Module Prospects : import, enrichissement, qualification
├── Module Campagnes : creation, envoi, monitoring
└── Module Newsletters : generation, envoi, analytics
```

Usage : Projets SaaS avec modules independants.

### Pattern 3 — Par User Story

```
"En tant que marketeur, je veux creer une campagne"
├── Tache : UI creation campagne
├── Tache : Selection prospects
├── Tache : Generation sequence emails
├── Tache : Assignation domaines
└── Tache : Preview + confirmation
```

Usage : Projets centre utilisateur, feature CDC.

### Pattern 4 — Par Phase Temporelle

```
Phase 1 (fondations) → Phase 2 (core) → Phase 3 (automation) → Phase 4 (scale)
```

Usage : Projets from scratch avec roadmap claire.

**Recommandation** : Combiner Pattern 4 (phases) + Pattern 1 (couches par phase).

## Gestion des Dependances

### Notation

```
A → B    = B depend de A (A doit etre fait avant B)
A | B    = A et B sont independants (parallelisables)
A + B → C = C depend de A ET B
```

### Diagramme ASCII

```
1.1 Schema ──────────┐
1.2 Types ───────────┤ (parallele)
1.3 Scripts PHP ─────┤
                     │
                     ▼
              1.4 RLS ────────────┐
                                  │
                     ┌────────────┤
                     ▼            ▼
              2.1 Skill CRUD   2.2 Skill Action
                     │
                     ▼
              3.1 Monitoring
```

### Matrice de dependances (pour projets complexes)

```
     | 1.1 | 1.2 | 1.3 | 1.4 | 2.1 | 2.2 |
-----|-----|-----|-----|-----|-----|-----|
1.1  |  -  |  -  |  -  |  -  |  -  |  -  |
1.2  |  X  |  -  |  -  |  -  |  -  |  -  |
1.3  |  -  |  -  |  -  |  -  |  -  |  -  |
1.4  |  X  |  -  |  -  |  -  |  -  |  -  |
2.1  |  -  |  -  |  -  |  X  |  -  |  -  |
2.2  |  -  |  -  |  X  |  X  |  -  |  -  |
```

X = depend de (ligne depend de colonne)

## Waves d'Execution

Regrouper les taches parallelisables en waves :

```
WAVE 1 (parallele) : taches sans dependance
├── 1.1 Schema DB
├── 1.2 Types TypeScript
└── 1.3 Scripts PHP

WAVE 2 (sequentiel apres wave 1) :
├── 1.4 RLS policies
└── 1.5 Docs partagees

WAVE 3 (parallele apres wave 2) :
├── 2.1 Skill personae
├── 2.2 Skill prospect-import
└── 2.3 Skill debounce

WAVE 4 (integration) :
└── Test bout en bout
```

**Regle** : chaque wave attend la completion de la wave precedente.
A l'interieur d'une wave, tout est parallele.

## Chemin Critique

Le chemin critique = la chaine de dependances la plus longue.
C'est le minimum incompressible de temps.

```
Exemple :
  Schema (1j) → RLS (0.5j) → Skill CRUD (1j) → Tests (0.5j) = 3 jours
  Types (0.5j) → Hooks (1j) → UI (2j) → Tests (0.5j) = 4 jours ← CRITIQUE
  Scripts PHP (1j) = 1 jour

Chemin critique = 4 jours (branche frontend)
```

Identifier le chemin critique permet de :
- Savoir le temps MINIMUM du projet
- Prioriser les taches sur ce chemin
- Savoir ou ajouter des ressources est utile

## Assignation Executeurs

### Matrice de Decision

| Critere | Executeur recommande |
|---------|---------------------|
| Interaction utilisateur recurrente | Skill Cowork custom |
| Schema/migration DB | Agent DB specialise |
| Policies/securite DB | Agent DB SQL |
| Types/interfaces code | Agent frontend core |
| Composants UI | Agent UI (React/Vue selon stack) |
| API/webhooks | Agent backend (edge functions, etc.) |
| Tache ponctuelle (script, template) | Claude Code direct |
| Tache recurrente automatique | Tache planifiee (`/schedule`) |
| Audit qualite/securite | Agent specialise (audit, security) |
| Integration multi-couches | Agent integration |

### Nommage Generique

Le CDC doit utiliser des noms GENERIQUES pour les executeurs,
pas des noms specifiques au framework SYM :

| Generique (dans le CDC) | Exemple SYM | Exemple autre |
|--------------------------|-------------|---------------|
| "Agent DB migration" | sym-db-migration | prisma migrate |
| "Agent DB SQL" | sym-db-sql | raw SQL |
| "Agent frontend types" | sym-fe-core | manual TS |
| "Agent UI Vue" | sym-fe-ui-vue | manual Vue |
| "Agent UI React" | sym-fe-ui-react | manual RN |
| "Skill Cowork custom" | .claude/skills/ | .claude/skills/ |
| "Claude Code direct" | prompt direct | prompt direct |
| "Tache planifiee" | /schedule | cron |

Si le projet utilise le framework SYM (detecte via `~/.claude/agents/`),
ajouter la colonne "Agent SYM" avec le nom precis.
