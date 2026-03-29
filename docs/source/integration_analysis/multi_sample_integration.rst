Spatialsnake for multi-sample integration
==========

进行阅读前请确保您已经学习过至少一个Select your data platform 中的教程,了解如何准备样本表和运行 Spatialsnake。
本教程专属于当您有多个实验条件不同的空间转录组数据集时使用,例如不同的肿瘤类型,不同的正常组织类型等。
对于空间转录组,通过此步骤整合的zarr数据和单样本一致,都可进行后续的分析,仅分析结果稍有不同。

多样本数据通常整个多个数据集,为了简便演示,这里我们使用  等人的 visium 多个小鼠大脑切片数据集进行结果演示

https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-11114


数据下载准备
--------------------------------

本教程使用 5 个公开样本：

- 第一组：``ST8059048``、``ST8059049``、``ST8059050``
- 第二组：``ST8059051``、``ST8059052``

步骤 1: 在项目根目录创建下载脚本
--------------------------------

先确保当前工作目录下存在 ``data/`` 文件夹,然后在工作目录创建脚本文件 ``touch download.sh``

.. code-block:: bash

   #!/usr/bin/env bash
   set -euo pipefail
   ids=(ST8059048 ST8059049 ST8059050 ST8059051 ST8059052)
   for id in "${ids[@]}"; do
   mkdir -p "data/${id}"
   cd "data/${id}"
   wget -c "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/114/E-MTAB-11114/Files/${id}_filtered_feature_bc_matrix.h5"
   wget -c "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/114/E-MTAB-11114/Files/${id}_spatial.tar.gz"
   tar -xvzf "${id}_spatial.tar.gz"
   cd - >/dev/null
   done


步骤 2: 赋予执行权限并运行脚本
-------------------------------

.. code-block:: bash

   chmod +x download.sh
   ./download.sh

步骤 3: 准备带分组信息的样本表
--------------------------------

多样本整合时，于单样本类似``sample.txt`` 需要包含分组列。

.. code-block:: text

   sample_id   input_path         group
   ST8059048   data/ST8059048     Group1
   ST8059049   data/ST8059049     Group1
   ST8059050   data/ST8059050     Group1
   ST8059051   data/ST8059051     Group2
   ST8059052   data/ST8059052     Group2

步骤 4: 执行整合与合并
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



步骤 5: 多样本预处理（差异点）
-------------------------------

单样本通常不设置批次校正，多样本建议显式启用：

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --min_genes 100 --min_cells 100

步骤 6: 后续步骤直接沿用 compare_analysis 部分结果会输出多个样本的可视化图像或数据，但由于是整合数据 在手动注释部分可默认将多个样本间的cluster进行合并注释
-----------------------------------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=clustering --resolution 0.8 --pcs 20
   spatialsnake compare_analysis sample.txt visium --option=annotion_help
   spatialsnake compare_analysis sample.txt visium --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt

我们仅根据小鼠大脑分析做简要的broad region 注释,注释仅供参考,并非复现原文中的注释。
.. code-block:: bash

   sample 0 1 2 3 4 5.........please input anno by order of cluster
   thalamus,cortex,cortex,amygdala,hypothalamus,hypothalamus,striatum,cortex,cortex,white matter,hypothalamus,thalamus,hippocampus,hippocampus,hippocampus,piriform_cortex,cortex,cortex,cortex,cortex,cortex,cortex,cortex,amygdala,thalamus,thalamus


您已成功得到一个整合后的空转数据,后续的分析流程于单样本分析流程类似,部分注意细节在每个步骤中会有说明,请认真阅读。
------------------------------------------------------------
Continue to :doc:`data_input/index`


这里展示一下我们的可视化结果
------------------------------------------------------------
Continue to :doc:`data_input/index`
