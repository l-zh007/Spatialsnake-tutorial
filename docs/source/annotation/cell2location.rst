算法注释（cell2Location）
=========================

功能对应 ``workflow/rules/cell2Location_run.smk``，先训练映射，再执行可视化输出。

输入要求
--------

- ``input_spatial``：空间转录组对象
- ``input_singlecell``：参考单细胞表达矩阵与细胞类型标签

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=cell2Location --device=cuda --max_cores=16

关键参数
--------

- ``--max_epochs_reference``
- ``--N_cells_per_location``
- ``--max_epochs_st``
- ``--device``

输出
----

- ``results/{sample}/cell2Location/{sample}.zarr``
