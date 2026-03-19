配置文件详解
============

本章节系统解释 Spatialsnake 在 ``workflow/envs`` 中提供的全部配置模板，帮助读者在保证可复现性的前提下，完成参数的科学化调优与流程定制。

每个子页面均围绕三项核心信息展开：

1. 参数名称与默认值（对应模板原始配置）
2. 参数的计算语义与适用场景
3. 实际调参中的优先级与联动关系

.. toctree::
   :maxdepth: 1

   integrate_yaml
   preprocess_yaml
   clustering_yaml
   annotion_help_yaml
   reclustering_yaml
   annotion_yaml
   advance_analysis_yaml
   compare_stage_yaml
   splitting_yaml
   merge_yaml
   transform_yaml
