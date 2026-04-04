Module 3: Cell-Cell Communication (liana)
=========================================

Although Spatialsnake already provides ligand-receptor analysis through :doc:`step2_cellphonedb` and CellChat, we also include ``liana`` because it offers a broader and more flexible framework for communication inference.
``liana`` runs multiple ligand-receptor scoring methods through a unified interface and writes the results back into the analysis object for downstream reuse.
This multi-method design can provide a more robust view of intercellular communication than relying on a single algorithm alone.

One important distinction is that ``liana`` does not explicitly model spatial distance in the same way as spatially constrained methods.
If spatial proximity is central to your biological question, we recommend first restricting the analysis to a smaller ROI and then running ``liana`` on that subset.

``liana`` is also useful for integrated interpretation across spatial and single-cell datasets generated under similar experimental conditions, allowing you to compare communication patterns across modalities.


Workflow overview
-----------------

1. **Read the input and parse the grouping parameters**
   Load a spatial or single-cell object (``.zarr`` or ``.h5ad``) and extract the selected cell-type annotation column for downstream grouping.
2. **Run LIANA with the selected method**
   Execute the communication method specified in the configuration, such as ``cellphonedb``, ``connectome``, or ``cellchat``, using the selected resource database, such as ``consensus``. Low-expression features are filtered according to the expression proportion threshold and minimum cell count.
3. **Filter and summarize significant interactions**
   Retain high-confidence ligand-receptor interactions and store key scores such as magnitude and specificity in ``.uns``.
4. **Generate summary figures automatically**
   Produce a dot plot for selected cell-pair interactions, a tile plot for highly ranked interactions, and a circle plot for the global communication network when possible.
5. **Export the annotated result object**
   Save the object containing the LIANA results as a new ``.zarr`` or ``.h5ad`` file for downstream inspection and custom visualization.

Prepare the input files
-----------------------

Recommended ``sample.txt`` format. If you want to use single-cell data instead, simply replace the path with the relevant ``.h5ad`` file:

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

Input requirements:

1. The input object should contain a cell-type annotation column, typically ``celltype``.
2. Using a fully annotated object is strongly recommended so that sender and receiver populations remain biologically interpretable.

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=liana

Optional configuration
----------------------

For the configuration reference, see :doc:`../config_reference/advance_analysis_yaml`.

Commonly used parameters in ``advance_analysis.yaml`` include:

.. list-table::
   :header-rows: 1
   :widths: 26 22 52

   * - Parameter
     - Typical values
     - Description
   * - ``runpipe``
     - ``liana``
     - Selects the LIANA branch
   * - ``cellPhoneDB_input``
     - ``results/S1/annotation/S1.zarr``
     - Input object path
   * - ``liana_method``
     - ``cellphonedb`` / ``connectome`` / ``cellchat``
     - Communication scoring method
   * - ``liana_resource_name``
     - ``consensus``
     - Ligand-receptor resource database
   * - ``liana_expr_prop``
     - ``0.1``
     - Expression proportion threshold used to filter low-expression ligands and receptors
   * - ``liana_min_cells``
     - ``5``
     - Minimum number of cells required per group
   * - ``liana_use_raw``
     - ``true``
     - Whether to prioritize ``adata.raw``
   * - ``celltype_col``
     - ``celltype``
     - Cell-type grouping column

Supported ``liana_method`` values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The current workflow supports the following method names directly:

1. ``cellphonedb``: evaluates ligand-receptor significance using mean expression and permutation-based logic.
2. ``connectome``: emphasizes network connectivity and edge strength.
3. ``natmi``: prioritizes cell-type-specific ligand-receptor specificity.
4. ``singlecellsignalr``: uses LRscore-style ranking for rapid prioritization.
5. ``cellchat``: applies a CellChat-like probabilistic scoring logic within the LIANA interface.
6. ``geometric_mean``: uses geometric mean summarization to reduce the impact of extreme values.
7. ``logfc``: prioritizes expression change amplitude and is useful in differential-expression-oriented settings.
8. ``rank_aggregate``: aggregates rankings across methods to produce a consensus score.
9. ``scseqcomm``: provides an additional statistical perspective on candidate interactions.

Notes:

- ``log2fc`` is mapped automatically to ``logfc``.
- ``cellphone_db`` is mapped automatically to ``cellphonedb``.
- Any other method name is validated against the LIANA version available in the local environment.

``liana_resource_name`` options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``consensus`` (default):
   the LIANA integrated resource, appropriate for most routine analyses and tutorial use.
2. Other resource names:
   LIANA can switch among different ligand-receptor resources, depending on the locally installed version and available data. This is helpful when you want to align the analysis with a specific publication or historical workflow.

Recommendation:

- Start with ``consensus`` for initial analyses.
- Switch to a specific resource only when strict comparability with another database is required.

Result file structure
---------------------

.. code-block:: text

   results/
   └── liana_output/
       ├── {sample}.zarr
       ├── dotplot.png
       ├── tileplot.png
       └── circle.png   # generated when cell-type labels can be mapped consistently for network visualization

How to interpret the results
----------------------------

1. Ligand-receptor dot plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_dot_plot.png
   :width: 85%
   :align: center
   :alt: liana dotplot

Interpretation:
This plot shows specific ligand-receptor pairs between selected source and target cell types. Dot size typically reflects significance, such as the negative log p-value, whereas color reflects interaction strength. It is one of the most informative figures for mechanism-oriented interpretation.

2. Ranked interaction tile plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_heatmap.png
   :width: 85%
   :align: center
   :alt: liana tileplot

Interpretation:
This plot highlights the highest-ranked ligand-receptor interactions across the full dataset or within selected cell pairs. The fill color represents interaction strength and helps you identify the strongest candidate communication axes quickly.

3. Global communication circle plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_chord_plot.png
   :width: 85%
   :align: center
   :alt: liana circle plot

Interpretation:
This figure provides a global overview of the communication network across all cell types. Nodes represent cell groups, and edge thickness and color summarize the number and overall strength of interactions. It is particularly helpful for identifying potential communication hubs in the tissue microenvironment.

Additional note:
If the cell-type labels in the input object cannot be mapped cleanly to the source and target labels in the LIANA results, the workflow preserves the ``dotplot`` and ``tileplot`` outputs first and may skip ``circle.png`` to avoid a hard failure.

4. Communication result object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interpretation:
The full LIANA output tables are written to the ``.uns`` slot of the result object. Advanced users can load this object and extract the raw numerical results for custom filtering, visualization, or additional analysis in the Scanpy or SpatialData ecosystem.
