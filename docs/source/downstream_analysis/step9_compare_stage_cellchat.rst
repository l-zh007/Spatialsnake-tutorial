Module 8: Comparative Communication Analysis (compare_stage + cellchat)
=======================================================================

The CellChat comparison module summarizes communication differences between two completed, condition-level CellChat objects. It follows the official CellChat comparison framework by harmonizing cell identities, merging the objects, comparing global network properties, and examining pathway- and ligand--receptor-level changes.

This module performs a pairwise descriptive comparison of inferred communication probabilities. It does not re-estimate CellChat models from expression matrices, and it does not treat biological replicates as statistical units. A single condition should therefore be analysed with ``single_analysis --option=advance_analysis --runpipe=cellchat``. Studies with three or more conditions should use explicitly defined pairwise comparisons.

For the complete parameter reference, see :doc:`../config_reference/compare_stage_yaml`.

.. important::

   The order of the two rows in ``sample.txt`` defines the comparison direction. All differences are calculated as ``condition 2 - condition 1``. The first row should therefore contain the biological reference condition.


Workflow overview
-----------------

The comparison proceeds through six stages:

1. **Validate the CellChat objects.**
   The workflow requires two completed CellChat ``.rds`` objects containing ``net`` and ``netP`` results. Their datatype and ligand--receptor database must be compatible.
2. **Harmonize cell identities.**
   The union of cell identities is constructed, and missing identities are added with ``liftCellChat()``. The aligned objects are then combined with ``mergeCellChat()``.
3. **Compare global communication.**
   ``compareInteractions()`` summarizes the total inferred interaction count and communication strength in each condition.
4. **Localize sender--receiver differences.**
   Official CellChat circle and heatmap functions display positive and negative changes in interaction count and weight.
5. **Compare pathways and ligand--receptor interactions.**
   ``rankNet()`` compares pathway information flow. Focused bubble plots display automatically selected or user-defined sender, receiver, pathway, and ligand--receptor combinations.
6. **Export reproducible results.**
   Complete comparison tables, the data used in focused plots, aligned CellChat objects, and the merged object are written to disk.


Choose the appropriate CellChat workflow
----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 36 36

   * - Analysis scenario
     - Recommended workflow
     - Interpretation
   * - One sample or one experimental condition
     - ``single_analysis --option=advance_analysis --runpipe=cellchat``
     - Complete communication inference and visualization within one condition
   * - Replicates from the same condition
     - Build one condition-level CellChat object before comparison
     - The object represents the integrated communication landscape of that condition
   * - Two experimental conditions
     - ``compare_analysis --option=compare_stage --runpipe=cellchat``
     - Descriptive comparison of two completed condition-level CellChat objects
   * - Three or more conditions
     - Prepare one two-row sample file for each biologically meaningful contrast
     - Independent pairwise comparisons with a clearly defined reference
   * - Replicate-aware statistical testing
     - Use a method that explicitly models biological replicates
     - The present CellChat comparison does not provide replicate-level differential significance


Prepare ``sample.txt``
----------------------

Exactly two data rows are required. Each row contains a display name and the path to a completed CellChat RDS object:

.. code-block:: text

   sample_id       input_path
   Non_Lesional    results/group_Non_Lesional/cellchat/cellchat.rds
   Lesional        results/group_Lesional/cellchat/cellchat.rds

In this example, ``Non_Lesional`` is the reference. Positive differences and the label ``Lesional_higher`` indicate a larger inferred value in Lesional tissue. Negative differences and ``Non_Lesional_higher`` indicate a larger value in Non-Lesional tissue.

Input requirements
~~~~~~~~~~~~~~~~~~

1. Both files must be CellChat ``.rds`` objects produced after communication probability and pathway aggregation have completed.
2. The two objects must use compatible species-specific interaction databases and the same CellChat datatype, such as ``spatial`` or ``RNA``.
3. Cell identities must represent comparable biological annotations. The workflow can add a missing identity during alignment, but it cannot determine whether differently named populations are biologically equivalent.
4. Each RDS should represent one experimental condition. If a condition contains several replicates, their integration or within-condition analysis must be completed before this comparison.
5. The first row must be the intended reference. Reversing the rows reverses every reported difference and condition-higher label.

.. note::

   A cell identity that occurs in only one condition remains valid after ``liftCellChat()``. Its absent-condition communication values are represented as zero. Interpret these differences together with cell abundance, annotation quality, and expression support.


Run the comparison
------------------

The minimal command is:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium \
     --option=compare_stage \
     --runpipe=cellchat \
     --threads 4

``visium`` selects the workflow platform at the command level. The comparison step does not recalculate spatial distances because the input RDS objects already contain completed CellChat inference results.

Generate and edit a configuration template when a dedicated result directory or focused visualization is required:

