Visium Segment 输入教程
=======================

适用 ``run_type: visium_segment``。

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
- 实验输出：图像分割流程产物（如实验室内部分割脚本输出）。
- 占位符写法：先写 ``data/S1``，等你整理好后替换为真实样本目录。

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

运行命令示例
------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type visium_segment

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── S1/
   │   └── integrate/
   │       └── S1.zarr
   └── merge_data/
       └── integrate/
           └── concatenated_sdata
