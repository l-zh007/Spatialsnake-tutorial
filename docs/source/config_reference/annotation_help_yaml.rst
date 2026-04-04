annotation_help.yaml Reference
==============================

This configuration file corresponds to ``--option=annotation_help`` and is used for marker statistics, spatial rendering, and pathway-enrichment support.

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - Parameter
     - Default
     - Description
   * - ``option``
     - ``advance_analysis``
     - Stage identifier field stored in the file
   * - ``results_folder``
     - ``results``
     - Root directory for analysis outputs
   * - ``data_fold``
     - ``data``
     - Root directory for raw input data
   * - ``sample_list``
     - ``sample.txt``
     - Path to the sample list file
   * - ``run_type``
     - ``visium``
     - Platform type
   * - ``channel``
     - ``compare_analysis``
     - Analysis channel
   * - ``markers_algorithm``
     - ``wilcoxon``
     - Statistical method used for marker gene detection
   * - ``shape_type``
     - ``False``
     - Keyword used to filter shape layer names
   * - ``image_type``
     - ``False``
     - Keyword used to filter image layer names
   * - ``species``
     - ``human``
     - Species background used for GO or KEGG enrichment
   * - ``image_slice``
     - ``False``
     - Whether to crop the image
   * - ``x1`` / ``x2`` / ``y1`` / ``y2``
     - ``0``
     - Coordinates of the cropping window

Tuning suggestions
------------------

1. First confirm the appropriate ``markers_algorithm`` and species background ``species``.
2. Enable ``image_slice`` and define coordinates only when reviewing a local tissue region.
3. For cross-sample comparisons, keep ``image_type`` and ``shape_type`` as consistent as possible.
