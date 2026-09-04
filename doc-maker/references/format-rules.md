# Regles de Format Documentation

## Structure Type Fichier Doc

```markdown
# [Sujet] — [Aspect]

## Table des Matieres (si > 100 lignes)
1. [Section 1](#section-1)
2. [Section 2](#section-2)

## Vue d'Ensemble
[1-3 phrases — comprehensible isolement]

## Concepts Cles
[Explications avec exemples code]

## Patterns Recommandes
[Configurations, code snippets, commandes]

## Anti-Patterns
[Ce qu'il ne faut PAS faire + pourquoi + correction]

## Sources
- [Titre](url) — [ce qu'on en a tire]
```

## Contraintes Taille

| Metrique | Limite | Pourquoi |
|----------|--------|----------|
| Fichier doc | < 300 lignes | Au-dela = decouper en 2 fichiers |
| TdM obligatoire | si > 100 lignes | Claude voit le scope meme en lecture partielle |
| _index.md | < 50 lignes | Juste les liens + description 1 ligne |
| Total par sujet | 5-15 fichiers max | Au-dela = trop granulaire |

## Principes de Redaction

1. **Sections autonomes** — chaque section comprehensible isolement, pas de "comme vu plus haut"
2. **Terminologie consistante** — choisir UN terme et s'y tenir partout
3. **Relations explicites** — "OAuth 2.0 de Supabase" pas "la methode mentionnee"
4. **Snippets > paragraphes** — 1 exemple code vaut mieux que 3 paragraphes
5. **Markdown pur** — jamais de HTML (consomme 80-90% plus de tokens)
6. **Sources toujours** — chaque fichier cite ses sources avec URLs

## Format _index.md

```markdown
# [Sujet] — Documentation Reference

> [Description 1 ligne]

| Fichier | Contenu |
|---------|---------|
| [01-overview.md](01-overview.md) | Vue d'ensemble |
| [02-xxx.md](02-xxx.md) | [Description] |

Sources : [N] pages web consultees le [date]
```

## Naming Fichiers

- `_index.md` — index obligatoire par dossier
- `XX-kebab-case.md` — numerote, kebab-case
- `sources.md` — consolidation sources (optionnel)
- `CDC-kebab-case.md` — cahiers des charges
