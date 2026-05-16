Core Analysis Workflow
======================

Following the standard spatial transcriptomics workflow, Spatialsnake organizes the core analysis into four stages:

1. Data integration (``integrate``)
2. Preprocessing (``preprocess``)
3. Clustering (``clustering``)
4. Annotation support (``annotation_help``)


我们根据空间转录组常见分析顺序与其中的分析决策阶段,将核心流程拆分为上述四个分析流程,通过四个流程您将完成从一份原始的空转数据到熟知样本中包含的细胞类型的分析。
Because the outputs are largely consistent across platforms, this section uses a single-sample Visium HD dataset to demonstrate the full core workflow from start to finish. The final output is a cell annotation result that can be used as input for downstream analysis modules.

If you are working with another spatial transcriptomics platform, or with an already integrated multi-sample dataset, we recommend reading the documentation for each step in full. The individual pages explain the differences in commands and parameters where needed.


.. toctree::
   :maxdepth: 1
   :titlesonly:

   Ingesting
   preprocess
   clustering
   annotation_help
