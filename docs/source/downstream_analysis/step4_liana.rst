模块 3：细胞通讯（liana）
=========================

功能对应 ``workflow/rules/run_liana.smk``。

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=liana --liana_method=cellphonedb --liana_resource_name=consensus

关键参数
--------

- ``--liana_method``
- ``--liana_resource_name``
- ``--liana_expr_prop``
- ``--liana_min_cells``
- ``--liana_use_raw``

输出
----

- ``results/liana_output/{sample}.zarr``