.. code-block:: bash

   spatialsnake produce-file --option=compare_stage

   spatialsnake compare_analysis sample.txt visium \
     --option=compare_stage \
     --runpipe=cellchat \
     --threads 4 \
     --configfile compare_stage.yaml

A concise CellChat comparison configuration is:

.. code-block:: yaml

   runpipe: "cellchat"
   cellchat_compare_output_dir: "results/compare_cellchat"

   cellchat_compare_focus_cells: ""
   cellchat_compare_cell_pairs: ""
   cellchat_compare_source_cells: ""
   cellchat_compare_target_cells: ""
   cellchat_compare_pathways: ""
   cellchat_compare_lr_pairs: ""

   cellchat_compare_top_cell_pairs: 3
   cellchat_compare_top_pathways: 3
   cellchat_compare_top_lr: 20
   cellchat_compare_plot_advanced: True
   cellchat_compare_gene_plot_type: "dot"
   cellchat_compare_save_merged: True


Visualization selection
-----------------------

The module separates global summaries from focused results. Global figures always describe the complete communication network and are not altered by cell-focused parameters. Focused figures apply the following priority:

1. ``cellchat_compare_cell_pairs`` specifies exact communication directions.
2. ``cellchat_compare_focus_cells`` includes all directions among selected cell identities.
3. ``cellchat_compare_source_cells`` and ``cellchat_compare_target_cells`` specify sender and receiver sets separately.
4. If all cell parameters are empty, the workflow selects the three directed cell pairs with the largest absolute communication-strength differences.

Within the resulting cell scope, pathway and ligand--receptor selection is performed automatically unless the corresponding parameters are provided. Invalid pathway or ligand--receptor names are ignored with a warning, followed by automatic selection within the same cell scope.

Main parameter guide
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 18 48

   * - Parameter
     - Default
     - Recommended use
   * - ``cellchat_compare_output_dir``
     - ``results/compare_cellchat``
     - Use a unique directory for each pairwise contrast to prevent overwriting.
   * - ``cellchat_compare_sample_name1`` / ``sample_name2``
     - empty
     - Leave empty to use ``sample_id`` values. Override only for publication-facing labels.
   * - ``cellchat_compare_focus_cells``
     - empty
     - Recommended first customization when only the cell annotations of interest are known.
   * - ``cellchat_compare_cell_pairs``
     - empty
     - Use for exact directions. ``A|B`` and ``A->B`` mean sender A to receiver B; ``A<->B`` expands both directions.
   * - ``cellchat_compare_source_cells`` / ``target_cells``
     - empty
     - Use when several senders should be compared against a distinct receiver set.
   * - ``cellchat_compare_pathways``
     - empty
     - Set after inspecting ``compare_pathway.csv``. Empty values select pathways automatically within the chosen cell scope.
   * - ``cellchat_compare_lr_pairs``
     - empty
     - Enter ``ligand|receptor`` pairs after inspecting ``compare_lr.csv``.
   * - ``cellchat_compare_top_cell_pairs``
     - ``3``
     - Increase cautiously when the dataset contains many cell identities. Values between 3 and 6 usually remain readable.
   * - ``cellchat_compare_top_pathways``
     - ``3``
     - Controls automatic pathway selection for focused plots and tables.
   * - ``cellchat_compare_top_lr``
     - ``20``
     - Limits unique ligand--receptor interactions in focused bubble plots.
   * - ``cellchat_compare_plot_advanced``
     - ``True``
     - Disable for a faster global overview. When enabled, automatic analysis uses the top pathway; manual analysis uses every valid requested pathway.
   * - ``cellchat_compare_gene_plot_type``
     - ``dot``
     - ``dot`` is the most compact option. CellChat 1.6.1 also supports ``violin`` and ``bar``.
   * - ``cellchat_compare_save_merged``
     - ``True``
     - Retain the aligned objects and merged CellChat object for reproducibility and custom R analysis.


Common analysis scenarios
-------------------------

Fully automatic comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~

Leave all focused parameters empty when the communication changes are not known in advance:

.. code-block:: yaml

   cellchat_compare_focus_cells: ""
   cellchat_compare_cell_pairs: ""
   cellchat_compare_source_cells: ""
   cellchat_compare_target_cells: ""
   cellchat_compare_pathways: ""
   cellchat_compare_lr_pairs: ""

The workflow selects representative cell pairs, pathways, and ligand--receptor interactions from the observed differences. This is the recommended initial run.

Focus on known cell annotations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   cellchat_compare_focus_cells: "Tumor,Endothelial,Macrophage"

This setting examines every sender--receiver direction among the three populations. Pathways and ligand--receptor interactions are then selected automatically within this restricted scope.

