Module 6: Cell Communication Network Analysis (cellchat)
========================================================

``cellchat`` infers cell-cell communication networks from ligand-receptor relationships among annotated cell types and quantifies interaction number, interaction strength, and pathway-level information flow.
In spatial mode, the workflow incorporates the spatial distance between cells or spots when estimating communication probabilities, so providing scale-factor files is strongly recommended for reliable distance calibration.

This module supports single-sample spatial data, integrated replicate samples, and single-cell input:

1. Multi-sample integration is recommended only for biological replicates generated under the **same experimental condition**.
2. If you need to compare different experimental conditions, run this module separately for each condition and then use ``compare_stage`` with comparative CellChat analysis.
3. Single-cell input can be enabled with ``is_single_cell=True`` and does not require spatial distance parameters.

In this tutorial, we use ``Colon_Cancer_P2_008um.h5ad`` for CellChat analysis.
To reduce memory usage, convert the reannotated object to conventional ``h5ad`` format before running the workflow.

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/Colon_Cancer_P2_008um/reannotation/Colon_Cancer_P2_008um.zarr --transform_from=zarr --transform_to=h5ad


Workflow overview
-----------------

1. **Read the input and convert it into a CellChat-compatible object**
   Automatically detect ``.h5ad`` or ``.rds`` input and build the CellChat object using the selected ``celltype_col`` as the grouping variable.
2. **Select the database and signaling category**
   Choose ``CellChatDB.human`` or ``CellChatDB.mouse`` according to ``species`` and focus on the Secreted Signaling subset.
3. **Calibrate spatial distances in spatial mode**
   Read the coordinates and rescale them using ``scale_factors`` or ``scale_factors_list`` so that communication probabilities are estimated on a biologically meaningful distance scale.
4. **Infer communication probabilities and pathway-level structure**
   Run overexpressed gene and interaction detection, communication probability inference, low-cell-count filtering, pathway inference, and network aggregation.
5. **Summarize network structure and mechanism-level outputs**
   Generate communication network plots, pathway information-flow summaries, heatmaps, and LR-level tables for downstream interpretation and validation.

.. note::
   This module produces the core figures and CSV tables required to summarize ligand-receptor communication in the current dataset.
   If you want more detailed visualization, or if you want to compare communication strength between different experimental conditions, continue to :doc:`step9_compare_stage_cellchat`.
   That downstream comparison step uses the ``cellchat.rds`` object produced here as its input.
   For datasets with different experimental conditions, run this module separately for each condition first. Integrated CellChat analysis in this step is intended only for biological replicates from the same condition.

Prepare the input files
-----------------------

Scenario 1: single-sample spatial data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   input_path  scale_factor_path
   Colon_Cancer_P2_008um results/useful_results/Colon_Cancer_P2_008um.h5ad results/Colon_Cancer_P2_008um/scale_factor.json

Scenario 2: integrated replicate samples from the same condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   input_path  scale_factor_path
   SampleA_Rep1  results/SampleA_Rep1/annotation/SampleA_Rep1.h5ad  results/SampleA_Rep1/scale_factor.json
   SampleA_Rep2  results/SampleA_Rep2/annotation/SampleA_Rep2.h5ad  results/SampleA_Rep2/scale_factor.json

