Module 6: Cell Communication Network Analysis (cellchat)
========================================================

``cellchat`` is a downstream communication-analysis module that infers cell-cell signaling relationships from ligand-receptor pairs and summarizes how strongly different cell groups communicate with one another.
For spatial transcriptomics data, the workflow further considers physical distance between spots or cells so that the inferred communication probabilities better match tissue architecture.

This module is suitable for three common scenarios:

1. **Single-cell data**
   Use this mode when the input is conventional single-cell expression data without spatial coordinates.
2. **One spatial transcriptomics sample**
   Use this mode when you want to reconstruct the communication network within one tissue section or one spatial sample.
3. **Multiple spatial replicates from the same experimental condition**
   Use this mode when the samples are biological replicates of the same condition and you want an integrated communication result.

.. important::
   Multiple spatial samples should be integrated in this module only when they belong to the same biological condition.
   If the goal is to compare two or more different conditions, first run CellChat separately for each condition and then perform downstream comparative analysis.

What This Module Does
---------------------

At the user level, the workflow can be understood as the following sequence:

1. **Load the annotated expression object**
   The input object must already contain cell-type labels or another biologically meaningful grouping variable.
2. **Define communication groups**
   CellChat uses the selected annotation column to determine which cell populations will act as candidate senders and receivers.
3. **Match ligand-receptor information**
   The workflow selects the species-specific communication database and searches for signaling relationships supported by the observed expression data.
4. **Incorporate spatial structure when applicable**
   For spatial data, the workflow uses spot or cell coordinates together with platform-appropriate spatial scaling information.
5. **Estimate communication probability**
   Interaction strength is inferred at the ligand-receptor level and then summarized to signaling pathways and cell-group networks.
6. **Generate interpretable outputs**
   The module produces network plots, pathway summaries, heatmaps, and ligand-receptor tables for biological interpretation.

.. note::
   This module produces the core figures and CSV tables required to summarize ligand-receptor communication in the current dataset.
   If you want more detailed visualization, or if you want to compare communication strength between different experimental conditions, continue to :doc:`step9_compare_stage_cellchat`.
   That downstream comparison step uses the ``cellchat.rds`` object produced here as its input.
   For datasets with different experimental conditions, run this module separately for each condition first. Integrated CellChat analysis in this step is intended only for biological replicates from the same condition.

How To Prepare and Run This Module
----------------------------------

The practical workflow can be organized into five steps.

Step 1. Confirm the analysis scenario
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before preparing files, first decide which of the following scenarios matches your study design:

1. **Single-cell data**
   Use this setting when the data contain no spatial coordinates. In this case, the module focuses entirely on expression-defined communication and does not require spatial scaling information.
2. **One spatial sample**
   Use this setting when the goal is to characterize communication within one tissue section.
3. **Multiple spatial samples from the same condition**
   Use this setting only for same-condition replicates. The resulting network represents the integrated communication pattern of that condition rather than a comparison between conditions.

Step 2. Prepare the input object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The input object should already be annotated and ready for downstream communication analysis. In practical terms, this means:

1. The object contains a biologically meaningful grouping column, usually a cell-type annotation.
2. The expression matrix is available in a standard format compatible with the workflow.
3. Spatial datasets retain valid spot or cell coordinates.
4. For spatial analysis, the platform-specific information required to interpret spatial distances is available.

Step 3. Write ``sample.txt`` according to platform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The structure of ``sample.txt`` depends on both the data platform and the analysis scenario. The first two columns always identify the sample and its input object. The main difference lies in whether a third column is required and what it means biologically.

Practical formatting rules:

1. Keep the header row.
2. Use one sample per line.
3. Separate columns with tabs or spaces consistently.
4. Do not omit the third column when the selected platform requires it.

General rule:

1. **Single-cell input**
   Usually requires only two columns: sample identifier and input object.
