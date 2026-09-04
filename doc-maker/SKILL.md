---
name: doc-maker
description: >
  Cree de la documentation de reference structuree a partir de recherches web.
  Pipeline : recherche multi-sources parallele, extraction, synthese, fichiers dans docs/.
  Declenche avec "documente", "doc sur X", "recherche et documente", "cree la doc".
argument-hint: "[sujet] [dossier-destination]"
effort: high
allowed-tools: Read Write Edit Glob Grep Bash WebSearch WebFetch
---

# Doc Maker — Createur de Documentation Reference

Tu crees de la documentation de reference structuree en recherchant sur le web,
extrayant le contenu, synthetisant et generant des fichiers prets a l'emploi.

## References disponibles

| Fichier | Quand le lire |
|---------|---------------|
| [references/format-rules.md](references/format-rules.md) | Etape 4-5 : structurer et generer les fichiers |
| [references/organization-rules.md](references/organization-rules.md) | Etape 5 : choisir l'emplacement |
| [references/search-patterns.md](references/search-patterns.md) | Etape 2-3 : rechercher et extraire |

## Agents disponibles

| Agent | Quand l'utiliser |
|-------|------------------|
| [agents/researcher.md](agents/researcher.md) | Etape 2 : generer et executer les recherches |
| [agents/fetcher.md](agents/fetcher.md) | Etape 3 : extraire le contenu des URLs |
| [agents/synthesizer.md](agents/synthesizer.md) | Etape 4 : structurer la documentation |
| [agents/validator.md](agents/validator.md) | Etape 6 : auditer la qualite |

## Workflow (7 etapes)

### Etape 1 — Cadrer le sujet

