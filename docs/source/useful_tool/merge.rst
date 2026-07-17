Data Merge Tool (``merge``)
===========================

``merge`` provides two complementary operations for routine spatial transcriptomics workflows:

1. ``sample`` concatenates independent, fully processed SpatialData samples into a cohort-level object.
2. ``annotation`` writes refined labels from CSV files or subset Zarr objects back into a complete parent object.

The command continues to execute the Python utility directly and does not invoke a Snakemake workflow. It does not perform batch correction, joint dimensionality reduction, expression normalization, or geometric registration of tissue sections.

For the configuration reference, see :doc:`../config_reference/merge_yaml`.


Before you start
----------------

Make sure that:

1. Every full object is a readable SpatialData Zarr directory with a valid annotation table.
2. The table retains valid ``region_key`` and ``instance_key`` metadata linking observations to Shapes, Points, or Labels.
3. Independent samples use comparable expression features. The default sample merge uses the intersection of genes.
4. Subcluster results retain stable cell or spot IDs from their parent object.

The historical ``cluster``, ``celltype``, and ``reannotation`` merge modes are no longer accepted. Use ``sample`` for independent objects and ``annotation`` for subset result write-back.


Command template
----------------

.. code-block:: bash

   spatialsnake useful_tool --option=merge <INPUT1> <INPUT2> ... \
     --merge_by=<sample|annotation> \
     --output_dir=results/useful_results

The default outputs are:

.. code-block:: text

   results/useful_results/concatenated_sdata.zarr
   results/useful_results/merge_report.csv


Mode 1: concatenate independent samples
---------------------------------------

Use ``merge_by=sample`` when each input represents an independent tissue section or sample. This is appropriate after running a sample-level method such as RCTD separately and then assembling the processed samples for cohort-level visualization or downstream analysis.

Do not use this mode to reconstruct subsets produced from the same parent object. A table-only split retains the parent's spatial elements in every subset; treating those subsets as independent samples would duplicate the same Shapes, Points, Images, and Labels under sample-specific element names. Conflicting region and observation names would also be suffixed, while coordinate-system definitions would be combined according to SpatialData concatenation rules. Even when the subsets are mutually exclusive and their observation counts sum to the parent count, the result is therefore not identical to the original object. Use :ref:`merge-annotation-reconstruction` instead.

.. code-block:: bash

   spatialsnake useful_tool --option=merge \
     results/S1/RCTD/S1.zarr \
     results/S2/RCTD/S2.zarr \
     results/S3/RCTD/S3.zarr \
     --merge_by=sample \
     --sample_ids=S1,S2,S3 \
     --feature_join=inner \
     --output_dir=results/useful_results

During concatenation:

- observation IDs are first checked across all inputs; globally unique IDs remain unchanged, whereas duplicated IDs receive a sample suffix once;
- spatial element names are also checked before concatenation; when all names are globally unique they remain unchanged, whereas any cross-input collision activates SpatialData's sample-suffix handling for the affected concatenation;
- ``obs`` columns are retained by column union; values remain associated with their original observations, and columns absent from one input are missing for that input;
- ``X`` is joined by gene name according to ``feature_join``; compatible ``layers`` and ``raw`` matrices are concatenated without normalization or value transformation;
- compatible ``obsm`` fields are retained; DataFrame-valued results, including ``RCTD_weights``, are aligned by column name and missing estimates remain ``NaN``;
- pairwise graphs are combined block-diagonally, so no cross-sample edges are introduced;
- ``_merge_source`` records the input object from which each observation originated;
- ``sample_col`` is preserved when present and populated from the resolved sample ID when absent or empty;
- the ``region_key`` and ``instance_key`` field names are preserved; instance values remain unchanged, and region values follow spatial-element renaming only when a collision is resolved;
- non-spatial table metadata are retained under ``uns["merge_sources"]``, and the operation is recorded in ``uns["merge_history"]``.

