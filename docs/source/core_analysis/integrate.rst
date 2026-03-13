数据整合（integrate）
=====================

功能对应 ``workflow/rules/integrate.smk``，用于读取原始数据并输出统一对象。

单样本命令
----------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=integrate

多样本命令
----------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=integrate

输入要求
--------

- ``single_analysis``：``sample.txt`` 包含样本名与输入目录
- ``compare_analysis``：``sample.txt`` 增加分组列，且会触发 ``merge.smk`` 生成整合对象

输出
----

- 单样本：``results/{sample}/integrate/{sample}.zarr``
- 多样本：``results/merge_data/integrate/concatenated_sdata``
