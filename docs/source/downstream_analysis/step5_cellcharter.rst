模块 4：空间域建模（cellcharter）
==================================

``cellcharter`` 用于结合表达信息与空间邻域结构进行空间域建模，得到更贴近组织结构的空间分区。
对应实现为 ``workflow/rules/run_cellcharter.smk`` 与 ``workflow/scripts/cellcharter.py``。

配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。

处理逻辑概述
------------

1. 读取输入对象并构建 ``counts`` 层，准备 SCVI 表达潜变量。
2. 构建空间邻接图并聚合邻域特征（``X_cellcharter``）。
3. 在给定簇数范围内自动选择稳定聚类数并写入 ``spatial_cluster``。
4. 输出邻域富集图、空间叠加图、比例图及 cluster 导出表。

准备输入文件
------------

``sample.txt`` 推荐格式：

.. code-block:: text

   sample_id   input_path
   S1          results/S1/annotion/S1.zarr

输入要求：

1. 输入对象需包含空间坐标信息（``obsm['spatial']`` 或可转换坐标）。
2. 推荐输入为已注释对象（包含 ``celltype``），以便输出富集解释图。
3. 多样本比较时建议输入整合对象，并在对象中保留样本列与条件列。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellcharter

运行可选的参数设置(配置文件版)
------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 24 52

   * - 参数
     - 常用值
     - 作用
   * - ``runpipe``
     - ``cellcharter``
     - 进入 cellcharter 分支
   * - ``cellcharter_input``
     - ``results/.../*.zarr``
     - 分析对象路径（在流程中由 ``sample.txt`` 第二列提供）
   * - ``max_cluster``
     - ``10`` 或 ``12``
     - 自动选簇上限，决定搜索范围
   * - ``cellcharter_col``
     - ``spatial_cluster``
     - 写入空间域标签的列名
   * - ``significance``
     - ``0.05``
     - 差异邻域图显著性阈值（比较模式）
   * - ``sample_col``
     - ``region``
     - 比较模式下样本标识列
   * - ``condition_col``
     - ``condition``
     - 比较模式下条件分组列
   * - ``celltype_col``
     - ``celltype``
     - 用于 celltype-空间域富集解释
   * - ``image_type`` / ``shape_type``
     - ``hires`` / ``cell_boundaries``
     - 空间叠加图所用图层关键字

结果文件结构
------------

.. code-block:: text

   results/
   └── cellcharter/
       ├── {sample}_cellcharter.zarr/
       ├── {sample}_celchar.png
       ├── {sample}_enrichment.png
       ├── {sample}_nhood_enrichment.png
       ├── {sample}_diff_enrichment.png
       ├── {sample}_{image}_Clusters.png
       ├── {sample}_Clusters_proportion.png
       └── *_cell_clusters.csv

图表与结果解释
--------------

1. ``*_celchar.png``：展示不同簇数下稳定性趋势，用于判断空间域划分是否可靠。
2. ``*_nhood_enrichment.png``：显示空间域之间的邻接富集关系，反映组织微环境共现模式。
3. ``*_enrichment.png``：空间域与已注释 celltype 的对应关系，帮助将“空间簇”转译为生物学含义。
4. ``*_{image}_Clusters.png``：组织图像叠加空间域标签，用于验证空间连续性与组织学一致性。
5. ``*_cellcharter.zarr`` 与 ``*_cell_clusters.csv``：分别用于后续流程复用与外部复核/共享。
