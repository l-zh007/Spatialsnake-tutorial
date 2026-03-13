模块 4：空间域建模（cellcharter）
==================================

功能对应 ``workflow/rules/run_cellcharter.smk``。

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellcharter --max_cluster=12 --cellcharter_col=spatial_cluster

关键参数
--------

- ``--significance``
- ``--max_cluster``
- ``--condition_col``
- ``--sample_col``
- ``--cellcharter_col``

输出
----

- ``results/cellcharter/{sample}_cellcharter.zarr``
