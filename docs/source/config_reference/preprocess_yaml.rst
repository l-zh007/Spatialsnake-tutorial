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
     - Enables additional per-sample YAML overrides; optional sample-table QC columns are read automatically
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
     - Shared workflow value; the standard graph is constructed in ``clustering``
   * - ``batch_method``
     - ``harmony``
     - Batch correction method: ``harmony``, ``bbknn``, or ``None``
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

1. Optional ``min_cells min_counts [mt_threshold]`` columns in the core sample table take precedence over per-sample YAML values and global defaults. Enable ``filter_list`` when using additional ``sample_parameters`` YAML overrides in single-sample mode.
2. For multi-sample analyses, Harmony provides a corrected PCA representation, whereas BBKNN provides a corrected neighbor graph. The ``sample`` column is preferred as the batch key, with ``region`` used as a fallback.
3. For datasets containing millions of cells, enable ``sketch`` to improve clustering speed. The Zarr contains the sketch reference and ``sketch.h5ad`` retains the full table for downstream projection.
