Select your data platform
=========================

This chapter contains one input tutorial for each supported ``run_type``.
Before running the workflow, organize the raw data according to the platform
requirements and prepare ``sample.txt`` so that Spatialsnake can create a
SpatialData Zarr object.

- Complete input file checklist, including required and optional files, file formats, and filename patterns
- File sources and how to obtain them, such as official platform downloads, experimental outputs, or placeholder paths
- Reproducible directory structure examples
- Example ``integrate`` commands and matching ``sample.txt`` formats


Spatial transcriptomics platforms provide dedicated primary-processing software,
such as Space Ranger for 10x Genomics data and SAW for BGI Stereo-seq data.
These tools align reads or decode transcripts and produce expression and spatial
outputs. Spatialsnake reads these processed outputs and represents them in a
common SpatialData object for downstream analysis.
Use the project-root layout described in :doc:`../usage`. Each platform page
shows its required files and core sample table. After ingestion, continue with
:doc:`../core_analysis/preprocess`; multi-sample users should prepare the cohort
table using :doc:`../integration_analysis/multi_sample_integration` first.

The analysis stages are shared, but filtering thresholds, resolution, species,
and image/shape/point layers depend on the data. Do not copy CRC P2 thresholds
or cell labels to a different platform without inspecting your own results.


Quick reference for ``run_type``
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - run_type
     - Output type
     - Tutorial page
   * - ``visium``
     - ``.zarr``
     - :doc:`visium`
   * - ``visium_segment``
     - ``.zarr``
     - :doc:`visium_segment`
   * - ``visium_HD``
     - ``.zarr``
     - :doc:`visium_HD`
   * - ``xenium``
     - ``.zarr``
     - :doc:`xenium`
   * - ``Merfish``
     - ``.zarr``
     - :doc:`Merfish`
   * - ``stereoseq``
     - ``.zarr``
     - :doc:`stereo-seq`

For each supported platform, we provide a public demonstration dataset.

.. list-table::
   :header-rows: 1
   :widths: 18 22 30 30

   * - run_type
     - Demo dataset
     - Source
     - Download link
   * - ``visium``
     - Visium_FFPE_Mouse_Brain
     - 10x Genomics
     - `Adult Mouse Brain FFPE <https://www.10xgenomics.com/datasets/adult-mouse-brain-ffpe-1-standard-1-3-0>`_
   * - ``visium_HD``
     - Human Colon Cancer P2
     - 10x Genomics
     - `Human CRC P2 <https://www.10xgenomics.com/platforms/visium/product-family/dataset-human-crc>`_
   * - ``visium_segment``
     - Visium_Segmentation_Demo
     - 10x Genomics / Lab output
     - `multisample_raw_data.tar.gz <https://cf.10xgenomics.com/supp/spatial-exp/analysis-workshop/multisample_raw_data.tar.gz>`_
   * - ``xenium``
     - Xenium_Human_Breast_Demo
     - 10x Genomics
     - `Xenium Prime FFPE <https://www.10xgenomics.com/datasets/xenium-prime-ffpe-human-breast-cancer>`_
   * - ``Merfish``
     - MERFISH_Vizgen_Demo
     - Vizgen
     - `Vizgen MERFISH <https://console.cloud.google.com/storage/browser/vz-merfish2-showcase/202409242358_240916JHHUBC0005XQ-V2V-HubcTMA-V2-BY_VMSC02511>`_
   * - ``stereoseq``
     - Stereo-seq Mouse_Brain demo
     - Public repository
     - `STOmics Mouse_Brain <https://www.stomics.tech/col1317>`_

.. note::
   To follow the complete analysis workflow with the demonstration data,
   continue to :doc:`/core_analysis/index`.

Detailed tutorials by data type
-------------------------------

.. toctree::
   :maxdepth: 1

   visium
   visium_HD
   visium_segment
   xenium
   Merfish
   stereo-seq

.. note::

   If you want to run multi-sample integration analysis, we recommend moving to :doc:`/integration_analysis/multi_sample_integration` after first reading the single-sample tutorials for the basic workflow.