2. **Spatial input**
   May require an additional platform-specific third column so that the workflow can convert image-space or bin-space distances into a biologically meaningful spatial scale.

Why the third column differs across platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Different spatial platforms use different coordinate systems:

1. **Visium-family platforms**
   The coordinates are linked to image resolution and spot geometry. Therefore, a scale-factor description is needed to translate coordinate distances into spot-scale distances.
2. **Stereo-seq**
   The key spatial unit is often a bin or a cell-bin definition. The workflow therefore expects a bin-related specification rather than an image-derived scale-factor file.
3. **MERFISH, MERSCOPE, and Xenium**
   These platforms usually provide coordinates at higher spatial resolution, often closer to the cell level. The workflow can use platform defaults for spatial scaling more directly, so an extra third-column specification is typically not required.

Suggested ``sample.txt`` layouts by platform
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Visium-family platforms

Single spatial sample:

.. code-block:: bash

   sample_id	input_path	scale_factor
   SampleA	/path/to/SampleA.h5ad	/path/to/SampleA_scalefactors_json.json

Multiple spatial replicates from the same condition:

.. code-block:: bash

   sample_id	input_path	scale_factor
   Rep1	/path/to/concatenated_sdata.zarr	/path/to/Rep1_scalefactors_json.json
   Rep2	/path/to/concatenated_sdata.zarr	/path/to/Rep2_scalefactors_json.json
   Rep3	/path/to/concatenated_sdata.zarr	/path/to/Rep3_scalefactors_json.json

Explanation:
The third column should contain the scale-factor description associated with each sample. For Visium-family data, communication distance should be calibrated relative to the physical spot geometry rather than raw image coordinates alone.

Stereo-seq

Single bin-based sample:

.. code-block:: bash

   sample_id	input_path	bin_or_cellbin
   StereoA	/path/to/StereoA.h5ad	50

Single cell-bin sample:

.. code-block:: bash

   sample_id	input_path	bin_or_cellbin
   StereoCellBin	/path/to/StereoCellBin.h5ad	cellbin

Multiple Stereo-seq replicates from the same condition:

.. code-block:: bash

   sample_id	input_path	bin_or_cellbin
   Rep1	/path/to/concatenated_sdata.zarr	50
   Rep2	/path/to/concatenated_sdata.zarr	50
   Rep3	/path/to/concatenated_sdata.zarr	50

Explanation:
For Stereo-seq, the third column is not an image scale-factor file. It must record the spatial aggregation unit, usually a bin size or ``cellbin``. This determines how the workflow interprets the physical size of each observation and therefore directly affects spatial communication modeling.

MERFISH, MERSCOPE, and Xenium

Single spatial sample:

.. code-block:: bash

   sample_id	input_path
   XeniumA	/path/to/XeniumA.h5ad

Multiple spatial replicates from the same condition:

.. code-block:: bash

   sample_id	input_path
   Rep1	/path/to/concatenated_sdata.zarr
   Rep2	/path/to/concatenated_sdata.zarr
   Rep3	/path/to/concatenated_sdata.zarr

Explanation:
These platforms usually provide higher-resolution coordinates, so the workflow can generally proceed without an additional third-column specification. In this case, the spatial scale is handled using platform-level defaults.

Single-cell data

Single dataset:

.. code-block:: bash

   sample_id	input_path
   sc_sample	/path/to/sc_sample.rds

Integrated single-cell object:

.. code-block:: bash

   sample_id	input_path
   sc_integrated	/path/to/sc_integrated.h5ad

Explanation:
Because there is no spatial geometry in standard single-cell data, no third column is needed for spatial calibration.

How to set ``sample.txt`` for different sample organizations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Single-cell data

1. Prepare one row per sample.
2. Provide the sample identifier and input object.
3. Enable single-cell mode in the parameter configuration.
4. No spatial scale information is required.

Recommended template:

.. code-block:: bash

   sample_id	input_path
   sc_sample	/path/to/sc_sample.rds

