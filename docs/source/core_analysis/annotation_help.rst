注释辅助（annotion_help）
=========================

``annotion_help`` 在聚类结果基础上执行 marker 基因统计与富集分析，用于为后续 ``annotion`` 提供可解释的生物学证据。
在单样本场景中，该步骤用于确定各 cluster 的候选细胞类型；在多样本联合场景中，还需要评估 marker 与通路结果是否受样本构成影响。

配置文件详解请见 :doc:`../config_reference/annotion_help_yaml`。

处理逻辑概述
------------
1. 读取 ``clustering`` 阶段输出对象与 ``clusters`` 标签。
2. 按 cluster 计算差异 marker 基因并导出总表与分簇子表。
3. 绘制 marker dotplot、样本-簇比例图与空间叠加图。
4. 基于 marker 基因执行 KEGG 富集分析并输出通路结果。
5. 将注释辅助结果统一写入 ``clustering`` 目录，供 ``annotion`` 直接调用。

.. note::

   若您的数据并非Visium HD平台或为多样本整合数据，请阅读完后查看文末，学习不同平台和样本数量下的输入与输出差异。


Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion_help
   spatialsnake compare_analysis sample.txt visium --option=annotion_help

运行可选的参数设置(命令行版)
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--markers_algorithm``
     - ``wilcoxon``
     - marker 统计方法，常用 ``wilcoxon``；也可按数据特征选择 ``t-test`` 等方法
   * - ``--spacies``
     - ``human``
     - 富集分析物种背景，常用 ``human`` / ``mouse``

以上参数由命令行直接传入 ``annotion_help`` 与富集流程。若您希望快速替换分析策略，可在命令后追加参数（如 ``--markers_algorithm t-test --spacies mouse``）。


运行可选的参数设置(配置文件版)
------------------------------------------------------------
若您已熟悉 Spatialsnake，建议通过配置文件统一管理 ``image_type``、``shape_type``、``image_slice`` 等可视化参数，并在多样本中保持一致。

运行下列命令获取 yaml 模板

.. code-block:: bash

   spatialsnake produce-file --option=annotion_help

在 yaml 中可进一步细化空间可视化范围与图层渲染策略，适用于跨样本或多区域的统一注释辅助流程。


运行最终运行命令吧
----------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotion_help --configfile annotion_help.yaml


结果文件结构
------------

当前示例为 ``visium_HD`` 单样本注释辅助。建议先确认 ``marker_genes_pval.csv`` 与 ``kegg_data.csv`` 已生成，再进入人工注释。

.. code-block:: text

   results/
   └── {sample}_{bin}um/
       └── clustering/
           ├── marker_genes_pval.csv
           ├── kegg_data.csv
           ├── {sample}rank_genes_groups_dotplot.png
           ├── Clusters_proportion.png
           ├── [image]_Clusters.png
           ├── [cluster_id]/
           │   └── cluster_[cluster_id].csv
           └── clusters.csv

其中，``marker_genes_pval.csv`` 与 ``kegg_data.csv`` 是后续注释的核心依据；其余图表用于评估 cluster 区分度、空间分布一致性与样本构成差异。

.. note::

   core_analysis中关于空间转录组的大体分析流程已经完结了，得到的注释辅助结果已经存储在 ``clustering`` 目录下，后续请跳转 :doc:`../annotation/index` 进行人工注释或其他注释对注释信息进行探索吧！




多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - 场景
     - 推荐命令
   * - 单样本（Visium HD，本节演示）
     - ``spatialsnake single_analysis sample.txt visium_HD --option=annotion_help``
   * - 单样本（常规 zarr 平台：visium / xenium / visium_segment）
     - ``spatialsnake single_analysis sample.txt visium --option=annotion_help``
   * - 单样本（slide_seq）
     - ``spatialsnake single_analysis sample.txt slide_seq --option=annotion_help``
   * - 多样本联合注释辅助
     - ``spatialsnake compare_analysis sample.txt visium --option=annotion_help``


关键参数建议
------------

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - 参数类别
     - 单样本建议
     - 多样本或跨条件建议
   * - ``--markers_algorithm``
     - 首选 ``wilcoxon``，结果稳定、解释直观
     - 建议全样本保持同一统计方法，降低比较偏差
   * - ``--spacies``
     - 与样本物种一致（``human`` 或 ``mouse``）
     - 必须在全部样本间保持一致，否则富集结果不可直接横向比较
   * - image_type / shape_type（yaml）
     - 可保持默认并先完成全局分析
     - 联合对象建议统一图层类型，避免因可视化基准变化影响判读
   * - image_slice（yaml 参数）
     - 通常关闭，先看整体结构
     - 仅在目标区域分析时开启，并建议同步记录裁剪坐标以便复现


