Xenium 输入教程
===============

``run_type: xenium`` 这里我们使用   等人的 xenium 数据进行结果演示

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

输入校验逻辑（源码）
--------------------------------

- 目录校验：读取前检查 ``cells.parquet``、``transcripts.parquet``、``morphology.ome.tif``、``experiment.xenium``。
- 计数矩阵自动识别顺序：``filtered_feature_bc_matrix.h5`` → ``raw_feature_bc_matrix.h5`` → ``cell_feature_matrix.h5`` → ``filtered_feature_cell_matrix.h5`` → ``raw_feature_cell_matrix.h5``。
- 可选读取开关：``cells_boundaries``、``nucleus_boundaries``、``nucleus_labels``、``morphology_mip`` 控制附加元素是否加载。

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
       └──  ........

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

Run the command
------------------------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type xenium

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── X1/
   │   └── integrate/
   │       ├── X1.zarr
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

- 主输出：``results/<sample>/integrate/<sample>.zarr``，其中包含 image/shapes/labels/points/table 等空间元素。
- 比较分析附加输出：``results/merge_data/integrate/concatenated_sdata``。
- 附加 QC 图：读取脚本会在 ``integrate`` 目录写入 5 张质控图。

结果图展示（占位符）
--------------------

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: xenium result placeholder

   Xenium ``integrate`` 阶段结果示意图（占位符）。

- 建议存放路径：``docs/source/_static/images/data_input/xenium_result.png``。
- 建议替换方式：将上方 ``figure`` 路径改为 ``/_static/images/data_input/xenium_result.png``。
- 建议图注解释要点：cell/label/point 图层一致性、转录本分布与细胞边界关系、核与细胞边界参数对结果的影响。

If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration`.
else continue to :doc:`data_input/index`