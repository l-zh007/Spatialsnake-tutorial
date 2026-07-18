Module 6: Cell Communication Network Analysis (CellChat)
========================================================

``cellchat`` is a downstream module for cell-cell communication analysis. It infers signaling relationships from ligand-receptor pairs and summarizes the strength of communication between cell populations.
For spatial transcriptomics data, the workflow also accounts for physical distance between spots or cells across different platforms, allowing the inferred communication probabilities to better reflect tissue architecture.

What This Module Does
---------------------

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
   This module generates the core figures and CSV tables required to summarize ligand-receptor communication in the current dataset.
   For more detailed visualization, or to compare communication strength across experimental conditions, continue to :doc:`step9_compare_stage_cellchat`.
   That downstream comparison step uses the ``cellchat.rds`` object produced here as its input.
   For datasets with different experimental conditions, run this module separately for each condition first. Integrated CellChat analysis in this step is intended only for biological replicates from the same condition.
   In spatial mode, the communication range is primarily controlled by ``cellchat_interaction_length`` together with the platform-specific spatial scale.

How To Prepare and Run This Module
----------------------------------

Step 1. Confirm the analysis scenario
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before preparing files, first decide which of the following scenarios matches your study design:

1. **Single-cell data**
   Use this setting when the data contain no spatial coordinates. In this case, the module focuses entirely on expression-defined communication and does not require spatial scaling information.
2. **Single spatial sample**
   Use this setting when the goal is to characterize communication within a single tissue section. Spatialsnake automatically reads the spatial coordinates from the sample object and uses them to constrain communication distance.
3. **Multiple spatial samples from the same condition**
   Use this setting only for biological replicates from the same condition. The resulting network represents the integrated communication pattern of that condition rather than a between-condition comparison.
4. **The spatial transcriptomics platform used in the analysis**
   Select the command-line platform type that matches the coordinate system and observation unit in the input object. This choice determines how scale factors, spot or bin size, and spatial distance are interpreted.

.. important::
   Multiple spatial samples should be integrated in this module only when they belong to the same biological condition.
   If the goal is to compare two or more different conditions, first run CellChat separately for each condition and then perform downstream comparative analysis.
   For same-condition spatial replicates, the integrated object must retain separate image or slice identities and valid coordinates for every observation.
   CellChat releases that accept ``spatial.factors`` can use the per-slice factors supplied by this workflow. With older CellChat releases, including version 1.6.1, per-slice factors are not accepted by ``computeCommunProb()``; in that environment, analyze slices separately unless their coordinate systems have been made explicitly non-overlapping before integration.

Step 2. Prepare the input object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The input object should already be annotated and ready for downstream communication analysis. In practical terms, this means:

1. Ensure that the object has completed annotation and contains the column specified by ``celltype_col``. At least two valid cell groups are required.
2. Use an ``h5ad`` or Seurat ``rds`` object. If the data are stored as SpatialData ``zarr``, convert the object to ``h5ad`` before running this module.
3. Ensure that the active assay contains a non-negative normalized expression matrix in its ``data`` layer. The workflow reads this layer first and uses the count layer only as a compatibility fallback.
4. Remove empty annotation values and inspect group sizes. Groups with fewer observations than ``cellchat_min_cells`` are reported and may be filtered from communication inference.
5. For spatial mode, retain coordinates and platform image information in the object. For single-cell mode, coordinates are not required.

.. note::
   CellChat communication probabilities are statistical predictions supported by expression, database annotation, and, in spatial mode, physical proximity. They do not by themselves demonstrate direct molecular interaction and should be interpreted together with expression support and biological context.

Step 3. Write ``sample.txt`` according to platform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``sample.txt`` differs across platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We synthesized recommendations from the CellChat authors together with guidance from GitHub community discussions to optimize the workflow for spatial transcriptomics analysis. Because spot or cell spacing differs across platforms, different parameter settings are required for accurate communication modeling. Users therefore need to provide the appropriate platform field or bin size so that the workflow can select the most suitable spatial settings automatically. This design also reduces manual tuning and allows users to focus on biological interpretation.

1. **Visium-family platforms**
   The coordinates are linked to image resolution and spot geometry. Therefore, a scale-factor description is needed to translate coordinate distances into spot-scale distances.
