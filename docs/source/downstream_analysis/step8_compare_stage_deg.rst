模块 7：差异表达比较（compare_stage）
======================================

功能对应 ``workflow/rules/compare_gene.smk`` 与 ``workflow/scripts/DEseq2.py``。

运行命令
--------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --cell_focus=CAF --compare_algorithm=DEseq2

适用场景
--------

- 该步骤输入为已注释结果
- 输出差异基因表与富集结果

输出路径
--------

- ``results/merge_data/compare_analysis/marker_genes_pval.csv``
- ``results/merge_data/compare_analysis/positive/kegg_data.csv``
