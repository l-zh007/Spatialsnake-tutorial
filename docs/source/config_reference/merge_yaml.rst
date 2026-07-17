merge.yaml Reference
====================

This configuration controls ``spatialsnake useful_tool --option=merge``. The utility supports independent-sample concatenation and annotation write-back to a complete parent SpatialData object.

.. list-table::
   :header-rows: 1
   :widths: 28 20 52

   * - Parameter
     - Default
     - Description
   * - ``output_dir``
     - ``results/useful_results``
     - Output directory
   * - ``output_name``
     - ``concatenated_sdata.zarr``
     - Output Zarr directory name
   * - ``table_key``
     - ``""``
     - Table selected when an object contains multiple tables
   * - ``merge_by``
     - ``sample``
     - ``sample`` or ``annotation``
   * - ``sample_ids``
     - ``""``
     - Comma-separated source IDs in input order
   * - ``sample_col``
     - ``sample``
     - Observation column containing sample identities
   * - ``feature_join``
     - ``inner``
     - ``inner`` retains shared genes; ``outer`` retains the union
   * - ``label_cols``
     - ``""``
     - Comma-separated observation labels transformed during sample merge
   * - ``label_policy``
     - ``preserve``
     - ``preserve``, ``prefix``, or ``offset``
   * - ``annotation_csv``
     - ``""``
     - CSV file, directory, or comma-separated CSV files used in annotation mode
   * - ``annotation_col``
     - ``auto``
     - Annotation column in CSV or subset Zarr sources
   * - ``target_col``
     - ``sub_celltype``
     - Parent observation column receiving annotations
   * - ``fallback_col``
     - ``celltype``
     - Parent column used to initialize a new target column
   * - ``csv_cell_col``
     - ``auto``
     - Cell or spot ID column in annotation CSV files
   * - ``csv_region_col``
     - ``auto``
     - Region or sample column used when IDs repeat across regions
   * - ``input_cell_col``
     - ``auto``
     - Parent cell ID column; ``auto`` uses the SpatialData instance key
   * - ``input_region_col``
     - ``auto``
     - Parent region column; ``auto`` uses the SpatialData region key
   * - ``conflict_policy``
     - ``error``
     - ``error``, ``first``, or ``last`` for contradictory source labels
   * - ``existing_policy``
     - ``overwrite_matched``
     - ``overwrite_matched``, ``fill_missing``, or ``error``
   * - ``min_match_rate``
     - ``0.95``
     - Minimum valid source ID fraction matched to the parent


Recommended use
---------------

1. Use ``merge_by=sample`` for independent samples after sample-level RCTD, cell2location, annotation, or clustering.
2. Use ``merge_by=annotation`` with the original parent plus CSV files or subset Zarr tables after reclustering and reannotation.
3. Keep ``feature_join=inner`` for samples produced by the same platform unless a gene-union analysis is explicitly required.
4. Keep ``conflict_policy=error`` and inspect ``merge_report.csv`` before downstream analysis.
5. ``merge`` does not perform batch correction or spatial registration.

Subsets derived from one parent are not independent samples. Do not pass table-only splitting outputs to ``merge_by=sample`` to reconstruct the parent: each subset still contains the parent's spatial elements, which would be duplicated under sample-specific element and region names during concatenation. Instead, pass the original parent as the first input to ``merge_by=annotation`` and use the subset CSV or Zarr tables only as annotation sources. This preserves the parent expression matrices, observation order, and spatial geometry while adding the refined annotation column.

Sample concatenation checks observation and spatial-element names before renaming. Names that are already globally unique are retained; sample suffixes are added only when a real collision must be resolved. This prevents redundant suffix accumulation when a previously merged object is used in a later merge.