2. **Stereo-seq**
   The key spatial unit is often a bin or a cell-bin definition. The workflow therefore expects a bin-related specification rather than an image-derived scale-factor file.
3. **MERFISH, MERSCOPE, and Xenium**
   These platforms usually provide coordinates at higher spatial resolution, often approaching single-cell resolution. The workflow can therefore rely more directly on platform defaults for spatial scaling, and an additional third-column specification is typically unnecessary.

Visium-family platforms

Single spatial sample:

.. code-block:: text

   sample_id    input_path    scale_factor
   SampleA    /path/to/SampleA.h5ad    /path/to/SampleA_scalefactors_json.json

Multiple spatial replicates from the same condition:

.. code-block:: text

   sample_id    input_path    scale_factor
   Rep1    /path/to/condition_integrated.h5ad    /path/to/Rep1_scalefactors_json.json
   Rep2    /path/to/condition_integrated.h5ad    /path/to/Rep2_scalefactors_json.json
   Rep3    /path/to/condition_integrated.h5ad    /path/to/Rep3_scalefactors_json.json

Explanation:
The third column should contain the scale-factor description associated with each sample. For Visium-family data, communication distance should be calibrated relative to the physical spot geometry rather than raw image coordinates alone.
For same-condition integration, each row points to the same integrated ``h5ad`` object while providing the scale-factor file for the corresponding image or slice.
The image names stored in the object should match the sample identifiers whenever possible.

Stereo-seq

Single bin-based sample:

.. code-block:: text

   sample_id    input_path    bin_or_cellbin
   StereoA    /path/to/StereoA.h5ad    50

Single cell-bin sample:

.. code-block:: text

   sample_id    input_path    bin_or_cellbin
   StereoCellBin    /path/to/StereoCellBin.h5ad    cellbin

Multiple Stereo-seq replicates from the same condition:

.. code-block:: text

   sample_id    input_path    bin_or_cellbin
   Rep1    /path/to/condition_integrated.h5ad    50
   Rep2    /path/to/condition_integrated.h5ad    50
   Rep3    /path/to/condition_integrated.h5ad    50

Explanation:
For Stereo-seq, the third column is not an image scale-factor file. Instead, it records the spatial aggregation unit, usually a bin size or ``cellbin``. This directly determines how the workflow interprets the physical size of each observation and therefore affects spatial communication modeling.

MERFISH, MERSCOPE, and Xenium

Single spatial sample:

.. code-block:: text

   sample_id    input_path
   XeniumA    /path/to/XeniumA.h5ad

Multiple spatial replicates from the same condition:

.. code-block:: text

   sample_id    input_path
   Rep1    /path/to/condition_integrated.h5ad
   Rep2    /path/to/condition_integrated.h5ad
   Rep3    /path/to/condition_integrated.h5ad

Explanation:
These platforms usually provide higher-resolution coordinates, so the workflow can generally proceed without an additional third-column specification. In these cases, spatial scaling is handled using platform-level defaults.

Single-cell data

Single dataset:

.. code-block:: text

   sample_id    input_path
   sc_sample    /path/to/sc_sample.rds

Explanation:
Because there is no spatial geometry in standard single-cell data, no third column is needed for spatial calibration.

Run the command for the selected platform
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the platform keyword that matches the input object:

.. code-block:: bash

   # Standard Visium
   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat

   # Visium HD
   spatialsnake single_analysis sample.txt visium_HD --option=advance_analysis --runpipe=cellchat

   # Visium segmentation
   spatialsnake single_analysis sample.txt visium_segment --option=advance_analysis --runpipe=cellchat

   # Stereo-seq
   spatialsnake single_analysis sample.txt stereoseq --option=advance_analysis --runpipe=cellchat

   # Xenium or MERFISH/MERSCOPE
   spatialsnake single_analysis sample.txt xenium --option=advance_analysis --runpipe=cellchat
   spatialsnake single_analysis sample.txt Merfish --option=advance_analysis --runpipe=cellchat

For a non-spatial single-cell object, enable single-cell mode explicitly. The required ``TYPE`` argument is used only to select the workflow branch and does not introduce a distance constraint when ``cellchat_is_single_cell`` is true:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis \
     --runpipe=cellchat --cellchat_is_single_cell=True

