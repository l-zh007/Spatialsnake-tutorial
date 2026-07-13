Module 7: Differential Expression Comparison (compare_stage)
============================================================

In multi-sample spatial transcriptomics studies, robust gene differential expression analysis should be performed at the biological replicate level.
The ``compare_stage`` gene branch therefore uses a **cell-type-specific pseudobulk workflow**: within each selected cell type, raw counts are summed per sample, and group differences are modeled using the sample-level condition labels from ``sample.txt``.

In this section, we continue with the integrated and annotated mouse brain example from :doc:`../integration_analysis/multi_sample_integration`.

For the configuration reference, see :doc:`../config_reference/compare_stage_yaml`.

What does this module do?
-------------------------

1. **Compare biological groups defined in ``sample.txt``**
   The workflow treats ``region`` in the integrated zarr as the sample or biological replicate identifier, and uses the final group column from ``sample.txt`` as the experimental condition.
2. **Analyze one, multiple, or all cell types**
   ``cell_focus="CAF"`` analyzes one cell type. ``cell_focus="CAF,T_cell,Macrophage"`` analyzes each listed cell type independently. ``cell_focus="all"`` analyzes every eligible cell type.
3. **Run replicate-aware formal DEG**
   ``DESeq2`` uses PyDESeq2 with raw pseudobulk counts and ``design="~condition"``. ``edgeR`` uses raw pseudobulk counts, ``filterByExpr``, TMM normalization, dispersion estimation, ``glmQLFit``, and ``glmQLFTest``.
4. **Write exploratory Scanpy output separately**
   Optional Scanpy Wilcoxon rankings are saved under ``exploratory_scanpy/`` and are labeled as cell-level exploratory results, not replicate-aware formal DEG.
5. **Generate publication-ready summaries and enrichment results**
   The workflow exports pseudobulk QC plots, volcano plots, MA plots, top DEG heatmaps, cross-celltype DEG summaries, GO/KEGG ORA, and ranked GSEA outputs in both PNG and PDF formats.

Important statistical note:
Multiple selected cell types are **not pooled** by default. Each cell type is modeled independently because cell types differ in expression profile, sequencing depth, cell abundance, and dispersion. Pooling multiple cell types without an explicit biological compartment definition would confound gene-level changes with cell composition changes.

Prepare the input files
-----------------------

``compare_stage`` is best run with the same sample table used in ``compare_analysis``. The last group column should contain the **true biological group name**.

.. code-block:: text

   sample_id   input_path       group
   ST8059048  data/ST8059048   Control
   ST8059049  data/ST8059049   Control
   ST8059050  data/ST8059050   Disease
   ST8059051  data/ST8059051   Disease

Input requirements:

1. Before entering this step, complete ``annotation`` under ``compare_analysis`` so that ``results/merge_data/annotation/concatenated_sdata.zarr`` exists.
2. ``region`` in the zarr table must represent the sample or biological replicate id.
3. The sample ids in ``sample.txt`` must match the values stored in ``obs['region']``.
4. Each condition needs at least ``min_replicates`` biological replicates after cell-type filtering. The default is ``2``.
5. Formal DEG requires raw counts, preferably in ``adata.layers['counts']``. If this layer is absent, Spatialsnake tries ``raw_counts``, ``adata.raw.X``, or integer-like ``adata.X``.

Common parameters
-----------------

.. list-table::
   :header-rows: 1
   :widths: 26 24 50

   * - Parameter
     - Typical values
     - Description
   * - ``runpipe``
     - ``compare_gene``
     - Selects the differential expression comparison branch
   * - ``compare_algorithm``
     - ``DESeq2`` / ``edgeR``
     - Formal replicate-aware pseudobulk algorithm
   * - ``cell_focus``
     - ``CAF`` / ``CAF,T_cell`` / ``all``
     - Cell types to analyze independently
   * - ``compare_sample_col``
     - ``region``
     - Sample or biological replicate column in ``obs``
   * - ``compare_condition_col``
     - ``group``
     - Backup condition column in ``obs``; ``sample.txt`` group labels are used first
   * - ``compare_celltype_col``
     - ``celltype``
     - Cell type annotation column in ``obs``
   * - ``count_layer``
     - ``counts``
     - Raw count layer name
   * - ``min_replicates``
     - ``2``
     - Minimum biological replicates per condition
   * - ``min_cells_per_sample``
     - ``30``
     - Minimum cells or spots per sample within each cell type
   * - ``min_total_counts_per_gene``
     - ``10``
     - Low-expression gene filter after pseudobulk aggregation
   * - ``run_scanpy_reference``
     - ``True`` / ``False``
     - Whether to export exploratory cell-level Scanpy Wilcoxon rankings
   * - ``species``
     - ``human`` / ``mouse``
     - Species background used for GO/KEGG/GSEA

