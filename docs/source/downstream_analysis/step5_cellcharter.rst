Module 1: Spatial Domain Modeling (CellCharter)
===============================================

``cellcharter`` runs CellCharter to combine gene-expression information with local spatial-neighborhood structure and identify spatial domains consistent with tissue organization.
In addition to spatial domain identification, the pipeline also incorporates CellCharter's enrichment analysis to compare cell-type enrichment patterns within a single sample or across multiple samples.
In this tutorial, we use an already annotated example dataset to illustrate the spatial domain modeling workflow.

This module supports GPU acceleration. If running in a CPU-only environment, the overall runtime will typically increase substantially.

For the complete parameter configuration reference, see :doc:`../config_reference/advance_analysis_yaml`.


1. Read and preprocess the input object.
2. Construct a feature representation that incorporates spatial neighborhood information.
3. Evaluate stability across a range of candidate cluster numbers and select the most appropriate number of spatial domains.
4. Output single-sample or multi-sample comparison results according to the run branch.

More specifically, the pipeline reads a ``.zarr`` or ``.h5ad`` object and selects a validated non-negative integer count matrix from ``layers["counts"]``, aligned ``raw.X``, or integer-valued ``X``. When ``X`` itself contains counts, it is normalized and log-transformed for the working expression representation while the original counts are retained for scVI. The workflow then builds a generic Delaunay spatial graph, removes long-distance edges with the 99th-percentile threshold, and aggregates three neighborhood layers from ``X_scVI`` into ``X_cellcharter``. AutoK evaluates candidate domain numbers from 2 through ``max_cluster`` and writes the selected labels to ``spatial_cluster``.

Step 1: Configure ``sample.txt``
------------------------------------------------------

The recommended ``sample.txt`` format is as follows; replace ``{sample_id}`` with your own sample ID:

.. code-block:: text

   sample_id   input_path
   {sample_id} results/{sample_id}/annotation/{sample_id}.zarr


Input requirements:

1. The input object must contain spatial coordinate information, which may be stored in ``obsm['spatial']`` or other equivalent convertible fields.
2. It is recommended to use an object that already contains ``celltype`` annotations to ensure that enrichment results have clear biological interpretability.
3. For an integrated object, retain sample identity (``sample_col``) so spatial
   neighbors are not built across tissue sections. Set ``condition_col`` to the
   actual study-group field; Spatialsnake objects normally contain ``group``.
   Distinct conditions and biological replicates are needed for interpreting
   differential neighborhood enrichment.

Step 2: Parameter Selection and Configuration
------------------------------------------------------------------------------------------

In the CellCharter module, the following parameters are usually the most important to understand first:

.. list-table::
   :header-rows: 1
   :widths: 28 18 54

   * - Parameter
     - Example
     - Description
   * - ``runpipe``
     - ``cellcharter``
     - Specifies the current advanced analysis branch as CellCharter
   * - ``max_cluster``
     - ``10``
     - Upper limit for the number of candidate spatial domains; used for automatic evaluation of the optimal number of clusters
   * - ``significance``
     - ``0.05``
     - Significance threshold for enrichment results
   * - ``condition_col``
     - ``condition``
     - Column name used to define condition groups in multi-sample comparison mode
   * - ``sample_col``
     - ``region``
     - Column name used to identify sample origin in multi-sample comparison mode
   * - ``celltype_col``
     - ``celltype``
     - Column name of the cell-type annotation in the input object, used for enrichment analysis
   * - ``cellcharter_col``
     - ``spatial_cluster``
     - Column name used when writing CellCharter spatial domain labels back into the object
   * - ``image_type``
     - ``hires``
     - Image layer used for spatial overlay display
   * - ``shape_type``
     - ``cell_boundaries``
     - Layer used for spatial boundary visualization

Configuration recommendations:

