Clustering
==========

Based on the preprocessed object, ``clustering`` builds the neighbor graph, generates low-dimensional visualizations, and performs unsupervised clustering. This is a central step for annotation and downstream biological interpretation.
Compare the suggested number of PCs with nearby settings and assess marker
specificity, sample composition, and spatial distribution. UMAP separation alone
does not establish a biologically meaningful partition.


Workflow overview
-----------------
1. Read the filtered object generated in ``preprocess`` and select the PCA, Harmony, or precomputed BBKNN representation.
2. Construct or reuse the neighbor graph and run the selected clustering algorithm.
3. Generate UMAP and, when applicable, t-SNE, and write the cluster labels back to the object.
4. Export visualization results and cluster labels for use in ``annotation_help``.

.. note::
   In this tutorial, we continue from the object generated in the previous ``preprocess`` step.
   If your data are not from the Visium HD platform, or if you are analyzing integrated multi-sample data, read through the following steps and replace the key parameters according to the command-line usage patterns introduced in previous tutorials.


Step 1: Configure ``sample.txt``
--------------------------------

Reuse the raw-data sample table from ``ingestion``; do not replace its paths
with a downstream Zarr. The example below is for one Visium HD sample. Other
platforms and multi-sample channels use the :ref:`core table headers <sample-tables>`.

.. code-block:: text
  
   sample_id input_path bin_size
   S1 data/S1 8

Step 2: Select parameters
-------------------------

Adjust the following parameters to the platform, resolution, and study design.

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--cluster_algorithm``
     - ``leiden``
     - Clustering algorithm; supported values include ``leiden``, ``louvain``, and ``Kmeans`` (K-means)
   * - ``--resolution``
     - ``0.8``
     - Community detection granularity for ``leiden`` or ``louvain``, controlling clustering resolution
   * - ``--n_clusters``
     - ``15``
     - Number of clusters used only for ``Kmeans``
   * - ``--pcs``
     - ``25``
     - Number of PCA dimensions used for clustering; adjust according to dataset size and computational resources, or use the value suggested in ``preprocess``
   * - ``--tsne``
     - ``False``
     - Whether to generate an additional t-SNE visualization

Configuration recommendations:
   1. For all scenarios: We recommend tuning ``pcs`` based on the ``pca_variance_ratio`` plot from the ``preprocess`` step and the recommended number of PCs printed in the terminal output. The configured starting value is ``25``. Similarly, begin with the configured ``resolution`` of ``0.5`` and adjust it according to tissue heterogeneity and marker consistency; the demo below uses ``0.8`` to illustrate a finer partition.

   2. The ``clustering`` module supports Leiden, Louvain, and K-means. Leiden and Louvain use the active neighbor graph. K-means uses the selected PCA or Harmony components directly; because BBKNN corrects a graph rather than an embedding, it does not alter the K-means feature matrix. UMAP is always generated. Additional t-SNE visualization can be enabled with ``--tsne True`` for full-data analysis.

   3. If sketch-based sampling was enabled in ``preprocess``, retain the same setting in ``clustering``. Clustering is fitted on the sketch, after which ``clusters`` and UMAP coordinates are projected to the full table in its original observation order. t-SNE is skipped in sketch mode because Scanpy does not support reference-to-query projection of a t-SNE embedding.

   4. In multi-sample analysis, Harmony clustering uses ``X_pca_harmony``. BBKNN reuses the batch-balanced graph generated during preprocessing instead of replacing it with an ordinary PCA graph. The final ``clusters`` column is categorical and is written to the full output Zarr for direct use by ``annotation_help``.


Run with your own data
----------------------

After preprocessing, adjust PCs and resolution using PC diagnostics, marker
consistency, and spatial coherence. This command illustrates parameter changes;
the CRC P2 demo below uses 15 PCs.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --resolution=0.8 --pcs=20

Keep your actual TYPE and use ``compare_analysis`` for the integrated core
workflow. For several settings, use the optional :ref:`YAML configuration
<cli-configuration>` with the :doc:`../config_reference/clustering_yaml` reference.


Demo: CRC P2 clustering
-----------------------

We use the ``Colon_Cancer_P2_008um`` data ingested in the previous step for this clustering demonstration.
The same ``sample.txt`` can be reused from the earlier analysis steps to maintain a consistent core analysis on the same sample.

