# Galerie d'Exemples de Skills

## 1. Skill Simple — Objets d'Email Cold

```yaml
---
name: email-subject
description: >
  Genere des objets d'email accrocheurs pour le cold mailing.
  Declenche avec "objet email", "sujet email", "email subject".
argument-hint: "[personae] [theme]"
---

Genere 5 objets d'email pour du cold mailing.

Contexte :
- Personae cible : $0 (si fourni, sinon demander)
- Theme : $1 (si fourni, sinon demander)

Regles pour les objets :
- Max 50 caracteres (affichage mobile)
- Personnalise avec prenom si possible
- Curiosite > vente directe
- Pas de spam words (gratuit, urgent, offre)
- Mix : question, stat, benefice, teasing

Exemple output :
1. "[Prenom], votre prochain client vous attend ici"
2. "73% des agents immo ignorent cette technique IA"
3. "J'ai teste ca sur 200 prospects — resultats"
4. "[Prenom], une question rapide sur [ville]"
5. "Ce que vos concurrents utilisent depuis mars"
```

**Taille** : ~30 lignes | **Structure** : SKILL.md seul | **Complexite** : Simple

---

## 2. Skill Multi-Fonctions — Gestion Personae

```yaml
---
name: personae
description: >
  Gere les personae MyCommu : lister, creer, modifier, supprimer.
  Declenche avec "personae", "gere les personae", "liste personae",
  "nouveau personae", "modifie personae".
argument-hint: "[action] [nom-personae]"
allowed-tools: Read Write Edit Bash
---

# Gestion Personae

## /personae list (ou "liste personae")
Lis le fichier de config personae dans Supabase ou le fichier local.
Affiche un tableau : nom | description | ville | nb prospects | nb membres.

## /personae create [nom] (ou "nouveau personae")
Demande :
1. Nom du personae (ex: "agent-immo")
2. Description metier
3. Ville(s) cible(s)
4. Themes newsletter (ex: "immobilier + IA + ville")
5. Ton des emails (formel, decontracte, expert)

Cree l'entree dans la config.

## /personae edit [nom] (ou "modifie personae")
Charge le personae existant. Demande quel champ modifier.
Met a jour.

## /personae stats [nom] (ou "stats personae")
Affiche les stats du personae :
- Nb prospects
- Nb membres qualifies
- Taux de qualification
- Derniere newsletter envoyee
- Taux d'ouverture moyen
```

**Taille** : ~40 lignes | **Structure** : SKILL.md seul (multi-fonctions) | **Complexite** : Moyenne

---

## 3. Skill avec Scripts — Debounce

```yaml
---
name: debounce
description: >
  Verifie la validite d'une liste d'emails via les domaines OVH.
  Declenche avec "debounce", "verifie ces emails", "check emails".
argument-hint: "[fichier-ou-liste]"
disable-model-invocation: true
allowed-tools: Read Bash
---

# Debouncer

Verifie la validite d'emails en utilisant l'infra OVH.

## Etape 1 — Charger les emails
Si $ARGUMENTS est un fichier, lis-le (CSV, TXT, JSON).
Si c'est une liste, parse-la.
Affiche le nombre d'emails a verifier.

## Etape 2 — Verifier
Lance le script de verification :
```bash
python ${CLAUDE_SKILL_DIR}/scripts/check_emails.py $ARGUMENTS
```

## Etape 3 — Rapport
Affiche le rapport :
| Statut | Count |
|--------|-------|
| Valide | X |
| Invalide | X |
| Catch-all | X |
| Timeout | X |

Liste les emails invalides a retirer.
```

**Taille** : ~30 lignes | **Structure** : SKILL.md + scripts/ | **Complexite** : Moyenne

---

## 4. Skill avec Agents — Newsletter Generate

```yaml
---
name: newsletter-generate
description: >
  Genere une newsletter IA hebdomadaire ultra-nichee par personae et ville.
  Orchestre 3 agents (recherche buzz, tuto, use case).
  Declenche avec "newsletter", "genere newsletter [personae]".
argument-hint: "[personae] [ville]"
effort: high
allowed-tools: Read Write Bash WebSearch WebFetch
---

# Newsletter Generator

## References
| Fichier | Usage |
|---------|-------|
| references/personae-specs.md | Ton et themes par personae |
| references/template-html.md | Template HTML newsletter |

## Agents
| Agent | Mission |
|-------|---------|
| agents/researcher.md | 5 sujets IA buzz de la semaine |
| agents/tutorial-writer.md | 1 tutoriel IA pratique |
| agents/usecase-writer.md | 1 cas complet d'agent IA |

## Etape 1 — Identifier le contexte
Demande (si pas dans $ARGUMENTS) :
- Personae : $0
- Ville : $1 (optionnel)
Charge references/personae-specs.md pour le personae choisi.

## Etape 2 — Recherche (agent parallele)
Lance agents/researcher.md :
- Trouver 5 sujets IA buzz de la semaine
- Filtrer par pertinence pour le personae
- Output : titre + resume + source par sujet

## Etape 3 — Contenu (agents paralleles)
En parallele :
- agents/tutorial-writer.md : 1 tuto pratique
- agents/usecase-writer.md : 1 cas agent IA applique au metier

## Etape 4 — Assemblage
Charge references/template-html.md.
Assemble les resultats dans le template.
Adapte le ton au personae.

## Etape 5 — Livraison
Presente la newsletter pour review.
```

**Taille** : ~50 lignes | **Structure** : SKILL.md + agents/ + references/ | **Complexite** : Avancee

---

## 5. Skill Background Knowledge — Infra OVH

```yaml
---
name: ovh-infra-context
description: >
  Contexte de l'infrastructure cold email OVH de MyCommu.
  Charge automatiquement quand on parle de domaines, boites mail,
  reputation, envoi, ou infrastructure email.
user-invocable: false
---

# Infrastructure Cold Email — Contexte

## Architecture
- Domaines OVH a 2 EUR/piece avec hebergement gratuit + 5 boites mail
- OVH = seul hebergeur port 25 ouvert (crucial pour debounce)
- Chaque domaine = unite autonome (API PHP : shoot, debounce, unsub, stats)

## Limites
- 150 emails/jour max par domaine
- ~1000 verifications debounce/jour par domaine
- 5 boites mail par domaine

## Reputation
- Score calcule automatiquement par boite
- Volume ajuste selon reputation
- Objectif : 100-150 boites en rotation = 5000 cold emails/jour

## Warmup
- Inscription livres blancs / SaaS trials
- IA repond aux sales pour faire durer les conversations
- = warmup gratuit avec domaines reputes

## Qualification
- Prospect → Membre si : reponse positive OU clic lien OU 3 ouvertures
- Membre = inscrit newsletter
```

**Taille** : ~30 lignes | **Structure** : SKILL.md seul | **Complexite** : Simple (background)
