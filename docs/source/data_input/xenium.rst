Xenium 输入教程
===============

``run_type: xenium`` 这里我们使用 10xgenomics 官网公开数据集 中的 breast cancer

link: https://www.10xgenomics.com/datasets/xenium-prime-ffpe-human-breast-cancer


必需文件清单
------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - 文件名/通配
     - 必选
     - 格式
     - 说明
   * - ``cells.parquet``
     - 是
     - Parquet
     - 细胞级统计与坐标
   * - ``transcripts.parquet``
     - 是
     - Parquet
     - 转录本点位信息
   * - ``morphology.ome.tif``
     - 是
     - OME-TIFF
     - 形态学图像
   * - ``experiment.xenium``
     - 是
     - Xenium 元数据
     - 平台信息与文件索引
   * - ``cell_feature_matrix.h5`` / ``filtered_feature_cell_matrix.h5`` / ``raw_feature_cell_matrix.h5`` / ``filtered_feature_bc_matrix.h5`` / ``raw_feature_bc_matrix.h5``
     - 否
     - H5
     - 可被自动识别的候选矩阵名

文件来源与获取方式
------------------------

- 官方下载：10x Xenium on-board analysis 导出目录。
- 实验输出：平台交付的完整样本目录。


目录结构示例
------------

.. code-block:: text

   data/
   └── breast_cancer/
       ├── experiment.xenium
       ├── cells.parquet
       ├── transcripts.parquet
       ├── morphology.ome.tif
       └── cell_feature_matrix.h5
       └──  ........

sample.txt 示例
---------------

single_analysis：

.. code-block:: text

   sample_id input_path
   breast_cancer data/breast_cancer


Run the command (make sure the sample.txt file is in your current working directory)
-------------------------------------------------------------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt xenium --option integrate

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── breast_cancer/
   │   └── integrate/
   │       ├── breast_cancer.zarr
   │       ├── total.png
   │       ├── total_umi_by_sample.png
   │       ├── total_genes_by_sample.png
   │       ├── genes_by_sample.png
   │       └── scatter.png

输出解释
--------------------

- 附加 QC 图：读取脚本会在 ``integrate`` 目录写入 5 张质控图。


If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration`.
else continue to :doc:`data_input/index`