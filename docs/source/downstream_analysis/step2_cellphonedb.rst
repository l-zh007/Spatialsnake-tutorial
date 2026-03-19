模块 1：细胞通讯（cellPhoneDB）
===============================

``cellPhoneDB`` 用于在细胞类型之间推断配体-受体通讯关系。

配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。

处理逻辑概述
------------
1. 读取输入对象并抽取 ``cell_id`` 与细胞类型标签，生成 cellPhoneDB 所需元数据表。
2. 根据参数选择分析模式（``statistical`` 或 ``degs``）运行通讯推断。
3. 生成主结果文本文件（means、pvalues、deconvoluted、interaction scores）。
4. 基于结果自动输出热图、点图、家族点图和弦图等可视化文件。

该流程既给出可复用的通讯结果矩阵，也提供了适合汇报与复核的图件输出。

准备输入文件
------------
 ``sample.txt`` 至少包含样本 ID 与输入对象路径：

.. code-block:: text

   sample_id   input_path
   SampleA     results/SampleA/SampleA_cellcharter.zarr

说明：

1. ``input_path`` 建议填写包含 ``obs`` 注释列的上游对象（如 ``cellcharter``、``clustering`` 或已整合对象）。
2. 输入对象中需包含细胞类型列（默认 ``celltype``），并建议包含空间分区列（如 ``spatial_cluster``）以支持微环境约束。
3. 若不通过 ``sample.txt`` 传入对象，也可在 ``advance_analysis.yaml`` 中直接设置 ``cellPhoneDB_input``。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellPhoneDB --count-data hgnc_symbol --threads 16 --output_name Normal

运行可选的参数设置(命令行版)
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--runpipe``
     - ``cellPhoneDB``
     - 指定进入 cellPhoneDB 分支（核心参数）
   * - ``--count-data``
     - ``hgnc_symbol``
     - 指定基因标识类型（需与表达矩阵一致）
   * - ``--threads``
     - ``16``
     - 设置并行线程数，影响速度与资源占用
   * - ``--output_name``
     - ``Normal``
     - 输出文件后缀名，便于区分多轮分析结果

说明：命令行主要覆盖通用启动参数；cellPhoneDB 分支的高级参数建议在 yaml 中配置。

运行可选的参数设置(配置文件版)
------------------------------------------------------------
先生成高级分析配置模板：

.. code-block:: bash

   spatialsnake produce-file --option=advance_analysis

随后在 ``advance_analysis.yaml`` 中重点设置以下字段：

