聚类（clustering）
==================

功能对应 ``workflow/rules/cluster.smk``，调用 ``workflow/scripts/clustering.py``。

输入与输出
----------

- 输入：预处理结果 ``filter_{sample}.zarr`` 或 ``filter_{sample}.h5ad``
- 输出：``results/{sample}/clustering/{sample}.zarr``（slide-seq 为 ``.h5ad``）
- 比较分析输出：``results/merge_data/clustering/concatenated_sdata``

最小命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=clustering

常用参数
--------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--cluster_algorithm``
     - ``leiden``
     - 可选 ``leiden`` / ``louvain`` / ``Kmeans``
   * - ``--resolution``
     - ``0.5``
     - 社区发现分辨率
   * - ``--n_clusters``
     - ``15``
     - KMeans 聚类数
   * - ``--pcs``
     - ``30``
     - PCA 维度
   * - ``--NEIGHBORS``
     - ``10``
     - 邻域图参数

命令示例
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=clustering --cluster_algorithm=leiden --resolution=0.8 --pcs=25
