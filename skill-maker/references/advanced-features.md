# Features Avancees des Skills

## 1. Injection de Contexte Dynamique

La syntaxe `` !`<command>` `` execute des commandes shell AVANT envoi a Claude.
Claude ne voit que le resultat, pas la commande.

```yaml
---
name: pr-summary
context: fork
agent: Explore
---

## Contexte PR
- Diff: !`gh pr diff`
- Commentaires: !`gh pr view --comments`
- Fichiers: !`gh pr diff --name-only`
```

Multi-lignes avec bloc ` ```! ` :

````markdown
## Environnement
```!
node --version
npm --version
git status --short
```
````

**Quand l'utiliser** : Donnees dynamiques necessaires avant execution (git, API, fichiers).

## 2. Variables de Substitution

| Variable | Description | Exemple |
|----------|-------------|---------|
| `$ARGUMENTS` | Tous les arguments passes | `/skill arg1 arg2` → "arg1 arg2" |
| `$ARGUMENTS[0]` ou `$0` | Premier argument | `/skill hello` → "hello" |
| `$ARGUMENTS[1]` ou `$1` | Deuxieme argument | `/skill a b` → "b" |
| `${CLAUDE_SESSION_ID}` | ID session | Pour logs, fichiers uniques |
| `${CLAUDE_SKILL_DIR}` | Dossier du skill | Pour referencer scripts bundled |

```yaml
---
name: fix-issue
---

Corrige l'issue GitHub $ARGUMENTS.
1. Lis la description de l'issue
2. Implemente le fix
3. Ecris les tests
```

Si `$ARGUMENTS` n'est pas dans le contenu, Claude recoit `ARGUMENTS: <valeur>` a la fin.

## 3. Execution en Subagent (context: fork)

Le skill tourne dans un contexte ISOLE — pas d'acces a l'historique conversation.

```yaml
---
name: deep-research
context: fork
agent: Explore     # Outils read-only optimises
---

Recherche $ARGUMENTS en profondeur.
Trouve les fichiers pertinents et resume.
```

Types d'agents disponibles :
- `Explore` : read-only, exploration codebase
- `Plan` : architecture, planning
- `general-purpose` : tous les outils
- Nom d'un custom agent dans `.claude/agents/`

**Quand l'utiliser** : Recherche isolee, analyse sans polluer le contexte principal.

## 4. Controle d'Invocation

| Config | User invoque | Claude invoque | Description en contexte |
|--------|-------------|----------------|------------------------|
| Defaut | Oui | Oui | Oui |
| `disable-model-invocation: true` | Oui | Non | Non |
| `user-invocable: false` | Non | Oui | Oui |

Combinaison typique pour MyCommu :
- `/campaign-send` : `disable-model-invocation: true` (envoi = effet de bord)
- Contexte infra OVH : `user-invocable: false` (background knowledge)
- `/newsletter-generate` : defaut (user + Claude peuvent trigger)

## 5. Restriction d'Outils

```yaml
# Mode lecture seule (exploration)
allowed-tools: Read Grep Glob

# Mode ecriture controlee
allowed-tools: Read Write Edit Glob Grep

# Avec commandes specifiques
allowed-tools:
  - Read
  - Bash(python *)
  - Bash(npm test)
```

## 6. Paths (Activation Conditionnelle)

Le skill ne se charge que quand on travaille avec des fichiers qui matchent :

```yaml
paths: "templates/newsletters/**"
# ou
paths:
  - "**/*.newsletter.md"
  - "**/*.email.html"
```

## 7. Hooks Lifecycle

Actions automatiques liees au cycle de vie du skill :

```yaml
hooks:
  PostToolUse:
    - command: "python scripts/validate.py"
      tools: ["Write", "Edit"]
```

## 8. Extended Thinking

Inclure le mot "ultrathink" n'importe ou dans le contenu du skill active le mode thinking etendu.

## Matrice de Decision Features

| Besoin | Feature a utiliser |
|--------|-------------------|
| Donnees dynamiques avant execution | `` !`command` `` injection |
| Arguments utilisateur | `$ARGUMENTS`, `$0`, `$1` |
| Scripts bundled portables | `${CLAUDE_SKILL_DIR}` |
| Isolation du contexte | `context: fork` |
| Empecher Claude de trigger | `disable-model-invocation: true` |
| Background knowledge | `user-invocable: false` |
| Limiter outils | `allowed-tools` |
| Activation par fichier | `paths` |
| Raisonnement profond | "ultrathink" dans le contenu |