Scenario 3: single-cell input (non-spatial mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   input_path
   sc_sample   results/sc_sample/annotation/sc_sample.rds

Notes:

1. Input can be ``.h5ad`` or ``.rds``; the workflow detects the format automatically.
2. The object must contain a cell-type annotation column, typically ``celltype``.
3. Multi-sample integration is intended only for same-condition replicates. Cross-condition comparison should be performed later in the CellChat comparison module.
4. Scale-factor files are recommended in spatial mode but are unnecessary in single-cell mode.


Optional configuration
----------------------

For the configuration reference, see :doc:`../config_reference/advance_analysis_yaml`.


.. list-table::
   :header-rows: 1
   :widths: 24 24 52

   * - Parameter
     - Typical values
     - Description
   * - ``runpipe``
     - ``cellchat``
     - Selects the CellChat branch
   * - ``celltype_col``
     - ``celltype``
     - Cell-type annotation column
   * - ``species``
     - ``human`` / ``mouse``
     - Species used to select the CellChat database
   * - ``assay``
     - ``Spatial``
     - Analysis type label
   * - ``min_cells``
     - ``10``
     - Minimum cell number used to filter very small groups
   * - ``workers``
     - ``32``
     - Number of parallel workers
   * - ``scale_factors``
     - ``results/S1/scale_factor.json``
     - Scale-factor file for single-sample spatial distance calibration
   * - ``scale_factors_list``
     - ``sf1.json,sf2.json``
     - Comma-separated list of scale-factor files for multi-sample analysis
   * - ``sample_names``
     - ``SampleA_Rep1,SampleA_Rep2``
     - Sample names corresponding to ``scale_factors_list``
   * - ``spot_size``
     - ``65``
     - Reference diameter used for multi-sample spatial standardization
   * - ``trim``
     - ``0.1``
     - Truncation proportion for ``truncatedMean``, affecting robustness
   * - ``interaction_length``
     - ``150``
     - Spatial communication distance threshold
   * - ``is_single_cell``
     - ``False``
     - When ``True``, runs in single-cell mode without spatial distances

.. code-block:: bash

   celltype_col: "celltype"
   assay: "Spatial"  # specify the analysis mode
   species: "human"
   min_cells: 10
   workers: 32
   is_single_cell: FALSE
   trim: 0.1
   interaction_length: 250


Run the command
------------------------------

.. code-block:: bash

   # single sample
   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat
   # multi-sample replicate analysis
   spatialsnake compare_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat


Differences between single-sample and multi-sample results
----------------------------------------------------------

1. Both modes generate network plots, information-flow summaries, heatmaps, and LR-level statistics.
2. The integrated multi-sample result reflects the overall communication pattern across same-condition replicates and should not be interpreted as a cross-condition comparison.
3. To compare condition A with condition B, run CellChat separately for each condition and then proceed to the comparative CellChat module.

Result file structure
---------------------

.. code-block:: text

   results/
   └── {sample}/
       └── cellchat/
           ├── cellchat.rds
           ├── {sample}_cellchat_network.png
           ├── {sample}_cellchat_network.pdf
           ├── {sample}_cellchat_infoflow_bar.png
           ├── {sample}_cellchat_count_heatmap.png
           ├── {sample}_cellchat_heatmap.png
           ├── {sample}_cellchat_signaling_role_network.png
           ├── {sample}_cellchat_signaling_role_scatter.png
           ├── {sample}_cellchat_signaling_role_outgoing.png
           ├── {sample}_cellchat_signaling_role_incoming.png
           ├── {sample}_cellchat_stats.csv
           ├── {sample}_cellchat_lr.csv
           ├── {sample}_cellchat_lr_summary.csv
           ├── {sample}_cellchat_pathway_pairs.csv
           ├── {sample}_cellchat_pathway_summary.csv
           └── {sample}_cellchat_pathway_net.csv

How to interpret the results
----------------------------

1. Network overview plot
~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_network.png
   :width: 85%
   :align: center
   :alt: cellchat network

Interpretation:
The left panel shows the number of interactions between cell groups, whereas the right panel shows interaction strength. These figures are useful for quickly identifying communication hubs and the dominant sender-receiver relationships.

2. Information-flow bar plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_infoflow_bar.png
   :width: 85%
   :align: center
   :alt: cellchat info flow

Interpretation:
This plot compares information flow across signaling pathways and helps prioritize the most active or biologically relevant communication programs.

3. Communication heatmaps
~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_heatmap.png
   :width: 85%
   :align: center
   :alt: cellchat heatmap

Interpretation:
``count_heatmap`` summarizes the number of interactions between cell groups, whereas ``cellchat_heatmap`` summarizes interaction weight. Viewed together, they help distinguish communication programs that are widespread but weak from those that are sparse but strong.

4. Signaling-role plots
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_signaling_role_scatter.png
   :width: 85%
   :align: center
   :alt: cellchat signaling role scatter

Interpretation:
For one automatically selected signaling pathway, the workflow generates network, scatter, outgoing, and incoming role plots. These figures help you examine which cell groups act as senders, receivers, or central intermediates within that pathway.

5. LR-level detail and summary statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interpretation:
``lr.csv`` contains ligand-receptor evidence at the individual interaction level, whereas ``lr_summary.csv`` provides aggregated interaction strength and significance by LR pair. Together, they form one of the main foundations for mechanistic interpretation and reproducible follow-up analysis.
