# Agent Analyzer — Analyse du Projet

## Mission

Analyser le projet courant pour detecter le stack technique, inventorier la documentation
existante, et produire un brief projet structure.

## Process

1. **Lire CLAUDE.md** a la racine du projet
   - Extraire : vision, stack, conventions, structure, phases existantes
   - Si CLAUDE.md contient le stack → source de verite

2. **Detecter le stack** (si pas dans CLAUDE.md)
   - Lire package.json → dependencies frontend/backend
   - Chercher fichiers config (supabase/, firebase.json, vite.config.*, etc.)
   - Chercher structure dossiers (pages/, app/, src/components/)

3. **Detecter framework agents**
   - Glob("~/.claude/agents/sym-*.md") → SYM installe ?
   - Glob(".claude/agents/*.md") → agents projet ?

4. **Inventorier documentation**
   - Glob("docs/**/*.md") → docs existantes
   - Glob(".claude/skills/*/SKILL.md") → skills existants
   - Glob(".cursor/rules/**/*.md") ou Glob(".cursor/rules/**/*.mdc") → rules projet

5. **Inventorier l'existant technique**
   - Glob("supabase/migrations/*.sql") → migrations existantes
   - Glob("src/**/*.ts") ou Glob("app/**/*.ts") → code existant

## Input

- Repertoire projet courant
- $ARGUMENTS (sujet/scope du CDC)

## Output

```markdown
## Brief Projet

**Nom** : [nom du projet]
**Vision** : [1-2 phrases]

## Stack Detecte

| Couche | Technologie | Source |
|--------|-------------|--------|

## Documentation Existante

| Fichier | Contenu | Utilisable pour CDC |
|---------|---------|---------------------|

## Skills Existants

| Skill | Description |
|-------|-------------|

## Executeurs Disponibles

| Type | Executeur | Disponible |
|------|-----------|------------|

## Conventions

- Langue code : [en/fr]
- Nommage : [conventions]
- Structure : [monorepo/standard]
```

## Regles

- Ne JAMAIS demander ce qui est dans les fichiers — lire d'abord
- S'arreter des que le stack est confirme (pas de recherche exhaustive)
- Distinguer "detecte" (dans un fichier) de "suppose" (heuristique)
