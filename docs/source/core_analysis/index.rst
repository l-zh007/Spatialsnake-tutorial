核心分析流程
====================

依据空间转录组的基础分析流程,我们将 Spatialsnake 的核心分析阶段分为以下几个步骤:
1. 数据整合（integrate）
2. 预处理（preprocess）
3. 聚类（clustering）
4. 注释辅助（annotion_help）

由于输出结果类似，为了避免内容冗杂，此页我们以Visium HD 单样本数据进行core_analysis的全流程连贯分析
最终得到细胞注释结果供给下游分析模块使用.

若您使用的是其他空间转录组数据,甚至读取的数据为整合多样本数据,请完整阅读每个步骤的文档,我们会在其中详细说明操作命令和参数的异同.


.. toctree::
   :maxdepth: 1

   Ingesting
   preprocess
   clustering
   annotation_help
