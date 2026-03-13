人工注释（mannul）
==================

功能对应 ``workflow/rules/mannul.smk``，调用 ``workflow/scripts/mannul_annotion.py``。

准备映射表
----------

.. code-block:: text

   clusters    celltype
   0           Tumor
   1           T_cell
   2           Fibroblast

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt

输出
----

- ``results/{sample}/annotion/{sample}.zarr``
