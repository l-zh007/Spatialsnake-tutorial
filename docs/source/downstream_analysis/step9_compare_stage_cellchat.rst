模块 8：通讯比较（compare_stage + cellchat）
============================================

为了迎合当前空间转录组分析的需求，我们新增了 ``compare_stage`` 模块，用于比较两个 CellChat 结果对象的通讯数量、强度与通路差异。
我们的输入为cellchat模块生成的 ``.rds`` 文件，将cellchat对象整合进行多样本间配受体与通路的比较分析，从而方便用户挖掘不同实验条件下的细胞通讯差异。


运行步骤与内容
--------------

1. **对象加载与细胞层级对齐**
   读取用户输入的多个独立 CellChat 分析结果对象（``.rds``）。为确保比较的科学性，系统会自动检查并使用 ``liftCellChat`` 函数将不同对象的细胞类型（idents）层级同步对齐，避免因细胞群缺失导致的合并错误。
2. **通讯数量与强度全局比对**
   将对齐后的对象合并（``mergeCellChat``），从宏观层面计算并比对不同条件间的通讯交互总数（Number of interactions）与总强度（Interaction strength），生成概览统计图。
3. **网络拓扑差异分析**
   通过差值计算，识别并生成差异网络图，直观展现不同实验条件下（如正常与肿瘤组织）特定细胞群之间通讯链路的增强（红色）或减弱（蓝色）。
4. **通路级信号重塑与角色转换**
   对比不同条件下的通路强度排名（RankNet），并计算每个细胞类型在关键信号通路中扮演的角色转换（发送者、接收者、中介者等），生成信号角色差异热图。
5. **精细化配受体对比与结果导出**
   基于用户在配置中指定的关注通路（``pathways``）和细胞对（``source_cells``/``target_cells``），深入挖掘受调控的特定配体-受体交互，生成对比气泡图与基因表达图，最后可选将合并后的对象保存，方便进行更复杂的个性化后续分析。

准备 ``sample.txt``
-------------------

情景 1：单样本 CellChat 深度可视化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/cellchat/cellchat.rds

情景 2：双样本条件对比
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   input_path
   Tumor       /abs/path/tumor_cellchat.rds
   Normal      /abs/path/normal_cellchat.rds

输入要求：

1. 第二列必须是有效 ``.rds`` 文件路径。
2. 可输入单个或两个 ``.rds``；单样本用于深度展示，双样本用于差异比较。
3. 可在配置中设置展示名（``cellchat_compare_sample_name1/2``）。
4. 双样本建议使用一致的细胞类型命名体系，减少自动对齐带来的解释偏差。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=cellchat

运行可选的参数设置(配置文件版)
------------------------------------------------------------
配置文件详解请见 :doc:`../config_reference/compare_stage_yaml`。

.. code-block:: bash

   cellchat_compare_output_dir: "results/compare_cellchat"   # 输出目录
   cellchat_compare_sample_name1: ""                   # 样本1显示名称
   cellchat_compare_sample_name2: ""                   # 样本2显示名称
   cellchat_compare_pathways: "MIF"                             # 通路名列表, 逗号分隔, 例: "CXCL,CCL"
   cellchat_compare_source_cells: "Tumor_I,Tumor_III"                         # 发送细胞: 逗号分隔的细胞类型名称, 例: "Tumor_I,Tumor_III"
   cellchat_compare_target_cells: "Tumor_I,Tumor_III"                          # 接收细胞: 逗号分隔的细胞类型名称, 例: "Tumor_II,Tumor_IV"
   cellchat_compare_receiver_cells: "Tumor_I,Tumor_III"                    # netVisual_aggregate 接收端: 逗号分隔的细胞类型名称, 例: "Tumor_III,Tumor_IV"
   cellchat_compare_bubble_angle: 45                         # 比较气泡图 x 轴角度
   cellchat_compare_bubble_remove_isolate: True              # 是否移除孤立节点
   cellchat_compare_do_ranknet: True                         # 是否输出 rankNet 比较图
   cellchat_compare_do_role_heatmap: True                    # 是否输出 signaling role heatmap
   cellchat_compare_do_pathway_plots: True                   # 是否输出通路汇总图
   cellchat_compare_do_compare_overview: True                # 是否输出两组整体比较图
   cellchat_compare_do_compare_bubble: True                  # 是否输出 compare bubble (需 source/target)
   cellchat_compare_do_single_bubble: True                   # 是否输出单组 bubble (需 source)
   cellchat_compare_do_gene_expression: True                # 是否输出 plotGeneExpression
   cellchat_compare_gene_colors: "white,#FEC44F,#D95F0E"      # plotGeneExpression 颜色梯度
   cellchat_compare_gene_plot_type: "dot"                    # plotGeneExpression 类型: dot 或 heatmap
   cellchat_compare_pair_lr_use: "SPP1_CD44"                          # 空间特征图的 pairLR，例: "SPP1_CD44"
   cellchat_compare_save_merged: True                        # 双样本时是否保存合并后的 rds