One spatial transcriptomics sample

1. Prepare one row for the sample.
2. Provide the sample identifier and input object.
3. Add the platform-appropriate third-column information when required.
4. Keep spatial mode enabled.

Recommended templates:

Visium-family:

.. code-block:: bash

   sample_id	input_path	scale_factor
   SampleA	/path/to/SampleA.h5ad	/path/to/SampleA_scalefactors_json.json

Stereo-seq:

.. code-block:: bash

   sample_id	input_path	bin_or_cellbin
   StereoA	/path/to/StereoA.h5ad	50

MERFISH, MERSCOPE, or Xenium:

.. code-block:: bash

   sample_id	input_path
   XeniumA	/path/to/XeniumA.h5ad

Multiple spatial replicates from the same condition

1. Prepare one row per replicate.
2. Use consistent platform-specific formatting across all rows.
3. Ensure all samples belong to the same biological condition.
4. For platforms that require a third column, every sample should provide its own matching spatial-scale specification.
5. In ``compare_analysis`` mode, all rows should point to the same integrated object in the second column; the different rows are used to preserve per-sample names and per-sample spatial calibration information.

Recommended templates:

Visium-family:

.. code-block:: bash

   sample_id	input_path	scale_factor
   Rep1	/path/to/concatenated_sdata.zarr	/path/to/Rep1_scalefactors_json.json
   Rep2	/path/to/concatenated_sdata.zarr	/path/to/Rep2_scalefactors_json.json

Stereo-seq:

.. code-block:: bash

   sample_id	input_path	bin_or_cellbin
   Rep1	/path/to/concatenated_sdata.zarr	50
   Rep2	/path/to/concatenated_sdata.zarr	50

MERFISH, MERSCOPE, or Xenium:

.. code-block:: bash

   sample_id	input_path
   Rep1	/path/to/concatenated_sdata.zarr
   Rep2	/path/to/concatenated_sdata.zarr

Platform-specific spatial parameters and auto-selection logic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In CellChat spatial analysis, ``spot.diameter`` represents the effective physical size of one observation unit.
This value cannot be shared across platforms because different technologies do not measure the tissue at the same spatial resolution.
Some platforms summarize transcripts in relatively large spots, whereas others work at bin-level or near single-cell resolution.
As a result, the same coordinate distance can correspond to very different biological distances across platforms.

According to the official CellChat spatial tutorial and the discussion in issue ``#6``, spatial distances should be interpreted on a biologically meaningful scale.
Therefore, ``spot.diameter`` should be set either from an officially provided platform description or from a platform-specific calculation based on the true spatial unit.

How ``spot.diameter`` is selected for each platform
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 18 18 28 36

   * - Platform
     - Selection type
     - Basis
     - Current workflow behavior
   * - ``Visium``
     - Official recommendation
     - Standard spot diameter defined by the platform
     - Uses ``65`` as the default ``spot.diameter`` and reads the third-column JSON information to recover the coordinate-to-spot relationship
   * - ``Visium HD``
     - Calculated from dataset naming or user setting
     - Effective bin size may differ by dataset
     - First tries to infer the bin size from the input name; if not available, falls back to the configured ``cellchat_spot_size``; still requires the third-column JSON description
   * - ``Visium segment``
     - Practical default with optional override
     - Observation units are smaller than standard Visium spots
     - Uses the Visium-family scale-factor branch but defaults to a smaller observation size unless the user provides a custom value
   * - ``Stereo-seq`` bin mode
     - Platform-specific calculation
     - The true spatial unit depends on the bin definition
     - Reads the third column as a positive bin size and converts it internally to the effective ``spot.diameter`` using the workflow's Stereo-seq rule
   * - ``Stereo-seq`` cell-bin mode
     - Platform-specific calculation
     - The observation unit is a cell-bin rather than a classical spot
     - Reads the third column as ``cellbin`` and switches to the dedicated cell-bin branch with a small default physical unit
   * - ``MERFISH`` / ``MERSCOPE`` / ``Xenium``
     - Practical default with optional override
     - These platforms are already high resolution and closer to cell-level coordinates
     - Uses a small default ``spot.diameter`` when the user does not override it, without requiring a third-column scale-factor file

