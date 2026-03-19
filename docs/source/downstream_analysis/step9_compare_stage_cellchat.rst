模块 8：通讯比较（compare_stage + cellchat）
============================================

该模块用于比较两个 CellChat 结果对象的通讯数量、强度与通路差异。
对应实现为 ``workflow/rules/compare_LR.smk`` 与 ``workflow/scripts/cellchat_compare.R``。

配置文件详解请见 :doc:`../config_reference/compare_stage_yaml`。

处理逻辑概述
------------

1. 读取两个 CellChat ``.rds`` 对象并对齐细胞类型层级。
2. 合并对象后比较网络交互数量、权重与通路强度。
3. 按配置输出 rankNet、热图、差异网络图、气泡图等结果。
4. 可选保存合并对象，便于后续继续筛选与可视化。

准备 ``sample.txt``
-------------------

.. code-block:: text

   sample_id   input_path
   Tumor       /abs/path/tumor_cellchat.rds
   Normal      /abs/path/normal_cellchat.rds

输入要求：

1. 第二列必须是有效 ``.rds`` 文件路径。
2. 建议两组对象使用一致的细胞类型命名体系，减少自动对齐带来的解释偏差。
3. 可在配置中设置展示名（``cellchat_compare_sample_name1/2``）。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=cellchat

运行可选的参数设置(配置文件版)
------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - 参数
     - 常用值
     - 作用
   * - ``cellchat_compare_output_dir``
     - ``results/compare_cellchat``
     - 比较结果输出目录
   * - ``cellchat_compare_pathways``
     - ``CXCL,CCL``
     - 指定重点比较通路
   * - ``cellchat_compare_source_cells``
     - ``T_cell,Macrophage``
     - 发送细胞筛选
   * - ``cellchat_compare_target_cells``
     - ``Tumor,Fibroblast``
     - 接收细胞筛选
   * - ``cellchat_compare_receiver_cells``
     - ``1,2,3``
     - 通路聚合图 receiver 节点
   * - ``cellchat_compare_do_ranknet``
     - ``TRUE``
     - 是否输出通路强度比较图
   * - ``cellchat_compare_do_role_heatmap``
     - ``TRUE``
     - 是否输出 signaling role 热图
   * - ``cellchat_compare_do_compare_bubble``
     - ``TRUE``
     - 是否输出双组气泡对比图
   * - ``cellchat_compare_save_merged``
     - ``TRUE``
     - 是否保存合并后的 CellChat 对象

结果文件结构
------------

.. code-block:: text

   results/
   └── compare_cellchat/
       ├── compare_overview_number_strength.pdf
       ├── compare_diff_number_strength_net.pdf
       ├── compare_heatmap_count_weight.pdf
       ├── compare_pathway_strength.pdf
       ├── compare_signaling_role_all.pdf
       ├── compare_signaling_role_outgoing.pdf
       ├── compare_signaling_role_incoming.pdf
       ├── compare_lr_regulated.pdf
       ├── compare_pathway_aggregate_hierarchy.pdf
       ├── compare_pathway_aggregate_chord.pdf
       ├── compare_pathway_heatmap.pdf
       ├── compare_pathway_contribution.pdf
       ├── cellchat_object.list.rds
       └── cellchat_merged.rds

图表与结果解释
--------------

1. ``compare_overview_number_strength.pdf``：比较两组总体通讯数量与强度，先判断全局差异方向。
2. ``compare_diff_number_strength_net.pdf``：展示差异网络边增减，识别重塑最明显的细胞对。
3. ``compare_pathway_strength.pdf``：比较通路层级强度变化，定位条件特异的信号轴。
4. ``compare_lr_regulated.pdf``：在指定 source/target 细胞对中查看 LR 变化，是机制验证主图之一。
5. ``cellchat_merged.rds``：保存可复用合并对象，便于后续追加通路或细胞对筛选。
