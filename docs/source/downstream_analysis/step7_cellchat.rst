模块 6：细胞通讯网络（cellchat）
=================================

功能对应 ``workflow/rules/run_cellchat.smk``。

运行命令
--------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat --celltype_col=celltype --cellchat_species=human

关键参数
--------

- ``--cellchat_assay``
- ``--cellchat_species``
- ``--cellchat_min_cells``
- ``--cellchat_workers``
- ``--cellchat_interaction_length``

输出
----

- ``results/{sample}/cellchat/{sample}_cellchat_network.png``
- ``results/{sample}/cellchat/{sample}_cellchat_stats.csv``
