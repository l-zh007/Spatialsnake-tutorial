二次聚类（reclustering）
========================

功能对应 ``workflow/rules/reclustering.smk``，调用 ``workflow/scripts/reclustering.py``。

用途
----

- 对某个已完成注释/聚类的对象重新细分亚群
- 输出新的 UMAP、空间图和 marker 表

输入要求
--------

``sample.txt`` 第二列改为已处理对象路径（例如 ``results/S1/annotion/S1.zarr``）。

最小命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=reclustering

关键参数
--------

- ``--recluster_resolution``
- ``--recluster_n_top_genes``
- ``--recluster_neighbors``
- ``--recluster_n_pcs``
