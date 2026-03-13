Xenium 输入教程
===============

适用 ``run_type: xenium``。

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
- 占位符写法：先写 ``/path/to/xenium_sample``，等你补齐实际路径。

目录结构示例
------------

.. code-block:: text

   data/
   └── X1/
       ├── experiment.xenium
       ├── cells.parquet
       ├── transcripts.parquet
       ├── morphology.ome.tif
       └── cell_feature_matrix.h5

sample.txt 示例
---------------

single_analysis：

.. code-block:: text

   sample_id input_path
   X1 data/X1
   X2 data/X2

compare_analysis：

.. code-block:: text

   sample_id input_path group
   X1 data/X1 tumor
   X2 data/X2 normal

运行命令示例
------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type xenium

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── X1/
   │   └── integrate/
   │       └── X1.zarr
   └── merge_data/
       └── integrate/
           └── concatenated_sdata
