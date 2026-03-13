注释辅助（annotion_help）
=========================

功能对应 ``workflow/rules/annotion_help.smk``，先运行 marker 计算，再运行富集分析。

步骤一：生成 marker
-------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion_help --markers_algorithm=wilcoxon

步骤二：读取富集结果
------------------------

``annotion_help`` 阶段会继续调用 ``workflow/scripts/enrichment.R`` 输出 ``kegg_data.csv``。

关键输出
--------

- ``marker_genes_pval.csv``：聚类 marker 统计
- ``kegg_data.csv``：KEGG 富集结果

输出路径
--------

- 单样本：``results/{sample}/clustering/``
- 比较分析：``results/merge_data/clustering/``
