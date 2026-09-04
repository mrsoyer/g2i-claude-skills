# Skills Claude pour Garcia Ingénierie

Trois « skills » (fiches de méthode que Claude suit tout seul) utilisés pendant l'atelier IA + Claude Cowork.
Ils fonctionnent dans **Claude Cowork** (application Claude sur Mac ou Windows) et dans **Claude Code**.

| Skill | À quoi ça sert | Comment on l'appelle |
|-------|----------------|----------------------|
| `doc-maker` | Cherche sur le web et écrit une documentation de référence propre dans un dossier `docs/` | `/doc-maker [sujet]` |
| `cdc-maker` | Transforme un besoin en cahier des charges : tâches, dépendances, qui fait quoi | `/cdc-maker [projet ou fonctionnalité]` |
| `skill-maker` | Crée un nouveau skill à partir d'une procédure que vous répétez | `/skill-maker [description du skill]` |

La méthode vue en atelier : **documenter** (`/doc-maker`) → **cadrer** (`/cdc-maker`) → **exécuter** (Cowork) → **capitaliser** (`/skill-maker`) → **planifier** (tâche planifiée).

## Installation dans Claude Cowork (sans rien coder)

1. Téléchargez le fichier `.zip` du skill voulu dans le dossier [`dist/`](dist/) : [doc-maker.zip](dist/doc-maker.zip), [cdc-maker.zip](dist/cdc-maker.zip), [skill-maker.zip](dist/skill-maker.zip).
2. Ouvrez l'application Claude, puis **Paramètres** → **Fonctionnalités** (ou *Capabilities*) → **Skills**.
3. Cliquez sur **Ajouter un skill** et choisissez le fichier `.zip`.
4. Dans une tâche Cowork, tapez `/doc-maker` suivi de votre sujet. Le skill se déclenche aussi tout seul quand votre demande correspond à sa description.

Le libellé exact des menus peut changer selon la version de l'application. Si vous ne trouvez pas le menu Skills, demandez-le au formateur.

## Installation dans Claude Code (terminal)

```bash
git clone https://github.com/mrsoyer/g2i-claude-skills.git
mkdir -p ~/.claude/skills
cp -r g2i-claude-skills/doc-maker g2i-claude-skills/cdc-maker g2i-claude-skills/skill-maker ~/.claude/skills/
```

Puis dans Claude Code : `/doc-maker API BOAMP` par exemple.

Les scripts d'audit (`scripts/*.py`) demandent Python 3. Ils sont facultatifs : le skill fonctionne sans eux, il saute simplement l'étape de notation.

## Contenu de chaque skill

```
doc-maker/
├── SKILL.md              la fiche que Claude suit
├── references/           règles de format, d'organisation, de recherche
├── agents/               sous-rôles (chercheur, extracteur, synthétiseur, relecteur)
└── scripts/doc-audit.py  note la doc produite sur 20
```

Même structure pour `cdc-maker` (méthodologie, découpage des tâches, détection du stack) et `skill-maker` (règles de rédaction, anti-patterns, galerie d'exemples).

## Règle d'or

L'IA propose, vous décidez. Relisez ce que le skill produit avant de l'utiliser, surtout les chiffres et les références techniques.

---
Atelier IA + Claude Cowork · Garcia Ingénierie · septembre 2026
