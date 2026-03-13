模块 2：调控网络（pysenic）
============================

功能对应 ``workflow/rules/py_senic.smk``，流程包含 loom 转换、GRN 推断、ctx、AUCell。

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=pysenic --senic_workers=16 --senic_input=results/S1/annotion/S1.zarr

必须准备
--------

- ``--tfs_input``
- ``--feather_input``
- ``--motifs_input``

输出目录
--------

- ``results/pysenic_results/``