Platform-specific spatial parameters and auto-selection logic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In CellChat spatial analysis, ``spot.diameter`` represents the effective physical size of one observation unit.
This value cannot be shared across platforms because different technologies do not measure the tissue at the same spatial resolution.
Some platforms summarize transcripts in relatively large spots, whereas others work at bin-level or near single-cell resolution.
As a result, the same coordinate distance can correspond to very different biological distances across platforms.

According to the official CellChat spatial tutorial and the discussion in issue ``#6``, spatial distances should be interpreted on a biologically meaningful scale.
Therefore, ``spot.diameter`` should be set either from an officially provided platform description or from a platform-specific calculation based on the true spatial unit.

How ``spot.diameter`` is selected for each platform
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The table below summarizes which parameters are automatically adjusted according to the underlying platform technology.

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

In short, ``spot.diameter`` should always match the real biological observation unit of the platform rather than the raw coordinate number itself.

.. important::
   For Visium HD, the workflow attempts to infer the bin size from names containing patterns such as ``008um`` or ``square_008um``.
   If the input name does not encode the bin size, set ``cellchat_spot_size`` explicitly to the effective bin or segmented-cell diameter instead of retaining the standard Visium default of 65.
   For Xenium, MERFISH, MERSCOPE, or segmented data, ``cellchat_spot_size`` should similarly represent the effective cell or segmentation diameter in the same physical unit used to interpret the coordinates.

``cellchat_interaction_length`` defines the maximum spatial communication range used by CellChat after coordinate scaling.
It should be selected according to platform resolution and the biological process of interest: contact-dependent interactions generally require a shorter range than diffusible signaling.
When changing ``cellchat_spot_size`` or the coordinate unit, re-evaluate ``cellchat_interaction_length`` because the two parameters jointly determine which observations are considered spatially proximal.

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
     - ``Spatial`` / ``RNA``
     - Compatibility label for the assay context; the expression matrix is read from the active assay's ``data`` layer
   * - ``cellchat_min_cells``
     - ``10``
     - Filters out very small cell groups that are unlikely to support robust communication inference
   * - ``--threads`` / ``cellchat_workers``
     - A positive integer
     - Controls parallel computation; ``cellchat_workers`` is retained as a legacy alias of the workflow-wide ``--threads`` option
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
   * - ``cellchat_db_subset``
     - ``all_interactions`` / ``secreted_only`` / ``secreted_ecm``
     - Selects all database interactions, secreted signaling only, or secreted signaling together with ECM-receptor interactions
   * - ``cellchat_future_max_size_gb``
     - ``64`` or a larger positive value
     - Sets the memory-transfer limit used by the R ``future`` framework; ``0`` removes this limit but does not reduce actual memory consumption
   * - ``cellchat_focus_cells``
     - comma-separated cell groups
     - Recommended focused-visualization parameter; all directed combinations among these groups are displayed
   * - ``cellchat_cell_pairs``
     - ``A|B,A<->C``
     - Optional exact directed or bidirectional cell pairs; takes priority over all other cell-scope parameters
   * - ``cellchat_source_cells`` / ``cellchat_target_cells``
     - comma-separated cell groups
     - Optional sender and receiver sets used when an asymmetric communication scope is required
   * - ``cellchat_pathways`` / ``cellchat_lr_pairs``
     - pathway or ``ligand|receptor`` names
     - Optional advanced filters; empty values automatically select the strongest pathways and LR interactions within the chosen cell scope
   * - ``cellchat_top_cell_pairs`` / ``cellchat_top_pathways`` / ``cellchat_bubble_top_lr``
     - ``3`` / ``3`` / ``20``
     - Limits automatic cell-pair, pathway, and unique LR selection to maintain readable focused figures
   * - ``cellchat_plot_advanced``
     - ``True`` / ``False``
     - Controls official pathway aggregate, LR-contribution, gene-expression, and signaling-role figures

Copyable configuration examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Single spatial sample:

.. code-block:: yaml

   celltype_col: "celltype"
   cellchat_species: "human"
   cellchat_is_single_cell: False
   cellchat_db_subset: "all_interactions"
   cellchat_interaction_length: 250
   cellchat_min_cells: 10
   cellchat_trim: 0.1

Single-cell mode:

