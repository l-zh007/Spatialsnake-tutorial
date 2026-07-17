splitting.yaml Reference
========================

This configuration corresponds to ``spatialsnake useful_tool --option=splitting``. The command continues to execute ``workflow/function/splitting.py`` directly with Python; the YAML file supplies defaults and does not define a Snakemake workflow.

.. list-table::
   :header-rows: 1
   :widths: 28 20 52

   * - Parameter
     - Default
     - Description
   * - ``INPUT_FILE``
     - empty
     - Input ``zarr`` or ``h5ad`` path supplied positionally on the command line
   * - ``output_zarr_path``
     - ``results``
     - Legacy output-root field retained for compatibility
   * - ``output_dir``
     - ``results/useful_results``
     - Output directory for subset objects, annotation CSV files, and available previews
   * - ``split_by``
     - ``sample``
     - Observation metadata column or special mode: ``sample``, ``region``, ``group``, ``ROI``, or ``image``
   * - ``barcodes``
     - ``None``
     - Optional values to retain; commas combine labels into one output and pipes create independent outputs
   * - ``table_key``
     - ``""``
     - Table to split when a SpatialData object contains multiple tables; a single table is selected automatically and ``table`` is preferred
   * - ``subset_mode``
     - ``table``
     - ``table`` filters observations while retaining complete spatial elements; ``spatial`` also synchronizes associated Shapes or Points
   * - ``shape_elements``
     - ``None``
     - Legacy spatial-element or coordinate-system selector retained for image-crop compatibility
   * - ``coordinate_system``
     - ``""``
     - Explicit coordinate system for polygon ROI selection or bounding-box cropping
   * - ``roi_csv``
     - ``""``
     - Loupe/Xenium ROI CSV file or directory; supports barcode tables, selected-cell tables, and polygon-coordinate tables
   * - ``roi_label_col``
     - ``""``
     - ROI label column used when an ID table contains more than one possible annotation column
   * - ``roi_region``
     - ``""``
     - Region restriction for integrated objects whose instance identifiers are not globally unique
   * - ``annotation_format``
     - ``auto``
     - Annotation export format: ``auto``, ``loupe``, ``xenium``, ``both``, or ``none``
   * - ``annotation_cols``
     - ``""``
     - Comma-separated additional ``obs`` columns exported for external visualization
   * - ``max_x`` / ``min_x`` / ``max_y`` / ``min_y``
     - ``0``
     - Floating-point coordinate boundaries used only for ``split_by=image``; minima must be smaller than maxima


Mode-specific behavior
----------------------

``metadata``
   Any column in ``table.obs`` can be used as ``split_by``. With an empty ``barcodes`` value, every category is exported independently. ``A,B`` combines categories into one object, whereas ``A|B`` creates two objects.

``sample`` / ``region`` / ``group``
   Sample and region modes retain their coordinate-system-based SpatialData behavior. A group is exported by complete coordinate systems only when the region-to-group mapping is unambiguous; otherwise its table is filtered by observation identity.

``ROI``
   Accepts Loupe ``barcode,<category>`` tables, Xenium selected-cell tables containing ``Cell ID``, and Xenium polygon tables containing ``Selection,X,Y`` or legacy ``X,Y``. ID matching uses the SpatialData instance key and never row position. Set ``roi_region`` when IDs repeat across samples.

``image``
   Performs a true SpatialData bounding-box crop and therefore does not use table-only behavior. Set ``coordinate_system`` and valid coordinate boundaries when the object contains multiple spatial systems.


Important compatibility behavior
--------------------------------

1. Keep ``subset_mode: "table"`` for the usual reclustering or reannotation workflow. The filtered table retains its original observation IDs, order, layers, ``obsm``, variables, and ``spatialdata_attrs``; images, labels, Shapes, Points, and transformations remain complete.
2. Set ``subset_mode: "spatial"`` only when associated Shapes or Points should be filtered with the selected observations. Use ``split_by: "image"`` when a raster image also needs to be cropped.
3. Table-only output may remain large on disk because non-table spatial elements are intentionally retained.
4. Points-only Stereo-seq objects are supported; a Shapes element is not required for metadata or ID-based ROI splitting.


ROI and annotation CSV formats
------------------------------

The ROI reader recognizes the following structures:

.. code-block:: text

   barcode,ROI
   AAACAAGTATCTCCCA-1,Tumor_edge

.. code-block:: text

   Cell ID,Selection
   101,ROI_1

.. code-block:: text

   Selection,X,Y
   ROI_1,100.5,230.0

Annotation output is controlled by ``annotation_format``. Loupe output contains ``barcode`` followed by one or more annotation columns. Xenium Explorer output uses one ``cell_id,group`` file per annotation column. ``annotation_cols`` can add fields such as ``celltype``, ``clusters``, or ``spatial_cluster``. Set ``annotation_format: "none"`` when no interoperability CSV is required.


Tuning suggestions
------------------

1. For downstream subclustering, use a metadata field with ``subset_mode: "table"``. Use commas when several populations should be analyzed together and pipes when they should be processed independently.
2. For an ROI exported from external software, leave format detection automatic. Set ``roi_label_col``, ``roi_region``, or ``coordinate_system`` only when the input is genuinely ambiguous.
3. Use ``annotation_format: "auto"`` for routine work, ``both`` when the same result must be inspected in both Loupe and Xenium Explorer, and ``none`` to suppress CSV export.
4. For a rectangular physical crop, use ``split_by: "image"`` and provide the coordinate system and all four boundaries.
5. Keep ``output_dir`` fixed across related splitting commands to simplify subsequent ``sample.txt`` construction.
