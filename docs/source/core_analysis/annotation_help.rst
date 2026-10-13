Annotation Support
==================

Based on the clustering results, ``annotation_help`` performs marker gene statistics, enrichment analysis, and spatial cluster visualization to provide interpretable biological evidence for the downstream ``annotation`` step.
In a single-sample setting, this stage helps identify candidate cell types for each cluster. In an integrated multi-sample setting, it also helps assess whether marker and pathway results are influenced by sample composition.


Workflow overview
-----------------
1. Read the output object from ``clustering`` together with the ``clusters`` labels.
2. Compute differential marker genes by cluster on the log-normalized expression matrix and export both a combined table and per-cluster tables.
3. Generate marker dotplots, sample-by-cluster proportion plots, and spatial overlay figures.
4. Run GO and KEGG enrichment analyses based on the marker genes and export pathway results.
5. Write all annotation support outputs into the ``clustering`` directory so that they can be used directly by ``annotation``.


Step 1: Configure ``sample.txt``
--------------------------------

Reuse the raw-data sample table from ``integrate``; do not replace its paths
with a downstream Zarr. The example below is for one Visium HD sample. Other
platforms and multi-sample channels use the :ref:`core table headers <sample-tables>`.

.. code-block:: text
  
   sample_id input_path bin_size
   S1 data/S1 8

Step 2: Parameter Selection and Configuration
---------------------------------------------

This step includes several important parameters. Please adjust them according to your needs. Below are some key parameters and their functions:

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--markers_algorithm``
     - ``wilcoxon``
     - Marker statistics method; ``wilcoxon`` is commonly used, but ``t-test`` and others can also be selected when appropriate
   * - ``--species``
     - ``human``
     - Species background used for enrichment analysis, typically ``human`` or ``mouse``

Run with your own data
----------------------

Use a species background matching your data (``human`` or ``mouse``). Marker
genes and enrichment provide annotation evidence, not an automatic cell-type
assignment. The CRC Demo below uses default ``wilcoxon``; this command instead
illustrates switching to ``t-test``.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotation_help --markers_algorithm=t-test --species=human

Keep your actual TYPE and use ``compare_analysis`` for the integrated core
workflow. For several settings, use the optional :ref:`YAML configuration
<cli-configuration>` with the :doc:`../config_reference/annotation_help_yaml` reference.


Demo for annotation_help with visium_HD
---------------------------------------

We use the ``Colon_Cancer_P2_008um`` data from the previous step for this annotation_help demonstration.
The same ``sample.txt`` can be reused from the earlier analysis steps to maintain a consistent core analysis on the same sample.

.. code-block:: text
  
   sample_id input_path bin_size
   Colon_Cancer_P2 data/Colon_Cancer_P2 8


.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotation_help

The Demo uses default ``wilcoxon`` markers and the human enrichment background.
For mouse data, add ``--species=mouse``. Use the output tables to review each
cluster before :doc:`../annotation/manual`.


Result file structure
---------------------

This example shows single-sample annotation support for ``visium_HD``. Before moving to manual annotation, first confirm that ``marker_genes_pval.csv`` and ``kegg_data.csv`` have been generated.
The workflow creates one subdirectory for each cluster, containing its differential marker table, KEGG enrichment results, spatial visualization outputs, and related files, making it easier to interpret the characteristic features of each candidate cell type.

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── clustering/
           ├── marker_genes_pval.csv
           ├── kegg_data.csv
           ├── Colon_Cancer_P2rank_genes_groups_dotplot.png
           ├── Clusters_proportion.png
           ├── Colon_Cancer_P2_hires_image_Clusters.png
           ├── [cluster_id]/
           │   └── cluster_[cluster_id].csv
           └── Colon_Cancer_P2_cell_clusters.csv

.. note::

   The main core analysis workflow is now complete. The annotation support results are stored in the ``clustering`` directory. Next, continue to :doc:`../annotation/index` for manual annotation or algorithm-based annotation.


Input and output structure
--------------------------

