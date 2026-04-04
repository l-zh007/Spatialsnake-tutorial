Select your data platform
=========================

This chapter is divided into six sub-tutorials according to the ``run_type`` platform. Each tutorial covers the corresponding starting steps for analysis.
Before running the workflow, you need to organize the raw data according to the platform requirements and prepare the sample list file ``sample.txt`` so that the SpatialData ``zarr`` object can be created correctly.

- Complete input file checklist, including required and optional files, file formats, and filename patterns
- File sources and how to obtain them, such as official platform downloads, experimental outputs, or placeholder paths
- Reproducible directory structure examples
- Example ``integrate`` commands and matching ``sample.txt`` formats

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
     - :doc:`visium_hd`
   * - ``xenium``
     - ``.zarr``
     - :doc:`xenium`
   * - ``Merfish``
     - ``.zarr``
     - :doc:`merfish`
   * - ``slide_seq``
     - ``.h5ad``
     - :doc:`slide_seq`
   * - ``stereo_seq``
     - ``.h5ad``
     - :doc:`slide_seq`

For each supported platform, we provide a public demonstration dataset.

.. list-table::
   :header-rows: 1
   :widths: 18 22 30 30

   * - run_type
     - Demo dataset
     - Source
     - Download link
   * - ``visium``
     - Visium_BreastCancer_Section1
     - 10x Genomics
     - ``https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/114/E-MTAB-11114/Files``
   * - ``visium_HD``
     - VisiumHD_MouseBrain_Demo
     - 10x Genomics
     - ``https://www.10xgenomics.com/platforms/visium/product-family/dataset-human-crc``
   * - ``visium_segment``
     - Visium_Segmentation_Demo
     - 10x Genomics / Lab output
     - ``<https://cf.10xgenomics.com/supp/spatial-exp/analysis-workshop/multisample_raw_data.tar.gz>``
   * - ``xenium``
     - Xenium_Human_Breast_Demo
     - 10x Genomics
     - ``<https://www.10xgenomics.com/datasets/xenium-prime-ffpe-human-breast-cancer>``
   * - ``Merfish``
     - MERFISH_Vizgen_Demo
     - Vizgen
     - ``<MERFISH_DATASET_URL>``
   * - ``slide_seq``
     - SlideSeq_Mouse_Hippocampus_Demo
     - Public repository / Lab output
     - ``<SLIDE_SEQ_DATASET_URL>``

.. note::
    If you want to gain a basic understanding of SpatialSnake's functionality using our sample data, please jump directly to :doc:`/core_analysis/index` and follow the instructions to proceed.

Detailed tutorials by data type
-------------------------------

.. toctree::
   :maxdepth: 1

   visium
   visium_hd
   visium_segment
   xenium
   merfish
   slide_seq

.. note::

   If you want to run multi-sample integration analysis, we recommend moving to :doc:`/integration_analysis/multi_sample_integration` after first reading the single-sample tutorials for the basic workflow.
