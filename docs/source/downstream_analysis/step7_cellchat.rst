模块 6：细胞通讯网络（cellchat）
=================================

``cellchat`` 用于从细胞类型间配体-受体关系构建通讯网络，并输出网络强度、通路与 LR 明细。
对应实现为 ``workflow/rules/run_cellchat.smk`` 与 ``workflow/scripts/Cellchat.R``。

配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。

处理逻辑概述
------------

1. 读取输入对象并转换为 Seurat 数据结构，设置 ``celltype_col`` 分组。
2. 根据 ``species`` 加载对应 CellChat 数据库并筛选信号通路。
3. 计算通讯概率、通路层级网络并聚合为细胞群间通讯图。
4. 输出网络图、统计表、LR 明细与 pathway 汇总表。

准备输入文件
------------

``sample.txt`` 推荐格式：

.. code-block:: text

   sample_id   input_path
   S1          results/S1/annotion/S1.h5ad

说明：

1. 输入可为 ``.h5ad`` 或 ``.rds`` （脚本自动识别）。
2. 输入对象需包含细胞类型列（默认 ``celltype``）。
3. 空间模式下建议提供可用坐标信息；多样本场景可配合 scale factor 参数修正距离尺度。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat

运行可选的参数设置(配置文件版)
------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 24 52

   * - 参数
     - 常用值
     - 作用
   * - ``runpipe``
     - ``cellchat``
     - 进入 cellchat 分支
   * - ``celltype_col``
     - ``celltype``
     - 细胞类型列名
   * - ``species``
     - ``human`` / ``mouse``
     - 选择通讯数据库物种
   * - ``assay``
     - ``Spatial``
     - 分析类型标签
   * - ``min_cells``
     - ``10``
     - 过滤细胞数量过少的群体
   * - ``workers``
     - ``32``
     - 并行线程数
   * - ``trim``
     - ``0.1``
     - truncatedMean 截尾比例，影响稳健性
   * - ``interaction_length``
     - ``150``
     - 空间通讯距离阈值
   * - ``is_single_cell``
     - ``False``
     - 指定是否按单细胞模式计算

结果文件结构
------------

.. code-block:: text

   results/
   └── {sample}/
       └── cellchat/
           ├── cellchat.rds
           ├── {sample}_cellchat_network.png
           ├── {sample}_cellchat_network.pdf
           ├── {sample}_cellchat_infoflow_bar.png
           ├── {sample}_cellchat_heatmap.png
           ├── {sample}_cellchat_stats.csv
           ├── {sample}_cellchat_lr.csv
           ├── {sample}_cellchat_lr_summary.csv
           ├── {sample}_cellchat_pathway_pairs.csv
           ├── {sample}_cellchat_pathway_summary.csv
           └── {sample}_cellchat_pathway_net.csv

图表与结果解释
--------------

1. ``*_cellchat_network.png``：左图为通讯数量，右图为通讯强度，先用于判断主导通讯细胞群。
2. ``*_cellchat_infoflow_bar.png``：比较各通路信息流强弱，用于筛选核心通路。
3. ``*_cellchat_heatmap.png``：展示细胞群之间通讯权重矩阵，适合识别高互作对。
4. ``*_cellchat_lr.csv`` 与 ``*_cellchat_lr_summary.csv``：给出可追溯的 LR 明细与聚合统计，是后续机制解释的核心依据。