Basic principle behind the choice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **If the platform already defines a standard physical spot size**
   The workflow follows the official or widely used platform recommendation.
2. **If the platform uses bins or cell-bins**
   The workflow derives the effective spatial unit from the bin specification, because the correct scale depends on how the data were aggregated.
3. **If the platform is already near single-cell resolution**
   The workflow uses a smaller default physical unit, because each observation corresponds to a much more localized spatial entity.

In short, ``spot.diameter`` should always match the real biological observation unit of the platform rather than the raw coordinate number itself.

Step 4. Configure key parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the configuration reference, see :doc:`../config_reference/advance_analysis_yaml`.

The following parameters are the most important for routine use:

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
     - Annotation column used to define communicating cell groups
   * - ``cellchat_species``
     - ``human`` / ``mouse``
     - Selects the species-specific ligand-receptor database
   * - ``cellchat_assay``
     - ``Spatial``
     - Indicates the analysis context used by the module
   * - ``cellchat_min_cells``
     - ``10``
     - Filters out very small cell groups that are unlikely to support robust communication inference
   * - ``cellchat_workers``
     - A moderate or high integer depending on available CPU resources
     - Controls parallel computation
   * - ``cellchat_is_single_cell``
     - ``False`` or ``True``
     - Switches between spatial mode and single-cell mode
   * - ``cellchat_trim``
     - ``0.1``
     - Controls robustness of the truncated-mean strategy used during probability estimation
   * - ``cellchat_interaction_length``
     - Platform- and tissue-dependent
     - Sets the effective spatial communication range in spatial mode
   * - ``cellchat_spot_size``
     - Platform-dependent
     - Represents the effective observation diameter or cell-size proxy used for spatial scaling

How to think about parameter choice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **``celltype_col``**
   This should correspond to the annotation level that is biologically interpretable for communication analysis. If the grouping is too coarse, meaningful cell-state differences may be masked. If it is too fine, some groups may become too small for robust inference.
2. **``cellchat_species``**
   This must match the species of the dataset, because ligand-receptor databases are species-specific.
3. **``cellchat_is_single_cell``**
   Set this to single-cell mode only when the input truly lacks spatial geometry. Spatial datasets should remain in spatial mode even if each observation is close to a single cell.
4. **``cellchat_interaction_length``**
   This should be interpreted biologically as the expected signaling range. Short-range signaling and broad tissue-level signaling need different values.
5. **``cellchat_spot_size``**
   This should reflect the physical size of the observation unit. The more aggregated each spot or bin is, the larger this value should generally be.

Step 5. Run according to the study design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After ``sample.txt`` and the core parameters are prepared, choose the run mode according to the biological design:

1. **Single-cell dataset**
   Use the single-sample workflow with single-cell mode enabled.
2. **One spatial sample**
   Use the single-sample workflow in spatial mode.
3. **Multiple spatial samples from the same condition**
   Use the multi-sample workflow in spatial mode with one row per replicate.

The key principle is simple:

