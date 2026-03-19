Select your data platform
=========================

本章按 ``run_type`` 拆分为 6 个子教程。每个子教程都包含：

- 全部输入文件清单（必选/可选、文件格式、通配规则）
- 文件来源与获取方式（平台官方下载、实验输出、占位符写法）
- 可复制目录结构示例
- 对应 ``integrate`` 运行命令与 ``sample.txt`` 示例

run_type 选择速览
-----------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - run_type
     - 产物类型
     - 入口页面
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

对于每个平台的类型我们提供了不同的公共数据集进行演示。

.. list-table::
   :header-rows: 1
   :widths: 18 22 30 30

   * - run_type
     - 演示数据名称（建议）
     - 数据来源
     - 下载链接（待填写）
   * - ``visium``
     - Visium_BreastCancer_Section1
     - 10x Genomics
     - ``<VISIUM_DATASET_URL>``
   * - ``visium_segment``
     - Visium_Segmentation_Demo
     - 10x Genomics / Lab output
     - ``<VISIUM_SEGMENT_DATASET_URL>``
   * - ``visium_HD``
     - VisiumHD_MouseBrain_Demo
     - 10x Genomics
     - ``<VISIUM_HD_DATASET_URL>``
   * - ``xenium``
     - Xenium_Human_Breast_Demo
     - 10x Genomics
     - ``<XENIUM_DATASET_URL>``
   * - ``Merfish``
     - MERFISH_Vizgen_Demo
     - Vizgen
     - ``<MERFISH_DATASET_URL>``
   * - ``slide_seq``
     - SlideSeq_Mouse_Hippocampus_Demo
     - Public repository / Lab output
     - ``<SLIDE_SEQ_DATASET_URL>``

先看这两个共性规则
------------------

1. ``sample.txt`` 第一行是表头，后续每行一个样本，列间用空格或 tab 分隔。
2. 执行 ``--option=integrate`` 时，程序会先校验输入目录关键文件，再自动识别 count 文件名。

sample.txt 列规则
-----------------

- ``single_analysis``：至少两列（``sample_id input_path``）。
- ``compare_analysis``：至少三列（``sample_id input_path group``）。
- ``visium_HD``：必须提供 bin 列；单样本三列（``sample_id input_path bin``），比较分析四列（``sample_id input_path bin group``）。

.. note::

   If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration` after reading the single sample tutorials for basic Usage.


按数据类型查看详细教程
----------------------

.. toctree::
   :maxdepth: 1

   visium
   visium_segment
   visium_hd
   xenium
   merfish
   slide_seq

.. note::

   如果路径看起来正确但仍报错，先检查 ``sample.txt`` 是否存在全角空格、隐藏字符或错误换行。
   多样本读取与整合请直接参考 :doc:`/integration_analysis/multi_sample_integration`。
