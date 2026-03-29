Start with 10x Genomics Visium
==============================

``run_type: visium`` 这里我们使用 10xgenomics 官网公开数据集进行结果演示

link: https://www.10xgenomics.com/datasets/adult-mouse-brain-ffpe-1-standard-1-3-0
下载Feature / barcode matrix HDF5 (filtered)  与  图像信息 Spatial imaging data(需使用 tar -xfvz 解压)

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

目录结构示例
------------

.. code-block:: text

   project_root/
   ├── data/ (存放你的原始数据)
   │   └── Visium_FFPE_Mouse_Brain/
   │
   ├── sample.txt (重要样本参数文件)
   ├── results/ (存放分析结果)
   └── <analysis_option>.yaml (配置文件 可选)

   data/
   └── Visium_FFPE_Mouse_Brain/
       ├── filtered_feature_bc_matrix.h5
       └── spatial/
           ├── tissue_positions_list.csv
           ├── scalefactors_json.json
           ├── tissue_lowres_image.png
           └── tissue_hires_image.png

部分数据h5文件具有前缀如 Visium_FFPE_Mouse_Brain_filtered_feature_bc_matrix.h5 但请确保此前缀即为您的样本文件夹名称我们的pipeline会自动读取检查

sample.txt 示例
---------------

single_analysis:

.. code-block:: text

   sample_id input_path
   Visium_FFPE_Mouse_Brain data/Visium_FFPE_Mouse_Brain

sample_id:样本名 结果以此id创建文件夹 
input_path:样本数据文件夹路径

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=integrate

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── Visium_FFPE_Mouse_Brain/
   │   └── integrate/
   │       ├── Visium_FFPE_Mouse_Brain.zarr
   │       ├── total.png
   │       ├── total_umi_by_sample.png
   │       ├── total_genes_by_sample.png
   │       ├── genes_by_sample.png
   │       └── scatter.png

输出解释
--------------------

- 主输出：``results/<sample>/integrate/<sample>.zarr``。
- 比较分析附加输出：``results/merge_data/integrate/concatenated_sdata``。
- 附加 QC 图：读取脚本会在 ``integrate`` 目录写入 5 张质控图（``total.png``、``total_umi_by_sample.png``、``total_genes_by_sample.png``、``genes_by_sample.png``、``scatter.png``）；这些文件并未在 Snakemake ``output`` 中逐一声明，但会实际落盘。


.. note::

   此步骤输出的图主要用于 QC 检查,建议在preprocess预处理步骤提前了解您的数据的质量情况。

If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration`.
else continue your analysis :doc:`core_analysis/index`