结果文件结构
------------

情景 1：输入单个 ``.rds``（cellchat深度可视化）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   results/
   └── compare_cellchat/
       ├── {sample}_aggregate_hierarchy.png
       ├── {sample}_aggregate_chord.png
       ├── {sample}_pathway_heatmap.png
       ├── {sample}_pathway_contribution.png
       ├── {sample}_bubble.png
       ├── {sample}_selected_bubble.png
       ├── {sample}_signaling_role_network.png
       ├── {sample}_signaling_role_scatter.png
       ├── {sample}_signaling_role_outgoing.png
       ├── {sample}_signaling_role_incoming.png
       ├── {sample}_spatial_feature_pairlr.png
       └── {sample}_gene_expression.png

情景 2：输入两个 ``.rds``（不同实验条件cellchat差异比较）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   results/
   └── compare_cellchat/
       ├── compare_overview_number_strength.png
       ├── compare_diff_number_strength_net.png
       ├── compare_heatmap_count_weight.png
       ├── compare_pathway_strength.png
       ├── compare_signaling_role_all.png
       ├── compare_signaling_role_outgoing.png
       ├── compare_signaling_role_incoming.png
       ├── compare_lr_regulated.png
       ├── compare_pathway_aggregate_hierarchy.png
       ├── compare_pathway_aggregate_chord.png
       ├── compare_pathway_heatmap.png
       ├── compare_pathway_contribution.png
       ├── cellchat_object.list.rds
       └── cellchat_merged.rds

单样本与双样本差异说明：

1. 单样本不会生成 ``compare_overview`` / ``diffInteraction`` / ``merged.rds`` 等跨条件比较结果，而是输出该对象的深度机制可视化。
2. 双样本会进入合并比较流程，重点输出通讯数量/强度差异、差异网络、通路强度重塑与角色热图。
3. ``source_cells`` / ``target_cells`` / ``pathways`` 在两种情景下都可指定；未指定时脚本会自动回退到可用默认集合。

图表与结果解释
--------------

1. 通讯总数与强度概览图（``compare_overview_number_strength.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_infoflow_bar.png
   :width: 85%
   :align: center
   :alt: cellchat compare overview

解释：
通过并排的柱状图，直观对比两个实验条件在细胞通讯网络层面的宏观差异，帮助判断整体通讯格局是受到抑制还是被激活。

2. 差异网络拓扑图（``compare_diff_number_strength_net.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_network.png
   :width: 85%
   :align: center
   :alt: cellchat compare diff net

解释：
利用网络连线展示特定细胞对之间的通讯数量或强度差异。红色连线表示在条件二（相较于条件一）中增加的通讯，蓝色则表示减少，可快速锁定响应最剧烈的细胞亚群。

3. 通路强度重塑图（``compare_pathway_strength.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_infoflow_bar.png
   :width: 85%
   :align: center
   :alt: cellchat compare pathway strength

解释：
基于信息流计算出的 RankNet 对比图，明确哪些特定信号通路在某种条件下被特异性上调或下调，是功能解释的重要切入点。

4. 差异配受体对比气泡图（``compare_lr_regulated.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_dot_plot.png
   :width: 85%
   :align: center
   :alt: cellchat compare lr bubble

解释：
在指定的发送细胞（Source）和接收细胞（Target）之间，展示受实验条件显著调控的配体-受体对。气泡大小代表显著性，颜色表示表达概率，常用于机制验证和关键靶点挖掘。

5. 整合与保存对象（``cellchat_merged.rds``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
包含多样本对齐与合并后完整信息的标准 CellChat R 对象。研究人员可以直接将其导入 R 环境，继续使用官方包生成更多细粒度的图表（如特定基因的表达小提琴图、特定通路的弦图等）。
