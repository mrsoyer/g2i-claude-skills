#!/usr/bin/env python3
"""Audit qualite d'un dossier de documentation.

Verifie la structure, le format, les sources et la taille des fichiers.

Usage:
    python doc-audit.py <chemin-dossier-doc>
    python doc-audit.py docs/supabase-rls/

Exit codes:
    0 = doc OK (score >= 70%)
    1 = doc avec problemes (score < 70%)
    2 = erreur d'utilisation
"""

import os
import re
import sys


def count_lines(filepath):
    """Compte les lignes d'un fichier."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return len(f.readlines())
    except (IOError, OSError):
        return 0


def read_file(filepath):
    """Lit le contenu d'un fichier."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except (IOError, OSError):
        return ""


def audit(doc_path):
    """Audite un dossier de documentation."""
    doc_path = os.path.expanduser(doc_path)
    results = {"checks": [], "score": 0, "max_score": 20}

    # Lister tous les fichiers .md
    md_files = []
    for f in sorted(os.listdir(doc_path)):
        if f.endswith(".md") and os.path.isfile(os.path.join(doc_path, f)):
            md_files.append(f)

    mdc_files = [
        f
        for f in os.listdir(doc_path)
        if f.endswith(".mdc") and os.path.isfile(os.path.join(doc_path, f))
    ]

    # Check 1: _index.md existe (3 pts)
    has_index = "_index.md" in md_files
    if has_index:
        results["score"] += 3
        results["checks"].append(("V", "_index.md existe", 3))
    else:
        results["checks"].append(("X", "_index.md MANQUANT", 0))

    # Check 2: Chaque fichier < 300 lignes (2 pts)
    all_under_300 = True
    over_300 = []
    for f in md_files:
        lines = count_lines(os.path.join(doc_path, f))
        if lines > 300:
            all_under_300 = False
            over_300.append(f"{f} ({lines} lignes)")
    if all_under_300:
        results["score"] += 2
        results["checks"].append(("V", f"Tous les fichiers < 300 lignes ({len(md_files)} fichiers)", 2))
    else:
        results["checks"].append(("X", f"Fichiers > 300 lignes : {', '.join(over_300)}", 0))

    # Check 3: TdM si > 100 lignes (1 pt)
    needs_toc = []
    has_toc_issue = False
    for f in md_files:
        filepath = os.path.join(doc_path, f)
        lines = count_lines(filepath)
        if lines > 100:
            content = read_file(filepath)
            has_toc = (
                "Table des Matieres" in content
                or "## Table" in content
                or content.count("\n## ") >= 3
            )
            if not has_toc:
                has_toc_issue = True
                needs_toc.append(f)
    if not has_toc_issue:
        results["score"] += 1
        results["checks"].append(("V", "TdM presente si > 100 lignes", 1))
    else:
        results["checks"].append(("!", f"TdM manquante : {', '.join(needs_toc)}", 0))

    # Check 4: Sources citees (3 pts)
    files_without_sources = []
    for f in md_files:
        if f in ("_index.md", "sources.md"):
            continue
        content = read_file(os.path.join(doc_path, f))
        has_sources = (
            "## Sources" in content
            or "## Source" in content
            or "](http" in content
        )
        if not has_sources:
            files_without_sources.append(f)
    if not files_without_sources:
        results["score"] += 3
        results["checks"].append(("V", "Sources citees dans tous les fichiers", 3))
    elif len(files_without_sources) <= 1:
        results["score"] += 1
        results["checks"].append(("!", f"Sources manquantes : {', '.join(files_without_sources)}", 1))
    else:
        results["checks"].append(("X", f"Sources manquantes : {', '.join(files_without_sources)}", 0))

    # Check 5: Exemples code (2 pts)
    files_with_code = 0
    for f in md_files:
        if f == "_index.md":
            continue
        content = read_file(os.path.join(doc_path, f))
        if "```" in content:
            files_with_code += 1
    content_files = len([f for f in md_files if f != "_index.md"])
    if content_files > 0 and files_with_code / content_files >= 0.5:
        results["score"] += 2
        results["checks"].append(("V", f"Exemples code dans {files_with_code}/{content_files} fichiers", 2))
    elif files_with_code > 0:
        results["score"] += 1
        results["checks"].append(("!", f"Exemples code dans {files_with_code}/{content_files} fichiers (< 50%)", 1))
    else:
        results["checks"].append(("X", "Aucun exemple de code", 0))

    # Check 6: Pas de contenu vague (2 pts)
    vague_patterns = [
        r"fais? bien",
        r"de mani[eè]re? appropriee?",
        r"comme il faut",
        r"correctement",
    ]
    vague_found = []
    for f in md_files:
        content = read_file(os.path.join(doc_path, f)).lower()
        for pattern in vague_patterns:
            if re.search(pattern, content):
                vague_found.append(f)
                break
    if not vague_found:
        results["score"] += 2
        results["checks"].append(("V", "Pas de contenu vague detecte", 2))
    else:
        results["checks"].append(("!", f"Contenu vague dans : {', '.join(vague_found)}", 0))

    # Check 7: Emplacement correct (3 pts)
    abs_path = os.path.abspath(doc_path)
    in_docs = "/docs/" in abs_path or abs_path.endswith("/docs")
    in_rules = "/.claude/rules/" in abs_path or "/.cursor/rules/" in abs_path
    in_skill_refs = "/references/" in abs_path and "/skills/" in abs_path
    if in_docs or in_skill_refs:
        results["score"] += 3
        results["checks"].append(("V", f"Emplacement correct : {abs_path}", 3))
    elif in_rules:
        results["checks"].append(("X", "MAUVAIS emplacement (.claude/rules/ ou .cursor/rules/) → deplacer vers docs/", 0))
    else:
        results["score"] += 1
        results["checks"].append(("!", f"Emplacement non-standard : {abs_path}", 1))

    # Check 8: Format .md (1 pt)
    if not mdc_files:
        results["score"] += 1
        results["checks"].append(("V", "Format .md standard (pas de .mdc)", 1))
    else:
        results["checks"].append(("X", f"Fichiers .mdc detectes : {', '.join(mdc_files)} → renommer en .md", 0))

    # Check 9: Naming XX-kebab-case.md (1 pt)
    bad_names = []
    for f in md_files:
        if f.startswith("_"):
            continue
        if not re.match(r"^\d{2}-[a-z0-9-]+\.md$", f) and f not in ("sources.md",):
            if not f.startswith("CDC-"):
                bad_names.append(f)
    if not bad_names:
        results["score"] += 1
        results["checks"].append(("V", "Naming XX-kebab-case.md respecte", 1))
    else:
        results["checks"].append(("!", f"Naming non-standard : {', '.join(bad_names)}", 0))

    # Check 10: Pas de fichiers vides (2 pts)
    empty_files = []
    for f in md_files:
        size = os.path.getsize(os.path.join(doc_path, f))
        if size < 10:
            empty_files.append(f)
    if not empty_files:
        results["score"] += 2
        results["checks"].append(("V", f"Aucun fichier vide ({len(md_files)} fichiers)", 2))
    else:
        results["checks"].append(("X", f"Fichiers vides : {', '.join(empty_files)}", 0))

    return results, md_files


