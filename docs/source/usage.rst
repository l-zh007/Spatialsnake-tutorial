Usage of Spatialsnake
========

若使用存在任何问题或对Spatialsnake功能有任何可扩展的建议, 欢迎在github上提交issue.
link: https://github.com/l-zh007/spatialsnake/issues

.. _quick_start:

Avaliable Platforms
--------------
- Sequence based
1. ``visium``: 10x genomics 空间转录组数据
2. ``visium HD`` : 10x genomics 高分辨率空间转录组数据
3. ``visium segment``: 10x genomics spaceranger 细胞分割结果
4. ``stereo-seq``: 华大基因 stereo-seq 空间转录组数据

- Image based
5. ``xenium``: 10x genomics Xenium 基于图像的空间转录组数据
6. ``Merfish``: Vigzen 空间转录组数据

.. note::
   尽管当前空间转录组存在很多优秀的测序平台, 考虑到技术分类和平台热度我们选取了其中的6个常用平台进行支持,对于未列出的平台
   spatialdata官方文档提供了多种接口,可以自行进行zarr格式读取后再使用spatialsnake进行后续的分析.

Basic Analysis Pipeline
--------------
我们将繁复的分析流程简化为若干个模块, 每个阶段都有对应的参数和推荐设置,覆盖了从初始数据到生物学意义挖掘的完整流程.

1. ``Ingesting``：读取原始空间转录组数据并标准化到统一对象
2. ``preprocess``：质控、过滤、归一化与降维准备
3. ``clustering``：聚类与可视化
4. ``annotation_help``：自动 marker 与富集提示
5. ``annotation``：人工或算法注释
6. ``reclustering``：对感兴趣的聚类结果进行二次亚群聚类（可选）
7. ``advance_analysis``：下游高级分析（如细胞通讯、调控网络等）
8. ``compare_stage``：多样本间差异分析与通讯比较

Diverse of Analysis Pipeline
--------------
对于不同的实验条件设置,我们根据不同的分析需求,提供了不同的分析流程,为多样本分析提供了便捷的解决方案.

- ``single_analysis``：单样本分析
- ``compare_analysis``：多样本整合比较分析 适用于不同或相同实验条件的空转数据整合


Useful Tools provided
--------------
面对不同的实验场景,我们提供了一些有用的工具,帮助用户更方便地应对各种分析需求.

- ``splitting``：切分对象, 适用于将大样本数据切分至多个小样本,选取ROI, 与Xenium Explorer 或 Loupe Browser 互作
- ``merge``：合并对象, 适用于将多个小样本数据 或 亚群注释数据合并至大样本
- ``transform``：格式转换, 适用于将数据转换为其他格式, 如 ``zarr`` 转换为 ``h5ad`` 或 ``seurat``


The hardware requirements for Spatialsnake
--------------
Linux

- 内存：建议 16GB 以上
- 硬盘空间：根据数据量和分析需求，建议 100GB 以上
- CPU：多核处理器
- GPU：可选，用于加速某些分析（如可视化）


Start your analysis with Spatialsnake!
--------------
下载与环境配置 :doc:`environment_setup`

命令行与项目结构（已整合）
--------------

.. include:: project_layout.rst
   :start-line: 4
