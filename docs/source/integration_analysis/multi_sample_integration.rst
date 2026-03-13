多样本整合
==========

本教程只覆盖与单样本流程不同的部分，单样本通用步骤请参考核心分析模块。

步骤 1：准备带分组信息的样本表
--------------------------------

多样本整合时，``sample.txt`` 需要包含分组列。

示例文件：``examples/sample_multi.txt``

.. code-block:: text

   sample    input_path                 group
   Tumor_1   data/Tumor_1/filtered...   Tumor
   Tumor_2   data/Tumor_2/filtered...   Tumor
   Normal_1  data/Normal_1/filtered...  Normal
   Normal_2  data/Normal_2/filtered...  Normal

步骤 2：执行整合与合并
-----------------------

.. code-block:: bash

   spatialsnake compare_analysis examples/sample_multi.txt visium --option=integrate

该步骤会在 ``integrate`` 后自动触发 ``merge.smk`` 输出 ``concatenated_sdata``。

步骤 3：多样本预处理（差异点）
-------------------------------

单样本通常不设置批次校正，多样本建议显式启用：

.. code-block:: bash

   spatialsnake compare_analysis examples/sample_multi.txt visium --option=preprocess --batch_method=harmony

步骤 4：后续步骤直接沿用 compare_analysis
-----------------------------------------

.. code-block:: bash

   spatialsnake compare_analysis examples/sample_multi.txt visium --option=clustering
   spatialsnake compare_analysis examples/sample_multi.txt visium --option=annotion_help
   spatialsnake compare_analysis examples/sample_multi.txt visium --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt

步骤 5：使用可执行脚本一键运行
------------------------------

.. code-block:: bash

   bash examples/run_multi_sample_integration.sh

示例数据与脚本
--------------

- ``examples/sample_multi.txt``：多样本整合输入清单
- ``examples/annotion_multi.txt``：整合后 cluster 注释映射
- ``examples/run_multi_sample_integration.sh``：可执行流程脚本
