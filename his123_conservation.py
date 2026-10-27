#!/usr/bin/env python3
"""Conservation d'un résidu dans un alignement multiple (format FASTA).

Usage :
    python his123_conservation.py ryr2_aln.fasta
    python his123_conservation.py ryr2_aln.fasta --ref RYR2_HUMAN --pos 123 --aa H --flank 5
"""
import argparse
import csv
from Bio import AlignIO


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("alignment", help="alignement multiple au format FASTA")
    p.add_argument("--ref", default="RYR2_HUMAN", help="identifiant de la séquence de référence")
    p.add_argument("--pos", type=int, default=123, help="position du résidu dans la référence (sans gaps)")
    p.add_argument("--aa", default="H", help="résidu attendu à cette position")
    p.add_argument("--flank", type=int, default=5, help="nombre de résidus de part et d'autre")
    p.add_argument("--out", default="conservation.csv", help="fichier CSV de sortie")
    args = p.parse_args()

    aln = AlignIO.read(args.alignment, "fasta")
    ref = next(r for r in aln if r.id == args.ref)

    # colonne de l'alignement correspondant à la position de la référence (gaps ignorés)
    n, col = 0, None
    for i, aa in enumerate(ref.seq):
        if aa != "-":
            n += 1
            if n == args.pos:
                col = i
                break
    if col is None:
        raise SystemExit(f"La position {args.pos} n'existe pas dans {args.ref}")
    if ref.seq[col] != args.aa:
        raise SystemExit(f"{args.ref} a {ref.seq[col]} (et non {args.aa}) en position {args.pos}")

    print(f"Colonne de l'alignement : {col + 1}")
    rows, conserved = [], 0
    for r in aln:
        before = str(r.seq[max(0, col - args.flank):col])
        after = str(r.seq[col + 1:col + 1 + args.flank])
        aa = str(r.seq[col])
        conserved += aa == args.aa
        rows.append([r.id, before, aa, after])
        print(f"{r.id:15s} {before:>{args.flank}s} [{aa}] {after}")

    print(f"\nRésidu {args.aa} conservé : {conserved}/{len(aln)} séquences")

    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sequence", "avant", "residu", "apres"])
        w.writerows(rows)
    print(f"Résultats enregistrés dans {args.out}")


if __name__ == "__main__":
    main()
