Module 6: Regulatory Network Inference (pySCENIC)
=================================================

``pysenic`` runs pySCENIC to infer transcription-factor regulatory networks (regulons) from the expression matrix and calculate regulon activity for each cell or spot using AUCell.
In addition to the standard heatmap-style outputs, Spatialsnake generates dot plots, violin plots, and activity tables to make the results easier to interpret and reproduce.
The Demo follows CRC P2 manual annotation and selects vascular-associated
Smooth_Muscle_Cells and Endothelial_Cells. The current parent yields 52,165
observations. The completed Demo retains 209 regulons with at least 10 target
genes and writes a 52,165-by-209 AUC matrix.

For the configuration reference, see :doc:`../config_reference/advance_analysis_yaml`.

Workflow overview
-----------------

1. **Read the input object and convert formats**
   Load the spatial transcriptomics object (``.zarr`` or ``.h5ad``) and convert it to the ``.loom`` format required by pySCENIC.
2. **Infer the co-expression network with GRNBoost2**
   Use GRNBoost2 to infer candidate transcription factor-target co-expression relationships from the expression matrix.
3. **Filter candidate modules by motif enrichment with CisTarget**
   Evaluate the candidate target sets against TF-motif databases, remove unsupported interactions, and define high-confidence regulons.
4. **Score regulon activity with AUCell**
   Calculate an AUC activity score for each regulon in each cell or spot.
5. **Generate summary metrics and figures**
   Write the AUC matrix back into the object, compute Regulon Specificity Scores (RSS), derive Z-score summaries by cell type, and generate heatmaps, dot plots, and violin plots.

Prepare the input files
-----------------------

Demo: prepare the subset and sample table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Complete :doc:`../annotation/manual` first. Run from the project root:

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr --split_by=celltype --barcodes=Smooth_Muscle_Cells,Endothelial_Cells

Save :download:`pyscenic_sample.txt </config/demo_resources/pyscenic_sample.txt>`
in the project root, or copy:

.. code-block:: text

   sample_id input_path
   CRC_P2_vascular results/useful_results/data_splitting/celltype_selected_Smooth_Muscle_Cells_Endothelial_Cells.zarr

Command teaching: alternative inputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Single-cell ``.h5ad`` files can also be used directly:

.. code-block:: text

   sample_id   input_path
   sc_sample   data/sc_sample.h5ad

Key input requirements:

1. ``input_path`` must contain a valid expression matrix. Keeping a ``celltype`` column in the object is strongly recommended for downstream interpretation.
2. Before running pySCENIC, prepare three classes of official resources: ``tfs_input`` (TF list), ``feather_input`` (cisTarget rankings database), and ``motifs_input`` (motif-to-TF annotation table).
3. All three resources must use the same species and compatible versioning, preferably v10, to avoid mismatches that can drastically reduce the number of recovered regulons.
4. Gene identifiers in ``adata.var_names`` should match the selected TF list and motif annotation namespace, for example HGNC symbols for human or MGI symbols for mouse. Spatialsnake does not perform automatic ortholog conversion in this module.
5. The expression matrix should represent gene expression values for cells or spots. Avoid using PCA embeddings, batch-corrected latent spaces, or scaled residual matrices as the main expression matrix for pySCENIC.

Official resource links (human and mouse)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``tfs_input`` (TF list)

   - Human (hg38):
     `allTFs_hg38.txt <https://resources.aertslab.org/cistarget/tf_lists/allTFs_hg38.txt>`_
   - Mouse (mm):
     `allTFs_mm.txt <https://resources.aertslab.org/cistarget/tf_lists/allTFs_mm.txt>`_

2. ``motifs_input`` (motif-to-TF annotation table, v10 recommended)

   - Human (HGNC):
     `motifs-v10nr_clust-nr.hgnc-m0.001-o0.0.tbl <https://resources.aertslab.org/cistarget/motif2tf/motifs-v10nr_clust-nr.hgnc-m0.001-o0.0.tbl>`_
   - Mouse (MGI):
     `motifs-v10nr_clust-nr.mgi-m0.001-o0.0.tbl <https://resources.aertslab.org/cistarget/motif2tf/motifs-v10nr_clust-nr.mgi-m0.001-o0.0.tbl>`_

3. ``feather_input`` (cisTarget rankings databases; two gene-based rankings are recommended)

   - Human (hg38):
     `hg38_10kbp_up_10kbp_down_full_tx_v10_clust <https://resources.aertslab.org/cistarget/databases/homo_sapiens/hg38/refseq_r80/mc_v10_clust/gene_based/hg38_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather>`_
     `hg38_500bp_up_100bp_down_full_tx_v10_clust <https://resources.aertslab.org/cistarget/databases/homo_sapiens/hg38/refseq_r80/mc_v10_clust/gene_based/hg38_500bp_up_100bp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather>`_
   - Mouse (mm10):
     `mm10_10kbp_up_10kbp_down_full_tx_v10_clust <https://resources.aertslab.org/cistarget/databases/mus_musculus/mm10/refseq_r80/mc_v10_clust/gene_based/mm10_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather>`_
     `mm10_500bp_up_100bp_down_full_tx_v10_clust <https://resources.aertslab.org/cistarget/databases/mus_musculus/mm10/refseq_r80/mc_v10_clust/gene_based/mm10_500bp_up_100bp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather>`_

Multiple ranking databases can be supplied as a comma-separated string in ``advance_analysis.yaml``. This is useful when combining the broad promoter window and the proximal promoter database recommended by the pySCENIC/cisTarget workflow:

.. code-block:: yaml

   feather_input: "data/hg38_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather,data/hg38_500bp_up_100bp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather"



Demo: download databases and configure the run
----------------------------------------------

