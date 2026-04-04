merge.yaml Reference
====================

This configuration file corresponds to ``spatialsnake useful_tool --option=merge`` and is used for object merging and external annotation write-back.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Parameter
     - Default
     - Description
   * - ``output_dir``
     - ``results/useful_results``
     - Output directory for merged results
   * - ``merge_by``
     - ``sample``
     - Merge strategy, such as ``sample``, ``clusters``, ``celltype``, or ``reannotation``
   * - ``reordering``
     - ``False``
     - Whether to reorder cluster labels
   * - ``re_sample``
     - ``False``
     - Whether to rebuild sample names
   * - ``cluster_key``
     - ``clusters``
     - Name of the clustering field
   * - ``annotation_csv``
     - ``""``
     - Path to an external annotation file for the ``reannotation`` branch
   * - ``csv_cell_col``
     - ``Barcode``
     - Cell ID column name in the external annotation file
   * - ``csv_label_col``
     - ``Grouped_Annotation``
     - Label column name in the external annotation file
   * - ``input_cell_col``
     - ``cell_id``
     - Cell ID column name in the input object
   * - ``target_col``
     - ``sub_celltype``
     - Target column name for annotation write-back
   * - ``original_celltype_col``
     - ``celltype``
     - Original label column used as a fallback reference

Tuning suggestions
------------------

1. For standard merging, ``merge_by`` and ``output_dir`` are usually sufficient.
2. For external annotation write-back, first verify that ``csv_cell_col`` and ``input_cell_col`` match correctly.
3. When writing back new labels, it is usually better to change ``target_col`` and preserve the original ``celltype`` column for traceability.
