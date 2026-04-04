Module 4: Spatial Domain Modeling (cellcharter)
===============================================

``cellcharter`` combines gene expression with local neighborhood structure to identify spatial domains that better match tissue architecture.
The workflow also uses CellCharter's enrichment analysis to compare cell-type enrichment patterns within a sample or across samples.
In this tutorial, we use a previously annotated example dataset to demonstrate spatial domain modeling.

This module can take advantage of GPU acceleration. If you run it on CPU only, runtime may be substantially longer.


For the configuration reference, see :doc:`../config_reference/advance_analysis_yaml`.

Workflow overview
-----------------

1. **Read and preprocess the input**
   Load ``.zarr`` or ``.h5ad`` objects, standardize the expression matrix, and construct a ``counts`` layer for comparable downstream modeling.
2. **Construct neighborhood-aware spatial features**
   Build the spatial neighborhood graph and combine intrinsic expression with neighborhood context to generate ``X_cellcharter``.
3. **Select the optimal number of spatial domains**
   Evaluate clustering stability across the range ``(2, max_cluster)``, choose the most suitable domain number, and assign each spot or cell to a spatial domain.
4. **Generate branch-specific outputs**
   - Single-sample mode focuses on neighborhood enrichment relationships among spatial domains.
   - Multi-sample mode (``compare_analysis``) evaluates neighborhood structure within each condition and then highlights condition-specific changes in domain connectivity.

Prepare the input files
-----------------------

Recommended ``sample.txt`` format:

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

Input requirements:

1. The input object must contain spatial coordinates, either in ``obsm['spatial']`` or in a convertible equivalent.
2. Using an annotated object that includes ``celltype`` is recommended so the enrichment outputs remain interpretable.
3. For multi-sample comparison, use an integrated object and preserve both sample and condition columns, for example ``sample_col=region`` and ``condition_col=condition``.


Common parameters
-----------------

.. code-block:: bash

   image_type: "hires"
   shape_type: "cell_boundaries"
   significance: 0.05
   max_cluster: 10
   condition_col: "condition"
   sample_col: "region"
   celltype_col: "celltype"
   cellcharter_col: "spatial_cluster"


Run the workflow
----------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellcharter



Result file structure
---------------------

Single-sample output (default mode):

.. code-block:: text

   results/
   └── cellcharter/
       ├── {sample}_cellcharter.zarr/
       ├── {sample}_celchar.png
       ├── {sample}_enrichment.png
       ├── {sample}_nhood_enrichment.png
       ├── {sample}_{image}_Clusters.png
       └── {sample}_cell_clusters.csv

Multi-sample output (``channel=compare_analysis``):

.. code-block:: text

   results/
   └── cellcharter/
       ├── {sample}_cellcharter.zarr/
       ├── {sample}_celchar.png
       ├── {sample}_enrichment.png
       ├── {sample}_{conditionA}_enrichment.png
       ├── {sample}_{conditionB}_enrichment.png
       ├── {sample}_diff_enrichment.png
       ├── {sample}_Clusters_proportion.png
       ├── {sample}_{image}_Clusters.png
       └── {sample}_cell_clusters.csv

When is the differential enrichment plot generated?
---------------------------------------------------

``{sample}_diff_enrichment.png`` is generated only when all of the following conditions are met:

1. The workflow is running in the multi-sample comparison branch (``channel=compare_analysis``).
2. The input object contains ``condition_col`` with at least two condition groups.
3. The input object contains ``sample_col``, which is required for sample-level neighborhood comparison.

How to interpret the results
----------------------------

1. Cluster stability plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_celchar.png
   :width: 85%
   :align: center
   :alt: cellcharter autok stability

Interpretation:
This figure shows the stability of candidate cluster numbers across repeated runs and helps you assess whether the selected number of spatial domains is reliable.

2. Neighborhood enrichment plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_nhood_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter neighborhood enrichment

Interpretation:
This plot highlights domain-domain adjacency enrichment or depletion and helps identify co-localized or mutually exclusive patterns within the tissue microenvironment.

3. Condition-specific enrichment plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter per-condition enrichment

Interpretation:
In multi-sample mode, CellCharter generates enrichment plots separately for each ``condition_col`` group so that domain organization can be examined within each condition.

4. Differential neighborhood enrichment plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter differential neighborhood enrichment

Interpretation:
This figure compares neighborhood enrichment across conditions and emphasizes domain-domain relationships that change significantly. It is one of the most informative outputs for comparative spatial analysis.

5. Spatial overlay plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_Colon_Cancer_P2_hires_image_Clusters.png
   :width: 85%
   :align: center
   :alt: cellcharter spatial overlay

Interpretation:
This figure overlays spatial domain labels on the tissue image so that you can assess whether the inferred partitioning agrees with tissue morphology and derive a biologically meaningful interpretation of each domain.
