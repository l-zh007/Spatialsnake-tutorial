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
     - ``advance_analysis``
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
   * - ``shape_type`` / ``image_type``
     - ``False`` / ``False``
     - Keywords used to filter spatial layers
   * - ``image_slice``
     - ``False``
     - Whether to crop the image region
   * - ``x1`` / ``x2`` / ``y1`` / ``y2``
     - ``0``
     - Coordinates of the cropping window
   * - ``threads``
     - ``64``
     - Thread setting for RCTD
   * - ``RCTD_mode``
     - ``doublet``
     - RCTD running mode
   * - ``cell_type_col``
     - ``celltype``
     - Cell type column name in the RCTD reference object
   * - ``group_by``
     - ``sample``
     - Grouping column name used for RCTD visualization
   * - ``max_cores``
     - ``8``
     - Maximum number of parallel cores for RCTD

Tuning suggestions
------------------

1. First decide on ``anno_algorithm``, then tune only the parameters relevant to that branch to avoid mixing settings across methods.
2. For deep-learning-based annotation, first verify the ``device`` setting and the training epoch parameters.
3. For the RCTD branch, first confirm that ``cell_type_col`` and ``RCTD_mode`` are set consistently with the reference data and analysis goal.
