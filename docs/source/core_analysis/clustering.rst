聚类（clustering）
==================

``clustering`` 在预处理基础上执行邻域图构建、降维可视化与无监督分群，是注释与后续生物学解释的核心步骤。
聚类结果的质量直接影响后续注释与生物学解释的准确性，建议在聚类阶段以“推荐值、推荐值±5”进行并行试验，综合轮廓清晰度、空间连续性与 marker 一致性选择最终维度。

配置文件详解请见 :doc:`../config_reference/clustering_yaml`。

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
若您已经熟练掌握 Spatialsnake, 且对空间转录组参数设置有一定的了解, 或您想了解更多参数设置, 请参考 [yaml解释]。

运行下列命令进行yaml文件获取

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
   └── {sample}_{bin}um/
       └── clustering/
           ├── {sample}.zarr/
           ├── {sample}UMAP.png
           ├── {sample}Cell_Distribution_Across_Clusters.png
           └── {sample}tsene.png

其中，``{sample}.zarr``（或多样本场景下 ``concatenated_sdata``）包含 ``obs['clusters']`` 聚类标签，是 ``annotion_help`` 的直接输入。若 ``tsene=False``，则不会生成 ``tsene`` 图。


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



结果解读
----------------

本节建议按“结果展示 → 结构解释 → 参数回调建议”的顺序判断聚类质量。若为多样本联合对象，请重点关注聚类是否被 ``group`` 主导，避免将技术差异误判为生物学亚群。

1. UMAP 聚类图（``{sample}UMAP.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/core_analysis/clustering/UMAP.png]

解释：
理想情况下，簇间边界清晰且簇内连续性良好；若出现过度碎片化，通常提示分辨率偏高或 PCs 偏多；若仅呈现少数大团块，可能分辨率偏低或局部结构被过度平滑。

建议：
优先以 preprocess 推荐 PCs 作为基线，并在 clustering 阶段测试“推荐值、推荐值±5”；同时联动 ``resolution`` 小范围调整，观察簇稳定性与可解释性变化。

2. 样本-簇分布图（``{sample}Cell_Distribution_Across_Clusters.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/core_analysis/clustering/Cell_Distribution_Across_Clusters.png]

解释：
该图用于评估各样本（或 region）在不同簇中的分布均衡性。若某些簇几乎完全由单一样本占据，需结合组织背景与批次信息判断该簇是生物学特异群体，还是潜在技术偏移。

建议：
多样本联合分析时，若样本偏倚过强，可回到 preprocess 阶段检查 ``batch_method``，并在 clustering 中同步调整 ``pcs`` 与 ``NEIGHBORS``，再比较分布改善情况。

3. tSNE 图（``{sample}tsene.png``，当 ``tsene=True`` 时）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/core_analysis/clustering/tsene.png]

解释：
tSNE 可作为 UMAP 的补充视角，用于观察局部邻域关系是否一致。若 UMAP 与 tSNE 在主要簇结构上趋势一致，通常提示聚类结果较稳健。

建议：
tSNE 建议用于结果复核而非单一决策依据；最终仍应以簇 marker 一致性、空间位置连续性与生物学可解释性综合定稿。

4. 聚类对象与下游衔接（``{sample}.zarr`` / ``concatenated_sdata``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
聚类完成后，簇标签写入对象 ``obs['clusters']``，该标签将直接用于 ``annotion_help`` 的 marker 筛选与富集分析。

建议：
进入注释前建议完成三项检查：簇数量与研究目标匹配、主要簇具备清晰 marker 候选、跨样本分布无明显技术主导。若不满足，优先回调 ``resolution`` 与 ``pcs`` 后重跑聚类。
