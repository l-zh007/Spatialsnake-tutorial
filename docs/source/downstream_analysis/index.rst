下游分析模块总览
================

本模块对应 ``option=advance_analysis`` 与 ``option=compare_stage``，按功能模块组织。
建议先完成核心分析与注释，再按研究问题选择对应模块。

配置文件详解：

- ``advance_analysis`` 参见 :doc:`../config_reference/advance_analysis_yaml`
- ``compare_stage`` 参见 :doc:`../config_reference/compare_stage_yaml`


下游分析分为两类入口：

1. ``--option=advance_analysis``：单模块运行（cellPhoneDB / pysenic / liana / cellcharter / banksy / cellchat）。
2. ``--option=compare_stage``：组间比较（差异表达 compare_gene 或 cellchat 比较）。

其中 ``advance_analysis`` 通常读取上游 ``annotion`` 或其他下游模块产出的 ``.zarr/.h5ad``；``compare_stage`` 读取比较所需对象（注释整合对象或 CellChat ``.rds``）。


准备 ``sample.txt``
-------------------

场景 A：``single_analysis + advance_analysis`` （最常用）

.. code-block:: text

   sample_id   input_path
   S1          results/S1/annotion/S1.zarr

场景 B：``compare_analysis + advance_analysis`` （仅支持一个整合对象路径）

.. code-block:: text

   sample_id            input_path
   concatenated_sdata   results/merge_data/annotion/concatenated_sdata

场景 C：``compare_analysis + compare_stage --runpipe=cellchat`` （比较两个 CellChat 结果）

.. code-block:: text

   sample_id   input_path
   Tumor       /abs/path/tumor_cellchat.rds
   Normal      /abs/path/normal_cellchat.rds

统一命令入口
------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=<module>

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=<module>



.. toctree::
   :maxdepth: 1

   step1_prepare_input
   step2_cellphonedb
   step3_pysenic
   step4_liana
   step5_cellcharter
   step6_banksy
   step7_cellchat
   step8_compare_stage_deg
   step9_compare_stage_cellchat
