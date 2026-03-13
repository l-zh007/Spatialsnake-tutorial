Slide-seq 输入教程
==================

适用 ``run_type: slide_seq``。

必需文件清单
------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - 文件名/通配
     - 必选
     - 格式
     - 说明
   * - ``BeadLocationsForR.csv``
     - 是
     - CSV
     - bead 空间坐标（xcoord/ycoord）
   * - ``MappedDGEForR.csv``
     - 是
     - CSV
     - bead × gene 计数矩阵

说明：该类型的主文件固定识别为 ``MappedDGEForR.csv``。

文件来源与获取方式
------------------------

- 官方下载：Slide-seq 标准处理流程输出目录。
- 实验输出：实验室 mapping 步骤导出的 BeadLocations 与 MappedDGE 文件。
- 占位符写法：先写 ``data/SQ1``，后续替换为真实样本目录。

目录结构示例
------------

.. code-block:: text

   data/
   └── SQ1/
       ├── BeadLocationsForR.csv
       └── MappedDGEForR.csv

sample.txt 示例
---------------

single_analysis：

.. code-block:: text

   sample_id input_path
   SQ1 data/SQ1
   SQ2 data/SQ2

compare_analysis：

.. code-block:: text

   sample_id input_path group
   SQ1 data/SQ1 tumor
   SQ2 data/SQ2 normal

运行命令示例
------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type slide_seq

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── SQ1/
   │   └── integrate/
   │       └── SQ1.h5ad
   └── merge_data/
       └── integrate/
           └── concatenated_sdata
