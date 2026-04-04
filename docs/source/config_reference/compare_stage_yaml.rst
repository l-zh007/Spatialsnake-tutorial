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
     - ``DEseq2``
     - Differential expression algorithm
   * - ``cell_focus``
     - ``CAF``
     - Cell type of interest
   * - ``species``
     - ``human``
     - Species background used for enrichment
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
2. When ``runpipe=cellchat``, first define the relevant source and target cell groups and the pathway set of interest.
3. If too many figures are being generated, temporarily disable selected ``cellchat_compare_do_*`` options for faster iteration.
