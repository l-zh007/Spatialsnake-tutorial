reclustering.yaml Reference
===========================

This configuration file corresponds to ``--option=reclustering`` and is used for secondary subdivision of target populations and subcluster marker identification.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Parameter
     - Default
     - Description
   * - ``option``
     - ``reclustering``
     - Fixed identifier for the analysis stage
   * - ``results_folder``
     - ``results``
     - Root directory for analysis outputs
   * - ``sample_list``
     - ``sample.txt``
     - Path to the sample list file
   * - ``channel``
     - ``single_analysis``
     - Analysis channel
   * - ``run_type``
     - ``visium``
     - Platform type
   * - ``threads``
     - ``8``
     - CPU threads assigned to each input zarr job; combine with CLI ``-j/--jobs`` to control how many zarr jobs run concurrently
   * - ``recluster_resolution``
     - ``0.8``
     - Resolution used for reclustering
   * - ``recluster_n_top_genes``
     - ``2000``
     - Number of highly variable genes
   * - ``recluster_neighbors``
     - ``15``
     - Number of neighbors used for the neighbor graph
   * - ``recluster_n_pcs``
     - ``30``
     - Number of PCA dimensions used in reclustering
   * - ``recluster_marker_method``
     - ``wilcoxon``
     - Statistical method used for subcluster marker detection
   * - ``recluster_min_pct``
     - ``0.1``
     - Minimum positive fraction threshold for marker detection
   * - ``recluster_logfc_threshold``
     - ``0.25``
     - Minimum logFC threshold for marker detection

Tuning suggestions
------------------

1. Tune ``recluster_resolution`` before ``recluster_n_pcs`` so the effect of each parameter is easier to interpret. Because reclustering usually targets a smaller dataset, modest values are often sufficient.
2. ``recluster_min_pct`` and ``recluster_logfc_threshold`` jointly determine how stringent marker detection will be.
