advance_analysis.yaml Reference
===============================

This configuration file corresponds to ``--option=advance_analysis`` and covers six downstream modules: cellPhoneDB, pysenic, liana, cellchat, cellcharter, and banksy.

Global fields
-------------

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - Parameter
     - Default
     - Description
   * - ``option``
     - ``advance_analysis``
     - Fixed stage identifier
   * - ``results_folder`` / ``data_fold`` / ``sample_list``
     - ``results`` / ``data`` / ``sample.txt``
     - Output directory, data directory, and sample list
   * - ``run_type`` / ``channel`` / ``runpipe``
     - ``visium_HD`` / ``single_analysis`` / ``cellPhoneDB``
     - Platform type, analysis channel, and downstream module entry point
   * - ``threads``
     - ``8``
     - Threads allocated to the selected downstream module

Module-specific parameters
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 32 20 48

   * - Parameter
     - Default
     - Description
   * - ``senic_input`` / ``tfs_input`` / ``feather_input`` / ``motifs_input``
     - See the generated template
     - PySCENIC input object and database resource paths. ``feather_input`` accepts one database path or comma-separated ranking databases
   * - ``sample_type`` / ``gene_attr`` / ``cell_attr``
     - ``Colon_Cancer_P2`` / ``var_names`` / ``cell_id``
     - pySCENIC output label and gene/cell identifier attributes used during Loom conversion
   * - ``pyscenic_top_regulons`` / ``pyscenic_min_regulon_genes``
     - ``20`` / ``10``
     - Number of pySCENIC regulons shown in dotplot/violin plots and minimum target genes retained per regulon
   * - ``cellPhoneDB_input``
     - ``""``
     - Optional explicit input object for CellPhoneDB; an empty value uses the object supplied in ``sample.txt``
   * - ``species`` / ``output_name``
     - ``human`` / ``""``
     - CellPhoneDB input species and optional result suffix; mouse genes are projected to one-to-one human orthologs
   * - ``counts_data`` / ``threshold`` / ``pvalue`` / ``iterations``
     - ``hgnc_symbol`` / ``0.1`` / ``0.05`` / ``1000``
     - Statistical thresholds and permutation settings for CellPhoneDB
   * - ``cpdb_method``
     - ``statistical``
     - CellPhoneDB analysis mode
   * - ``microenvs_file_path`` / ``active_tf_path`` / ``degs_file_path``
     - ``""``
     - Optional external microenvironment, active-TF, and DEG input files
   * - ``niche_col`` / ``is_single_cell``
     - ``spatial_cluster`` / ``false``
     - Automatic niche column and switch that disables spatial-niche use for single-cell input
   * - ``cell_pairs`` / ``cell_type1`` / ``cell_type2`` / ``gene_family``
     - ``Tumor_I<->Tumor_II`` / ``Tumor_II`` / ``Tumor_I`` / ``""``
     - CellPhoneDB visualization focus in the generated demonstration template. Clear the cell fields for automatic selection; ``cell_pairs`` accepts multiple directed or bidirectional pairs, such as ``A|B,A<->C``
   * - ``cpdb_pathway`` / ``interaction_pairs`` / ``cpdb_genes``
     - ``""``
     - Optional CellPhoneDB pathway, ligand-receptor pair, and gene filters used for focused plots
   * - ``liana_method`` / ``liana_resource_name``
     - ``cellphonedb`` / ``consensus``
     - LIANA method and resource database
   * - ``liana_expr_prop`` / ``liana_min_cells`` / ``liana_use_raw``
     - ``0.1`` / ``5`` / ``true``
     - LIANA filtering thresholds and expression matrix source
   * - ``liana_pvalue`` / ``liana_top_n``
     - ``0.05`` / ``6``
     - LIANA p-value cutoff for p-value-based plots and number of highlighted interactions
   * - ``liana_source_celltypes`` / ``liana_target_celltypes`` / ``liana_cell_pairs`` / ``liana_pairs``
     - ``""`` / ``""`` / ``""`` / ``""``
     - Optional LIANA focused visualization filters. Cell types are comma-separated; directed cell pairs use ``source|target`` or ``source<->target``; ligand-receptor pairs use ``ligand|receptor``
   * - ``cellchat_assay`` / ``cellchat_species`` / ``cellchat_min_cells`` / ``cellchat_trim`` / ``cellchat_interaction_length``
     - ``Spatial`` / ``human`` / ``10`` / ``0.1`` / ``250``
     - CellChat species, filtering, robust mean, and spatial distance parameters
   * - ``cellchat_is_single_cell`` / ``cellchat_spot_size`` / ``cellchat_db_subset``
     - ``false`` / ``65`` / ``all_interactions``
     - CellChat single-cell mode, spatial spot/cell-size proxy, and database subset
   * - ``cellchat_future_max_size_gb``
     - ``64``
     - Maximum size of globals exported by CellChat parallel workers; ``0`` disables this limit
   * - ``cellchat_focus_cells`` / ``cellchat_cell_pairs``
     - ``""`` / ``""``
     - Recommended cell-set focus and optional exact directed/bidirectional CellChat pairs. Exact pairs take priority
   * - ``cellchat_source_cells`` / ``cellchat_target_cells``
     - ``""`` / ``""``
     - Optional asymmetric sender and receiver sets used when no exact pair or focus-cell list is supplied
   * - ``cellchat_pathways`` / ``cellchat_lr_pairs``
     - ``""`` / ``""``
     - Optional advanced pathway and ligand-receptor filters; empty values trigger automatic selection within the chosen cell scope
   * - ``cellchat_top_cell_pairs`` / ``cellchat_top_pathways`` / ``cellchat_bubble_top_lr`` / ``cellchat_plot_advanced``
     - ``3`` / ``3`` / ``20`` / ``true``
     - Limits automatic focused outputs and controls official selected-pathway advanced figures
   * - ``cellchat_pair_lr_use``
     - ``""``
     - Legacy single-LR override for spatial plotting; new analyses should use ``cellchat_lr_pairs``
   * - ``max_cluster`` / ``condition_col`` / ``sample_col`` / ``cellcharter_col``
     - ``10`` / ``condition`` / ``region`` / ``spatial_cluster``
     - CellCharter clustering search and comparison fields
   * - ``image_type`` / ``shape_type`` / ``significance``
     - ``hires`` / ``cell_boundaries`` / ``0.05``
     - CellCharter spatial visualization layers and enrichment significance threshold
   * - ``k_geom`` / ``max_m`` / ``nbr_weight_decay`` / ``lambda_list``
     - ``15`` / ``1`` / ``scaled_gaussian`` / ``[0.8]``
     - BANKSY neighborhood geometry and spatial weighting parameters
   * - ``banksy_max_features`` / ``banksy_feature_col``
     - ``2000`` / ``highly_variable``
     - Lightweight BANKSY feature selection for large Visium HD/Xenium/Stereo-seq objects
   * - ``banksy_n_comps`` / ``banksy_resolution`` / ``banksy_num_nn``
     - ``20`` / ``[0.5]`` / ``50``
     - BANKSY PCA and Leiden graph parameters following the pyBANKSY workflow
   * - ``banksy_add_umap`` / ``banksy_plot_full`` / ``banksy_run_nonspatial``
     - ``false`` / ``false`` / ``false``
     - Optional heavier BANKSY outputs; disabled by default for lightweight large-data runs
   * - ``banksy_plot_celltype_enrichment`` / ``banksy_plot_max_points``
     - ``true`` / ``200000``
     - Optional cell-type enrichment plot and maximum observations displayed in the lightweight spatial figure
   * - ``banksy_sample_col`` / ``banksy_selected_lambda`` / ``banksy_selected_resolution``
     - ``region`` / ``""`` / ``""``
     - Sample-aware BANKSY execution and optional final parameter-combination selection
   * - ``banksy_seed``
     - ``12345``
     - Random seed for BANKSY clustering and plotting subsampling

Tuning suggestions
------------------

1. First set ``runpipe``, then focus only on the parameters used by the selected downstream module.
2. For communication-focused modules, first confirm that ``celltype_col`` matches the annotation column in the input object.
3. For more complex analyses, use absolute paths for database resources to reduce environment-dependent errors.
