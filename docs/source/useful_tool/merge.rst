Merge Tool (``merge``)
======================

``merge`` is used either to combine multiple ``zarr`` objects into one object or to write external annotation results back into a base object.
For users without a programming background, it can be understood as a tool for "multi-object concatenation plus annotation-field write-back".

For the configuration reference, see :doc:`../config_reference/merge_yaml`.

Typical use cases
-----------------

1. You want to merge multiple sample-level analysis results into one combined object for comparative analysis.
2. You want to merge multiple subset objects back into one object for downstream processing.
3. You have completed subcluster annotation and want to write ``celltype_annotations.csv`` back into the original parent object.


Before you start
----------------

Make sure that:

1. All input objects are valid ``.zarr`` paths.
2. For reannotation write-back, the CSV contains at least a cell ID column and an annotation label column.
3. The command is executed from the correct working directory, or absolute paths are used.


Command template
----------------

.. code-block:: bash

   spatialsnake useful_tool --option=merge <INPUT1> <INPUT2> ... --merge_by=<mode> --output_dir=results/useful_results


Scenario 1: merge by sample
---------------------------

Use this mode to combine multiple sample objects into one ``concatenated_sdata.zarr`` object.

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/S1/annotation/S1.zarr results/S2/annotation/S2.zarr --merge_by=sample --re_sample=True --output_dir=results/useful_results

Notes:

- With ``--re_sample=True``, if the object lacks a ``sample`` column, the tool automatically reconstructs it from the filename.
- The output file is always written as ``results/useful_results/concatenated_sdata.zarr``.


Scenario 2: merge by cluster labels and reorder them
----------------------------------------------------

Use this mode to merge multiple objects by cluster labels and remap cluster IDs into a continuous sequence so that label conflicts are avoided.

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/S1/annotation/S1.zarr results/S2/annotation/S2.zarr --merge_by=clusters --cluster_key=clusters --reordering=True --output_dir=results/useful_results

If you want to reorder another column, such as ``celltype``, change ``--cluster_key`` accordingly:

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/subset1.zarr results/subset2.zarr --merge_by=clusters --cluster_key=celltype --reordering=True --output_dir=results/useful_results

Notes:

- With ``--reordering=True``, the script remaps labels from each object into a new continuous series following the input order.
- With ``--reordering=False``, original labels are preserved, which is suitable when all objects already use a unified label system.


Scenario 3: write external reannotation results back into the base object
-------------------------------------------------------------------------

Use this mode to write annotation results from an external CSV file back into the original ``zarr`` object, which is especially useful after subcluster annotation.

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr --merge_by=reannotation --annotation_csv=results/reclustering/celltype_annotations.csv --csv_cell_col=Barcode --csv_label_col=Grouped_Annotation --input_cell_col=cell_id --target_col=sub_celltype --original_celltype_col=celltype --output_dir=results/useful_results

Notes:

- ``--annotation_csv`` can be a single CSV file, a directory, or multiple CSV paths separated by commas.
- The tool matches cells by ID and updates ``target_col`` accordingly.
- If no label is found for a cell in the CSV file, the existing value in ``target_col`` is preserved; if that field does not exist, the tool falls back to ``original_celltype_col``.


Key parameters in practice
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 20 56

   * - Parameter
     - Typical values
     - Description
   * - ``--merge_by``
     - ``sample`` / ``clusters`` / ``reannotation``
     - Selects the merge mode
   * - ``--re_sample``
     - ``True`` / ``False``
     - When ``merge_by=sample``, determines whether the ``sample`` column is reconstructed automatically
   * - ``--reordering``
     - ``True`` / ``False``
     - When ``merge_by=clusters``, determines whether cluster labels are reordered to avoid conflicts
   * - ``--cluster_key``
     - ``clusters`` / ``celltype`` / ``leiden``
     - Selects the column used for cluster-label merging or reordering
   * - ``--annotation_csv``
     - ``anno.csv`` / ``anno_dir`` / ``a.csv,b.csv``
     - Source of annotation data in ``reannotation`` mode
   * - ``--csv_cell_col``
     - ``Barcode`` / ``cell_id``
     - Column name in the CSV file used to match cell IDs
   * - ``--csv_label_col``
     - ``Grouped_Annotation`` / ``celltype``
     - Column name in the CSV file containing annotation labels
   * - ``--input_cell_col``
     - ``cell_id``
     - Column name in the base ``zarr`` object used for cell ID matching
   * - ``--target_col``
     - ``sub_celltype``
     - Target column used for writing the annotation back
   * - ``--original_celltype_col``
     - ``celltype``
     - Fallback reference column if ``target_col`` does not yet exist
   * - ``--output_dir``
     - ``results/useful_results``
     - Output directory


How to validate the results
---------------------------

1. Check whether ``concatenated_sdata.zarr`` or the expected output object has been generated.
2. Try loading the object in the downstream workflow to confirm that it can be used normally.
3. In ``reannotation`` mode, verify that the expected new labels appear in ``target_col``.


Common errors and how to fix them
---------------------------------

1. ``annotation csv not found``

   - Cause: the path given in ``--annotation_csv`` is incorrect.
   - Fix: use an absolute path, or confirm that the directory actually contains CSV files.

2. ``required columns not found in <csv>``

   - Cause: the CSV file is missing either the cell ID column or the label column.
   - Fix: check that ``--csv_cell_col`` and ``--csv_label_col`` match the actual column names.

3. ``no tables found in base zarr``

   - Cause: the input object is invalid or the path is not a valid ``zarr`` object.
   - Fix: first confirm that the object can be loaded correctly in the upstream workflow.


Suggested next steps
--------------------

- After merging, continue to downstream comparison or visualization modules for cross-sample analysis.
- After reannotation write-back, continue with annotation export and result review.
