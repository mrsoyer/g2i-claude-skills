# Reference Frontmatter — Tous les Champs YAML Officiels

## Table des Matieres
1. [name](#name)
2. [description](#description)
3. [argument-hint](#argument-hint)
4. [disable-model-invocation](#disable-model-invocation)
5. [user-invocable](#user-invocable)
6. [allowed-tools](#allowed-tools)
7. [model](#model)
8. [effort](#effort)
9. [context](#context)
10. [agent](#agent)
11. [hooks](#hooks)
12. [paths](#paths)
13. [shell](#shell)

---

## name

Nom affiche du skill. Devient la commande `/name`.

| Spec | Valeur |
|------|--------|
| Requis | Non (defaut: nom du dossier) |
| Format | Minuscules, chiffres, tirets uniquement |
| Max | 64 caracteres |

```yaml
name: newsletter-generate
```

## description

Ce que fait le skill et quand l'utiliser. Mecanisme principal de declenchement auto.

| Spec | Valeur |
|------|--------|
| Requis | Recommande (defaut: 1er paragraphe du contenu) |
| Max utile | 250 chars (tronquee au-dela dans le listing) |
| Budget total | 1% fenetre contexte, fallback 8000 chars |

```yaml
# BON — front-loadee, mots-cles, < 250 chars
description: >
  Genere des newsletters IA hebdomadaires par personae et ville.
  Orchestre 3 agents (recherche, tuto, use case).
  Declenche avec "newsletter", "genere la newsletter [personae]".

# MAUVAIS — vague, pas de mots-cles
description: Un skill pour les newsletters.
```

## argument-hint

Indice affiche pendant l'autocompletion pour montrer les arguments attendus.

```yaml
argument-hint: "[personae] [ville]"
# Affiche: /newsletter-generate [personae] [ville]

argument-hint: "[issue-number]"
# Affiche: /fix-issue [issue-number]
```

## disable-model-invocation

Empeche Claude de declencher le skill automatiquement. Seul l'utilisateur peut invoquer.

| Spec | Valeur |
|------|--------|
| Defaut | `false` (Claude peut invoquer) |
| Quand `true` | Description PAS chargee en contexte |

```yaml
# Pour les skills avec effets de bord
disable-model-invocation: true
# Cas: /deploy, /send-email, /campaign-send, /delete-data
```

## user-invocable

Cache le skill du menu `/`. Seul Claude peut l'invoquer (background knowledge).

| Spec | Valeur |
|------|--------|
| Defaut | `true` (visible dans le menu /) |
| Quand `false` | Cache du menu, Claude invoque quand pertinent |

```yaml
# Background knowledge — pas une commande utilisateur
user-invocable: false
# Cas: contexte infra, conventions equipe, legacy system docs
```

## allowed-tools

Outils que Claude peut utiliser SANS demander permission quand le skill est actif.

```yaml
# String separe par espaces
allowed-tools: Read Write Edit Glob Grep Bash

# Ou liste YAML
allowed-tools:
  - Read
  - Grep
  - Bash(python *)

# Mode lecture seule
allowed-tools: Read Grep Glob
```

## model

Modele a utiliser quand le skill est actif.

```yaml
model: opus
# ou
model: sonnet
```

## effort

Niveau d'effort. Override le niveau session.

| Valeur | Usage |
|--------|-------|
| `low` | Taches rapides, reponses courtes |
| `medium` | Defaut |
| `high` | Taches complexes, multi-etapes |
| `max` | Opus 4.6 uniquement, raisonnement profond |

```yaml
effort: high
```

## context

`fork` = executer dans un subagent isole. Le skill n'a PAS acces a l'historique conversation.

```yaml
context: fork
# Le contenu du SKILL.md devient le prompt du subagent
# Utile pour: recherche isolee, analyse sans contexte
```

## agent

Type de subagent quand `context: fork`. Options: `Explore`, `Plan`, `general-purpose`, ou custom.

```yaml
context: fork
agent: Explore
# Le subagent Explore a des outils read-only optimises pour exploration
```

## hooks

Hooks scopes au lifecycle du skill. Meme format que les hooks globaux.

```yaml
hooks:
  PostToolUse:
    - command: "python scripts/validate.py"
      tools: ["Write", "Edit"]
```

## paths

Glob patterns pour limiter l'activation automatique. Le skill se charge uniquement quand
on travaille avec des fichiers qui matchent.

```yaml
paths: "**/*.newsletter.md"
# ou
paths:
  - "templates/newsletters/**"
  - "**/*.email.html"
```

## shell

Shell pour les commandes inline `` !`command` ``.

```yaml
shell: bash       # defaut
shell: powershell # Windows uniquement, requiert CLAUDE_CODE_USE_POWERSHELL_TOOL=1
```

---

## Tableau Recapitulatif

| Champ | Defaut | Cas d'usage principal |
|-------|--------|----------------------|
| `name` | nom dossier | Toujours definir explicitement |
| `description` | 1er paragraphe | Toujours definir (declenchement) |
| `argument-hint` | aucun | Skills avec arguments |
| `disable-model-invocation` | false | Effets de bord (envoi, deploy) |
| `user-invocable` | true | Background knowledge |
| `allowed-tools` | tous | Restreindre au necessaire |
| `model` | session | Forcer un modele specifique |
| `effort` | session | Taches complexes |
| `context` | inline | Isolation (fork) |
| `agent` | general-purpose | Type subagent si fork |
| `hooks` | aucun | Automation lifecycle |
| `paths` | tous fichiers | Activation conditionnelle |
| `shell` | bash | Windows PowerShell |