def print_report(results, md_files, doc_path):
    """Affiche le rapport."""
    score = results["score"]
    max_score = results["max_score"]
    pct = (score / max_score * 100) if max_score > 0 else 0

    print()
    print("=" * 60)
    print(f"  Audit Documentation : {os.path.basename(doc_path.rstrip('/'))}")
    print(f"  Chemin : {os.path.abspath(doc_path)}")
    print("=" * 60)
    print()

    for status, msg, pts in results["checks"]:
        icon = {"V": "  V", "X": "  X", "!": "  !"}[status]
        print(f"{icon} [{pts}pt] {msg}")

    print()
    total_lines = sum(
        count_lines(os.path.join(doc_path, f)) for f in md_files
    )
    print(f"Fichiers : {len(md_files)} | Lignes total : {total_lines}")
    print(f"Score : {score}/{max_score} ({pct:.0f}%)")

    if pct >= 90:
        print("  -> Documentation professionnelle !")
    elif pct >= 70:
        print("  -> Bonne documentation, quelques ameliorations possibles")
    elif pct >= 50:
        print("  -> Fonctionnelle mais incomplete")
    else:
        print("  -> A retravailler")

    print()
    return 0 if pct >= 70 else 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python doc-audit.py <chemin-dossier-doc>")
        print("Exemple: python doc-audit.py docs/supabase-rls/")
        sys.exit(2)

    doc_path = os.path.expanduser(sys.argv[1])

    if not os.path.isdir(doc_path):
        print(f"Erreur: '{doc_path}' n'est pas un dossier valide")
        sys.exit(2)

    results, md_files = audit(doc_path)
    exit_code = print_report(results, md_files, doc_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
