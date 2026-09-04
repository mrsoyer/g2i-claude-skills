# Anti-Patterns a Eviter dans les Skills

## 1. Description Trop Vague

```yaml
# MAUVAIS — Claude ne sait pas quand declencher
description: Un skill pour les newsletters.

# BON — mots-cles, contextes, specifique
description: >
  Genere des newsletters IA hebdomadaires par personae et ville.
  Orchestre 3 agents (recherche, tuto, use case).
  Declenche avec "newsletter", "genere la newsletter [personae]".
```

**Pourquoi** : La description est le mecanisme #1 de declenchement. Vague = jamais trigger.

## 2. SKILL.md Trop Long (> 500 lignes)

```markdown
# MAUVAIS ��� 800 lignes, tout melange
[templates HTML, exemples, specs API, instructions]

# BON — SKILL.md leger + references/
SKILL.md (150 lignes) = orchestration
references/templates.md = HTML
references/examples.md = exemples
references/api-specs.md = specs
```

**Pourquoi** : SKILL.md est charge en entier en contexte. Trop long = gaspillage de tokens.

## 3. Instructions Vagues

```markdown
# MAUVAIS
Analyse le contenu et fais quelque chose d'utile.

# BON
Analyse le contenu fourni. Identifie :
1. Le ton (formel, informel, technique)
2. La structure (titres, paragraphes, listes)
3. Les points faibles (phrases longues, jargon, repetitions)
Retourne un tableau : point faible | ligne | suggestion.
```

**Pourquoi** : Vague = Claude invente. Specifique = resultat previsible.

## 4. Pas de Format Output

```markdown
# MAUVAIS
Genere le rapport.

# BON
Genere le rapport au format :
## Resume Executif (3 phrases max)
## Metriques Cles
| Metrique | Valeur | Tendance |
## Recommandations (liste, max 5)
```

**Pourquoi** : Sans format, chaque execution donne un resultat different.

## 5. Skill Trop Narrow

```markdown
# MAUVAIS — ne marche que pour 1 cas
Genere un email pour Jean-Pierre de Acme au sujet du devis #4521.

# BON — generique et reutilisable
Genere un email de relance commerciale.
Inputs : nom contact, societe, objet (devis, proposition, etc.)
Ton : professionnel mais chaleureux.
```

**Pourquoi** : Un skill trop specifique ne sert qu'une fois. Inutile.

## 6. CAPS et MUST Partout

```markdown
# MAUVAIS
TU DOIS TOUJOURS ABSOLUMENT utiliser le format JSON.
NE JAMAIS OUBLIER de verifier les donnees.

# BON
Utilise le format JSON pour la sortie.
Raison : compatibilite avec l'API d'envoi.
Verifie les donnees avant traitement (emails valides, champs requis).
```

**Pourquoi** : CAPS partout = rien n'est important. Expliquer le pourquoi est plus efficace.

## 7. Inventer des Features Cowork

```markdown
# MAUVAIS
Utilise la fonction magicExport() de Cowork pour...
Active le mode turbo avec /turbo-mode...
Appelle l'API interne Cowork.generatePDF()...

# BON
[Ne decrire que des fonctionnalites reelles]
[En cas de doute, ne pas inventer]
```

**Pourquoi** : Claude va essayer d'executer des features qui n'existent pas = erreur.

## Detection Rapide

| Signal dans le SKILL.md | Anti-pattern probable |
|------------------------|---------------------|
| Description < 10 mots | #1 Description vague |
| > 500 lignes total | #2 Trop long |
| "fais quelque chose", "traite ca" | #3 Vague |
| Pas de format/exemple output | #4 Pas de format |
| Noms propres hardcodes | #5 Trop narrow |
| > 5% mots en FULL CAPS | #6 CAPS abusifs |
| Fonctions/APIs non documentees | #7 Features inventees |
