核心分析流程
====================

依据空间转录组的基础分析流程,我们将 Spatialsnake 的核心分析阶段分为以下几个步骤:
1. 数据整合（integrate）
2. 预处理（preprocess）
3. 聚类（clustering）
4. 注释辅助（annotion_help）
5. 二次聚类（reclustering，可选）

由于输出结果类似，为了避免内容冗杂，此页我们以Visium HD 单样本数据进行core_analysis的全流程连贯分析，所有异同将会在每一步骤的文档中进行说明。


.. toctree::
   :maxdepth: 1

   Ingesting
   preprocess
   clustering
   annotation_help
   reclustering
