核心分析流程
============

本模块对应 Snakefile 中的核心阶段 ``integrate``、``preprocess``、``clustering``、``annotion_help``、``reclustering``。

建议顺序：

1. 数据整合
2. 预处理
3. 聚类
4. 注释辅助
5. 二次聚类（可选）

.. toctree::
   :maxdepth: 1

   integrate
   preprocess
   clustering
   annotation_help
   reclustering
