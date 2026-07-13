compare_stage.yaml Reference
============================

This configuration file corresponds to ``--option=compare_stage`` and is used for differential expression comparison and two-sample CellChat network comparison.

.. list-table::
   :header-rows: 1
   :widths: 32 20 48

   * - Parameter
     - Default
     - Description
   * - ``option``
     - ``compare_stage``
     - Fixed stage identifier
   * - ``results_folder`` / ``data_fold`` / ``sample_list``
     - ``results`` / ``data`` / ``sample.txt``
     - Output directory, data directory, and sample list
   * - ``run_type`` / ``channel``
     - ``visium`` / ``compare_analysis``
     - Platform type and analysis channel
   * - ``runpipe``
     - ``compare_gene``
     - Comparison branch, either ``compare_gene`` or ``cellchat``
   * - ``compare_algorithm``
     - ``DESeq2``
     - Differential expression algorithm
   * - ``cell_focus``
     - ``CAF``
     - Cell type of interest; accepts one cell type, comma-separated cell types, or ``all``. Multiple cell types are modeled independently, not pooled.
   * - ``species``
     - ``human``
     - Species background used for enrichment
   * - ``compare_celltype_col``
     - ``celltype``
     - Cell type annotation column in the annotated zarr table
   * - ``compare_sample_col``
     - ``region``
     - Sample or biological replicate column in the annotated zarr table
   * - ``compare_condition_col``
     - ``group``
     - Backup condition column in the annotated zarr table; group labels from ``sample.txt`` are used first
   * - ``count_layer``
     - ``counts``
     - Raw count layer for pseudobulk aggregation
   * - ``min_replicates``
     - ``2``
     - Minimum biological replicates required per condition for formal DEG
   * - ``min_cells_per_sample``
     - ``30``
     - Minimum cells or spots required per sample within each selected cell type
   * - ``min_total_counts_per_gene``
     - ``10``
     - Low-expression gene filter after pseudobulk aggregation
   * - ``run_scanpy_reference``
     - ``True``
     - Whether to write exploratory Scanpy Wilcoxon rankings
   * - ``de_top_n``
     - ``30``
     - Number of top genes highlighted in DEG figures
   * - ``cellchat_compare_output_dir``
     - ``results/compare_cellchat``
     - Output directory for CellChat comparison results
   * - ``cellchat_compare_sample_name1`` / ``cellchat_compare_sample_name2``
     - ``group_Non_Lesional`` / ``group_Lesional``
     - Display names for the two groups
   * - ``cellchat_compare_pathways``
     - ``""``
     - Specific pathways to compare
   * - ``cellchat_compare_source_cells`` / ``cellchat_compare_target_cells``
     - ``1,2,3`` / ``1,2,3``
     - Sender and receiver cell selections
   * - ``cellchat_compare_receiver_cells``
     - ``1,2,3``
     - Receiver-cell setting for aggregate plots
   * - ``cellchat_compare_bubble_angle``
     - ``45``
     - Axis angle for bubble plots
   * - ``cellchat_compare_bubble_remove_isolate``
     - ``True``
     - Whether to remove isolated nodes
   * - ``cellchat_compare_do_ranknet`` / ``cellchat_compare_do_role_heatmap``
     - ``True`` / ``False``
     - Whether to output rankNet and role heatmap figures
   * - ``cellchat_compare_do_pathway_plots`` / ``cellchat_compare_do_compare_overview``
     - ``True`` / ``True``
     - Whether to output pathway summary and overview comparison plots
   * - ``cellchat_compare_do_compare_bubble`` / ``cellchat_compare_do_single_bubble``
     - ``True`` / ``True``
     - Whether to output paired-group and single-group bubble plots
   * - ``cellchat_compare_do_gene_expression``
     - ``False``
     - Whether to output ligand-receptor expression plots
   * - ``cellchat_compare_gene_colors``
     - ``white,#FEC44F,#D95F0E``
     - Color palette used for expression plots
   * - ``cellchat_compare_gene_plot_type``
     - ``dot``
     - Expression plot type
   * - ``cellchat_compare_save_merged``
     - ``True``
     - Whether to save the merged object

Tuning suggestions
------------------

1. When ``runpipe=compare_gene``, focus first on ``compare_algorithm`` and ``cell_focus``.
   ``region`` is interpreted as sample or biological replicate by default, while the group column from ``sample.txt`` is interpreted as condition.
   Formal DEG is skipped for a cell type if any condition has fewer than ``min_replicates`` retained samples.
2. When ``runpipe=cellchat``, first define the relevant source and target cell groups and the pathway set of interest.
3. If too many figures are being generated, temporarily disable selected ``cellchat_compare_do_*`` options for faster iteration.
