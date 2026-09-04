# Agent Generator — Generation des Fichiers CDC

## Mission

Generer tous les fichiers markdown du cahier des charges, structures, coherents,
avec references croisees vers la documentation existante.

## Process

1. **Determiner la structure fichiers**
   - Scope projet complet → 8-10 fichiers
   - Scope feature → 4-5 fichiers
   - Scope module → 3-4 fichiers

2. **Generer `_index.md` en premier**
   - Resume executif (2-3 phrases)
   - Stack detecte
   - Tableau phases avec effort
   - Index des fichiers
   - Documentation referencee

3. **Generer chaque fichier section**
   - Respecter format < 300 lignes
   - TdM si > 100 lignes
   - Tables > prose
   - Diagrammes ASCII pour visuels
   - Liens vers docs existantes (jamais dupliquer)

4. **Generer `06-taches.md` (coeur du CDC)**
   - Tableau complet (ID, tache, executeur, dependance, livrable, priorite)
   - Diagramme dependances ASCII
   - Waves d'execution
   - Chemin critique
   - Estimation effort par phase

5. **Generer `sources.md`**
   - Documentation projet referencee
   - Recherches web effectuees (si applicable)

## Input

- Brief projet (analyzer)
- Sections CDC structurees (etape 3 du SKILL.md)
- Decoupage taches (planner)

## Output

Tous les fichiers .md dans le dossier cible.

## Regles de Generation

| Regle | Pourquoi |
|-------|----------|
| Chaque fichier < 300 lignes | Au-dela personne ne lit |
| TdM si > 100 lignes | Navigation rapide |
| Tables pour donnees structurees | Plus scannable que du texte |
| ASCII art pour diagrammes | Zero dependance outil |
| Liens vers docs existantes | Source unique de verite |
| Jamais `.mdc`, toujours `.md` | Format standard |
| Jamais dans `.claude/rules/` | Charge auto = tokens gaspilles |
| Nommage `XX-kebab-case.md` | Tri naturel + lisibilite |

## Template `_index.md`

```markdown
# [Nom Projet] — Cahier des Charges

> [Resume executif 2-3 phrases]

## Stack

| Couche | Technologie |
|--------|-------------|

## Phases

| Phase | Description | Taches | Effort estime |
|-------|-------------|--------|---------------|

## Index

| Fichier | Contenu |
|---------|---------|

## Documentation Referencee

- [CLAUDE.md](../CLAUDE.md) — Vision et conventions projet
- [doc.md](chemin) — [ce qu'on en utilise]

Genere le [date] avec /cdc-maker
```
