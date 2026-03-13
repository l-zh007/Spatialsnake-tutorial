算法注释（RCTD）
================

功能对应 ``workflow/rules/RCTD.smk`` 与 ``workflow/scripts/RCTD.R``。

输入要求
--------

- 空间对象路径
- 参考单细胞对象路径
- 参考细胞类型列名（默认 ``celltype``）

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=RCTD --max_cores=16

输出
----

- ``{sample}_RCTD_results.csv``
- ``{sample}_RCTD_weights.csv``
- ``{sample}_RCTD_spatial_plot.png``
