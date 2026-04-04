Clustering (``clustering``)
===========================

Based on the preprocessed object, ``clustering`` builds the neighbor graph, generates low-dimensional visualizations, and performs unsupervised clustering. This is a central step for annotation and downstream biological interpretation.
Because clustering quality directly affects annotation quality, we recommend testing the suggested number of PCs together with nearby values, such as the recommended value and ``recommended ± 5``, and choosing the final setting based on boundary clarity, spatial continuity, and marker consistency.


Workflow overview
-----------------
1. Read the filtered object generated in ``preprocess`` and construct the neighbor graph.
2. Represent the structure of the sample or integrated object in a low-dimensional embedding such as UMAP or tSNE.
3. Run clustering with the selected algorithm and write the labels back to the object.
4. Export visualization results and cluster labels for use in ``annotation_help``.

.. note::
   In this tutorial, we continue from the object generated in the previous ``preprocess`` step.
   If your data are not from the Visium HD platform, or if you are analyzing integrated multi-sample data, read the notes at the end of this page to understand the input and output differences.


Optional parameters from the command line
-----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--cluster_algorithm``
     - ``leiden``
     - Clustering algorithm; supported values include ``leiden``, ``louvain``, and ``Kmeans``
   * - ``--resolution``
     - ``0.8``
     - Community detection granularity for ``leiden`` or ``louvain``, controlling clustering resolution
   * - ``--n_clusters``
     - ``15``
     - Number of clusters used only for ``Kmeans``
   * - ``--pcs``
     - ``25``
     - Number of PCA dimensions used for clustering; adjust according to dataset size and computational resources, or use the value suggested in ``preprocess``
   * - ``--tsene``
     - ``False``
     - Whether to generate an additional tSNE visualization

You can append parameters directly to the command, for example ``--resolution 1.0 --pcs 30``.
For the example dataset, we follow the reference analysis and start with ``resolution 0.8`` and ``pcs 20``.
If you want finer-grained clusters, you can increase ``resolution`` and ``pcs``, but keep in mind that larger values increase runtime and may reduce clustering stability.

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --resolution=0.8 --pcs=20



Optional parameters through a configuration file
------------------------------------------------

If you are already comfortable with Spatialsnake and want to manage more settings in a structured way, use the YAML configuration template described in :doc:`../config_reference/clustering_yaml`.

After editing the configuration file, pass it with ``--configfile``.

Generate the template with:
---------------------------

.. code-block:: bash

   spatialsnake produce-file --option=clustering

Each YAML file contains inline explanations of the available settings. Adjust them according to your dataset and analysis goals.

Run with a YAML file
--------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --configfile=clustering.yaml


Result file structure
---------------------

This example shows single-sample clustering for ``visium_HD``. After the run completes, first confirm that the clustered object can be loaded correctly, then judge whether the clustering is reasonable by combining the UMAP or tSNE view with the sample-by-cluster distribution plot.

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── clustering/
           ├── Colon_Cancer_P2.zarr/
           ├── Colon_Cancer_P2UMAP.png
           └── Colon_Cancer_P2Cell_Distribution_Across_Clusters.png

The output object ``{sample}.zarr`` (or ``concatenated_sdata`` in a multi-sample setting) contains the cluster labels in ``obs['clusters']`` and serves as the direct input for ``annotation_help``. If ``tsene=False``, the tSNE plot is not generated.


Cross-platform notes
--------------------

Differences in command usage
----------------------------

If your dataset is not from ``visium_HD``, replace ``visium_HD`` with the appropriate platform type:
.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=clustering --resolution 0.8 --pcs 20

If you are analyzing integrated samples, switch to ``compare_analysis`` and make sure ``sample.txt`` follows the format described earlier:
.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=clustering --resolution 0.8 --pcs 20

You can add command-line parameters at the end of the command or manage them through a YAML file exactly as shown in the example above.


Important parameter note
------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``sketch`` (YAML parameter)
     - ``False``
     - If ``sketch`` was enabled during ``preprocess``, this parameter must also be enabled so that cluster labels can be propagated correctly


Input and output structure
--------------------------
.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Analysis mode
     - Input
     - Output
   * - single_analysis (standard ``zarr`` mode)
     - ``sample.txt`` should contain at least ``sample_id input_path``; the input object is ``results/{sample}/preprocess/filter_{sample}.zarr``
     - ``results/{sample}/clustering/{sample}.zarr``
   * - single_analysis (``visium_HD``)
     - ``sample.txt`` should contain at least ``sample_id input_path bin``; the input object is ``results/{sample}_{bin}um/preprocess/filter_{sample}.zarr``
     - ``results/{sample}_{bin}um/clustering/{sample}.zarr``
   * - compare_analysis
     - ``sample.txt`` should contain at least ``sample_id input_path group``; for ``visium_HD``, an additional ``bin`` column is required. The input object is ``results/merge_data/preprocess/filter_concatenated_sdata``
     - ``results/merge_data/clustering/concatenated_sdata``



How to inspect the clustering results
-------------------------------------

The UMAP plot is usually the first figure to inspect. Start by checking cluster boundaries, then evaluate whether the internal structure of each cluster is continuous and whether the global layout looks biologically plausible. A good clustering result typically shows clear boundaries, coherent within-cluster structure, and a natural overall organization.

.. figure:: /_static/images/umap.png
   :width: 85%
   :align: center
   :alt: clustering umap plot


Key outputs
~~~~~~~~~~~

- Main object: ``results/{sample}_{bin}um/clustering/{sample}.zarr``
  This object now contains ``obs['clusters']`` and is the direct input for ``annotation_help``.
- Visualization files: ``{sample}UMAP.png``, ``{sample}Cell_Distribution_Across_Clusters.png``, and ``{sample}tsene.png`` (optional)
  These plots are used to judge whether the clustering structure is clear and whether sample-specific bias is present.


Other outputs
~~~~~~~~~~~~~

1. ``{sample}Cell_Distribution_Across_Clusters.png`` (sample-by-cluster distribution)

   - This plot shows whether each cluster is distributed evenly across samples.
   - If a cluster appears almost exclusively in one sample, determine whether this reflects biology or technical bias.
   - In multi-sample analyses, interpret this figure together with the preprocessing results.

2. ``{sample}tsene.png`` (tSNE embedding)

   - This plot serves as a secondary check on the conclusions suggested by the UMAP plot.
   - If the overall pattern agrees with UMAP, confidence in clustering stability is usually higher.
   - If the two views differ strongly, revisit the clustering parameters and adjust them gradually.


Next, continue to :doc:`annotation_help`.
