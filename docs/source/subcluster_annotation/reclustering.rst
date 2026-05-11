Secondary Clustering (``reclustering``)
=======================================

Spatial transcriptomics studies often require more detailed subcluster annotation than can be achieved in the initial clustering step. Because the original clustering is limited by the selected resolution and number of PCs, it may not separate subtle subpopulations well.
For this reason, Spatialsnake provides ``reclustering`` to refine a target cell population at higher resolution.


Here we use the manually annotated ``Colon_Cancer_P2`` example for demonstration.
We first select a cell population of interest. In this case, we isolate the ``Tumor`` compartment in order to resolve finer malignant subclusters.

.. note::
   Before starting this step, make sure your data have already been split according to the cell type of interest.
   If you have not yet done so, read :doc:`../useful_tool/index`, or use the command below to create the subset.
   由于这是一个重复进行分析的模块 重复Normalize之后的分析,以寻找更细的细胞类型标签,我们直接使用demo数据进行演示.若您为其他情况,请根据之前的经验更改对应必要参数.

Split the object
请直接选择需要细分的细胞类型,例如Tumor类型,请将barcodes设置为Tumor 即可. 若您需要拆分更多类型,请以逗号分隔顺序填写.具体操作请参考:doc:`../useful_tool/index`

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr --split_by=celltype --barcodes=Tumor

Then prepare ``sample.txt`` using the output under ``results/useful_results``:
若您想同时使用相同的参数对多个细胞类型进行细分,在此基础上增加sample_id input_path即可 spatialsnake将会利用多线程进行并行处理.

.. code-block:: bash

   sample_id input_path
   Colon_Cancer_P2_008um results/useful_results/celltype_selected_Tumor.zarr

重聚类的细胞异质性较小,所以选取的resolution和n_pcs参数推荐偏小,避免过聚类.

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=reclustering --recluster_resolution=0.4 --recluster_n_pcs=15

Workflow overview
-----------------
1. Read the input ``.zarr`` object and extract the first table as the reclustering target.
2. Build the neighbor graph from PCA and run Leiden clustering again, writing the new labels to ``obs['recluster']``.
3. Export the reclustered UMAP plot and spatial distribution plot.
4. Compute and export subcluster marker results with the selected thresholds.
5. Export the subcluster assignment table and write the updated labels back into a new ``{sample}.zarr`` object for downstream reuse.

.. note::

   The current ``reclustering`` script supports only ``.zarr`` input paths. ``.h5ad`` input will not pass the internal validation step.


Optional parameters from the command line
-----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--recluster_resolution``
     - ``0.8``
     - Leiden reclustering resolution, controlling subcluster granularity
   * - ``--recluster_n_top_genes``
     - ``2000``
     - Number of highly variable genes used in reclustering
   * - ``--recluster_neighbors``
     - ``15``
     - Number of neighbors in the neighbor graph, affecting local connectivity
   * - ``--recluster_n_pcs``
     - ``30``
     - Number of PCA dimensions used for the neighbor graph
   * - ``--recluster_marker_method``
     - ``wilcoxon``
     - Statistical method for marker detection
   * - ``--recluster_min_pct``
     - ``0.1``
     - Minimum positive fraction threshold for markers
   * - ``--recluster_logfc_threshold``
     - ``0.25``
     - Minimum log2FC threshold for markers

All of these parameters can be passed directly on the command line. If you want to quickly tune subcluster resolution or marker stringency, append them to the command, for example ``--recluster_resolution=1.0 --recluster_logfc_threshold=0.5``.


Optional parameters through a configuration file
------------------------------------------------

If you want to keep the reclustering strategy reproducible across multiple attempts, use a YAML configuration file.

See :doc:`../config_reference/reclustering_yaml` for the parameter reference.

Generate the YAML template with:

.. code-block:: bash

   spatialsnake produce-file --option=reclustering

The template lets you manage settings such as ``recluster_resolution``, ``recluster_n_pcs``, and ``recluster_marker_method`` in a versioned and reproducible way.


Run the workflow with the configuration file
-------------------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=reclustering --configfile=reclustering.yaml


Result file structure
---------------------

This example shows single-sample reclustering. Before interpreting the subcluster structure, first confirm that ``marker_genes.csv`` and ``cluster_assignments.csv`` have been generated.

.. code-block:: text

   results/
   └── {sample}/
       └── reclustering/
           ├── {sample}.zarr/
           ├── umap_recluster.png
           ├── spatial_clusters.png
           ├── marker_genes.csv
           └── cluster_assignments.csv

The file ``{sample}.zarr`` contains the new ``recluster`` labels. ``marker_genes.csv`` and ``cluster_assignments.csv`` are the main files used for downstream subcluster annotation and comparison.



Key parameter recommendations
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - Parameter category
     - Recommendation for single-sample analysis
     - Recommendation for multi-sample or cross-condition analysis
   * - ``recluster_resolution``
     - Start with small increments in the range ``0.6-1.0`` and prioritize interpretability
     - Avoid setting it too high at once, or sample-level differences may be split into technical subclusters
   * - ``recluster_n_pcs`` + ``recluster_neighbors``
     - Use ``30`` + ``15`` as a practical baseline and refine based on subcluster stability
     - Fix one parameter set before comparing conditions to reduce structural drift
   * - ``recluster_marker_method``
     - ``wilcoxon`` is usually preferred because it is robust and easy to interpret
     - Keep the same method across samples to avoid methodological bias
   * - ``recluster_min_pct`` + ``recluster_logfc_threshold``
     - Start with default values to obtain candidate markers, then tighten them if needed
     - Use a consistent threshold strategy for integrated objects so markers remain comparable



How to inspect the reclustering results
---------------------------------------


1. ``umap_recluster.png`` (subcluster structure)

   - Use this plot to assess whether the subclusters are separated clearly.
   - If many fragmented micro-clusters appear, the resolution may be too high.
   - If subclusters remain overly mixed, increase the resolution gradually and compare stability.

2. ``spatial_clusters.png`` (spatial subcluster map)

   - Use this plot to check whether subclusters occupy biologically plausible spatial locations in the tissue.
   - If one subcluster is highly fragmented without a clear explanation, rerun with adjusted parameters.
   - Subclusters with locally coherent spatial distributions are usually easier to interpret biologically.

3. ``marker_genes.csv`` (subcluster marker table)

   - This table is one of the main sources of evidence for naming subclusters.
   - Prioritize genes that are stably enriched in the target subcluster and consistent with the literature.
   - Interpret the table together with the images rather than relying on a single type of evidence.

4. ``cluster_assignments.csv`` (label assignment table)

   - This file records the assigned subcluster label for each cell or spot.
   - It is a key bridge file for manual naming and downstream comparison.
   - Check for extremely small subclusters before proceeding, as they can lead to unstable downstream statistics.

5. Input requirements and common pitfalls

   - Before reclustering, make sure the input object is well defined and structurally complete.
   - If the upstream object is unstable, the subcluster results will also be unstable.
   - Always confirm that the original clustering is interpretable before refining it further.


Example figures
~~~~~~~~~~~~~~~


.. figure:: /_static/images/umap_recluster.png
   :width: 85%
   :align: center
   :alt: reclustering umap

   Reclustering UMAP plot showing whether the subclusters are clearly separated or excessively fragmented.

.. figure:: /_static/images/spatial_clusters.png
   :width: 85%
   :align: center
   :alt: reclustering spatial clusters

   Spatial subcluster map showing spatial continuity and local enrichment patterns.

You can then use :doc:`reannotation` to assign biological labels to the reclustered subpopulations, following the same logic as before with marker-based interpretation.
