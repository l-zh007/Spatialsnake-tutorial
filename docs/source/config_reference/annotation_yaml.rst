annotation.yaml Reference
=========================

This configuration file corresponds to ``--option=annotation`` and centralizes the settings for manual annotation, reannotation, cell2location, and RCTD.

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - Parameter
     - Default
     - Description
   * - ``option``
     - ``annotation``
     - Stage identifier field stored in the file
   * - ``results_folder`` / ``data_fold`` / ``sample_list``
     - ``results`` / ``data`` / ``sample.txt``
     - Output directory, data directory, and sample list
   * - ``run_type`` / ``channel``
     - ``visium`` / ``compare_analysis``
     - Platform type and analysis channel
   * - ``anno_algorithm``
     - ``manual``
     - Annotation algorithm branch
   * - ``annotation_list``
     - ``annotation.txt``
     - Path to the manual mapping file
   * - ``device``
     - ``cuda``
     - Device used for model training
   * - ``max_epochs_reference``
     - ``250``
     - Number of training epochs for the cell2location reference model
   * - ``remove_mt``
     - ``True``
     - Whether to remove mitochondrial genes
   * - ``N_cells_per_location``
     - ``30``
     - Prior for the number of cells per location in cell2location
   * - ``max_epochs_st``
     - ``30000``
     - Number of training epochs for the cell2location spatial model
   * - ``labels_key_reference``
     - ``celltype``
     - Cell-type label column in the cell2location single-cell reference
   * - ``celltype_col``
     - ``celltype``
     - Existing spatial grouping column used for the cell2location abundance-correlation dotplot
   * - ``cell2location_microenvironment_threshold``
     - ``0.10``
     - Minimum n_fact=12 cell-type fraction exported to ``cellphonedb_microenvironments.tsv``
   * - ``shape_type`` / ``image_type``
     - ``cell_boundaries`` / ``hires``
     - Spatial layers used by annotation methods that render image/shape overlays
   * - ``image_slice``
     - ``False``
     - Whether to crop the image region
   * - ``x1`` / ``x2`` / ``y1`` / ``y2``
     - ``0``
     - Coordinates of the cropping window
   * - ``threads``
     - ``8``
     - Threads allocated to each annotation workflow rule
   * - ``RCTD_mode``
     - ``full``
     - RCTD running mode
   * - ``sc_cell_type_col`` / ``spatial_cell_type_col``
     - ``celltype`` / ``celltype``
     - Reference label column and existing unsupervised spatial-region column for RCTD
   * - ``group_by``
     - ``sample``
     - Sample column used for sample-balanced RCTD regional summaries
   * - ``rctd_dotplot_max_cell_types``
     - ``30``
     - Maximum number of cell types displayed in RCTD regional PDFs; ``0`` displays all
   * - ``rctd_dotplot_enrichment_clip``
     - ``2.5``
     - Symmetric log2-enrichment colour limit for RCTD regional dotplots

Tuning suggestions
------------------

1. First decide on ``anno_algorithm``, then tune only the parameters relevant to that branch to avoid mixing settings across methods.
2. For deep-learning-based annotation, first verify the ``device`` setting and the training epoch parameters.
3. For the RCTD branch, first confirm that ``sc_cell_type_col``, ``spatial_cell_type_col``, and ``RCTD_mode`` are set consistently with the data and analysis goal.
