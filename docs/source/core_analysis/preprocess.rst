预处理（preprocess）
=====================

功能对应 ``workflow/rules/preprocess.smk``，调用 ``workflow/scripts/preprocessing.py``。

输入与输出
----------

- 单样本输入：``results/{sample}/integrate/{sample}.zarr``（或 slide-seq 的 ``.h5ad``）
- 比较分析输入：``results/merge_data/integrate/concatenated_sdata``
- 输出：``results/{sample}/preprocess/filter_{sample}.zarr``（或 slide-seq 的 ``.h5ad``）

最小命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess

关键差异参数
------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--batch_method``
     - ``harmony``
     - 仅多样本比较时常用，降低批次效应
   * - ``--mt_threshold``
     - ``50``
     - 线粒体比例过滤阈值
   * - ``--n_top_genes``
     - ``1000``
     - 高变基因数量
   * - ``--n_comps``
     - ``50``
     - PCA 维度数
   * - ``--min_cells`` / ``--min_genes``
     - ``3`` / ``200``
     - 基因与 spot/cell 过滤阈值

命令示例
--------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --batch_method=harmony --mt_threshold=40
