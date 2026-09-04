# Patterns de Recherche — WebSearch + WebFetch

## Pipeline

```
WebSearch (decouverte, parallele)
  → Filtrer top 8-12 URLs
    → WebFetch (extraction, parallele)
      → Synthese cross-sources
```

## WebSearch — Regles

| Regle | Detail |
|-------|--------|
| Parallele | 5-8 requetes simultanees (1 message, N appels) |
| Annee | Toujours inclure 2026 dans les requetes |
| Sites officiels | `site:docs.officiel.com` en priorite |
| Diversifier | Officiel + blogs + github + community |
| Mots-cles precis | "Supabase RLS best practices 2026" > "supabase securite" |

## WebSearch — Angles de Recherche

| Angle | Pattern requete | Priorite |
|-------|----------------|----------|
| Doc officielle | `site:[domaine] [sujet]` | P0 |
| Best practices | `[sujet] best practices 2026` | P0 |
| Tutoriels | `how to [sujet] tutorial guide` | P1 |
| Anti-patterns | `[sujet] mistakes avoid errors` | P1 |
| Exemples | `[sujet] examples production` | P2 |
| Integration | `[sujet] [stack-projet] integration` | P2 |
| Community | `[sujet] tips reddit discussion` | P3 |

## WebFetch — Regles

| Regle | Detail |
|-------|--------|
| TOUJOURS parallele | 5-10 fetch simultanes = ~2s total |
| Prompt specifique | Adapter au type de source (voir ci-dessous) |
| Si echec | Passer a l'URL suivante (timeout 10s) |
| Preferer llms.txt | `site.com/llms.txt` si disponible |
| Cache 15 min | Re-fetch = gratuit dans la fenetre |

## WebFetch — Prompts par Type de Source

| Type source | Prompt d'extraction |
|-------------|--------------------|
| Doc officielle | "Extract ALL specifications, parameters, return types, constraints, and code examples about [sujet]" |
| Blog/tutorial | "Extract ALL concrete recommendations, step-by-step instructions, code snippets, and tips about [sujet]" |
| Anti-patterns | "Extract ALL anti-patterns, common mistakes, their corrections, and prevention strategies for [sujet]" |
| GitHub README | "Extract ALL setup instructions, configuration options, usage examples, and API reference for [sujet]" |

## Anti-Patterns Recherche

| Anti-Pattern | Correction |
|-------------|-----------|
| 1 seule requete | 5-8 requetes angles differents |
| Fetch sequentiel | PARALLELE (5-10 simultanes) |
| Prompt vague "resume cette page" | Prompt specifique "Extract ALL X about Y" |
| Pas de sources citees | URLs + dates dans chaque fichier |
| Pages JS-heavy fetchees | Preferer docs statiques |
