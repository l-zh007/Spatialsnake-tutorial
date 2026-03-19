模块 7：差异表达比较（compare_stage）
======================================

该模块用于在多样本条件间进行差异表达比较，并对上/下调基因做 GO/KEGG 富集。
对应实现为 ``workflow/rules/compare_gene.smk``、``workflow/scripts/DEseq2.py`` 与 ``workflow/scripts/diffent_analysis.R``。

配置文件详解请见 :doc:`../config_reference/compare_stage_yaml`。

处理逻辑概述
------------

1. 基于上游注释对象按 ``celltype`` 与 ``region`` 聚合表达矩阵。
2. 根据样本分组执行 ``DEseq2``（样本数不足时自动退回 ``edgeR``）。
3. 对每个条件对比输出差异基因表与火山图。
4. 对上调/下调基因分别做 GO 与 KEGG 富集，并输出通路图件。

准备输入文件
------------

``compare_stage`` 差异比较建议复用 ``compare_analysis`` 主流程的样本表（含分组列）：

.. code-block:: text

   sample_id   input_path   group
   S1          data/S1      Tumor
   S2          data/S2      Normal
   S3          data/S3      Tumor

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

1. ``marker_genes_pval.csv``：全量差异结果主表，包含 ``log2FoldChange`` 与显著性统计。
2. ``vocanal.pdf``：每个条件对比的火山图，用于快速识别显著上/下调基因。
3. ``positive/negative`` 下 ``kegg_data.csv`` 与 ``GO_data.csv``：分别反映上调与下调方向的功能富集。
4. ``contrast_summary.csv``：汇总各对比中上/下调基因数量，适合章节级结论汇总。
