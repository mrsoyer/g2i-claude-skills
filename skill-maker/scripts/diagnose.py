#!/usr/bin/env python3
"""Diagnostic de qualite pour un skill Cowork.

Analyse un dossier skill et genere un rapport de sante avec scoring.

Usage:
    python diagnose.py <chemin-du-skill>
    python diagnose.py ~/.claude/skills/mon-skill/

Exit codes:
    0 = skill OK (score >= 80%)
    1 = skill avec problemes (score < 80%)
    2 = erreur d'utilisation
"""

import os
import sys
import re


def read_file(path):
    """Lit un fichier et retourne son contenu."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (IOError, OSError):
        return None


def parse_frontmatter(content):
    """Extrait le frontmatter YAML du SKILL.md."""
    if not content or not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    fm_text = parts[1].strip()
    # Parse simple (sans dependance yaml)
    result = {}
    current_key = None
    current_value = []
    for line in fm_text.split("\n"):
        match = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if match:
            if current_key:
                result[current_key] = "\n".join(current_value).strip()
            current_key = match.group(1)
            current_value = [match.group(2)]
        elif current_key and (line.startswith("  ") or line.startswith("\t")):
            current_value.append(line.strip())
        elif current_key and line.strip() == "":
            current_value.append("")
    if current_key:
        result[current_key] = "\n".join(current_value).strip()
    return result


def count_caps_ratio(content):
    """Calcule le ratio de mots en FULL CAPS."""
    words = re.findall(r"\b[A-Za-z]+\b", content)
    if not words:
        return 0
    caps_words = [w for w in words if w.isupper() and len(w) > 2]
    return len(caps_words) / len(words)


def has_imperative(content):
    """Detecte la presence de verbes imperatifs francais/anglais."""
    imperative_patterns = [
        r"\b(Lis|Analyse|Genere|Cree|Envoie|Verifie|Affiche|Lance|Charge|Ecris)\b",
        r"\b(Read|Write|Create|Generate|Send|Check|Display|Launch|Load|Run)\b",
        r"\b(Identifie|Retourne|Propose|Demande|Formate|Compile|Extrais)\b",
    ]
    for pattern in imperative_patterns:
        if re.search(pattern, content):
            return True
    return False


def diagnose(skill_path):
    """Analyse un dossier skill et retourne le rapport."""
    results = {"errors": [], "warnings": [], "ok": [], "score": 0, "max_score": 0}

    skill_path = os.path.expanduser(skill_path)
    skill_name = os.path.basename(skill_path.rstrip("/"))

    # --- CRITIQUE (3 pts chaque) ---

    # C1: SKILL.md existe
    results["max_score"] += 3
    skill_md = os.path.join(skill_path, "SKILL.md")
    content = read_file(skill_md)
    if content:
        results["score"] += 3
        results["ok"].append("C1: SKILL.md present")
    else:
        results["errors"].append("C1: SKILL.md MANQUANT — fichier obligatoire")
        # Pas la peine de continuer
        return results, skill_name

    # C2: Frontmatter YAML valide
    results["max_score"] += 3
    fm = parse_frontmatter(content)
    if fm:
        results["score"] += 3
        results["ok"].append("C2: Frontmatter YAML valide")
    else:
        results["errors"].append("C2: Frontmatter YAML MANQUANT ou INVALIDE")
        fm = {}

    # C3: Champ name
    results["max_score"] += 3
    if fm.get("name"):
        name = fm["name"]
        if re.match(r"^[a-z0-9-]+$", name) and len(name) <= 64:
            results["score"] += 3
            results["ok"].append(f"C3: name = '{name}' (valide)")
        else:
            results["score"] += 1
            results["warnings"].append(
                f"C3: name = '{name}' — format non standard (kebab-case, max 64)"
            )
    else:
        results["warnings"].append("C3: Champ 'name' absent (utilisera nom dossier)")
        results["score"] += 1

    # C4: Champ description
    results["max_score"] += 3
    desc = fm.get("description", "")
    if desc:
        word_count = len(desc.split())
        char_count = len(desc)
        if word_count >= 20:
            results["score"] += 3
            info = f"C4: description = {word_count} mots, {char_count} chars"
            if char_count > 250:
                results["warnings"].append(
                    f"{info} — ATTENTION: > 250 chars (sera tronquee)"
                )
            else:
                results["ok"].append(info)
        else:
            results["score"] += 1
            results["warnings"].append(
                f"C4: description trop courte ({word_count} mots, recommande >= 20)"
            )
    else:
        results["errors"].append("C4: Champ 'description' MANQUANT")

    # C5: Corps non vide
    results["max_score"] += 3
    body = content.split("---", 2)[-1].strip() if "---" in content else content
    lines = body.split("\n")
    line_count = len([l for l in lines if l.strip()])
    if line_count > 10:
        results["score"] += 3
        results["ok"].append(f"C5: Corps = {line_count} lignes non-vides")
    elif line_count > 0:
        results["score"] += 1
        results["warnings"].append(
            f"C5: Corps court ({line_count} lignes, recommande > 10)"
        )
    else:
        results["errors"].append("C5: Corps VIDE")

    # C6: < 500 lignes
    results["max_score"] += 3
    total_lines = len(content.split("\n"))
    if total_lines <= 500:
        results["score"] += 3
        results["ok"].append(f"C6: {total_lines} lignes (< 500 OK)")
    else:
        results["score"] += 1
        results["warnings"].append(
            f"C6: {total_lines} lignes — depasse 500, deplacer dans references/"
        )

    # --- QUALITE (2 pts chaque) ---

    # Q1: Mode imperatif
    results["max_score"] += 2
    if has_imperative(body):
        results["score"] += 2
        results["ok"].append("Q1: Mode imperatif detecte")
    else:
        results["warnings"].append("Q1: Pas de verbes imperatifs detectes")

    # Q2: Pas de CAPS abusifs
    results["max_score"] += 2
    caps_ratio = count_caps_ratio(body)
    if caps_ratio < 0.05:
        results["score"] += 2
        results["ok"].append(f"Q2: CAPS ratio = {caps_ratio:.1%} (OK)")
    else:
        results["warnings"].append(
            f"Q2: CAPS ratio = {caps_ratio:.1%} — trop de majuscules"
        )

    # --- AVANCE (1 pt chaque) ---

    # Dossiers optionnels
    for folder in ["scripts", "references", "assets", "agents", "evals"]:
        folder_path = os.path.join(skill_path, folder)
        if os.path.isdir(folder_path):
            count = len(
                [f for f in os.listdir(folder_path) if not f.startswith(".")]
            )
            results["ok"].append(f"A: {folder}/ present ({count} fichier(s))")
            results["max_score"] += 1
            results["score"] += 1

    return results, skill_name


def print_report(results, skill_name):
    """Affiche le rapport formate."""
    score = results["score"]
    max_score = results["max_score"]
    pct = (score / max_score * 100) if max_score > 0 else 0

    print()
    print("=" * 60)
    print(f"  Diagnostic Skill : {skill_name}")
    print("=" * 60)
    print()

    if results["errors"]:
        print("ERREURS (a corriger) :")
        for e in results["errors"]:
            print(f"  X {e}")
        print()

    if results["warnings"]:
        print("AVERTISSEMENTS :")
        for w in results["warnings"]:
            print(f"  ! {w}")
        print()

    if results["ok"]:
        print("OK :")
        for o in results["ok"]:
            print(f"  V {o}")
        print()

    print(f"Score : {score}/{max_score} ({pct:.0f}%)")

    if pct == 100:
        print("  -> Skill en parfait etat !")
    elif pct >= 80:
        print("  -> Bon skill, quelques ameliorations possibles")
    elif pct >= 50:
        print("  -> Fonctionnel mais incomplet")
    else:
        print("  -> Problemes importants a corriger")

    print()
    return 0 if pct >= 80 else 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python diagnose.py <chemin-du-skill>")
        print("Exemple: python diagnose.py ~/.claude/skills/mon-skill/")
        sys.exit(2)

    skill_path = sys.argv[1]

    if not os.path.isdir(os.path.expanduser(skill_path)):
        print(f"Erreur: '{skill_path}' n'est pas un dossier valide")
        sys.exit(2)

    results, skill_name = diagnose(skill_path)
    exit_code = print_report(results, skill_name)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
