注释辅助（annotion_help）
=========================

``annotion_help`` 在聚类结果基础上执行 marker 基因统计与富集分析，用于为后续 ``annotion`` 提供可解释的生物学证据。
在单样本场景中，该步骤用于确定各 cluster 的候选细胞类型；在多样本联合场景中，还需要评估 marker 与通路结果是否受样本构成影响。


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
若您已熟悉 Spatialsnake,建议通过配置文件统一管理 

请参考配置文件并根据下述说明进行设置 :doc:`../config_reference/annotion_help_yaml`。

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
   └── Conlon_cancer_P1_008um/
       └── clustering/
           ├── marker_genes_pval.csv
           ├── kegg_data.csv
           ├── Conlon_cancer_P1rank_genes_groups_dotplot.png
           ├── Clusters_proportion.png
           ├── Conlon_cancer_P1_Clusters.png
           ├── [cluster_id]/
           │   └── cluster_[cluster_id].csv
           └── clusters.csv

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


How to explore the results of annotion_help?
-----------------------------------------------------------------

核心输出
~~~~~~~~

- 统计主表：``marker_genes_pval.csv`` 与 ``kegg_data.csv``
  分别对应 cluster 差异 marker 结果与 KEGG 富集结果，是注释阶段的核心证据。
- 分簇子表：``<cluster_id>/cluster_<cluster_id>.csv``
  便于逐簇深读，快速提取每个 cluster 的候选 marker。
- 可视化结果：``{sample}rank_genes_groups_dotplot.png``、``Clusters_proportion.png``、``[image]_Clusters.png``
  分别用于表达模式对比、样本构成判断与空间一致性核查。
- 导出表：``<sample>_cell_clusters.csv``
  记录每个细胞/spot 与聚类标签的对应关系，可直接用于下游整理。


细节探寻
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. marker_genes_pval.csv（marker 总表）

   - 来源于 ``sc.tl.rank_genes_groups`` 与 ``sc.get.rank_genes_groups_df``。
   - 该表按显著性筛选每个 cluster 的差异基因，是细胞类型判读的一级证据。
   - **此表及其重要，其中的marker基因应作为注释的基础**

2. <cluster_id>/cluster_<cluster_id>.csv（分簇子表）

   - 脚本会按 ``group`` 自动拆分总表并逐簇落盘。
   - 这类文件适合做“单簇精读”，避免在总表中来回筛选。
   - 若单个簇出现多谱系混合 marker，通常需要回看上游聚类参数。

3. kegg_data.csv（通路富集）

   - 由 ``enrichment.R`` 基于 marker 表执行 KEGG 富集后输出。
   - 通路结果应作为 marker 证据的补充，而不是替代。
   - 若通路方向与 marker 方向冲突，建议先复核 cluster 质量再注释。

4. {sample}rank_genes_groups_dotplot.png（表达模式总览）

   - 该图展示各 cluster 的代表性 marker 表达强弱。
   - 若一个 marker 仅在目标簇集中表达，注释置信度通常更高。
   - 若多个簇共享同一批高表达 marker，提示分群可能仍偏粗。

5. Clusters_proportion.png 与 [image]_Clusters.png（构成 + 空间）

   - ``Clusters_proportion.png`` 用于查看不同样本/区域的簇占比。
   - ``[image]_Clusters.png`` 将聚类标签叠加到空间图像，检查空间连贯性。
   - 当占比关系与空间结构一致时，通常更适合进入下一步人工注释。


结果图展示（占位符）
~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: annotion_help result placeholder

   ``annotion_help`` 阶段结果示意图（占位符）。


请继续探索 :doc:`../annotation/index`。



.. note::

   core_analysis中关于空间转录组的大体分析流程已经完结了，得到的注释辅助结果已经存储在 ``clustering`` 目录下，后续请跳转 :doc:`../annotation/index` 进行人工注释或其他注释对注释信息进行探索吧！
