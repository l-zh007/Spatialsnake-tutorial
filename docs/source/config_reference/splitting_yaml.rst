splitting.yaml Reference
========================

This configuration file corresponds to ``spatialsnake useful_tool --option=splitting`` and is used to split objects by sample, label, or spatial range.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Parameter
     - Default
     - Description
   * - ``output_zarr_path``
     - ``results``
     - Root directory for exported ``zarr`` objects
   * - ``split_by``
     - ``sample``
     - Splitting mode, such as ``sample``, ``group``, ``clusters``, ``celltype``, ``ROI``, or ``image``
   * - ``output_dir``
     - ``results/useful_results``
     - Output directory
   * - ``shape_elements``
     - ``None``
     - Shape element used when splitting by image
   * - ``max_x`` / ``min_x`` / ``max_y`` / ``min_y``
     - ``0``
     - Coordinate boundaries used for image-based splitting
   * - ``barcodes``
     - ``None``
     - Labels to retain, separated by commas
   * - ``roi_csv``
     - ``""``
     - Path to an ROI table or ROI directory

Tuning suggestions
------------------

1. For label-based splitting, start with ``split_by`` together with ``barcodes``.
2. For local tissue cropping, use ``split_by=image`` and define the coordinate boundaries at the same time.
3. If you perform multiple rounds of splitting, keep ``output_dir`` fixed to simplify output management.