1. Use **single-sample analysis** when the goal is to characterize one dataset.
2. Use **multi-sample integration** when the goal is to summarize one biological condition using multiple replicates.
3. Do **not** use this integration step to compare different conditions directly.

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
   * - ``cellchat_species``
     - ``human`` / ``mouse``
     - Species used to select the CellChat database
   * - ``cellchat_assay``
     - ``Spatial``
     - Analysis type label
   * - ``cellchat_min_cells``
     - ``10``
     - Minimum cell number used to filter very small groups
   * - ``cellchat_workers``
     - ``4`` or a larger value on multi-core machines
     - Number of parallel workers
   * - ``cellchat_spot_size``
     - ``65``
     - Reference spot diameter or cell size proxy used during spatial scaling; default interpretation depends on platform
   * - ``cellchat_trim``
     - ``0.1``
     - Truncation proportion for ``truncatedMean``, affecting robustness
   * - ``cellchat_interaction_length``
     - ``150``
     - Spatial communication distance threshold
   * - ``cellchat_is_single_cell``
     - ``False``
     - When ``True``, runs in single-cell mode without spatial distances

Copyable configuration examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Single-cell mode:

.. code-block:: bash

   celltype_col: "celltype"
   cellchat_species: "human"
   cellchat_is_single_cell: True
   cellchat_min_cells: 10
   cellchat_trim: 0.1

Single spatial sample:

.. code-block:: bash

   celltype_col: "celltype"
   cellchat_species: "human"
   cellchat_is_single_cell: False
   cellchat_interaction_length: 250
   cellchat_spot_size: 65
   cellchat_min_cells: 10
   cellchat_trim: 0.1

Higher-resolution spatial platforms:

.. code-block:: bash

   celltype_col: "celltype"
   cellchat_species: "human"
   cellchat_is_single_cell: False
   cellchat_interaction_length: 150
   cellchat_spot_size: 10
   cellchat_min_cells: 10
   cellchat_trim: 0.1

Run commands
------------

Single-cell dataset:

First set ``cellchat_is_single_cell: True`` in the configuration file, then run:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat

Explanation:
When ``cellchat_is_single_cell`` is enabled, the workflow skips spatial calibration. The command still uses a standard workflow entry token, but the analysis itself is performed in single-cell mode.

Single spatial Visium-family sample:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat

Single spatial Visium HD sample:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=advance_analysis --runpipe=cellchat

Single spatial Visium segment sample:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_segment --option=advance_analysis --runpipe=cellchat

Single Stereo-seq sample:

.. code-block:: bash

   spatialsnake single_analysis sample.txt stereo-seq --option=advance_analysis --runpipe=cellchat

Single MERFISH sample:

.. code-block:: bash

   spatialsnake single_analysis sample.txt Merfish --option=advance_analysis --runpipe=cellchat

Single Xenium sample:

.. code-block:: bash

   spatialsnake single_analysis sample.txt xenium --option=advance_analysis --runpipe=cellchat

Multiple same-condition spatial replicates after integration:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat

Multiple same-condition Stereo-seq replicates after integration:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt stereo-seq --option=advance_analysis --runpipe=cellchat

Important note for ``compare_analysis``:

.. code-block:: bash

   1. Use one row per sample in sample.txt.
   2. Keep the second column identical across rows.
   3. The second column must be the integrated object path.
   4. The sample-specific information is preserved through the sample ID and the platform-specific third column.


Differences between single-sample and multi-sample results
----------------------------------------------------------

1. Both modes generate network plots, information-flow summaries, heatmaps, and LR-level statistics.
2. The integrated multi-sample result reflects the overall communication pattern across same-condition replicates and should not be interpreted as a cross-condition comparison.
3. To compare condition A with condition B, run CellChat separately for each condition and then proceed to the comparative CellChat module.

Result file structure
---------------------

The module produces one communication-analysis result set for each run. The main output categories are:

1. **Serialized CellChat object**
   This object preserves the inferred communication model and can be reused in later comparative analysis.
2. **Network overview figures**
   These summarize the number and strength of interactions among cell groups.
3. **Pathway-level summary figures**
   These show which signaling programs dominate the current dataset.
4. **Heatmaps and signaling-role plots**
   These help interpret sender, receiver, and pathway-centrality patterns.
5. **Ligand-receptor and pathway summary tables**
   These provide the tabular evidence needed for downstream validation, filtering, and biological reporting.

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
