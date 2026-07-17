clustering.yaml Reference
=========================

This configuration file corresponds to ``--option=clustering`` and controls low-dimensional embedding, neighbor graph construction, and clustering.

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - Parameter
     - Default
     - Description
   * - ``option``
     - ``clustering``
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
     - Platform type
   * - ``channel``
     - ``compare_analysis``
     - Analysis channel
   * - ``threads``
     - ``8``
     - Threads allocated to graph construction and clustering
   * - ``tsne``
     - ``False``
     - Whether to generate an additional t-SNE plot
   * - ``MIN_DIST``
     - ``0.3``
     - UMAP ``min_dist`` parameter
   * - ``SPREAD``
     - ``2``
     - UMAP ``spread`` parameter
   * - ``cluster_algorithm``
     - ``leiden``
     - Clustering algorithm selection
   * - ``resolution``
     - ``0.5``
     - Resolution for Leiden or Louvain clustering
   * - ``n_clusters``
     - ``15``
     - Number of clusters for K-means
   * - ``n_comps``
     - ``20``
     - Number of principal components used for dimensionality reduction
   * - ``k_geom``
     - ``15``
     - BANKSY geometric neighbor parameter
   * - ``max_m``
     - ``1``
     - BANKSY neighborhood order
   * - ``nbr_weight_decay``
     - ``scaled_gaussian``
     - Strategy for neighborhood weight decay
   * - ``lambda_list``
     - ``0.2``
     - Weight for spatial enhancement
   * - ``sketch``
     - ``False``
     - Whether to use the sketched object for clustering label propagation
   * - ``pcs``
     - ``25``
     - Number of PCs used in clustering
   * - ``NEIGHBORS``
     - ``10``
     - Number of neighbors used for the neighbor graph

Tuning suggestions
------------------

1. In a standard workflow, start with ``cluster_algorithm=leiden`` and then tune ``resolution`` and ``pcs``.
2. If spatial continuity is important, explore spatial enhancement settings such as ``k_geom`` and ``lambda_list``.
3. If ``sketch`` was enabled during ``preprocess``, it should also be enabled at this stage.
