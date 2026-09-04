# Regles d'Organisation — Ou Ranger la Documentation

## Regle Fondamentale

**Documentation reference volumineuse → `docs/` (racine projet)**
**Regles courtes → `.claude/rules/` avec `paths:`**
**Doc liee a un skill → `.claude/skills/[skill]/references/`**

## Pourquoi PAS `.claude/rules/`

`.claude/rules/*.md` SANS `paths:` = charge AUTOMATIQUEMENT a chaque session.
= Chaque ligne consomme des tokens du contexte.
= Documentation volumineuse ici = gaspillage massif.

`.claude/rules/*.md` AVEC `paths:` = charge conditionnellement.
= Mieux, mais toujours reserve aux REGLES courtes, pas de la doc.

## Pourquoi `docs/`

- Jamais charge automatiquement = 0 tokens par defaut
- Claude lit avec l'outil Read quand on le lui demande
- Les skills peuvent pointer vers `docs/` dans leurs references
- Dossier standard reconnu par toutes les conventions

## Table de Decision

| Contenu | Emplacement | Format |
|---------|-------------|--------|
| Doc reference volumineuse | `docs/[sujet]/` | .md |
| CDC (cahier des charges) | `docs/[sujet]/CDC-*.md` | .md |
| Doc liee a un skill | `.claude/skills/[skill]/references/` | .md |
| Regles courtes conditionnelles | `.claude/rules/*.md` avec `paths:` | .md |
| Regles universelles | `CLAUDE.md` (< 200 lignes) | .md |

## Structure docs/

```
docs/
├── [sujet-1]/
│   ├── _index.md
│   ├── 01-overview.md
│   ├── 02-xxx.md
│   └── sources.md
├── [sujet-2]/
│   ├── _index.md
│   └── ...
└── ...
```

## Comment les Skills Accedent a docs/

```markdown
## References (dans SKILL.md)
| Fichier | Quand le lire |
|---------|---------------|
| docs/supabase/02-rls-policies.md | Quand tu crees des policies RLS |
| docs/ovh-email/01-api-specs.md | Quand tu configures l'envoi |
```

Claude lit le fichier UNIQUEMENT quand c'est pertinent.
