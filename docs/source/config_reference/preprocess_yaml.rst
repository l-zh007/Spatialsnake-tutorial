preprocess.yaml Reference
=========================

This configuration file corresponds to ``--option=preprocess`` and controls quality control, filtering, normalization, and dimensionality-reduction preparation.

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - Parameter
     - Default
     - Description
   * - ``option``
     - ``preprocess``
     - Fixed identifier for the analysis stage
   * - ``results_folder``
     - ``results``
     - Root directory for analysis outputs
   * - ``data_fold``
     - ``data``
     - Root directory for raw input data
   * - ``sample_list``
     - ``sample.txt``
     - Path to the sample list file
   * - ``run_type``
     - ``visium``
     - Spatial transcriptomics platform type
   * - ``channel``
     - ``compare_analysis``
     - Single-sample or integrated analysis mode
   * - ``threads``
     - ``8``
     - Threads allocated to preprocessing
   * - ``filter_list``
     - ``False``
     - Whether to read sample-specific thresholds from ``sample.txt`` in ``single_analysis``
   * - ``min_counts``
     - ``50``
     - Minimum total counts required per spot or cell
   * - ``min_cells``
     - ``50``
     - Minimum number of spots or cells in which a gene must be detected
   * - ``mt_threshold``
     - ``80.0``
     - Upper limit for mitochondrial proportion filtering
   * - ``variable``
     - ``False``
     - Whether to perform highly variable gene selection
   * - ``NEIGHBORS``
     - ``10``
     - Number of neighbors used for the neighbor graph
   * - ``batch_method``
     - ``harmony``
     - Batch correction method for multi-sample analysis
   * - ``n_top_genes``
     - ``3000``
     - Number of highly variable genes
   * - ``n_comps``
     - ``50``
     - Number of PCA components
   * - ``sketch``
     - ``False``
     - Whether to enable sketch-based analysis for large datasets
   * - ``sample_rate``
     - ``0.30``
     - Sampling fraction

Tuning suggestions
------------------

1. When sample quality differs substantially across samples, enable ``filter_list`` and provide the documented sample-specific threshold columns.
2. For multi-sample analyses, using ``batch_method`` is usually recommended to reduce batch effects.
3. For datasets containing millions of cells, enable ``sketch`` to improve iteration speed.
