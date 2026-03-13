模块 5：空间聚类增强（banksy）
==============================

功能对应 ``workflow/rules/run_banksy.smk``。

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=banksy --k_geom=15 --resolution=0.8

关键参数
--------

- ``--k_geom``
- ``--max_m``
- ``--nbr_weight_decay``
- ``--n_comps``
- ``--lambda_list``

输出
----

- ``results/banksy/{sample}_banksy.zarr``
