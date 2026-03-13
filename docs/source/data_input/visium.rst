Visium 输入教程
===============

适用 ``run_type: visium``。

必需文件清单
------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - 文件名/通配
     - 必选
     - 格式
     - 说明
   * - ``spatial/tissue_positions_list.csv``
     - 是
     - CSV
     - spot 坐标与组织位置信息
   * - ``spatial/scalefactors_json.json``
     - 是
     - JSON
     - 组织图像缩放因子
   * - ``spatial/tissue_lowres_image.png``
     - 是
     - PNG
     - 低分辨率组织图像
   * - ``spatial/tissue_hires_image.png``
     - 是
     - PNG
     - 高分辨率组织图像
   * - ``filtered_feature_bc_matrix.h5`` 或 ``raw_feature_bc_matrix.h5``
     - 是
     - H5
     - 主表达矩阵，程序优先读取 filtered
   * - ``cell_feature_matrix.h5`` / ``filtered_feature_cell_matrix.h5`` / ``raw_feature_cell_matrix.h5``
     - 否
     - H5
     - 兼容候选矩阵名，存在时可被自动识别

文件来源与获取方式
------------------------

- 官方下载：10x Genomics Space Ranger 标准输出目录。
- 实验输出：实验同事/测序平台交付的 Visium 分析结果目录。
- 占位符写法：可先在 ``sample.txt`` 填写 ``/path/to/visium_sample``，后续替换为真实路径。

目录结构示例
------------

.. code-block:: text

   data/
   └── S1/
       ├── filtered_feature_bc_matrix.h5
       └── spatial/
           ├── tissue_positions_list.csv
           ├── scalefactors_json.json
           ├── tissue_lowres_image.png
           └── tissue_hires_image.png

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

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type visium

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
