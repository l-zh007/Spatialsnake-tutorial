Spatialsnake for multi-sample integration
==========

进行阅读前请确保您已经学习过至少一个Select your data platform 中的教程,了解如何准备样本表和运行 Spatialsnake。
本教程专属于当您有多个实验条件不同的空间转录组数据集时使用,例如不同的肿瘤类型,不同的正常组织类型等。
对于空间转录组,通过此步骤整合的zarr数据和单样本一致,都可进行后续的分析,仅分析结果稍有不同。

这里我们使用 等人的 visium HD 多个结肠癌数据集进行结果演示

步骤 1: 准备带分组信息的样本表
--------------------------------

多样本整合时，于单样本类似``sample.txt`` 需要包含分组列。

.. code-block:: text

   sample    input_path                 group
   Colon_Cancer_P2   data/Colon_Cancer_P2   Tumor
   Colon_Normal_P5  data/Colon_Normal_P5 Normal

步骤 2: 执行整合与合并
-----------------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=integrate

结果文件于单样本结果文件类似
.. code-block:: text

   results/
   └── merge_data/
       └── integrate/
           └── concatenated_sdata
               ...........



步骤 3: 多样本预处理（差异点）
-------------------------------

单样本通常不设置批次校正，多样本建议显式启用：

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --batch_method=harmony

步骤 4: 后续步骤直接沿用 compare_analysis 部分结果会输出多个样本的可视化图像或数据，但由于是整合数据 在手动注释部分可默认将多个样本间的cluster进行合并注释
-----------------------------------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=clustering
   spatialsnake compare_analysis sample.txt visium --option=annotion_help
   spatialsnake compare_analysis sample.txt visium --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt


您已成功得到一个整合后的空转数据,后续的分析流程于单样本分析流程类似,部分注意细节在每个步骤中会有说明,请认真阅读。
------------------------------------------------------------
Continue to :doc:`data_input/index`

