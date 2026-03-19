Visium Segment 输入教程
=======================

``run_type: visium_segment`` 这里我们使用   等人的 visium HD  细胞分割数据进行结果演示

必需文件清单
------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - 文件名/通配
     - 必选
     - 格式
     - 说明
   * - ``segmented_outputs/spatial/tissue_hires_image.png``
     - 是
     - PNG
     - 分割坐标对应的高分辨率图像
   * - ``segmented_outputs/spatial/scalefactors_json.json``
     - 是
     - JSON
     - 图像缩放系数
   * - ``segmented_outputs/cell_segmentations.geojson``
     - 是
     - GeoJSON
     - 细胞分割多边形
   * - ``segmented_outputs/filtered_feature_bc_matrix.h5`` 或 ``segmented_outputs/raw_feature_bc_matrix.h5``
     - 是
     - H5
     - 主表达矩阵
   * - ``segmented_outputs/cell_feature_matrix.h5`` / ``segmented_outputs/filtered_feature_cell_matrix.h5`` / ``segmented_outputs/raw_feature_cell_matrix.h5``
     - 否
     - H5
     - 兼容候选矩阵名

文件来源与获取方式
------------------------

- 官方下载：10x Visium + segmentation 流程导出的 ``segmented_outputs``。
- 实验输出：图像分割流程产物。
- 占位符写法：先写 ``data/S1``，等你整理好后替换为真实样本目录。

输入校验逻辑（源码）
--------------------------------

- 目录校验：先检查 ``segmented_outputs`` 下 ``spatial/tissue_hires_image.png``、``spatial/scalefactors_json.json``、``cell_segmentations.geojson``。
- 计数矩阵自动识别顺序：``filtered_feature_bc_matrix.h5`` → ``raw_feature_bc_matrix.h5`` → ``cell_feature_matrix.h5`` → ``filtered_feature_cell_matrix.h5`` → ``raw_feature_cell_matrix.h5``。
- 实现细节：读取脚本会按 ``data/<sample>/segmented_outputs`` 拼接文件路径，建议保持该目录结构以避免路径解析偏差。

目录结构示例
------------

.. code-block:: text

   data/
   └── S1/
       └── segmented_outputs/
           ├── filtered_feature_bc_matrix.h5
           ├── cell_segmentations.geojson
           └── spatial/
               ├── tissue_hires_image.png
               └── scalefactors_json.json

sample.txt 示例
---------------

single_analysis：

.. code-block:: text

   sample_id input_path
   S1 data/S1
   S2 data/S2

compare_analysis：

.. code-block:: text

   sample_id input_path group
   S1 data/S1 tumor
   S2 data/S2 normal

Run the command
------------------------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type visium_segment

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── S1/
   │   └── integrate/
   │       ├── S1.zarr
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
- 附加 QC 图：读取脚本会在 ``integrate`` 目录写入 5 张质控图；这些文件不在 Snakemake ``output`` 声明中，但会实际生成。

结果图展示（占位符）
--------------------

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: visium segment result placeholder

   Visium Segment ``integrate`` 阶段结果示意图（占位符）。

- 建议存放路径：``docs/source/_static/images/data_input/visium_segment_result.png``。
- 建议替换方式：将上方 ``figure`` 路径改为 ``/_static/images/data_input/visium_segment_result.png``。
- 建议图注解释要点：细胞分割边界与组织图像匹配度、分割单元表达质量、后续注释可用性。

If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration`.
else continue to :doc:`data_input/index`