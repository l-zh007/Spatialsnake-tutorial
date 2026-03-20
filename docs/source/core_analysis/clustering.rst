聚类（clustering）
==================

``clustering`` 在预处理基础上执行邻域图构建、降维可视化与无监督分群，是注释与后续生物学解释的核心步骤。
聚类结果的质量直接影响后续注释与生物学解释的准确性，建议在聚类阶段以“推荐值、推荐值±5”进行并行试验，综合轮廓清晰度、空间连续性与 marker 一致性选择最终维度。


处理逻辑概述
------------
1. 读取预处理后的过滤对象并构建邻域图。
2. 在低维空间（如 UMAP/tSNE）进行样本内或联合对象的结构表示。
3. 按设定算法执行聚类并写回对象。
4. 输出可视化结果与聚类标签，供 ``annotion_help`` 使用。

.. note::

   若您的数据并非Visium HD平台或为多样本整合数据 请阅读完后查看文末,学习不同平台和样本数量下的输入与输出的差异。


Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=clustering
   spatialsnake compare_analysis sample.txt visium --option=clustering

运行可选的参数设置(命令行版)
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--cluster_algorithm``
     - ``leiden``
     - 聚类算法，可选 ``leiden`` / ``louvain`` / ``Kmeans``
   * - ``--resolution``
     - ``0.8``
     - 社区发现粒度（对 ``leiden`` / ``louvain`` 生效），控制分群粗细
   * - ``--n_clusters``
     - ``15``
     - 仅 ``Kmeans`` 生效，指定聚类簇数量
   * - ``--pcs``
     - ``25``
     - 聚类时使用的 PCA 维度数，您可根据数据维度和计算资源调整，默认值为25，也可以参考preprocess步骤输出的推荐pcs数量
   * - ``--tsene``
     - ``False``
     - 是否额外输出 tSNE 可视化结果

以上命令为常用参数组合。若您希望精细调参，可直接在命令后追加参数（如 ``--resolution 1.0 --pcs 30``），参数间以空格分隔。


运行可选的参数设置(配置文件版)
------------------------------------------------------------
若您已经熟练掌握 Spatialsnake, 且对空间转录组参数设置有一定的了解, 或您想了解更多参数设置

请参考配置文件并根据下述说明进行设置 :doc:`../config_reference/clustering_yaml`。

配置完成后在命令行使用configfile加入配置文件路径

获取配置文件命令
----------------------------

.. code-block:: bash

   spatialsnake produce-file --option=clustering

在yaml文件中,您可以根据自己的需求进行参数设置,每个文件注释都有详细的说明,请根据自己的需求进行修改，或更方便的，您可在文档中查看 【yaml解释】。

运行最终运行命令吧
----------------------------

.. code-block:: bash

   # 确保您的yaml文件与sample.txt在当前同一工作目录下
   spatialsnake single_analysis sample.txt visium_HD --option=clustering --configfile clustering.yaml


结果文件结构
------------

当前示例为 ``visium_HD`` 单样本聚类。建议先确认聚类后对象可正常读取，再结合 UMAP/tSNE 与样本-簇分布图综合判断分群是否合理。

.. code-block:: text

   results/
   └── Conlon_cancer_P1_008um/
       └── clustering/
           ├── Conlon_cancer_P1.zarr/
           ├── Conlon_cancer_P1UMAP.png
           ├── Conlon_cancer_P1Cell_Distribution_Across_Clusters.png

其中，``{sample}.zarr``（或多样本场景下 ``concatenated_sdata``）包含 ``obs['clusters']`` 聚类标签，是 ``annotion_help`` 的直接输入。若 ``tsene=False``，则不会生成 ``tsene`` 图。