.. code-block:: text
  
   sample_id input_path bin_size
   Colon_Cancer_P2 data/Colon_Cancer_P2 8

We use the parameter set ``--resolution 0.8 --pcs 15`` to identify transcriptionally coherent clusters in the sample.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --resolution=0.8 --pcs=15

Alternative YAML configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download :download:`crc_clustering.yaml </config/demo_resources/crc_clustering.yaml>`
as ``clustering.yaml`` for the same demo settings (resolution 0.8, pcs 15, sketch false).
Run the following **instead of** the preceding CLI command. Do not generate a
new template over the downloaded file.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --configfile=clustering.yaml


Result file structure
---------------------

This example shows single-sample clustering for ``visium_HD``. After the run completes, first confirm that the clustered object can be loaded correctly, then assess the clustering by combining the UMAP or t-SNE view with the sample-by-cluster distribution plot.

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── clustering/
           ├── Colon_Cancer_P2.zarr/
           ├── Colon_Cancer_P2UMAP.png
           └── Colon_Cancer_P2Cell_Distribution_Across_Clusters.png

The output object ``{sample}.zarr`` (or ``concatenated_sdata.zarr`` in a multi-sample setting) contains categorical cluster labels in ``obs['clusters']`` and serves as the direct input for ``annotation_help``. If ``tsne=False`` or sketch mode is enabled, the t-SNE plot is not generated. The Harmony sample UMAP is generated only when Harmony was actually applied to more than one batch.


Inputs and outputs
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Analysis mode
     - Input
     - Output
   * - single_analysis (standard ``zarr`` mode)
     - Use the platform's exact core header (Stereo-seq also needs ``input_spec``); the input object is ``results/{sample}/preprocess/filter_{sample}.zarr``
     - ``results/{sample}/clustering/{sample}.zarr``
   * - single_analysis (``visium_HD``)
     - ``sample.txt`` should contain at least ``sample_id input_path bin_size``; the input object is ``results/{sample}_{bin}um/preprocess/filter_{sample}.zarr``
     - ``results/{sample}_{bin}um/clustering/{sample}.zarr``
   * - compare_analysis
     - ``sample.txt`` contains ``sample_id input_path group``. For Visium HD, append bin_size after group in sample.txt. The input object is ``results/merge_data/preprocess/filter_concatenated_sdata.zarr``
     - ``results/merge_data/clustering/concatenated_sdata.zarr``


How to inspect the clustering results
-------------------------------------

Random seeds are fixed for clustering and dimensionality reduction, but minor differences may still occur across software versions and numerical backends.

.. figure:: /_static/images/umap.png
   :width: 85%
   :align: center
   :alt: UMAP representation of the clustering result


Key outputs
~~~~~~~~~~~

- Main object: ``results/{sample}_{bin}um/clustering/{sample}.zarr``
  This object now contains ``obs['clusters']`` and is the direct input for ``annotation_help``.
- Visualization files: ``{sample}UMAP.png``, ``{sample}Cell_Distribution_Across_Clusters.png``, ``{sample}_harmony_sample_UMAP.png`` (Harmony only), and ``{sample}tsne.png`` (optional)
  These plots are used to judge whether the clustering structure is clear and whether sample-specific bias is present.


Other outputs
~~~~~~~~~~~~~

1. ``{sample}Cell_Distribution_Across_Clusters.png`` (sample-by-cluster distribution)

   - This plot shows whether each cluster is distributed evenly across samples.
   - If a cluster appears almost exclusively in one sample, determine whether this reflects biology or technical bias.
   - In multi-sample analyses, interpret this figure together with the preprocessing results.

2. ``{sample}tsne.png`` (t-SNE embedding)

   - This is an alternative view of the same expression representation.
   - Agreement with UMAP is not an independent test of clustering stability.
     Review marker consistency and sensitivity to nearby PC/resolution settings
     before changing the partition.


For CRC P2, examine whether clusters separate broad epithelial, immune, and
stromal expression patterns in :doc:`annotation_help`. Nearly identical marker
profiles across small clusters may indicate overpartitioning; incompatible
lineage signatures within a cluster warrant closer inspection or subclustering.
In integrated data, a sample-specific cluster requires a biological or technical
explanation, not automatic removal.

Next, continue to :doc:`annotation_help`.
