# ryr2-his123-conservation
# Conservation de His123 de RyR2

Script qui lit un alignement multiple (FASTA) et indique, pour chaque séquence,
le résidu situé à la colonne correspondant à la position 123 de RYR2 humain (UniProt Q92736).

## Utilisation
    pip install biopython
    python his123_conservation.py ryr2_aln.fasta

## Environnement
Python 3.13.2, Biopython 1.88

## Données
Séquences téléchargées depuis UniProt le 26 octobre 2026, alignées avec MAFFT (EMBL-EBI Job Dispatcher).