This conflict-aware naming prevents repeated merges from accumulating redundant suffixes such as ``barcode-S1-S1``. A suffix is still required when two inputs genuinely contain the same observation or spatial-element name. The naming decisions are recorded as ``obs_names_renamed`` and ``spatial_names_renamed`` in ``uns["merge_history"]``.

If ``sample_ids`` is empty, the tool first looks for one unambiguous value in ``sample_col`` and otherwise uses the input Zarr directory name. Resolved IDs must be unique.


Feature alignment
~~~~~~~~~~~~~~~~~

The recommended default is:

.. code-block:: yaml

   feature_join: "inner"

This retains genes shared by every sample and is appropriate for samples generated with the same platform or probe panel. The report records both the feature intersection and union.

To retain the union explicitly:

.. code-block:: bash

   --feature_join=outer

Use ``outer`` cautiously. Genes absent from one input may be represented by zero or missing values depending on the underlying matrix representation. Object concatenation alone does not correct technical batch effects.


Cluster-label handling
~~~~~~~~~~~~~~~~~~~~~~

Labels are preserved by default:

.. code-block:: yaml

   label_cols: ""
   label_policy: "preserve"

If independently generated cluster IDs should not be interpreted as the same labels, specify the relevant columns:

.. code-block:: bash

   --label_cols=clusters --label_policy=prefix

This produces labels such as ``S1:0`` and ``S2:0``. ``label_policy=offset`` instead assigns continuous non-overlapping integer labels. Biological annotation fields such as ``celltype`` should normally remain unchanged.


.. _merge-annotation-reconstruction:

Mode 2: write refined annotations back to a parent
--------------------------------------------------

Use ``merge_by=annotation`` after splitting, reclustering, reannotation, manual annotation, or ROI-level analysis. The complete parent remains the only spatial reference; source subsets contribute table annotations only.

This is the recommended reconstruction workflow for several disjoint subsets derived from one large sample. It is deliberately an annotation overlay rather than a second spatial concatenation:

- the parent ``X``, ``var``, ``layers``, ``raw``, ``obsm``, observation names, observation order, and spatial elements remain unchanged;
- the original broad annotation, such as ``celltype``, remains unchanged;
- a new column such as ``sub_celltype`` is initialized from ``fallback_col`` and updated only for IDs present in the subset results;
- subset Shapes, Points, Images, Labels, and coordinate systems are ignored, so table-only splitting does not duplicate the parent geometry;
- matching is based on stable cell or spot IDs, and on ``(region_key, instance_key)`` when IDs are repeated across regions.

Consequently, the output has the same spatial and expression backbone as the parent, but it is not byte-for-byte identical: it additionally contains the requested annotation column and merge provenance in ``uns["merge_history"]``. This is normally the intended result after subclustering or reannotation.

The resulting parent can therefore contain multiple annotation levels:

.. code-block:: text

   celltype       broad annotation retained from the parent
   sub_celltype   refined labels for analyzed subsets, broad-label fallback elsewhere
   fine_celltype  optional additional level from a later merge run


CSV annotation sources
~~~~~~~~~~~~~~~~~~~~~~

Reannotation outputs can be supplied as one CSV, a directory of CSV files, or comma-separated CSV paths:

.. code-block:: bash

   spatialsnake useful_tool --option=merge \
     results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr \
     --merge_by=annotation \
     --annotation_csv=results/Colon_Cancer_P2_008um/reannotation/Tumor/celltype_annotations.csv,results/Colon_Cancer_P2_008um/reannotation/T_cell/celltype_annotations.csv \
     --target_col=sub_celltype \
     --fallback_col=celltype \
     --output_dir=results/useful_results

The standard ``Barcode`` and ``Grouped_Annotation`` columns are inferred automatically when they are unambiguous. Non-standard files can be specified explicitly:

.. code-block:: bash

   --csv_cell_col=spot_id \
   --annotation_col=refined_label


Zarr annotation sources
~~~~~~~~~~~~~~~~~~~~~~~

For direct Zarr write-back, the first input is always the complete parent and subsequent inputs are subset sources:

