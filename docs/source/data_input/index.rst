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
Please first follow the instructions below to set up the basic directory structure:


.. code-block:: bash

   mkdir -p project_root/data project_root/results
   touch project_root/sample.txt

.. code-block:: text

   project_root/ (current working directory)
   ├── data/ (stores your raw data)
   ├── sample.txt (key sample description file)
   └── results/ (stores analysis outputs; generated automatically)

After identifying your data platform, download and store the platform-specific output files under the ``data/`` directory, using the sample name as the subdirectory name. Ensure that the folder hierarchy follows the official output structure of that platform. At the same time, add the corresponding sample name to ``sample.txt`` so that Spatialsnake can correctly read the input files.
Whether your goal is single-sample analysis or you have multiple samples from different experimental conditions and intend to perform multi-sample integration, we recommend first selecting the tutorial for your specific platform to learn the basic workflow. The multi-sample analysis pipeline is broadly similar once you understand the fundamentals.


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
     - Visium_BreastCancer_Section1
     - 10x Genomics
     - `E-MTAB-11114 <https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/114/E-MTAB-11114/Files>`_
   * - ``visium_HD``
     - VisiumHD_MouseBrain_Demo
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
   * - ``Stereo-seq``
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
