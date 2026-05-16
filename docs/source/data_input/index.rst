Select your data platform
=========================

This chapter is divided into six sub-tutorials according to the ``run_type`` platform. Each tutorial covers the corresponding starting steps for analysis.
Before running the workflow, you need to organize the raw data according to the platform requirements and prepare the sample list file ``sample.txt`` so that the SpatialData ``zarr`` object can be created correctly.

- Complete input file checklist, including required and optional files, file formats, and filename patterns
- File sources and how to obtain them, such as official platform downloads, experimental outputs, or placeholder paths
- Reproducible directory structure examples
- Example ``integrate`` commands and matching ``sample.txt`` formats


对于一个基本的空间转录组测序平台来说都会存在基本的测序后分析软件，例如10x genomic 的Spaceranger、华大基因平台SAW 等。通过这些软件可以对空间转录组数据进行基本的分析，例如原始的fastq数据比对计数等。
Spatialsnake负责将各个软件的标准输出结果整合到一个SpatialData对象中，方便后续的分析和可视化。
对于所有的平台，Spatialsnake都提供了对应的教程，帮助用户快速上手。
首先请先完成下述教程，构建基本的文件层级结构:


.. code-block:: bash

   mkdir -p project_root/data project_root/results
   touch project_root/sample.txt

.. code-block:: text

   project_root/ (current working directory)
   ├── data/ (stores your raw data)
   ├── sample.txt (key sample description file)
   └── results/ (stores analysis outputs; generated automatically)

请后续确定您的数据平台，根据不同的平台，将所用到的软件输出数据下载存储到data目录下，以样本名称为目录名，层级符合官方输出文件层级结构,同时请在sample.txt文件中添加对应样本名称以便spatialsnake能正确读取对应文件。
无论您的分析目的为单样本分析 还是您手上存在多个不同实验条件的样本有意进行多样本整合分析，我们都推荐您先选择对应的平台教程进行初步的学习，了解基本的使用流程，多样本流程则大差不差


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
   * - ``stereo_seq``
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
     - ``<https://console.cloud.google.com/storage/browser/vz-merfish2-showcase/202409242358_240916JHHUBC0005XQ-V2V-HubcTMA-V2-BY_VMSC02511>``
   * - ``slide_seq``
     - SlideSeq_Mouse_Hippocampus_Demo
     - Public repository / Lab output
     - ``<https://www.stomics.tech/col1317>``

.. note::
    If you want to gain a basic understanding of SpatialSnake's functionality using our sample data, please jump directly to :doc:`/core_analysis/index` and follow the instructions to proceed.

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