Compare sender and receiver sets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   cellchat_compare_source_cells: "Tumor,Endothelial"
   cellchat_compare_target_cells: "Macrophage,T_cell"

This configuration maps directly to CellChat ``sources.use`` and ``targets.use``. It produces the sender-by-receiver cross-product defined by the two sets.

Specify exact communication directions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   cellchat_compare_cell_pairs: "Tumor|Macrophage,Endothelial<->Tumor"

The first expression selects ``Tumor -> Macrophage``. The second expands into ``Endothelial -> Tumor`` and ``Tumor -> Endothelial``. Each exact direction is plotted independently, and unspecified cross-combinations are not introduced.

Specify pathways or ligand--receptor pairs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   cellchat_compare_focus_cells: "Tumor,Macrophage"
   cellchat_compare_pathways: "MIF,SPP1"
   cellchat_compare_lr_pairs: "MIF|CD74_CD44,SPP1|CD44"

Pathway and ligand--receptor parameters should usually be set after the automatic run. ``compare_pathway.csv`` lists all pathway information-flow differences, and ``compare_lr.csv`` contains the available ligand and receptor names.

Run an overview without advanced pathway figures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   cellchat_compare_plot_advanced: False

The global overview, differential network, differential heatmap, pathway information-flow comparison, focused bubble plots, and CSV tables are still generated. Only aggregate networks, contribution plots, signaling-role heatmaps, and gene-expression support plots are skipped.

Compare three or more conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The module does not infer all pairwise contrasts from a multi-row sample file. Prepare one two-row file per scientifically justified contrast:

.. code-block:: text

   # treatment_A_vs_control.txt
   sample_id   input_path
   Control     results/Control/cellchat/cellchat.rds
   TreatmentA  results/TreatmentA/cellchat/cellchat.rds

.. code-block:: text

   # treatment_B_vs_control.txt
   sample_id   input_path
   Control     results/Control/cellchat/cellchat.rds
   TreatmentB  results/TreatmentB/cellchat/cellchat.rds

Assign a different ``cellchat_compare_output_dir`` to each run. This preserves an explicit reference condition and avoids ambiguous comparison directions.


Result files
------------

.. code-block:: text

   results/compare_cellchat/
   ├── compare_overview_number_strength.png
   ├── compare_diff_number_strength_net.png
   ├── compare_heatmap_count_weight.png
   ├── compare_pathway_strength.png
   ├── compare_lr_regulated.png
   ├── compare_pathway_network.png
   ├── compare_pathway_contribution.png
   ├── compare_signaling_role.png
   ├── compare_gene_expression.png
   ├── compare_global_summary.csv
   ├── compare_cell_pair.csv
   ├── compare_pathway.csv
   ├── compare_lr.csv
   ├── selected_interactions.csv
   ├── compare_parameters.csv
   ├── cellchat_object.list.rds
   └── cellchat_merged.rds

When several exact cell pairs or manually selected pathways are plotted, additional files include a cell-pair or pathway suffix. If no non-zero difference is detected, the module writes zero-valued comparison tables and explanatory figures instead of terminating.

Key result tables
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - File
     - Contents
   * - ``compare_global_summary.csv``
     - Total inferred interaction count and summed communication weight for each condition
   * - ``compare_cell_pair.csv``
     - Condition-specific count and weight for every sender--receiver pair, their differences, and the condition-higher label
   * - ``compare_pathway.csv``
     - Pathway information flow in each condition, the directional difference, and the condition-higher label
   * - ``compare_lr.csv``
     - Ligand, receptor, pathway, source, target, probability, p-value, probability difference, and direction
   * - ``selected_interactions.csv``
     - The exact rows displayed in focused bubble plots, including selection source, ranks, cell pair, and plot filename
   * - ``compare_parameters.csv``
     - Condition order, difference direction, cell scope, selected pathways and ligand--receptor interactions, datatype, and CellChat version


Interpretation
--------------

Global interaction number and strength
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``compare_overview_number_strength.png`` shows the total number of inferred interactions and the summed communication strength in each condition. These totals summarize network density and magnitude, but they are also influenced by the number and composition of annotated cell groups.

Directional sender--receiver differences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``compare_diff_number_strength_net.png`` contains four panels: count higher in condition 2, count higher in condition 1, weight higher in condition 2, and weight higher in condition 1. Edge width represents the magnitude of the corresponding positive difference.

``compare_heatmap_count_weight.png`` displays the same comparison in sender-by-receiver matrix form. The matrix is calculated as ``condition 2 - condition 1``. Positive values support condition 2, whereas negative values support condition 1.

Pathway information flow
~~~~~~~~~~~~~~~~~~~~~~~~

