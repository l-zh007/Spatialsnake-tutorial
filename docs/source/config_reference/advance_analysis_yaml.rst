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
     - PySCENIC input object and database resource paths
   * - ``senic_workers``
     - ``128``
     - Number of parallel workers for PySCENIC
   * - ``cellPhoneDB_input``
     - ``results/.../Colon_Cancer_P2_cellcharter.zarr``
     - Default input object for CellPhoneDB or LIANA
   * - ``counts_data`` / ``threshold`` / ``pvalue`` / ``iterations``
     - ``hgnc_symbol`` / ``0.1`` / ``0.05`` / ``500``
     - Statistical thresholds and permutation settings for CellPhoneDB
   * - ``cpdb_method`` / ``cpdb_de_method``
     - ``statistical`` / ``wilcoxon``
     - CellPhoneDB mode and differential method label
   * - ``cell_type1`` / ``cell_type2`` / ``gene_family``
     - ``Endothelial`` / ``Tumor`` / ``""``
     - Cell pairs and gene families emphasized in visualization
   * - ``liana_method`` / ``liana_resource_name``
     - ``cellphonedb`` / ``consensus``
     - LIANA method and resource database
   * - ``liana_expr_prop`` / ``liana_min_cells`` / ``liana_use_raw``
     - ``0.1`` / ``5`` / ``true``
     - LIANA filtering thresholds and expression matrix source
   * - ``assay`` / ``species`` / ``min_cells`` / ``workers`` / ``trim`` / ``interaction_length``
     - ``Spatial`` / ``human`` / ``10`` / ``32`` / ``0.1`` / ``150``
     - CellChat species, statistical, and spatial distance parameters
   * - ``max_cluster`` / ``condition_col`` / ``sample_col`` / ``cellcharter_col``
     - ``10`` / ``condition`` / ``region`` / ``spatial_cluster``
     - CellCharter clustering search and comparison fields
   * - ``k_geom`` / ``max_m`` / ``nbr_weight_decay`` / ``lambda_list``
     - ``15`` / ``1`` / ``scaled_gaussian`` / ``[0.8]``
     - BANKSY neighborhood geometry and spatial weighting parameters

Tuning suggestions
------------------

1. First set ``runpipe``, then focus only on the parameters used by the selected downstream module.
2. For communication-focused modules, first confirm that ``celltype_col`` matches the annotation column in the input object.
3. For more complex analyses, use absolute paths for database resources to reduce environment-dependent errors.
