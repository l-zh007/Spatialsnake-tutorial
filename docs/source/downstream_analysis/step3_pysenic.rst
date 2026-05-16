Module 2: Regulatory Network Inference (pysenic)
================================================

``pysenic`` infers transcription factor regulatory networks (regulons) from the expression matrix and calculates regulon activity for each cell or spot using AUCell.
In addition to the standard heatmap-style outputs, Spatialsnake generates dot plots, violin plots, and activity tables to make the results easier to interpret and reproduce.
Because pySCENIC is computationally intensive, we use a previously prepared subset of ``Colon_Cancer_P1`` for demonstration. If you want to analyze another cell population of interest, first create a subset as described in :doc:`../useful_tool/splitting`.

To reduce runtime and memory usage, it is often practical to begin with relatively small subsets.
For example, the combined ``Smooth_Muscle_Cells`` and ``Endothelial_Cells`` subset contains 44,396 cells and 15,450 genes, and required roughly 4 hours with 64 CPU cores in our test setting. Please make sure that your available memory is sufficient.

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr  --split_by celltype --barcodes Smooth_Muscle_Cells,Endothelial_Cells

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

Recommended ``sample.txt`` format:

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/useful_tool/celltype_selected_Smooth_Muscle_Cells_Endothelial_Cells.zarr

Key input requirements:

1. ``input_path`` must contain a valid expression matrix. Keeping a ``celltype`` column in the object is strongly recommended for downstream interpretation.
2. Before running pySCENIC, prepare three classes of official resources: ``tfs_input`` (TF list), ``feather_input`` (cisTarget rankings database), and ``motifs_input`` (motif-to-TF annotation table).
3. All three resources must use the same species and compatible versioning, preferably v10, to avoid mismatches that can drastically reduce the number of recovered regulons.

Official resource links (human and mouse)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``tfs_input`` (TF list)

   - Human（hg38）：
     `allTFs_hg38.txt <https://resources.aertslab.org/cistarget/tf_lists/allTFs_hg38.txt>`_
   - Mouse（mm）：
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



Optional configuration
----------------------

First generate the template:

.. code-block:: bash

   spatialsnake produce-file --option=advance_analysis


.. code-block:: yaml

   senic_input: ""    # provided through sample.txt
   sample_type: "Colon_Cancer_P2" # sample name
   tfs_input: "data/hs_hgnc_tfs.txt"
   feather_input: "data/hg38_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather"
   motifs_input: "data/motifs-v10nr_clust-nr.hgnc-m0.001-o0.0.tbl"
   senic_workers: 64 # adjust according to the available CPU cores
   gene_attr: "var_names"  # this works for data prepared with the Spatialsnake tutorial workflow
   cell_attr: "cell_id"    # change only if your object uses another cell ID column

在我们的github仓库中,您可以在 ``resource`` 目录下找到必要的资源文件,我们提供了human和 mouse部分资源文件以节省您的下载时间.


Run the command
---------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=pysenic --configfile advance_analysis.yaml

Result file structure
---------------------

The main outputs are written to ``results/pysenic_results/``:

.. code-block:: text

   results/
   └── pysenic_results/
       ├── {sample}.loom
       ├── {sample}.grn.tsv
       ├── {sample}.regulons.csv
       ├── {sample}.aucell.loom
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

1. Regulon activity heatmaps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_auc_heatmap.png
   :width: 85%
   :align: center
   :alt: pysenic auc heatmap

Interpretation:
``*_auc_heatmap.png`` displays the major regulon activity patterns based on the AUC matrix.
``*_zscore_heatmap.png`` is generated from the Z-score matrix calculated on cell-type means and is often more useful for identifying relatively cell-type-specific regulatory programs.

2. Regulon activity dot plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_dotplot_regulons.png
   :width: 85%
   :align: center
   :alt: pysenic dotplot

Interpretation:
Dot size represents the mean regulon activity within each cell group, while color intensity reflects the relative activity level. This figure is especially useful for rapidly comparing the dominant regulatory programs across cell types.

3. Activity distribution violin plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_violin_regulons.png
   :width: 85%
   :align: center
   :alt: pysenic violin regulons

Interpretation:
``*_violin_regulons.png`` shows the distributions of the top 12 regulons, whereas ``*_stacked_violin.png`` shows the top 20 regulons ranked by activity. These plots help you assess intra-group variability, skewness, and heterogeneity.

4. Cell-type specificity plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_rss.png
   :width: 85%
   :align: center
   :alt: pysenic rss

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
