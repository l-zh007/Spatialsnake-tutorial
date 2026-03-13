Visium HD 输入教程
==================

适用 ``run_type: visium_HD``。

必需文件清单
------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - 文件名/通配
     - 必选
     - 格式
     - 说明
   * - ``binned_outputs/square_{bin}um/spatial/tissue_positions.parquet``
     - 是
     - Parquet
     - bin 级坐标信息
   * - ``binned_outputs/square_{bin}um/spatial/scalefactors_json.json``
     - 是
     - JSON
     - 图像缩放系数
   * - ``binned_outputs/square_{bin}um/spatial/tissue_lowres_image.png``
     - 是
     - PNG
     - 低分辨率组织图像
   * - ``binned_outputs/square_{bin}um/filtered_feature_bc_matrix.h5`` 或 ``binned_outputs/square_{bin}um/raw_feature_bc_matrix.h5``
     - 是
     - H5
     - 主表达矩阵
   * - ``binned_outputs/square_{bin}um/cell_feature_matrix.h5`` / ``filtered_feature_cell_matrix.h5`` / ``raw_feature_cell_matrix.h5``
     - 否
     - H5
     - 兼容候选矩阵名

文件来源与获取方式
------------------------

- 官方下载：10x Visium HD 输出目录（含 ``binned_outputs``）。
- 实验输出：平台下游流程导出的 ``square_XXXum`` 目录。
- 占位符写法：先填 ``data/S1`` 与 bin 数值，后续替换为真实目录与分辨率。

目录结构示例
------------

.. code-block:: text

   data/
   └── S1/
       └── binned_outputs/
           └── square_008um/
               ├── filtered_feature_bc_matrix.h5
               └── spatial/
                   ├── tissue_positions.parquet
                   ├── scalefactors_json.json
                   └── tissue_lowres_image.png

sample.txt 示例
---------------

single_analysis（第三列是 bin，自动补零成 3 位）：

.. code-block:: text

   sample_id input_path bin
   S1 data/S1 8
   S2 data/S2 16

compare_analysis（第四列 group）：

.. code-block:: text

   sample_id input_path bin group
   S1 data/S1 8 tumor
   S2 data/S2 8 normal

运行命令示例
------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type visium_HD

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── S1_008um/
   │   └── integrate/
   │       └── S1.zarr
   └── merge_data/
       └── integrate/
           └── concatenated_sdata