Si `$ARGUMENTS` est fourni, extraire :
- **Sujet** : `$0` (ce qu'on documente)
- **Destination** : `$1` si fourni, sinon `docs/[sujet-kebab]/`

Si le sujet est trop vague (1-2 mots generiques), poser UNE question :
"Tu veux une doc complete sur [sujet] ou juste un aspect precis ?"

Verifier si `docs/[sujet]/` existe deja. Si oui, proposer :
- Mettre a jour l'existant
- Creer un complement dans un sous-dossier

Generer un plan de recherche : lister 5-8 angles a couvrir.

### Etape 2 — Rechercher (agent researcher)

Charge [references/search-patterns.md](references/search-patterns.md).

Generer 5-8 requetes WebSearch couvrant ces angles :

| Angle | Pattern |
|-------|---------|
| Doc officielle | `site:[domaine-officiel] [sujet]` |
| Best practices | `[sujet] best practices 2026` |
| Tutoriels | `how to [sujet] tutorial guide` |
| Anti-patterns | `[sujet] mistakes avoid common errors` |
| Exemples reels | `[sujet] examples production real world` |
| Integration projet | `[sujet] [stack-du-projet] integration` |

Lancer TOUTES les recherches en PARALLELE (1 message, N appels WebSearch).
Raison : 5 recherches paralleles = meme temps qu'une seule.

Filtrer les resultats : garder top 8-12 URLs.
Classer : officiel > blog technique > github > community.

### Etape 3 — Extraire (agent fetcher)

Lancer WebFetch en PARALLELE sur les 5-10 meilleures URLs.

Adapter le prompt d'extraction au type de source :
- **Doc officielle** : "Extract ALL specifications, parameters, code examples, and constraints"
- **Blog/tuto** : "Extract ALL concrete recommendations, step-by-step instructions, and code snippets"
- **Anti-patterns** : "Extract ALL anti-patterns, common mistakes, and their corrections with examples"

Regles :
- TOUJOURS parallele (5-10 simultanes)
- Si URL echoue (JS-heavy, timeout 10s) → passer a la suivante
- Preferer `[site]/llms.txt` si disponible (markdown pre-optimise pour LLMs)
- Cache 15 min = re-fetch meme URL gratuit

### Etape 4 — Synthetiser (agent synthesizer)

Charge [references/format-rules.md](references/format-rules.md).

Transformer les extractions en fichiers documentation :

1. **Regrouper par theme** — identifier 3-8 themes distincts
2. **Croiser les sources** — convergence (cite 3+ fois) = fait etabli, divergence = noter les deux positions
3. **Structurer chaque fichier** selon ce format :

```markdown
# [Sujet] — [Aspect]

## Vue d'Ensemble
[1-3 phrases]

## Concepts Cles
[Explications avec exemples code]

## Patterns Recommandes
[Configurations, snippets]

## Anti-Patterns
[Ce qu'il ne faut PAS faire + pourquoi]

## Sources
- [Titre](url) — [ce qu'on en a tire]
```

4. **Contraintes** :
   - Chaque fichier < 300 lignes
   - Si > 100 lignes : table des matieres en haut
   - Sections autonomes (comprehensibles isolement)
   - Terminologie consistante dans tous les fichiers

### Etape 5 — Generer les fichiers

Charge [references/organization-rules.md](references/organization-rules.md).

Determiner l'emplacement :
- Par defaut : `docs/[sujet-kebab]/`
- Si `$1` fourni : utiliser ce chemin
- Si lie a un skill : proposer `.claude/skills/[skill]/references/`
- **JAMAIS dans `.claude/rules/`** (charge auto = gaspille tokens)

Creer la structure :
```
docs/[sujet-kebab]/
├── _index.md          # Index obligatoire
├── 01-overview.md     # Vue d'ensemble
├── 02-[theme-1].md    # Premier theme
├── 03-[theme-2].md    # Deuxieme theme
├── ...
└── sources.md         # Toutes les sources consolidees
```

**`_index.md`** obligatoire avec ce format :
```markdown
# [Sujet] — Documentation Reference

> [Description 1 ligne du contenu]

| Fichier | Contenu |
|---------|---------|
| [01-overview.md](01-overview.md) | Vue d'ensemble |
| [02-xxx.md](02-xxx.md) | [Description] |

Sources : [N] pages web consultees le [date]
```

Ecrire TOUS les fichiers d'un coup.

### Etape 6 — Auditer (agent validator)

Executer `python ${CLAUDE_SKILL_DIR}/scripts/doc-audit.py [chemin]`.

Checklist :
- `_index.md` existe avec liens valides (3 pts)
- Chaque fichier < 300 lignes (2 pts)
- TdM si > 100 lignes (1 pt)
- Sources citees dans chaque fichier (3 pts)
- Exemples code presents (2 pts)
- Pas de contenu vague (2 pts)
- Emplacement correct — dans `docs/` (3 pts)
- Format `.md` standard (1 pt)
- Naming `XX-kebab-case.md` (1 pt)
- Pas de fichiers vides (2 pts)

Score /20 :
- 18+ : Professionnelle
- 14-17 : Bonne
- 10-13 : Incomplete
- < 10 : A retravailler

Si < 14 : appliquer les corrections et re-auditer.

### Etape 7 — Resume

```
DOCUMENTATION CREEE
Sujet : [sujet]
Emplacement : [chemin]
Fichiers : [N] fichiers, [X] lignes total
Score : [Y]/20
Sources : [Z] pages web consultees

Fichiers :
  _index.md
  01-overview.md (X lignes)
  02-xxx.md (X lignes)
  ...

Suggestions :
- Creer un skill qui utilise cette doc (/skill-maker)
- Creer un CDC base sur cette doc
- Documenter un sujet lie : [suggestion]
```

## Regles

- Documentation dans `docs/` — JAMAIS dans `.claude/rules/` (charge auto = tokens gaspilles)
- Format `.md` standard — JAMAIS `.mdc` (format Cursor)
- Recherche TOUJOURS parallele (WebSearch et WebFetch)
- Sources TOUJOURS citees avec URLs
- Fichiers < 300 lignes, TdM si > 100
- Si le sujet existe deja, proposer mise a jour avant de recreer