Example configuration:

.. code-block:: yaml

   compare_algorithm: "DESeq2"
   cell_focus: "CAF,T_cell,Macrophage"
   compare_sample_col: "region"
   compare_condition_col: "group"
   compare_celltype_col: "celltype"
   count_layer: "counts"
   min_replicates: 2
   min_cells_per_sample: 30
   min_total_counts_per_gene: 10
   run_scanpy_reference: True
   de_top_n: 30
   species: "human"
   cut_off_pvalue: 0.05
   cut_off_logFC: 1.5

Run the workflow
----------------

Analyze one cell type:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=compare_gene --cell_focus=CAF

Analyze multiple cell types independently:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=compare_gene --cell_focus=CAF,T_cell,Macrophage

Analyze all eligible cell types:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=compare_gene --cell_focus=all

Use edgeR instead of DESeq2:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=compare_gene --compare_algorithm=edgeR --cell_focus=all

Result file structure
---------------------

The workflow writes both machine-readable tables and ready-to-inspect figures.

.. code-block:: text

   results/
   └── merge_data/
       └── compare_analysis/
           ├── marker_genes_pval.csv              # DESeq2 combined result, if compare_algorithm=DESeq2
           ├── edgeR_counts.csv                   # edgeR manifest, if compare_algorithm=edgeR
           ├── edgeR_results.csv                  # edgeR combined formal DEG result
           ├── deg_manifest.csv
           ├── celltype_summary.csv
           ├── DEG_summary_by_celltype.csv
           ├── DEG_summary_by_celltype.png/.pdf
           ├── DEG_count_heatmap.png/.pdf
           ├── shared_deg_matrix.csv
           ├── shared_deg_matrix.png/.pdf
           ├── celltype_pathway_summary.csv
           ├── celltype_pathway_dotplot.png/.pdf
           ├── pseudobulk/
           │   └── {celltype}/
           │       ├── counts.csv
           │       ├── counts_all_samples.csv
           │       ├── metadata.csv
           │       ├── qc_metrics.csv
           │       └── method_summary.txt
           ├── qc/
           │   └── {celltype}/
           │       ├── n_cells.png/.pdf
           │       ├── library_size.png/.pdf
           │       ├── detected_genes.png/.pdf
           │       ├── pseudobulk_pca.png/.pdf
           │       └── sample_correlation.png/.pdf
           ├── DEG/
           │   └── {DESeq2|edgeR}/
           │       └── {celltype}/
           │           └── {groupA}_vs_{groupB}/
           │               ├── deg_all.csv
           │               └── deg_significant.csv
           ├── figures/
           │   └── {celltype}/
           │       └── {groupA}_vs_{groupB}/
           │           ├── diff_all.csv
           │           ├── deg_significant.csv
           │           ├── volcano.png/.pdf
           │           ├── top_deg_barplot.png/.pdf
           │           ├── log2fc_density.png/.pdf
           │           ├── ma_plot.png/.pdf
           │           ├── top_deg_heatmap.png/.pdf
           │           └── enrichment/
           │               ├── up/GO_data.csv, kegg_data.csv, GO_enrich.png/.pdf, KEGG_enrich.png/.pdf
           │               ├── down/GO_data.csv, kegg_data.csv, GO_enrich.png/.pdf, KEGG_enrich.png/.pdf
           │               └── all_ranked/GSEA_GO_data.csv, GSEA_KEGG_data.csv, GSEA_GO_plot.png/.pdf, GSEA_KEGG_plot.png/.pdf
           ├── exploratory_scanpy/
           │   └── {celltype}/
           │       └── {group}_scanpy_wilcoxon.csv
           └── positive/kegg_data.csv             # Snakemake completion marker retained for compatibility

How to interpret the results
----------------------------

1. Start with ``pseudobulk/qc_metrics.csv`` and the ``qc/`` plots. Confirm that every condition has enough samples and that library sizes are not dominated by a single outlier sample.
2. Use ``DEG_summary_by_celltype.png`` and ``DEG_count_heatmap.png`` to identify which cell types show the strongest transcriptional changes.
3. For a specific cell type and contrast, inspect ``volcano.png``, ``ma_plot.png``, and ``top_deg_heatmap.png`` together. A reliable candidate gene should have a meaningful effect size, a stable adjusted p-value, and coherent pseudobulk expression across replicate samples.
4. Use ``enrichment/up`` and ``enrichment/down`` to interpret direction-specific biological programs. Use ``enrichment/all_ranked`` for GSEA-style ranked pathway exploration.
5. Treat ``exploratory_scanpy/`` as a reference marker ranking only. It does not replace the formal pseudobulk DEG because it does not model biological replicates.