输入输出结构的差异
------------------
完成 ``clustering`` 后，通常可直接复用同一份 ``sample.txt`` 进入 ``annotion_help``。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 分析模式
     - 输入
     - 输出
   * - single_analysis（常规 zarr 类型）
     - ``sample.txt`` 至少包含 ``sample_id input_path``；输入对象为 ``results/{sample}/clustering/{sample}.zarr``
     - ``results/{sample}/clustering/marker_genes_pval.csv`` 与 ``results/{sample}/clustering/kegg_data.csv``
   * - single_analysis（visium_HD）
     - ``sample.txt`` 至少包含 ``sample_id input_path bin``；输入对象为 ``results/{sample}_{bin}um/clustering/{sample}.zarr``
     - ``results/{sample}_{bin}um/clustering/marker_genes_pval.csv`` 与 ``results/{sample}_{bin}um/clustering/kegg_data.csv``
   * - compare_analysis
     - ``sample.txt`` 至少包含 ``sample_id input_path group``（visium_HD 需额外 ``bin``）；输入对象为 ``results/merge_data/clustering/concatenated_sdata``
     - ``results/merge_data/clustering/marker_genes_pval.csv`` 与 ``results/merge_data/clustering/kegg_data.csv``


结果解读
----------------

建议按“结果展示 → 解释 → 回调建议”的顺序阅读该步骤产物，并与 clustering 结果联动判断 cluster 是否具备可注释性。

1. marker 统计总表（``marker_genes_pval.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（文件占位）：

.. code-block:: text

   [在此插入文件路径：results/.../clustering/marker_genes_pval.csv]

解释：
该表汇总每个 cluster 的差异基因统计量，是细胞类型判定的一级证据。建议重点关注显著性、效应方向与基因是否具备已知生物学意义。

建议：
优先选择在同一 cluster 内稳定上调且文献支持充分的 marker 进入候选注释列表；对统计显著但生物学含义弱的基因保持审慎。

2. cluster 分层子表（``[cluster_id]/cluster_[cluster_id].csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（文件占位）：

.. code-block:: text

   [在此插入文件路径：results/.../clustering/[cluster_id]/cluster_[cluster_id].csv]

解释：
分簇子表适合进行逐簇深度审阅，可快速判断某 cluster 的 marker 是否集中于同一谱系，或存在混合信号。

建议：
若某 cluster 呈现多谱系混合 marker，可回到 clustering 阶段重新评估 ``resolution`` 与 ``pcs`` 设定。

3. 富集结果表（``kegg_data.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（文件占位）：

.. code-block:: text

   [在此插入文件路径：results/.../clustering/kegg_data.csv]

解释：
KEGG 富集用于提供通路层面的辅助证据，帮助区分“统计显著但难解释”的 marker 组合。多样本联合分析时，需警惕样本构成导致的通路偏移。

建议：
仅将与组织背景一致、且与 marker 证据方向一致的富集条目作为高置信注释依据。

4. 可视化结果（dotplot、cluster 比例、空间叠加图）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/core_analysis/annotion_help/rank_genes_groups_dotplot.png]
   [在此插入图片路径：/_static/images/core_analysis/annotion_help/Clusters_proportion.png]
   [在此插入图片路径：/_static/images/core_analysis/annotion_help/[image]_Clusters.png]

解释：
dotplot 用于比较各 cluster marker 的表达模式；比例图用于观察样本组成差异；空间叠加图用于验证 cluster 的空间连贯性与组织结构一致性。

建议：
当三类图像结论一致时，可直接进入 ``annotion`` 阶段；若三者冲突，建议先回调 clustering 参数再进行注释。


结果检查与下一步
----------------
建议在进入 ``annotion`` 前完成以下检查：

1. ``marker_genes_pval.csv`` 中主要 cluster 具备清晰且可解释的 marker 组合。
2. ``kegg_data.csv`` 中高显著通路与组织背景及 marker 方向一致。
3. dotplot、比例图与空间叠加图对主要 cluster 的结论一致。

若以上三项中任一项不满足，建议先回调 ``clustering`` 参数并重跑 ``annotion_help``，再进入细胞类型注释。



.. note::

   core_analysis中关于空间转录组的大体分析流程已经完结了，得到的注释辅助结果已经存储在 ``clustering`` 目录下，后续请跳转 :doc:`../annotation/index` 进行人工注释或其他注释对注释信息进行探索吧！
