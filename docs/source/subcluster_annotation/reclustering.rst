Secondary Clustering (``reclustering``)
=======================================

Spatial transcriptomics studies often require more detailed subcluster annotation than can be achieved in the initial clustering step. Because the original clustering is limited by the selected resolution and number of PCs, it may not separate subtle subpopulations well.
For this reason, Spatialsnake provides ``reclustering`` to refine a target cell population at higher resolution.

Workflow overview
-----------------
1. Read the input ``.zarr`` object and extract the first table as the reclustering target.
2. Build the neighbor graph from PCA and run Leiden clustering again, writing the new labels to ``obs['recluster']``.
3. Export the reclustered UMAP plot and spatial distribution plot.
4. Compute and export subcluster marker results with the selected thresholds.
5. Export the subcluster assignment table and write the updated labels back into a new ``{subset}.zarr`` object for downstream reuse.


Here we use the manually annotated ``Colon_Cancer_P2`` dataset as an example.
We first select a cell population of interest. In this case, we isolate the ``Tumor`` compartment in order to resolve finer malignant subclusters.

.. important::
   Before starting this step, make sure your data have already been split according to the cell type of interest.
   If you have not yet done so, read :doc:`../useful_tool/index`, or use the command below to create the subset.
   Because this module repeats the post-normalization analysis pipeline in order to identify finer cell-type labels, we use the example data directly here. For other scenarios, adjust the required parameters and paths according to your dataset.


1. Split the object
-------------------
Select the cell type to be subdivided directly, for example the ``Tumor`` population, by setting ``--barcodes=Tumor``. For detailed instructions, refer to :doc:`../useful_tool/index`.

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr --split_by=celltype --barcodes=Tumor

When several annotated classes should be reclustered together as one biological compartment, separate them with commas. This is useful when two labels belong to the same broad lineage or when one class contains too few cells for stable reclustering.

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr --split_by=celltype --barcodes=Tumor,T_cell

This command writes one combined object:

.. code-block:: text

   results/useful_results/celltype_selected_Tumor_T_cell.zarr

When different major cell classes should be reclustered independently, separate groups with a pipe. Because ``|`` is a shell pipe character, quote the argument in the command line.

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr --split_by=celltype --barcodes='Tumor|T_cell'

This command writes two independent objects:

.. code-block:: text

   results/useful_results/celltype_selected_Tumor.zarr
   results/useful_results/celltype_selected_T_cell.zarr

Then prepare ``sample.txt`` using the output under ``results/useful_results``.
Each row represents one independent cell-type subset and one input ``.zarr`` object.
The first column is the parent sample ID, not the subset ID. To subcluster several cell types from the same tissue in one run, repeat the parent sample ID and add one row per subset. Spatialsnake derives the subset name from ``celltype_selected_<name>.zarr`` and creates an independent Snakemake job for every row.

.. code-block:: bash

   sample_id input_path
   Colon_Cancer_P2_008um results/useful_results/celltype_selected_Tumor.zarr
   Colon_Cancer_P2_008um results/useful_results/celltype_selected_T_cell.zarr
   Colon_Cancer_P2_008um results/useful_results/celltype_selected_Myeloid.zarr

If the upstream split was generated with commas, list the combined object as a single row:

.. code-block:: bash

   sample_id input_path
   Colon_Cancer_P2_008um results/useful_results/celltype_selected_Tumor_T_cell.zarr

.. important::
   ``-j/--jobs`` controls the total CPU cores available to Snakemake, while ``--threads`` controls the cores assigned to each individual zarr job.
   The approximate maximum number of simultaneous reclustering jobs is ``floor(jobs / threads)``. For example, ``-j 32 --threads=8`` can run up to four zarr inputs concurrently, subject to available memory.

During reclustering, cellular heterogeneity within the subset is smaller, so it is recommended to use relatively low ``resolution`` and ``n_pcs`` values to avoid over-clustering.


2. Configure parameters
-----------------------

To keep the reclustering strategy reproducible across multiple runs, use a YAML configuration file.
See :doc:`../config_reference/reclustering_yaml` for the parameter reference.
The template lets you manage settings such as ``recluster_resolution``, ``recluster_n_pcs``, and ``recluster_marker_method`` in a versioned and reproducible way.

Generate the YAML template with:

.. code-block:: bash

   spatialsnake produce-file --option=reclustering


3. Run reclustering
-------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=reclustering --recluster_resolution=0.4 --recluster_n_pcs=15 -j 32 --threads=8

or

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=reclustering --configfile=reclustering.yaml


Result file structure
---------------------

Before interpreting the subcluster structure, confirm that ``marker_genes.csv`` and ``cluster_assignments.csv`` were generated for every input row.

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── reclustering/
           ├── Tumor/
           │   ├── Tumor.zarr/
           │   ├── umap_recluster.png
           │   ├── spatial_clusters.png
           │   ├── marker_genes.csv
           │   └── cluster_assignments.csv
           ├── T_cell/
           │   └── ...
           └── Myeloid/
               └── ...

The file ``{subset}/{subset}.zarr`` contains the new ``recluster`` labels. ``marker_genes.csv`` and ``cluster_assignments.csv`` are the main files used for downstream subcluster annotation and comparison.



Demo figures and interpretation
---------------------------------------

We use the ``Tumor`` subset as an example. The reclustering UMAP plot shows whether the subclusters are clearly separated or excessively fragmented.

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr --split_by=celltype --barcodes=Tumor


.. code-block:: bash

   sample_id input_path
   Colon_Cancer_P2_008um results/useful_results/celltype_selected_Tumor.zarr

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
