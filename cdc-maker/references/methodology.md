# Methodologie Cahier des Charges

## Table des Matieres

- [Sections par Scope](#sections-par-scope)
- [CDC Projet Complet](#cdc-projet-complet)
- [CDC Feature](#cdc-feature)
- [CDC Module](#cdc-module)
- [Principes de Redaction](#principes-de-redaction)
- [Anti-Patterns CDC](#anti-patterns-cdc)

## Sections par Scope

| Scope | Sections | Fichiers generes | Effort |
|-------|----------|-----------------|--------|
| Projet complet | 7 sections | 8-10 fichiers | High |
| Feature majeure | 5 sections | 4-5 fichiers | Medium |
| Module technique | 4 sections | 3-4 fichiers | Low-Medium |

## CDC Projet Complet

### 1. Contexte & Vision

**Contenu** :
- Probleme resolu (pain point quantifie si possible)
- Marche cible / utilisateurs
- Proposition de valeur unique
- Objectifs mesurables (OKRs)

**Format** :
```markdown
## Probleme
[Description du probleme avec chiffres]

## Solution
[Description de la solution en 3-5 phrases]

## Objectifs
| Objectif | Metrique | Cible |
|----------|----------|-------|
```

### 2. Perimetre Fonctionnel

**Contenu** :
- Features MVP (P0-P1) vs V2+ (P2-P4)
- User stories par role/personae
- Matrice MoSCoW (Must/Should/Could/Won't)

**Format** :
```markdown
## MVP (P0-P1)
| Feature | Description | Priorite |
|---------|-------------|----------|

## V2+ (P2-P4)
| Feature | Description | Priorite |
|---------|-------------|----------|

## User Stories
En tant que [role], je veux [action] pour [benefice].
```

### 3. Architecture Technique

**Contenu** :
- Stack technique (detecte automatiquement)
- Schema architecture (ASCII art)
- Integrations externes (APIs, services)
- Choix techniques justifies

**Format** :
```markdown
## Stack
| Couche | Technologie | Role |
|--------|-------------|------|

## Architecture
[Schema ASCII]

## Integrations
| Service | Usage | Cout |
|---------|-------|------|
```

### 4. Specifications par Module

**1 fichier par module si > 3 modules. Sinon 1 fichier consolide.**

**Contenu par module** :
- Description fonctionnelle
- Entites/tables concernees
- Endpoints/APIs
- Regles metier
- Cas limites

### 5. Planning & Phases

**Contenu** :
- Phases avec jalons (gates go/no-go)
- Estimation effort par phase
- Dependances inter-phases
- Chemin critique

**Format** :
```markdown
## Phases
| Phase | Description | Duree | Gate |
|-------|-------------|-------|------|

## Dependances
[Diagramme ASCII]
```

### 6. Criteres de Succes

**Contenu** :
- KPIs par phase
- Seuils go/no-go
- Metriques techniques (perf, uptime)
- Metriques business (adoption, ROI)

### 7. Risques & Mitigations

**Contenu** :
- Risques techniques (scalabilite, securite)
- Risques business (adoption, couts)
- Plan de mitigation par risque
- Plan B si risque majeur se realise

## CDC Feature

Meme principes, condenses en 5 sections :
1. Contexte & Objectif (pourquoi cette feature)
2. Specs Fonctionnelles (user stories, regles metier)
3. Specs Techniques (tables, APIs, integration)
4. Taches & Dependances (decoupage complet)
5. Criteres de Succes (definition of done)

## CDC Module

Version minimale, 4 sections :
1. Objectif (1 paragraphe)
2. Specifications (entites, regles, API)
3. Taches (tableau simple)
4. Validation (tests, criteres)

## Principes de Redaction

| Principe | Pourquoi |
|----------|----------|
| Actionnable > descriptif | Un CDC qui ne dit pas QUOI FAIRE est inutile |
| Quantifie > qualificatif | "150 emails/jour" > "beaucoup d'emails" |
| Reference > duplique | Si un doc existe, lien vers lui |
| 1 fichier < 300 lignes | Au-dela, personne ne lit |
| Diagrammes ASCII | Visuels sans dependance outil |
| Tables > texte | Plus scannable, plus precis |

## Anti-Patterns CDC

| Anti-Pattern | Symptome | Correction |
|-------------|----------|------------|
| CDC roman | 50+ pages, personne ne lit | 1 page/section max, tables |
| CDC sans taches | Vision sans execution | Toujours section taches |
| Taches sans executeur | "Quelqu'un fera X" | 1 tache = 1 executeur nomme |
| Taches sans livrable | "Faire le backend" | 1 tache = 1 livrable verifiable |
| Specs sans KPIs | Pas de definition de succes | KPIs mesurables par phase |
| Architecture inventee | Stack pas adapte au projet | Detecter l'existant d'abord |
| Copier-coller docs | Duplication → desync | Lien vers source unique |
| Tout en P0 | Pas de priorisation reelle | MoSCoW strict, 30% P0 max |
