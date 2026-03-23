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
   这里我们继续使用上一步骤输出的preprocess/Colon_Cancer_P2.zarr数据进行聚类分析
   若您的数据并非Visium HD平台或为多样本整合数据 请阅读完后查看文末,学习不同平台和样本数量下的输入与输出的差异。


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

可直接在命令后追加参数（如 ``--resolution 1.0 --pcs 30``），参数间以空格分隔,对于示例数据我们参照原论文进行聚类 尝试以0.8为resolution,20为pcs来进行聚类分析
一般想要获得更精细的分群结果,可以尝试增加resolution 和 pcs的数值,但同时也需要注意,增加这两个参数的值会增加计算时间,且可能会导致分群结果的不稳定性。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --resolution 0.8 --pcs 20



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
   spatialsnake single_analysis sample.txt visium_HD --option=clustering -resolution 0.8 --pcs 20 --configfile clustering.yaml


结果文件结构
------------

当前示例为 ``visium_HD`` 单样本聚类。建议先确认聚类后对象可正常读取，再结合 UMAP/tSNE 与样本-簇分布图综合判断分群是否合理。

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── clustering/
           ├── Colon_Cancer_P2.zarr/
           ├── Colon_Cancer_P2UMAP.png
           └── Colon_Cancer_P2Cell_Distribution_Across_Clusters.png

其中，``{sample}.zarr``（或多样本场景下 ``concatenated_sdata``）包含 ``obs['clusters']`` 聚类标签，是 ``annotion_help`` 的直接输入。若 ``tsene=False``，则不会生成 ``tsene`` 图。


多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------

若您使用的数据非Visium_HD平台,请将visium_HD更改为您所使用的平台数据字段即可。
.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=clustering --resolution 0.8 --pcs 20

若您使用的数据为整合样本,请将channel改为compare_analysis 整合分析,同时sample.txt文件需符合前文教程中的格式路径
.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=clustering --resolution 0.8 --pcs 20

同理在末尾你也可以进行命令行型参数设置或者在yaml文件中进行参数设置,步骤和我们的演示数据一致。


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

我们得到了umap图,建议先看簇边界,再看簇内连续性与整体结构是否自然,完美的umap聚类图应该是簇边界清晰,簇内连续性好,整体结构自然,这证明分群结果是合理的。

.. figure:: /_static/images/Colon_Cancer_P2UMAP.png
   :width: 85%
   :align: center
   :alt: clustering umap


核心输出
~~~~~~~~

- 主对象：``results/{sample}_{bin}um/clustering/{sample}.zarr``
  该对象新增了 ``obs['clusters']``，是 ``annotion_help`` 的直接输入。
- 可视化图：{sample}UMAP.png、{sample}Cell_Distribution_Across_Clusters.png、{sample}tsene.png（可选）
  用于快速判断聚类结构是否清晰、是否存在样本偏倚。


其他结果
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2. {sample}Cell_Distribution_Across_Clusters.png（样本-簇分布图）

   - 这张图用于看每个簇在不同样本中的分布是否均衡。
   - 若某簇几乎只出现在单一样本，需进一步判断是生物学特异性还是技术偏差。
   - 多样本场景建议与预处理结果一起综合判断。

3. {sample}tsene.png（可选复核图）

   - 这张图用于辅助复核 UMAP 的结论。
   - 若两者总体趋势一致，通常可增强对分群稳定性的信心。
   - 若差异明显，建议回到聚类参数做小步调整。


后续我们可以进行cluster信息的挖掘分析 :doc:`annotation_help`。
