#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/MTAB
for id in 5705STDY805828{0..5}; do
  wget -c -P data/MTAB "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/115/E-MTAB-11115/Files/${id}_filtered_feature_bc_matrix.h5"
done
wget -c -P data/MTAB "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/115/E-MTAB-11115/Files/cell_annotation.csv"
