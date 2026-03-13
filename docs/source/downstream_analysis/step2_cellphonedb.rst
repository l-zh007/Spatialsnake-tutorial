模块 1：细胞通讯（cellPhoneDB）
===============================

功能对应 ``workflow/rules/cellPhoneDB.smk``。

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellPhoneDB --threads=16 --output_name=Normal

常用参数
--------

- ``--counts_data``
- ``--celltype_col``
- ``--cpdb_method``
- ``--cpdb_de_method``
- ``--iterations``

输出目录
--------

- 单样本：``results/{sample}/cellPhoneDB_results/``
- 比较分析：``results/merge_data/cellPhoneDB_results/``