.. code-block:: yaml

   celltype_col: "celltype"
   cellchat_assay: "RNA"
   cellchat_species: "human"
   cellchat_min_cells: 10
   cellchat_is_single_cell: True
   cellchat_trim: 0.1

Single-cell dataset:
First set ``cellchat_is_single_cell: True`` in the configuration file, then run:

.. code-block:: yaml

   cellchat_is_single_cell: True
   celltype_col: "celltype"
   cellchat_species: "human"

The ``sample.txt`` file only needs two columns in this mode:

.. code-block:: text

   sample_id    input_path
   sc_sample    /path/to/sc_sample.h5ad

Then run:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis \
     --runpipe=cellchat --cellchat_is_single_cell=True

Spatial dataset:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat

Replace ``visium`` with ``visium_HD``, ``visium_segment``, ``stereoseq``, ``xenium``, or ``Merfish`` for the corresponding platform.

Analysis behavior by scenario
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Single-cell mode:** CellChat uses normalized expression and cell annotations without spatial distance constraints. Global and focused communication figures are generated, whereas ``cellchat_spatial_lr.png`` is skipped.
* **Single spatial sample:** CellChat combines expression with the resolved coordinates, platform scale, ``cellchat_spot_size``, and ``cellchat_interaction_length``. All global, focused, and spatial LR outputs are eligible for generation.
* **Same-condition spatial replicates:** The workflow analyzes the integrated condition-level object and uses the sample rows to collect slice names and scale information. Apply the version and coordinate-system precautions described in Step 1.
* **Different experimental conditions:** Run this module once per condition and retain each ``cellchat.rds`` object. Use :doc:`step9_compare_stage_cellchat` for increases, decreases, and condition-specific communication changes.

Focused visualization
~~~~~~~~~~~~~~~~~~~~~

Users are not expected to know which pathways or LR interactions will be detected before running CellChat.
The module therefore defines the cell scope first, ranks pathways within that scope, and finally selects the strongest LR interactions for visualization.
If all focused parameters are empty, the three strongest directed cell pairs, three strongest pathways within those pairs, and up to 20 unique LR interactions are selected automatically.

For routine use, users normally only need to provide cell annotation names through ``cellchat_focus_cells``:

.. code-block:: yaml

   cellchat_focus_cells: "Tumor_I,Tumor_II,Tumor_III"

This setting examines all directed combinations among the three selected groups.
Directional sender and receiver sets can instead be defined as follows:

.. code-block:: yaml

   cellchat_source_cells: "Tumor_I,Tumor_II"
   cellchat_target_cells: "Macrophage,T_cell"

Exact directions are specified with ``source|target`` or ``source->target``; ``source<->target`` expands to both directions:

.. code-block:: yaml

   cellchat_cell_pairs: "Tumor_I|Macrophage,Tumor_II<->T_cell"

When a pathway or LR pair is already of biological interest, it can be added without changing the cell scope:

.. code-block:: yaml

   cellchat_focus_cells: "Tumor_I,Macrophage"
   cellchat_pathways: "MIF,SPP1"
   cellchat_lr_pairs: "SPP1|CD44,MIF|CD74_CXCR4"

The parameter priority is ``cellchat_cell_pairs`` > ``cellchat_focus_cells`` > ``cellchat_source_cells/cellchat_target_cells`` > automatic cell-pair selection.
Invalid pathway or LR names trigger a warning and are replaced by automatic selections within the same valid cell scope; the workflow does not substitute unrelated global interactions.
If a user-selected cell scope contains no significant communication, focused figures are skipped and an empty selected-result table is written, while the global CellChat results remain available.


Result file structure
---------------------

The module produces one communication-analysis result set for each run. The main output categories are:

1. **Serialized CellChat object**
   This object preserves the inferred communication model and can be reused in subsequent comparative analyses.
2. **Network overview figures**
   These summarize the number and strength of interactions among cell groups.
3. **Pathway-level summary figures**
   These show which signaling programs dominate the current dataset.
4. **Heatmaps and signaling-role plots**
   These help interpret sender, receiver, and pathway-centrality patterns.
5. **Ligand-receptor and pathway summary tables**
   These provide the tabular evidence required for downstream validation, filtering, and biological reporting.

The principal outputs are:

