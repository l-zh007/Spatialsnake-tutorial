重注释（reannotation）
======================

功能对应 ``workflow/rules/reannotation.smk``，用于在已有注释基础上更新标签。

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=reannotation --annotation-file=annotion.txt

适用场景
--------

- 修改已有 cluster 的细胞类型名称
- 合并/拆分少量标签后快速回写结果