多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------
在特定位置根据自身数据平台和样本数量更换不同的命令参数即可，其他基本不变

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - 场景
     - 推荐命令
   * - 单样本（Visium HD，本节演示）
     - ``spatialsnake single_analysis sample.txt visium_HD --option=clustering``
   * - 单样本（常规 zarr 平台：visium / xenium / visium_segment）
     - ``spatialsnake single_analysis sample.txt visium --option=clustering``
   * - 多样本联合聚类
     - ``spatialsnake compare_analysis sample.txt visium --option=clustering``


关键参数建议
------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - sketch（yaml）
     - ``False``
     - 若之前的preprocess步骤开启了sketch，必须开启此参数，进行聚类标签传播，否则会报错!!!!!!!!!!!!!!


输入输出结构的差异
------------------
.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 分析模式
     - 输入
     - 输出
   * - single_analysis（常规 zarr 类型）
     - ``sample.txt`` 至少包含 ``sample_id input_path``；输入对象为 ``results/{sample}/preprocess/filter_{sample}.zarr``
     - ``results/{sample}/clustering/{sample}.zarr``
   * - single_analysis（visium_HD）
     - ``sample.txt`` 至少包含 ``sample_id input_path bin``；输入对象为 ``results/{sample}_{bin}um/preprocess/filter_{sample}.zarr``
     - ``results/{sample}_{bin}um/clustering/{sample}.zarr``
   * - compare_analysis
     - ``sample.txt`` 至少包含 ``sample_id input_path group``（visium_HD 需额外 ``bin``）；输入对象为 ``results/merge_data/preprocess/filter_concatenated_sdata``
     - ``results/merge_data/clustering/concatenated_sdata``



How to explore the results of clustering?
---------------------------------------------------------------

核心输出
~~~~~~~~

- 主对象：``results/{sample}_{bin}um/clustering/{sample}.zarr``
  该对象新增了 ``obs['clusters']``，是 ``annotion_help`` 的直接输入。
- 可视化图：{sample}UMAP.png、{sample}Cell_Distribution_Across_Clusters.png、{sample}tsene.png（可选）
  用于快速判断聚类结构是否清晰、是否存在样本偏倚。


细节探寻
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. {sample}UMAP.png（主结构图）

   - 脚本同时绘制 ``total_counts``、``n_genes_by_counts`` 与 ``clusters`` 三个视角。
   - 若 cluster 面板边界清晰、簇内连续，通常说明分群结构较稳定。
   - 若出现大量碎片簇，常见于 ``resolution`` 偏高或 ``pcs`` 过大。

2. {sample}Cell_Distribution_Across_Clusters.png（样本-簇分布图）

   - 该图来自 ``region × clusters`` 的交叉统计热图。
   - 若某些簇几乎被单一样本占据，需要区分“真实生物学特异性”与“技术偏移”。
   - 多样本分析时，建议结合 ``preprocess`` 的批次处理策略一起判断。

3. {sample}tsene.png（可选复核图）

   - 仅在 ``tsene=True`` 时生成。
   - 若 tSNE 与 UMAP 的主要簇结构趋势一致，通常可增强对聚类稳健性的信心。
   - 若两者差异明显，建议回到 ``pcs``、``NEIGHBORS`` 与 ``resolution`` 做小步调参。

4. obs['clusters']（关键标签字段）

   - 脚本把聚类标签写入对象观测表，字段名固定为 ``clusters``。
   - 后续 ``annotion_help`` 的 marker 统计与富集分析都依赖此字段。
   - 在进入下一步前，请先确认主要簇具备可解释的生物学候选 marker。

5. sketch=True 场景的特别提示

   - 若预处理阶段使用了 ``sketch``，聚类会读取 ``sketch.h5ad`` 并进行标签传播。
   - 此时更建议用样本-簇分布图检查是否出现传播偏倚。
   - 若异常，优先复核抽样比例与聚类主参数，而不是直接进入注释。


结果图展示（占位符）
~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: clustering result placeholder

   ``clustering`` 阶段结果示意图（占位符）。


请继续探索 :doc:`annotation_help`。
