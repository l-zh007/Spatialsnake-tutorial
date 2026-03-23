模块 6：细胞通讯网络（cellchat）
=================================

``cellchat`` 用于从细胞类型间配体-受体关系构建通讯网络，并输出网络强度、通路与 LR 明细。
由于我们的工具为空间转录组分析,因此在构建通讯网络时,我们会考虑细胞之间的空间距离,以更准确地反映细胞通讯关系,所以需要您提供 缩放因子文件。

我们的cellchat分析工具还支持多样本数据集的分析,您只需要在 ``sample.txt`` 中提供多个样本的输入路径即可，但依据官方文档,此步骤我们仅推荐相同实验条件，即生物学重复的样本进行空间坐标和表达矩阵的整合，进行cellchat算法的输入
若您想对比不同实验条件下的细胞通讯网络,则需先将两种条件由此步骤生成的结果文件,在后续compare_analysis的compare_cellchat模块中作为输入进行对比分析

处理逻辑概述
------------

1. 读取输入对象并转换为 Seurat 数据结构，设置 ``celltype_col`` 分组。
2. 根据 ``species`` 加载对应 CellChat 数据库并筛选信号通路。
3. 计算通讯概率、通路层级网络并聚合为细胞群间通讯图。
4. 输出网络图、统计表、LR 明细与 pathway 汇总表。

准备输入文件
------------

``sample.txt`` 推荐格式：若您为10x 官方的数据,则需要提供缩放因子文件路径

.. code-block:: text

   sample_id   input_path  scale_factor_path
   S1          results/S1/annotion/S1.h5ad results/S1/scale_factor.csv

若您想多样本整合请参考

.. code-block:: text

   sample_id   input_path  scale_factor_path
   S1          results/S1/annotion/S1.h5ad results/S1/scale_factor.csv
   S2          results/S2/annotion/S2.h5ad results/S2/scale_factor.csv

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
配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。


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
