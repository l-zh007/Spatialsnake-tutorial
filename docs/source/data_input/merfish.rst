MERFISH 输入教程
================

``run_type: merfish`` 这里我们使用   等人的 merfish 数据进行结果演示

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

输入校验逻辑（源码）
--------------------------------

- 目录校验：递归查找 ``cell_by_gene.csv``、``*transcripts*.csv*``、``*transcripts*.parquet``，三者至少命中一种。
- 读取后处理：若 points 中缺失转录本，读取函数会尝试注入 ``transcripts`` 点层，保持下游可用性。

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

Run the command
------------------------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type Merfish

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── M1/
   │   └── integrate/
   │       ├── M1.zarr
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

- 主输出：``results/<sample>/integrate/<sample>.zarr``。
- 比较分析附加输出：``results/merge_data/integrate/concatenated_sdata``。
- 附加 QC 图：单样本读取会在 ``integrate`` 目录写入 5 张质控图；这些文件未在 Snakemake ``output`` 中显式声明。

结果图展示（占位符）
--------------------

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: merfish result placeholder

   MERFISH ``integrate`` 阶段结果示意图（占位符）。

- 建议存放路径：``docs/source/_static/images/data_input/merfish_result.png``。
- 建议替换方式：将上方 ``figure`` 路径改为 ``/_static/images/data_input/merfish_result.png``。
- 建议图注解释要点：转录本点层是否完整注入、细胞表达矩阵质量、空间坐标与图像对应关系。

If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration`.
else continue to :doc:`data_input/index`