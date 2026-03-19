Slide-seq 输入教程
==================

``run_type: slide_seq`` 这里我们使用   等人的 slide-seq 数据进行结果演示



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

输入校验逻辑（源码）
--------------------------------

- 目录校验：读取前检查 ``BeadLocationsForR.csv`` 与 ``MappedDGEForR.csv`` 是否同时存在。
- 计数文件识别：``MappedDGEForR.csv`` 会被识别为主计数矩阵。
- 实现细节：读取脚本按 ``data/<sample>/`` 拼接 ``coor_file`` 和 ``count_file``，建议保持该目录结构。

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

Run the command
------------------------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type slide_seq

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── SQ1/
   │   └── integrate/
   │       ├── SQ1.h5ad
   │       ├── total.png
   │       ├── total_umi_by_sample.png
   │       ├── total_genes_by_sample.png
   │       ├── genes_by_sample.png
   │       └── scatter.png
   └── merge_data/
       └── integrate/
           └── concatenated_sdata

输出解释
--------------------

- 主输出：``results/<sample>/integrate/<sample>.h5ad``。
- 比较分析附加输出：``results/merge_data/integrate/concatenated_sdata``。
- 附加 QC 图：读取脚本会在 ``integrate`` 目录写入 5 张质控图；这些文件不在 Snakemake ``output`` 声明中，但会实际生成。

结果图展示（占位符）
--------------------

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: slide-seq result placeholder

   Slide-seq ``integrate`` 阶段结果示意图（占位符）。

- 建议存放路径：``docs/source/_static/images/data_input/slide_seq_result.png``。
- 建议替换方式：将上方 ``figure`` 路径改为 ``/_static/images/data_input/slide_seq_result.png``。
- 建议图注解释要点：bead 空间坐标与表达矩阵索引是否一致、空间覆盖连续性、导出 h5ad 的字段完整性。

If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration`.
else continue to :doc:`data_input/index`