.. code-block:: text

   cellchat.rds
   {sample}_cellchat_network.png
   {sample}_cellchat_network.pdf
   {sample}_cellchat_heatmap.png
   {sample}_cellchat_infoflow_bar.png
   {sample}_cellchat_stats.csv
   {sample}_cellchat_lr.csv
   {sample}_cellchat_pathway_summary.csv

Additional focused outputs are generated when valid pathway or ligand-receptor information is available:

.. code-block:: text

   {sample}_cellchat_bubble.png
   {sample}_cellchat_bubble_{source}_to_{target}.png
   {sample}_cellchat_selected_lr.csv
   {sample}_cellchat_selected_pathway_summary.csv
   {sample}_cellchat_spatial_lr.png
   advanced/{pathway}_*_aggregate_network.png
   advanced/{pathway}_*_lr_contribution.png
   advanced/{pathway}_gene_expression.png
   advanced/{pathway}_signaling_role.png

The network, heatmap, and information-flow figures always summarize the complete CellChat result and are not restricted by focused-visualization parameters.
The ``selected_lr.csv`` table records ``selection_source``, ``cell_pair``, pathway and LR ranks, and the exact bubble-plot filename, allowing every focused figure to be traced to its underlying interactions.
In automatic mode, advanced figures are limited to the strongest pathway; when pathways are explicitly provided, advanced figures are generated for every valid requested pathway.
The spatial LR figure is generated only for spatial mode and uses the highest-ranked selected LR interaction.

How to interpret the results
----------------------------

For a lightweight demonstration using the example data provided in this documentation, we recommend the CRC tumor subset obtained after subclustering and annotation in the reannotation step. Its relatively small size makes it suitable for basic workflow testing and result inspection. However, the resulting outputs are intended for demonstration purposes only and should not be interpreted as biologically meaningful findings.

.. code-block:: bash

   Tumor   results/useful_results/Tumor.h5ad    data/Colon_Cancer_P2_008um/binned_outputs/square_008um/spatial/scalefactors_json.json

1. Network overview plot
~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_network.png
   :width: 85%
   :align: center
   :alt: cellchat network

Interpretation:
The left panel shows the number of interactions between cell groups, whereas the right panel shows interaction strength. Node size reflects the number of cells or spots in each annotation group, and directed edges summarize sender-to-receiver communication. Together, these figures provide a rapid overview of communication hubs and dominant relationships; they should not be interpreted as evidence that every individual cell in two groups interacts.

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
The left panel summarizes the number of interactions between cell groups, whereas the right panel summarizes their total strength. Viewed together, they help distinguish communication programs that are widespread but weak from those that are sparse but strong.

4. Focused LR, pathway, and signaling-role plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The focused bubble plot displays the automatically or manually selected LR interactions for the effective sender-receiver scope.
Color represents communication probability and dot size represents CellChat's significance category.
When exact cell pairs are requested or selected automatically, each directed pair is plotted separately so that unrelated source-target combinations are not introduced.

For the strongest automatically selected pathway, or for each valid user-specified pathway, the workflow uses CellChat's official functions to generate an aggregate network, LR-contribution plot, gene-expression dot plot, and signaling-role heatmap.
The aggregate and contribution plots honor the selected sender-receiver scope.
``plotGeneExpression()`` and the signaling-role heatmap do not expose ``sources.use`` or ``targets.use`` in the CellChat interface; these plots therefore display all cell groups for the selected pathway.
Together, the four outputs distinguish network structure, the LR pairs driving the pathway, expression support, and dominant sender/receiver roles without duplicating the global summaries.

In spatial mode, ``cellchat_spatial_lr.png`` displays spatial expression support for the highest-ranked selected LR interaction using CellChat's binary expression view and the configured cutoff.
This figure localizes ligand and receptor support in the tissue; it is not a map of individually observed ligand-receptor binding events.

5. LR-level detail and summary statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interpretation:
``lr.csv`` contains ligand-receptor evidence at the individual interaction level, whereas ``lr_summary.csv`` provides aggregated interaction strength and significance for each LR pair. Together, these files form a primary basis for mechanistic interpretation and reproducible downstream analysis.
``selected_lr.csv`` and ``selected_pathway_summary.csv`` contain the exact scoped interactions used for focused visualization.
The former also records the selection mode, cell-pair direction, ranks, and output filename, making the plotted evidence directly auditable and reusable.