Save :download:`pyscenic_demo.yaml </config/demo_resources/pyscenic_demo.yaml>`
in the project root. The Demo uses one human v10 rankings database and matching
motif annotations; large databases are downloaded separately:

.. code-block:: bash

   mkdir -p data
   wget -c -P data https://resources.aertslab.org/cistarget/tf_lists/allTFs_hg38.txt
   wget -c -P data https://resources.aertslab.org/cistarget/motif2tf/motifs-v10nr_clust-nr.hgnc-m0.001-o0.0.tbl
   wget -c -P data https://resources.aertslab.org/cistarget/databases/homo_sapiens/hg38/refseq_r80/mc_v10_clust/gene_based/hg38_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather

.. literalinclude:: /config/demo_resources/pyscenic_demo.yaml
   :language: yaml

Important notes
---------------

``pysenic`` is implemented as a lightweight, single-cell-style regulon analysis module.
For spatial transcriptomics, the spatial scope is defined by the input object itself, such as a selected ROI, a splitting result, or a reannotated cell population.
This module does not build spatial neighborhoods or model ligand-receptor proximity; therefore, the output should be interpreted as regulon activity variation within the provided cells or spots.

For large spatial datasets, especially Visium HD, Xenium, or Stereo-seq objects, it is strongly recommended to run this module on a biologically meaningful subset.
During AUCell calculation, the expression matrix may need to be converted to a dense matrix; if the estimated dense matrix exceeds the internal memory threshold, the workflow stops with a clear message rather than silently exhausting memory.

The ``celltype_col`` field controls grouped summaries, including dot plots, violin plots, RSS, and cell-type mean AUC tables.
If this column is absent, Spatialsnake will try to use an available categorical observation column, but explicit annotation is preferred for reproducible interpretation.

``pyscenic_top_regulons`` only controls the number of regulons displayed in dotplot and violin-style figures; it does not remove regulons from the full AUC output table.
``pyscenic_min_regulon_genes`` controls the minimum number of target genes retained per regulon before AUCell scoring.
A value of ``10`` is a conservative default for avoiding very small, unstable regulons.

Use ``--threads`` to control the Snakemake thread allocation for GRNBoost2, ctx, and AUCell.
The historical ``senic_workers`` option is kept as a compatibility alias, but ``--threads`` is recommended for new analyses.


Run the command
---------------

.. code-block:: bash

   spatialsnake single_analysis pyscenic_sample.txt visium_HD --option=advance_analysis --runpipe=pysenic --configfile pyscenic_demo.yaml --threads 16 -j 16

Expected Demo outputs
---------------------

The main outputs are written to ``results/pysenic_results/``;
``{sample}`` is ``CRC_P2_vascular`` in this Demo:

.. code-block:: text

   results/
   └── pysenic_results/
       ├── {sample}.loom
       ├── {sample}.grn.tsv
       ├── {sample}.regulons.csv
       ├── {sample}.aucell.loom
       ├── {sample}.h5ad
       ├── {sample}_aucell.h5ad
       ├── {sample}.auc.csv
       ├── {sample}_regulon_genes.csv
       ├── {sample}_auc_mean_by_celltype.csv
       ├── {sample}_rss.csv
       ├── {sample}_rss_top10.csv
       ├── {sample}_dotplot_regulons.png
       ├── {sample}_violin_regulons.png
       ├── {sample}_auc_heatmap.png
       ├── {sample}_rss.png
       ├── {sample}_zscore_matrix.csv
       ├── {sample}_zscore_heatmap.png
       └── {sample}_stacked_violin.png

How to interpret the results
----------------------------

The images below are native outputs of the completed ``CRC_P2_vascular`` Demo.
Regulon counts and inferred relationships can vary between runs.

1. Regulon activity heatmaps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/CRC_P2_vascular_auc_heatmap.png
   :width: 85%
   :align: center
   :alt: pySCENIC regulon activity heatmap

Interpretation:
``*_auc_heatmap.png`` displays the major regulon activity patterns based on the AUC matrix.
``*_zscore_heatmap.png`` is generated from the Z-score matrix calculated on cell-type means and is often more useful for identifying relatively cell-type-specific regulatory programs.

2. Regulon activity dot plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/CRC_P2_vascular_dotplot_regulons.png
   :width: 85%
   :align: center
   :alt: pySCENIC regulon activity dot plot

Interpretation:
Dot size represents the fraction of observations with positive regulon activity;
color represents mean AUC scaled separately for each regulon across cell types.

3. Regulon z-score heatmap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/CRC_P2_vascular_zscore_heatmap.png
   :width: 85%
   :align: center
   :alt: pySCENIC regulon activity z-score heatmap


4. Cell-type specificity plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/CRC_P2_vascular_rss.png
   :width: 85%
   :align: center
   :alt: pySCENIC Regulon Specificity Score plot

Interpretation:
This plot is based on the Regulon Specificity Score (RSS). For each cell type, it highlights the most specific regulons and is therefore useful for defining cell states and prioritizing candidate master regulators.

5. Core result tables
~~~~~~~~~~~~~~~~~~~~~

Interpretation:
``*.auc.csv`` is the raw regulon activity matrix at single-cell or single-spot resolution.
``*_auc_mean_by_celltype.csv`` stores cell-type-level mean activity values.
``*_zscore_matrix.csv`` stores the standardized matrix that is typically used together with the Z-score heatmap to identify specific regulatory axes.

6. Specificity and network detail tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interpretation:
``*_rss.csv`` records regulon specificity scores for all cell types.
``*_rss_top10.csv`` summarizes the top 10 regulons for each cell type.
``*_regulon_genes.csv`` contains regulon-target gene relationships and is one of the most important tables for mechanistic interpretation and downstream experimental validation.
