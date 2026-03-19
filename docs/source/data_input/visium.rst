Start with 10x Genomics Visium
==============================

``run_type: visium`` 这里我们使用   等人的 visium 数据进行结果演示

必需文件清单(遵循10x genomics Space Ranger 标准输出目录格式)
----------------------------------------------------------------------

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

- 官方下载:10x Genomics Space Ranger 标准输出目录。
- 实验输出：实验/测序平台交付的 Visium 分析结果目录。
- 占位符写法：可先在 ``sample.txt`` 填写 ``/path/to/visium_sample``，后续替换为真实路径。

输入校验逻辑（源码）
--------------------------------

- 目录校验：读取前检查 ``spatial/tissue_positions_list.csv``、``spatial/scalefactors_json.json``、``spatial/tissue_lowres_image.png``、``spatial/tissue_hires_image.png``。
- 计数矩阵自动识别顺序：``filtered_feature_bc_matrix.h5`` → ``raw_feature_bc_matrix.h5`` → ``cell_feature_matrix.h5`` → ``filtered_feature_cell_matrix.h5`` → ``raw_feature_cell_matrix.h5``。

目录结构示例
------------

.. code-block:: text

   project_root/
   ├── data/ (存放你的原始数据)
   │   └── S1/
   │
   ├── sample.txt (重要样本参数文件)
   ├── results/ (存放分析结果)
   └── <analysis_option>.yaml (配置文件 可选)

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

sample_id:样本名 结果以此id创建文件夹 
input_path:样本数据文件夹路径
group:样本分组信息 (compare_analysis 中必填)

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=integrate

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
   └── merge_data/                  (compare_analysis 时生成)
       └── integrate/
           └── concatenated_sdata

输出解释
--------------------

- 主输出：``results/<sample>/integrate/<sample>.zarr``。
- 比较分析附加输出：``results/merge_data/integrate/concatenated_sdata``。
- 附加 QC 图：读取脚本会在 ``integrate`` 目录写入 5 张质控图（``total.png``、``total_umi_by_sample.png``、``total_genes_by_sample.png``、``genes_by_sample.png``、``scatter.png``）；这些文件并未在 Snakemake ``output`` 中逐一声明，但会实际落盘。

结果图展示（占位符）
--------------------

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: visium result placeholder

   Visium ``integrate`` 阶段结果示意图（占位符）。

- 建议存放路径：``docs/source/_static/images/data_input/visium_result.png``。
- 建议替换方式：将上方 ``figure`` 路径改为 ``/_static/images/data_input/visium_result.png``。
- 建议图注解释要点：组织图像与 spot 空间映射是否对齐、质控分布是否异常、输出对象是否可复用于后续步骤。

.. note::

   此步骤输出的图主要用于 QC 检查,建议在preprocess预处理步骤提前了解您的数据的质量情况。



If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration`.
else continue to :doc:`data_input/index`