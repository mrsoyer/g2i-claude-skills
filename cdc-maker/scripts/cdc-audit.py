#!/usr/bin/env python3
"""Audit qualite d'un cahier des charges genere par cdc-maker.

Usage: python cdc-audit.py <chemin-dossier-cdc>
Score: /20 points
"""

import sys
import os
import re
import unicodedata
from pathlib import Path


def _norm(s: str) -> str:
    """Minuscule + sans accents (NFKD), pour un matching accent-insensible."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c)
    )


def _unsourced_numbers(content: str) -> list:
    """Heuristique : chiffres dimensionnants (k€/€/%/contacts/leads) sans date ISO
    ni tag 'a valider'/'mesure' a proximite (~90 car) = chiffres potentiellement fantomes."""
    norm = _norm(content)
    flags = []
    for m in re.finditer(r"[~≈]?\s*\d[\d  .,]*\s*(k€|€|%|contacts|leads)", content):
        a, b = max(0, m.start() - 90), min(len(content), m.end() + 90)
        ctx = _norm(content[a:b])
        if not re.search(r"20\d\d-\d\d-\d\d", content[a:b]) and "a valider" not in ctx and "mesure" not in ctx:
            flags.append(m.group(0).strip())
    return flags[:12]


def audit_cdc(cdc_path: str) -> dict:
    """Audite un dossier CDC et retourne le score."""
    path = Path(cdc_path)
    results = []
    total = 0

    # 1. _index.md existe (3 pts)
    index_file = path / "_index.md"
    if index_file.exists():
        content = index_file.read_text()
        has_links = content.count("[") >= 3
        has_resume = ">" in content[:500]  # blockquote = resume executif
        if has_links and has_resume:
            results.append(("_index.md avec resume + liens", 3, 3))
            total += 3
        elif has_links:
            results.append(("_index.md avec liens (pas de resume)", 2, 3))
            total += 2
        else:
            results.append(("_index.md existe mais incomplet", 1, 3))
            total += 1
    else:
        results.append(("_index.md MANQUANT", 0, 3))

    # 2. Stack detecte et documente (2 pts)
    all_content = ""
    md_files = list(path.rglob("*.md"))
    for f in md_files:
        all_content += f.read_text()
    norm_content = _norm(all_content)

    stack_keywords = ["stack", "technologie", "frontend", "backend", "database", "db"]
    stack_found = sum(1 for kw in stack_keywords if _norm(kw) in norm_content)
    if stack_found >= 3:
        results.append(("Stack documente", 2, 2))
        total += 2
    elif stack_found >= 1:
        results.append(("Stack partiellement documente", 1, 2))
        total += 1
    else:
        results.append(("Stack NON documente", 0, 2))

    # 3. Taches avec executeur (3 pts)
    executeur_keywords = ["executeur", "agent", "skill", "claude code", "schedule", "planifi"]
    executeur_count = sum(1 for kw in executeur_keywords if _norm(kw) in norm_content)
    if executeur_count >= 3:
        results.append(("Taches avec executeurs assignes", 3, 3))
        total += 3
    elif executeur_count >= 1:
        results.append(("Executeurs partiellement assignes", 1, 3))
        total += 1
    else:
        results.append(("Executeurs NON assignes", 0, 3))

    # 4. Livrables verifiables (3 pts)
    livrable_keywords = ["livrable", "verifi", "test", "fonctionne", "valide", "checklist"]
    livrable_count = sum(1 for kw in livrable_keywords if _norm(kw) in norm_content)
    if livrable_count >= 3:
        results.append(("Livrables verifiables presents", 3, 3))
        total += 3
    elif livrable_count >= 1:
        results.append(("Livrables partiellement definis", 1, 3))
        total += 1
    else:
        results.append(("Livrables NON definis", 0, 3))

    # 5. Dependances documentees (2 pts)
    dep_keywords = ["dependance", "depend", "dep.", "prerequis", "wave", "apres", "avant"]
    dep_count = sum(1 for kw in dep_keywords if _norm(kw) in norm_content)
    if dep_count >= 3:
        results.append(("Dependances documentees", 2, 2))
        total += 2
    elif dep_count >= 1:
        results.append(("Dependances partiellement documentees", 1, 2))
        total += 1
    else:
        results.append(("Dependances NON documentees", 0, 2))

    # 6. Waves/parallelisme (2 pts)
    wave_keywords = ["wave", "parallele", "parallel", "simultane"]
    wave_count = sum(1 for kw in wave_keywords if _norm(kw) in norm_content)
    if wave_count >= 2:
        results.append(("Waves parallelisables identifiees", 2, 2))
        total += 2
    elif wave_count >= 1:
        results.append(("Parallelisme mentionne", 1, 2))
        total += 1
    else:
        results.append(("Parallelisme NON identifie", 0, 2))

    # 7. KPIs mesurables (2 pts)
    kpi_keywords = ["kpi", "metrique", "mesur", "objectif", "cible", "seuil", "taux"]
    kpi_count = sum(1 for kw in kpi_keywords if _norm(kw) in norm_content)
    if kpi_count >= 3:
        results.append(("KPIs mesurables", 2, 2))
        total += 2
    elif kpi_count >= 1:
        results.append(("KPIs partiellement definis", 1, 2))
        total += 1
    else:
        results.append(("KPIs NON definis", 0, 2))

    # 8. Fichiers < 300 lignes (1 pt)
    over_300 = []
    for f in md_files:
        line_count = len(f.read_text().splitlines())
        if line_count > 300:
            over_300.append(f"{f.name} ({line_count} lignes)")
    if not over_300:
        results.append(("Tous fichiers < 300 lignes", 1, 1))
        total += 1
    else:
        results.append((f"Fichiers > 300 lignes: {', '.join(over_300)}", 0, 1))

    # 9. Sources/docs referencees (2 pts)
    ref_keywords = ["source", "reference", "voir", "claude.md", "docs/"]
    ref_count = sum(1 for kw in ref_keywords if _norm(kw) in norm_content)
    if ref_count >= 3:
        results.append(("Sources/docs referencees", 2, 2))
        total += 2
    elif ref_count >= 1:
        results.append(("References partielles", 1, 2))
        total += 1
    else:
        results.append(("Aucune reference", 0, 2))

    return {
        "results": results,
        "total": total,
        "max": 20,
        "files": len(md_files),
        "total_lines": sum(len(f.read_text().splitlines()) for f in md_files),
        "unsourced": _unsourced_numbers(all_content),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python cdc-audit.py <chemin-dossier-cdc>")
        sys.exit(1)

    cdc_path = sys.argv[1]
    if not os.path.isdir(cdc_path):
        print(f"Erreur: {cdc_path} n'est pas un dossier")
        sys.exit(1)

    audit = audit_cdc(cdc_path)

    # Affichage
    print(f"\n{'='*50}")
    print(f"  AUDIT CDC : {cdc_path}")
    print(f"{'='*50}\n")

    for label, score, max_score in audit["results"]:
        status = "OK" if score == max_score else ("PARTIEL" if score > 0 else "MANQUE")
        print(f"  [{status:>7}] {label} ({score}/{max_score})")

    print(f"\n{'─'*50}")
    print(f"  Score : {audit['total']}/{audit['max']}")
    print(f"  Fichiers : {audit['files']}")
    print(f"  Lignes total : {audit['total_lines']}")

    level = "Professionnel" if audit["total"] >= 18 else \
            "Bon" if audit["total"] >= 14 else \
            "Incomplet" if audit["total"] >= 10 else "A retravailler"
    print(f"  Niveau : {level}")

    if audit["unsourced"]:
        print(f"\n  ⚠ Chiffres dimensionnants SANS date ni 'a valider' (verifier — fantomes ?) :")
        for n in audit["unsourced"]:
            print(f"      · {n}")
        print(f"  (le score keyword est INDICATIF, pas un gate de veracite — cf SKILL.md Etape 6)")
    print(f"{'='*50}\n")

    sys.exit(0 if audit["total"] >= 14 else 1)


if __name__ == "__main__":
    main()