After ``clustering`` is complete, you can usually reuse the same ``sample.txt`` file for ``annotation_help``.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Analysis mode
     - Input
     - Output
   * - single_analysis (standard ``zarr`` mode)
     - Use the platform's exact core header (Stereo-seq also needs ``input_spec``); the input object is ``results/{sample}/clustering/{sample}.zarr``
     - ``results/{sample}/clustering/marker_genes_pval.csv`` and ``results/{sample}/clustering/kegg_data.csv``
   * - single_analysis (``visium_HD``)
     - ``sample.txt`` should contain at least ``sample_id input_path bin_size``; the input object is ``results/{sample}_{bin}um/clustering/{sample}.zarr``
     - ``results/{sample}_{bin}um/clustering/marker_genes_pval.csv`` and ``results/{sample}_{bin}um/clustering/kegg_data.csv``
   * - compare_analysis
     - ``sample.txt`` contains ``sample_id input_path group``. For Visium HD, append bin_size after group in sample.txt. The input object is ``results/merge_data/clustering/concatenated_sdata.zarr``
     - ``results/merge_data/clustering/marker_genes_pval.csv`` and ``results/merge_data/clustering/kegg_data.csv``


How to inspect the results
--------------------------

This step produces a spatial cluster map showing the tissue distribution of each cluster.
The figure panels typically include the original H&E-stained image together with the mapped cluster assignments, allowing you to interpret the spatial organization of the clusters in histological context.

.. figure:: /_static/images/Colon_Cancer_P2_hires_image_Clusters.png
   :width: 85%
   :align: center
   :alt: Spatial distribution of clusters used for annotation support

The marker dotplot summarizes the strength and specificity of representative genes across clusters. You can combine it with the exported CSV tables to determine the defining markers for each cluster before annotation.

.. figure:: /_static/images/Colon_Cancer_P2rank_genes_groups_dotplot.png
   :width: 85%
   :align: center
   :alt: Marker gene dot plot across clusters



Each cluster-specific directory also contains differential marker tables and GO/KEGG enrichment results, helping you interpret the most enriched pathways for that cluster.

.. figure:: /_static/images/kegg_cluster.png
   :width: 85%
   :align: center
   :alt: KEGG pathway enrichment for an example cluster

.. figure:: /_static/images/GO_cluster.png
   :width: 85%
   :align: center
   :alt: GO enrichment for an example cluster



Other outputs
~~~~~~~~~~~~~

1. ``marker_genes_pval.csv`` (combined marker table)

   - This is the main evidence table for annotation and summarizes the most representative genes for each cluster.
   - Prioritize gene combinations that appear consistently and agree with known cell-type characteristics.
   - In most cases, this table forms the primary basis for assigning cell-type names.

2. ``<cluster_id>/cluster_<cluster_id>.csv`` (per-cluster marker table)

   - This file isolates each cluster into its own table for detailed inspection.
   - Cluster-specific review makes it easier to detect mixed signatures.
   - If one cluster contains multiple incompatible signals, revisit the upstream clustering settings and consider whether the clustering is too coarse.

3. ``kegg_data.csv`` (pathway enrichment)

   - This table provides additional evidence about the biological processes associated with each cluster.
   - Pathway results should be interpreted together with marker genes rather than used alone for annotation.
   - If pathway and marker evidence clearly conflict, re-evaluate clustering quality before assigning labels.

4. ``{sample}rank_genes_groups_dotplot.png`` (global expression pattern overview)

   - This plot helps you quickly see which genes are strongest in which clusters.
   - If some genes are clearly enriched in only one target cluster, annotation confidence is usually higher.
   - If several clusters share similar expression patterns, finer subclustering may still be useful.

5. ``Clusters_proportion.png`` and ``[image]_Clusters.png`` (composition and spatial distribution)

   - The cluster proportion plot shows compositional differences across samples or regions.
   - The spatial overlay figure helps verify whether cluster locations are coherent and consistent with tissue structure.
   - When composition patterns and spatial localization support the same interpretation, the data are usually ready for manual annotation.


Continue to :doc:`../annotation/index`.



.. note::

   The main core analysis workflow is now complete, and the annotation support results are stored in the ``clustering`` directory.
   At this point, it is common to inspect the marker genes and enrichment results for each cluster and infer likely cell identities with the help of resources such as CellMarker or PanglaoDB.
   Then continue to :doc:`../annotation/index` for manual annotation or algorithm-based annotation.
