数据整合（Ingesting）
=========================

``run_type: visium`` 这里我们使用   等人的 visium HD  数据进行全过程的使用演示，若您存在别的空转数据和多样本请跳转到对应页面进行Ingesting部分的运行。

配置文件详解请见 :doc:`../config_reference/integrate_yaml`。

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

输入校验逻辑（源码）
--------------------------------

- 目录校验：读取前检查 ``spatial/tissue_positions.parquet``、``spatial/scalefactors_json.json``、``spatial/tissue_lowres_image.png``。
- 计数矩阵自动识别顺序：``filtered_feature_bc_matrix.h5`` → ``raw_feature_bc_matrix.h5`` → ``cell_feature_matrix.h5`` → ``filtered_feature_cell_matrix.h5`` → ``raw_feature_cell_matrix.h5``。
- ``sample.txt`` 中 bin 会被规范为 3 位（例如 ``8`` 转为 ``008``），并映射到 ``binned_outputs/square_008um``。

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

Run the command
------------------------------

.. code-block:: bash

   spatialsnake --configfile config.yaml --option integrate --channel single_analysis --run_type visium_HD

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── S1_008um/
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

- 主输出：``results/<sample>_<bin>um/integrate/<sample>.zarr``。
- 比较分析附加输出：``results/merge_data/integrate/concatenated_sdata``。
- 附加 QC 图：读取脚本会在 ``integrate`` 目录写入 5 张质控图；这些文件不在 Snakemake ``output`` 声明中，但会实际生成。

结果图展示（占位符）
--------------------

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: visium hd result placeholder

   Visium HD ``integrate`` 阶段结果示意图（占位符）。

- 建议存放路径：``docs/source/_static/images/data_input/visium_hd_result.png``。
- 建议替换方式：将上方 ``figure`` 路径改为 ``/_static/images/data_input/visium_hd_result.png``。
- 建议图注解释要点：bin 粒度对空间分辨率的影响、不同 bin 输出的可比性、表达稀疏度与覆盖范围。