.. code-block:: bash

   spatialsnake useful_tool --option=merge \
     results/sample/annotation/sample.zarr \
     results/sample/reannotation/Tumor/Tumor.zarr \
     results/sample/reannotation/T_cell/T_cell.zarr \
     --merge_by=annotation \
     --annotation_col=celltype \
     --target_col=sub_celltype \
     --fallback_col=celltype \
     --output_dir=results/useful_results

Only the subset tables are read. Their images, shapes, points, labels, and coordinate systems are not copied, preventing duplication of spatial elements retained by table-only splitting.

CSV and Zarr annotation sources cannot be mixed in one invocation. Run the tool twice with different output directories if both source types are required.


ID matching and conflict handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-

By default, the parent and Zarr sources use their SpatialData ``instance_key``. For a single region with globally unique IDs, this key is sufficient. For multiple regions or repeated barcodes, matching uses ``(region_key, instance_key)``.

CSV files for multi-region parents must therefore contain a region or sample column. Specify non-standard columns with:

.. code-block:: bash

   --csv_region_col=sample_id \
   --input_region_col=region

Rows are never matched by position. The original parent observation order is retained.

The default policies are:

.. code-block:: yaml

   conflict_policy: "error"
   existing_policy: "overwrite_matched"
   min_match_rate: 0.95

- ``conflict_policy=error`` stops when sources assign different labels to the same cell. ``first`` and ``last`` are available only when deliberate precedence is required.
- ``existing_policy=overwrite_matched`` updates matched observations. ``fill_missing`` only fills empty values, whereas ``error`` refuses an existing target column.
- ``min_match_rate`` is calculated relative to valid source IDs, not all observations in the parent.


Key parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 26 22 52

   * - Parameter
     - Default
     - Description
   * - ``merge_by``
     - ``sample``
     - Selects independent-sample concatenation or parent annotation overlay
   * - ``output_name``
     - ``concatenated_sdata.zarr``
     - Output Zarr directory name
   * - ``table_key``
     - empty
     - Required when a SpatialData object contains multiple tables
   * - ``sample_ids``
     - empty
     - Optional source IDs corresponding to sample inputs
   * - ``sample_col``
     - ``sample``
     - Observation column containing sample identities
   * - ``feature_join``
     - ``inner``
     - Gene intersection or union for sample concatenation
   * - ``label_policy``
     - ``preserve``
     - Preserves, prefixes, or offsets columns listed in ``label_cols``
   * - ``annotation_csv``
     - empty
     - CSV file, directory, or comma-separated CSV paths
   * - ``annotation_col``
     - ``auto``
     - Source annotation column
   * - ``target_col``
     - ``sub_celltype``
     - Parent column receiving refined labels
   * - ``fallback_col``
     - ``celltype``
     - Parent column used to initialize a new target column
   * - ``conflict_policy``
     - ``error``
     - Controls contradictory labels for the same observation
   * - ``existing_policy``
     - ``overwrite_matched``
     - Controls updates when ``target_col`` already exists
   * - ``min_match_rate``
     - ``0.95``
     - Minimum accepted source-to-parent ID match rate


Result validation
-----------------

The tool writes the result to a temporary Zarr, reloads it, validates the selected table and spatial metadata, and then replaces the final output. ``merge_report.csv`` records the inputs and validation-relevant counts.

For sample mode, verify that:

- the merged observation count equals the sum across inputs;
- sample IDs and spatial element names are unique;
- expected ``obs`` and ``obsm`` results are present;
- no cross-sample spatial edges were introduced.

For annotation mode, verify that:

- the parent observation count and order are unchanged;
- the original broad annotation remains present;
- the target column contains the expected refined labels;
- parent images, shapes, points, labels, and expression matrices are unchanged.


Analysis boundaries
-------------------

``merge`` assembles compatible data containers and metadata. Adjacent-section alignment requires a spatial registration method, while cross-sample batch correction or joint clustering should be performed in the corresponding integration and clustering modules. Differential analysis should continue to use biological sample identities rather than treating spots or cells as independent replicates.