1. ``max_cluster`` directly affects the range over which the number of spatial domains is automatically selected. If the tissue structure is more complex, it can be increased moderately; if the sample size is small, it should not be set too high.
2. If you are interested in spatial organization differences between conditions, ``condition_col`` and ``sample_col`` must be accurately set; otherwise robust cross-condition enrichment comparison results cannot be generated.
3. ``celltype_col`` and ``cellcharter_col`` respectively determine the read/write logic for input annotations and output spatial domain labels, and are the most critical column-name parameters for interpreting results.

For optional customization, save these fields as ``advance_analysis.yaml``
and append ``--configfile=advance_analysis.yaml``; see :ref:`cli-configuration`.
Keep ``device=auto`` for automatic CPU/CUDA selection, or explicitly set
``device=cpu`` or ``device=cuda``.

A typical configuration example:

.. code-block:: yaml

   image_type: "hires"
   shape_type: "cell_boundaries"
   significance: 0.05
   max_cluster: 10
   condition_col: "condition"
   sample_col: "region"
   celltype_col: "celltype"
   cellcharter_col: "spatial_cluster"


Step 3: Run the Command
----------------------------------------------

Once input preparation and parameter confirmation are complete, run:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellcharter


Using the annotated example spatial object, the following demonstrates the standard CellCharter workflow.

1. Prepare the input object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use ``Colon_Cancer_P2_008um`` from the core analysis annotation step as the example dataset. Ensure that the preceding core analysis and annotation steps have already been completed.

sample.txt:

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

2. Set the key parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this demonstration, the default parameters are sufficient. For other samples, adjust the parameters as appropriate.

3. Run CellCharter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=advance_analysis --runpipe=cellcharter


Spatialsnake uses GPU acceleration automatically when a GPU is available. If no GPU is detected, it falls back to CPU computation. Ensure that sufficient GPU memory is available when running the accelerated version.

Result file structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Single-sample output (default mode):

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
         └── cellcharter/
               ├── Colon_Cancer_P2_008um_cellcharter.zarr/
               ├── Colon_Cancer_P2_008um_celchar.png
               ├── Colon_Cancer_P2_008um_enrichment.png
               ├── Colon_Cancer_P2_008um_nhood_enrichment.png
               ├── Colon_Cancer_P2_008um_<image_name>_Clusters.png
               └── *_cell_clusters.csv


Here, ``{sample}_diff_enrichment.png`` is generated only when all of the following conditions are met simultaneously:

1. The pipeline is running in the multi-sample comparison branch (``channel=compare_analysis``).
2. ``condition_col`` in the input object contains at least two condition groups.
3. ``sample_col`` is present in the input object to support sample-level neighborhood comparison.


1. Clustering stability plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_celchar.png
   :width: 85%
   :align: center
   :alt: cellcharter autok stability

This figure displays the stability of different candidate cluster numbers across repeated runs and is used to judge whether the final selected number of spatial domains is reliable.


2. Neighborhood enrichment plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_nhood_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter neighborhood enrichment

This figure displays adjacency enrichment or exclusion relationships among different spatial domains and helps identify co-localization patterns or mutually exclusive structures within the tissue microenvironment.


3. Cell-type enrichment within spatial domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_enrichment.png
   :width: 85%
   :align: center
   :alt: Cell-type enrichment within CRC P2 CellCharter domains

This single-sample dotplot summarizes enrichment of the existing ``celltype``
labels within CellCharter domains. It is not a condition comparison. Differential
neighborhood enrichment is a separate multi-sample output
(``*_diff_enrichment.png``), not illustrated by this CRC P2 Demo.

4. Spatial domain map
~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/CRC_P2_cellcharter_native_spatial.png
   :width: 85%
   :align: center
   :alt: Native CellCharter tissue image and spatial domain overlay

The native output shows the tissue image above the domain overlay. Its filename
includes the image element name; image-free objects use ``*_spatial_Clusters.png``.
Use this view with the enrichment and stability plots to assess spatial domains,
not as a direct cell-type annotation.
