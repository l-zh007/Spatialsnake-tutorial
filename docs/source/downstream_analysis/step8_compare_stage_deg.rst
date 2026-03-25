模块 7：差异表达比较（compare_stage）
======================================

在多样本空间转录组分析中，样本间基因表达差异分析是比较常见的任务。
该模块用于在多样本条件间进行差异表达比较，并对上/下调基因做 GO/KEGG 富集,方便用户挖掘不同实验条件下的基因表达差异。

配置文件详解请见 :doc:`../config_reference/compare_stage_yaml`。

运行步骤与内容
--------------

1. **构建 Pseudobulk 表达矩阵**
   读取整合后的空间或单细胞对象，利用伪群（Pseudobulk）策略，按照细胞类型（``celltype``）和样本来源（``region``）对原始表达矩阵进行求和聚合。同时可根据 ``cell_focus`` 参数筛选特定的细胞群体进行针对性比较。
2. **差异基因统计推断 (DEseq2/edgeR)**
   系统根据样本组（``condition``）的数量自动选择最优的差异分析算法。当样本量充足时，构建 PyDESeq2 分析模型（``~condition``）进行离散度估计和差异倍数计算；若样本量极少（<3），则自动回退至 edgeR 算法。计算并导出所有分组间两两对比的基因差异倍数（Log2FoldChange）和显著性（padj）。
3. **统计结果多维可视化**
   基于上述推断结果，根据预设的显著性阈值（如 ``padj < 0.05`` 且 ``|log2FC| > 1``）筛选出显著上调与下调的基因。随后自动生成展示全量基因分布的火山图（Volcano Plot）、MA 图，以及展示显著差异基因跨样本表达模式的聚类热图（Heatmap）。
4. **功能注释与通路富集分析**
   对筛选出的上调和下调基因，自动执行 ID 转换（Symbol 转 Entrez ID），并利用 ``clusterProfiler`` 执行 GO（BP/CC/MF）功能富集与 KEGG 代谢通路富集分析。
5. **高级富集图表生成**
   将富集结果转化为直观的生物学图表，包括按本体分类的 GO 气泡图、Cluster 专属柱状图，以及展示通路层级与基因流向的 KEGG 桑基气泡组合图（Sankey-Bubble plot）。

准备输入文件
------------

``compare_stage`` 差异比较建议复用 ``compare_analysis`` 主流程的样本表,输入整合样本即可:

.. code-block:: text

   sample_id   input_path
   Conlon_cancer_P1 results/concatenation

输入要求：

1. 进入本步骤前，应已完成 ``compare_analysis`` 下的 ``annotion``。
2. ``group`` 至少包含两个条件名称，用于构建设计矩阵。
3. ``cell_focus`` 可指定关注细胞类型；为空时默认对全部 celltype 聚合后比较。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=compare_gene

可选参数示例：

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=compare_gene --cell_focus=CAF --compare_algorithm=DEseq2

运行可选的参数设置(配置文件版)
------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 24 52

   * - 参数
     - 常用值
     - 作用
   * - ``runpipe``
     - ``compare_gene``
     - 指定使用差异表达分支
   * - ``compare_algorithm``
     - ``DEseq2`` / ``edgeR``
     - 差异分析算法
   * - ``cell_focus``
     - ``CAF`` 或 ``T_cell``
     - 仅比较目标细胞类型（支持逗号分隔多个关键词）
   * - ``spacies``
     - ``human`` / ``mouse``
     - 富集分析物种背景

结果文件结构
------------

.. code-block:: text

   results/
   └── merge_data/
       └── compare_analysis/
           ├── marker_genes_pval.csv
           ├── contrast_summary.csv
           ├── contrast_log2fc_heatmap.pdf
           ├── diff/
           │   └── {group1}_vs_{group2}.csv
           ├── positive/
           │   ├── diff_strict.csv
           │   ├── diff_loose.csv
           │   ├── GO_data.csv
           │   ├── kegg_data.csv
           │   ├── GO_enrich.pdf
           │   └── kegg_cluster.pdf
           ├── negative/
           │   ├── diff_strict.csv
           │   ├── diff_loose.csv
           │   ├── GO_data.csv
           │   ├── kegg_data.csv
           │   ├── GO_enrich.pdf
           │   └── kegg_cluster.pdf
           └── {contrast}/
               ├── diff_all.csv
               ├── vocanal.pdf
               ├── positive/...
               └── negative/...

图表与结果解释
--------------

1. 差异基因火山图（``vocanal.pdf``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/GO_cluster.png
   :width: 85%
   :align: center
   :alt: deg volcano plot

解释：
火山图直观地展示了基因在两个对比条件间的表达变化。横轴为差异倍数（Log2FoldChange），纵轴为显著性（-log10(p-value)）。分布在左上角和右上角的基因分别是显著下调和显著上调的关键基因。

2. 差异基因聚类热图（``contrast_log2fc_heatmap.pdf``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_heatmap.png
   :width: 85%
   :align: center
   :alt: deg heatmap

解释：
将显著差异基因进行标准化（rlog 转换）后绘制的热图。通过对样本和基因的双向聚类，展示不同实验条件下特征基因群的表达模式差异。

3. GO 功能富集气泡图（``GO_cluster.pdf`` / ``GO_enrich.pdf``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/GO_cluster.png
   :width: 85%
   :align: center
   :alt: deg go enrichment

解释：
气泡图按本体分类（生物学过程 BP、细胞组分 CC、分子功能 MF）展示显著富集的 GO 条目。气泡大小代表该通路包含的差异基因数量，颜色深浅代表富集的显著性（p-adjust）。

4. KEGG 代谢通路桑基气泡组合图（``kegg_cluster.pdf``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/kegg_cluster.png
   :width: 85%
   :align: center
   :alt: deg kegg enrichment

解释：
将传统的 KEGG 气泡图与桑基图（Sankey）结合，不仅展示了具体通路（Description）的富集显著性和倍数，还追溯了该通路所属的上游大类（Subcategory），帮助研究者从宏观和微观两个层面理解通路变化。

5. 汇总统计表（``marker_genes_pval.csv`` / ``contrast_summary.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
``marker_genes_pval.csv`` 是包含全量统计推断结果的主表（含 fold change 和 padj），``contrast_summary.csv`` 则宏观汇总了各对比组合中显著上/下调的基因数量，是撰写报告和结论汇总的核心参考。
