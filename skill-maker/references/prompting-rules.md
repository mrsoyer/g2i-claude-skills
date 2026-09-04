# Regles de Redaction pour Skills

## 1. Mode Imperatif (Obligatoire)

```markdown
# BON
Lis le document fourni. Identifie les points cles. Classe-les par priorite.

# MAUVAIS
Tu devrais peut-etre commencer par lire le document et essayer de trouver les points cles.
```

## 2. Expliquer le Pourquoi

```markdown
# BON
Limite chaque section a 3 phrases maximum.
Raison : les destinataires sont des dirigeants qui parcourent rapidement.

# MAUVAIS
Limite chaque section a 3 phrases maximum.
```

## 3. Structure en Etapes Numerotees

```markdown
## Etape 1 — Analyser l'entree
[instructions]

## Etape 2 — Traiter
[instructions]

## Etape 3 — Formater la sortie
[instructions]
```

## 4. Tailles Recommandees

| Zone | Ideal | Maximum |
|------|-------|---------|
| Description frontmatter | 50-100 mots | 250 chars utiles |
| Corps SKILL.md | 100-300 lignes | 500 lignes |
| Total SKILL.md | 150-350 lignes | 500 lignes |
| Fichier reference | < 200 lignes | 300 lignes (avec TdM) |

Si > 500 lignes → deplacer dans references/.

## 5. Pattern Structure SKILL.md

```markdown
---
name: [kebab-case]
description: [front-loadee, < 250 chars, mots-cles declencheurs]
---

# [Nom du Skill]

## Identite (optionnel)
Tu es [role]. Tu [capacite principale].

## References disponibles (si applicable)
| Fichier | Quand le lire |
|---------|---------------|

## Agents disponibles (si applicable)
| Agent | Quand l'utiliser |
|-------|------------------|

## Etape 1 — [Action]
[Instructions imperatives]
[Pourquoi si regle importante]

## Etape 2 — [Action]
[Instructions]

## Etape 3 — [Action]
[Instructions + exemples output]

## Regles
- [Regle 1]
- [Regle 2]
```

## 6. Description — Checklist

- [ ] Front-loader le cas d'usage principal (premiers 50 chars)
- [ ] Lister les contextes de declenchement
- [ ] Inclure 3-5 mots-cles naturels
- [ ] < 250 chars utiles
- [ ] Ton proactif sur le declenchement

## 7. Exemples dans le Corps

Toujours inclure 2-3 exemples d'output attendu :

```markdown
## Etape 3 — Formater la sortie

Genere un email avec cette structure :

**Exemple** :
Objet : [Prenom], decouvrez comment [benefice] avec l'IA
Corps : [2-3 phrases personnalisees selon le personae]
CTA : [lien vers contenu]
```

## 8. References a la Demande

```markdown
## References disponibles
Ce skill dispose de fichiers dans references/ — charge-les a la demande :

| Fichier | Quand le lire |
|---------|---------------|
| references/templates.md | Quand tu generes du HTML |
| references/personae.md | Pour adapter le ton au personae |
```

Claude charge le fichier UNIQUEMENT quand c'est pertinent. Pas en memoire par defaut.
