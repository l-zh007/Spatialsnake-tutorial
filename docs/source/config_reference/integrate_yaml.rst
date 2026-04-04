integrate.yaml Reference
========================

This configuration file corresponds to ``--option=integrate`` and defines how input data are organized for ingestion and cross-sample integration. The default values are listed below.

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - Parameter
     - Default
     - Description
   * - ``option``
     - ``integrate``
     - Fixed identifier for the analysis stage
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
     - Platform type, such as ``visium``, ``visium_HD``, or ``xenium``
   * - ``channel``
     - ``compare_analysis``
     - Analysis channel, either single-sample or multi-sample
   * - ``cells_boundaries``
     - ``False``
     - Whether to load the cell boundary layer for Xenium
   * - ``nucleus_boundaries``
     - ``False``
     - Whether to load the nucleus boundary layer for Xenium
   * - ``nucleus_labels``
     - ``False``
     - Whether to load the nucleus label layer for Xenium
   * - ``morphology_mip``
     - ``False``
     - Whether to load the morphology MIP image for Xenium
   * - ``geojson``
     - ``cell_segmentations.geojson``
     - Segmentation filename for ``visium_segment``
   * - ``image``
     - ``tissue_hires_image.png``
     - Tissue image filename for ``visium_segment``
   * - ``scale_factors``
     - ``scalefactors_json.json``
     - Scale factor filename
   * - ``coor_file``
     - ``BeadLocationsForR.csv``
     - Coordinate filename for ``slide_seq``

Tuning suggestions
------------------

1. In most projects, you only need to modify ``run_type``, ``channel``, and ``sample_list``.
2. Enable or adjust layer-related parameters only for Xenium or ``visium_segment`` data.
3. In collaborative projects, keep ``results_folder`` fixed so that downstream paths remain stable and reproducible.
