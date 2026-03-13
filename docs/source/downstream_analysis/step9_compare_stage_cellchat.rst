模块 8：通讯比较（compare_stage + cellchat）
============================================

功能对应 ``workflow/rules/compare_LR.smk``，比较两个 CellChat ``.rds`` 结果。

准备 ``sample.txt``
--------------------

.. code-block:: text

   sampleA    /abs/path/sampleA_cellchat.rds
   sampleB    /abs/path/sampleB_cellchat.rds

运行命令
--------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=cellchat

输出
----

- ``results/compare_cellchat/`` 下的比较图与汇总结果
