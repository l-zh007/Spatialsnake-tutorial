MERFISH 输入教程
================

适用 ``run_type: Merfish``。

必需文件清单
------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - 文件名/通配
     - 必选
     - 格式
     - 说明
   * - ``**/cell_by_gene.csv``
     - 至少其一
     - CSV
     - 细胞 × 基因表达矩阵（MERSCOPE 常见）
   * - ``**/*transcripts*.csv*``
     - 至少其一
     - CSV/CSV.GZ
     - 转录本坐标文件
   * - ``**/*transcripts*.parquet``
     - 至少其一
     - Parquet
     - 转录本坐标文件（parquet 版本）
   * - ``cell_feature_matrix.h5`` / ``filtered_feature_cell_matrix.h5`` / ``raw_feature_cell_matrix.h5`` / ``filtered_feature_bc_matrix.h5`` / ``raw_feature_bc_matrix.h5``
     - 否
     - H5
     - 兼容候选矩阵名，存在时可被识别

判定规则：``cell_by_gene.csv`` 与 ``transcripts`` 文件并非都强制存在，但目录下至少要找到一种关键输入，否则会退出。

文件来源与获取方式
------------------------

- 官方下载：Vizgen MERSCOPE/MERFISH 标准输出目录。
- 实验输出：实验室 MERFISH pipeline 导出的 cell/transcript 文件。
- 占位符写法：先写 ``/path/to/merfish_sample``，后续替换为真实目录。

目录结构示例
------------

.. code-block:: text

   data/
   └── M1/
       ├── region_0/
       │   ├── cell_by_gene.csv
       │   └── detected_transcripts.csv.gz
       └── images/
           └── morphology_mip.ome.tif

sample.txt 示例
---------------

single_analysis：

.. code-block:: text

   sample_id input_path
   M1 data/M1
   M2 data/M2

compare_analysis：

.. code-block:: text

   sample_id input_path group
   M1 data/M1 tumor
   M2 data/M2 normal

运行命令示例
------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type Merfish

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── M1/
   │   └── integrate/
   │       └── M1.zarr
   └── merge_data/
       └── integrate/
           └── concatenated_sdata