``compare_pathway_strength.png`` is generated with ``rankNet(mode="comparison")``. The stacked panel emphasizes relative information flow, while the grouped panel shows the condition-specific magnitude. A pathway detected in only one condition should be interpreted as condition-specific inference, not as direct evidence of pathway activation.

Focused ligand--receptor comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``compare_lr_regulated.png`` and any cell-pair-suffixed bubble plots show the selected ligand--receptor probabilities. Bubble colour represents communication probability, and bubble size reflects the CellChat p-value category. Missing bubbles indicate that the interaction did not pass the CellChat threshold in that condition and cell pair.

Advanced pathway support
~~~~~~~~~~~~~~~~~~~~~~~~

When ``cellchat_compare_plot_advanced`` is enabled, the workflow generates condition-specific aggregate networks, ligand--receptor contribution plots, signaling-role summaries, and ligand/receptor expression plots. ``compare_gene_expression.png`` should be used as expression support for an inferred pathway, not as an independent differential-expression test.

.. warning::

   CellChat probabilities are model-derived communication scores. ``Lesional_higher`` or ``Non_Lesional_higher`` indicates the larger inferred value, not replicate-aware statistical significance. Communication differences should be interpreted together with expression support, cell abundance, tissue context, and orthogonal biological evidence.


Troubleshooting and quality checks
----------------------------------

1. **The workflow rejects one or three RDS files.**
   This is expected. Compare-stage CellChat requires exactly two condition-level objects.
2. **The interaction databases are incompatible.**
   Re-run the single-condition CellChat analyses with the same species and ``cellchat_db_subset`` settings.
3. **A requested cell type is ignored.**
   Use the exact annotation label stored in the CellChat object. Cell names are matched case-insensitively, but spelling and punctuation must otherwise agree.
4. **A pathway or ligand--receptor pair is unavailable.**
   Inspect ``compare_pathway.csv`` and ``compare_lr.csv``. The workflow records a warning and returns to automatic selection within the valid cell scope.
5. **A signaling-role panel reports insufficient variation.**
   The selected pathway does not contain enough distinct role scores for a stable CellChat heatmap. Other comparison results remain valid.
6. **The two conditions have no non-zero difference.**
   The module writes complete zero-difference tables and explanatory figures. It does not force an artificial network visualization.

Before biological interpretation, confirm that ``compare_parameters.csv`` reports the intended condition order, that ``selected_interactions.csv`` matches the displayed bubble plots, and that the aligned identities in ``cellchat_merged.rds`` are biologically comparable.


Demonstration: Non-Lesional versus Lesional tissue
--------------------------------------------------

The following example used two completed spatial CellChat objects and CellChat 1.6.1. The sample order was ``Non_Lesional`` followed by ``Lesional``; therefore, all differences represent ``Lesional - Non_Lesional``. The run used empty focused parameters, allowing automatic selection of representative cell pairs, pathways, and ligand--receptor interactions.

Global communication overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/cellchat_compare_nonlesional_lesional_overview.png
   :width: 88%
   :align: center
   :alt: Global CellChat interaction count and strength in Non-Lesional and Lesional tissue

   Global comparison of inferred interaction number and total communication strength. In this demonstration, the Non-Lesional object contains more inferred interactions and a larger summed communication weight.

Directional differential network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/cellchat_compare_nonlesional_lesional_diff_network.png
   :width: 92%
   :align: center
   :alt: Directional differential CellChat network for Non-Lesional and Lesional tissue

   Cell-pair differences separated by direction and network measure. The left panels show communication inferred to be higher in Lesional tissue, whereas the right panels show communication inferred to be higher in Non-Lesional tissue.

Sender--receiver difference heatmap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/cellchat_compare_nonlesional_lesional_heatmap.png
   :width: 94%
   :align: center
   :alt: CellChat sender-receiver differential heatmap for Non-Lesional and Lesional tissue

   Differential interaction count and communication strength across sender--receiver combinations. The displayed values follow the ``Lesional - Non_Lesional`` direction.

Pathway information-flow comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/cellchat_compare_nonlesional_lesional_pathways.png
   :width: 92%
   :align: center
   :alt: CellChat pathway information-flow comparison in Non-Lesional and Lesional tissue

   Relative and absolute pathway information flow generated by ``rankNet()``. Shared pathways and condition-specific pathways are displayed in the same comparison framework.

Ligand and receptor expression support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/cellchat_compare_nonlesional_lesional_gene_expression.png
   :width: 92%
   :align: center
   :alt: Ligand and receptor gene-expression support for the selected CellChat pathway

   Mean scaled expression and percentage of expressing observations for genes in the automatically selected MIF pathway. The two panels provide expression context for the inferred communication results.

These figures demonstrate the expected output structure and should not be interpreted as a biological conclusion without considering experimental design, sample-level replication, cell abundance, and independent validation.