.. list-table::
   :header-rows: 1
   :widths: 26 20 54

   * - 参数
     - 常用值
     - 作用
   * - ``cellPhoneDB_input``
     - ``results/.../*.zarr``
     - 指定 cellPhoneDB 分析对象路径
   * - ``celltype_col``
     - ``celltype``
     - 指定细胞类型标签列
   * - ``cpdb_method``
     - ``statistical`` / ``degs``
     - 选择统计推断模式或 DEG 驱动模式
   * - ``cpdb_de_method``
     - ``wilcoxon``
     - 下游展示/筛选中使用的差异分析方法标签
   * - ``iterations``
     - ``500``
     - 统计模式下置换次数，越高越稳健但更耗时
   * - ``pvalue``
     - ``0.05``
     - 显著性阈值，控制通讯筛选严格程度
   * - ``threshold``
     - ``0.1``
     - 表达比例过滤阈值，控制参与计算的基因对
   * - ``niche_col``
     - ``spatial_cluster``
     - 空间数据微环境分组列
   * - ``is_singlecell``
     - ``False``
     - 标记输入对象类型，影响 microenvironment 约束逻辑
   * - ``degs_file_path``
     - ``path/to/degs.txt``
     - 启用 ``degs`` 模式时必需
   * - ``cell_type1`` / ``cell_type2``
     - ``Endothelial`` / ``Tumor``
     - 点图与弦图重点展示的细胞对
   * - ``gene_family``
     - ``chemokines``
     - 家族点图聚焦的配体-受体家族

运行最终运行命令吧
----------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellPhoneDB --configfile advance_analysis.yaml

结果文件结构
------------

完成运行后，主要结果位于 ``results/{sample}/cellPhoneDB_results/``：

.. code-block:: text

   results/
   └── {sample}/
       └── cellPhoneDB_results/
           ├── adata.h5ad
           ├── {sample}_cellid_cell_type.txt
           ├── {sample}_heatmap.png
           ├── {sample}_dot_plot.png
           ├── {sample}_dot_family_plot.png
           ├── {sample}_chord_plot.png
           └── cellphonedb_output/
               ├── statistical_analysis_means_{output_name}.txt
               ├── statistical_analysis_pvalues_{output_name}.txt
               ├── statistical_analysis_deconvoluted_{output_name}.txt
               ├── statistical_analysis_interaction_scores_{output_name}.txt
               └── statistical_analysis_relevant_interactions_{output_name}.txt

当 ``cpdb_method=degs`` 时，核心结果文件前缀会切换为 ``degs_analysis_*``，并以 DEG 文件驱动通讯推断。

输入输出结构说明
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 阶段
     - 输入
     - 输出
   * - 主分析
     - 输入对象 + ``celltype_col`` +（可选）``microenvs/degs`` 文件
     - ``cellphonedb_output`` 下通讯矩阵结果
   * - 可视化
     - means / pvalues / interaction scores / deconvoluted
     - heatmap、dot plot、family plot、chord plot

参数差异与可视化结果含义
------------------------

1. ``cpdb_method=statistical`` 与 ``cpdb_method=degs`` 的差异
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
``statistical`` 模式通过置换检验评估通讯显著性，重点输出统计显著的配体-受体关系；``degs`` 模式依赖外部差异基因结果，更偏向条件驱动的通讯解释。

输出差异：

- ``statistical`` 常见文件：``statistical_analysis_means_*``、``statistical_analysis_pvalues_*``、``interaction_scores_*``。
- ``degs`` 常见文件：``degs_analysis_means_*``、``degs_analysis_pvalues_*`` 等，解释重点更偏向 DEG 支持的通讯轴。

2. ``iterations``、``pvalue``、``threshold`` 对图的影响
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：

- ``iterations`` 增大：统计稳定性通常提高，热图与点图中显著关系更稳健。
- ``pvalue`` 变小：筛选更严格，热图“显著互作总量”通常减少，点图更稀疏。
- ``threshold`` 变大：低表达关系被过滤，噪声降低但可能漏掉弱信号通讯。

建议：
先用默认值建立基线，再按“降低噪声”或“保留弱信号”的目标小步回调。

3. ``cell_type1/cell_type2`` 与 ``gene_family`` 对图的影响
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：

- ``cell_type1``/``cell_type2`` 决定点图与弦图聚焦的细胞对，改变后会直接改变展示的通讯边集。
- ``gene_family`` 决定家族点图筛选范围；如 ``chemokines`` 更偏迁移/趋化相关通讯，``costimulatory`` 更偏免疫激活轴。

建议：
先用组织学上最关注的细胞对做主图，再补充第二组细胞对进行对照，避免一次纳入过多类型导致图形可读性下降。

分析结果解释与实用建议
--------------------------------

1. 热图（``{sample}_heatmap.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/downstream_analysis/cellphonedb/{sample}_heatmap.png]

解释：
热图反映细胞类型两两之间显著互作数量总览，适合快速识别“通讯枢纽细胞群”。

建议：
优先锁定热图中高互作组合，再到点图查看具体配体-受体对。

2. 点图（``{sample}_dot_plot.png``）与家族点图（``{sample}_dot_family_plot.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/downstream_analysis/cellphonedb/{sample}_dot_plot.png]
   [在此插入图片路径：/_static/images/downstream_analysis/cellphonedb/{sample}_dot_family_plot.png]

解释：
点图用于展示特定细胞对的具体配体-受体关系及显著性；家族点图在同一细胞对下聚焦特定信号家族，便于机制归纳。

建议：
点图用于“广覆盖筛选”，家族点图用于“机制聚焦验证”，两者配合使用更稳妥。

3. 弦图（``{sample}_chord_plot.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/downstream_analysis/cellphonedb/{sample}_chord_plot.png]

解释：
弦图用于展示核心互作对在细胞群之间的网络连接强度与方向感，适合总结主通讯通路结构。

建议：
若弦图过于拥挤，优先收窄 ``cell_type1/cell_type2`` 或限定 ``interaction_pairs`` 再绘制。

结果检查与下一步
----------------
进入后续生物学解释前建议完成以下检查：

1. ``cellphonedb_output`` 中核心结果文件（means、pvalues）已生成。
2. ``heatmap``、``dot_plot``、``dot_family_plot`` 至少三类图件均可正常打开。
3. 关键细胞对的显著互作与已知 marker / 通路先验基本一致。
4. 参数回调后主要结论方向保持一致，避免单参数驱动结论。

若不满足，建议按“输入注释列正确性 → 统计阈值参数 → 方法选择（statistical/degs）”顺序逐步回调。
