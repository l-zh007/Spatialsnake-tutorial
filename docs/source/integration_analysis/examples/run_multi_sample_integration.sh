#!/usr/bin/env bash
set -euo pipefail

spatialsnake compare_analysis examples/sample_multi.txt visium --option=integrate
spatialsnake compare_analysis examples/sample_multi.txt visium --option=preprocess --batch_method=harmony
spatialsnake compare_analysis examples/sample_multi.txt visium --option=clustering --cluster_algorithm=leiden --resolution=0.6
spatialsnake compare_analysis examples/sample_multi.txt visium --option=annotation_help --markers_algorithm=wilcoxon
spatialsnake compare_analysis examples/sample_multi.txt visium --option=annotation --anno_algorithm=manual --annotation-file=examples/annotation_multi.txt
