Clustering
==========

Based on the preprocessed object, ``clustering`` builds the neighbor graph, generates low-dimensional visualizations, and performs unsupervised clustering. This is a central step for annotation and downstream biological interpretation.
Because clustering quality directly affects annotation quality, we recommend testing the suggested number of PCs together with nearby values, such as the recommended value and ``recommended ± 5``, and choosing the final setting based on boundary clarity, spatial continuity, and marker consistency.


Workflow overview
-----------------
1. Read the filtered object generated in ``preprocess`` and construct the neighbor graph.
2. Represent the structure of the sample or integrated object in a low-dimensional embedding such as UMAP or tSNE.
3. Run clustering with the selected algorithm and write the labels back to the object.
4. Export visualization results and cluster labels for use in ``annotation_help``.

.. note::
   In this tutorial, we continue from the object generated in the previous ``preprocess`` step.
   If your data are not from the Visium HD platform, or if you are analyzing integrated multi-sample data, 阅读接下来的运行步骤,根据之前教程的命令行使用介绍将重要参数替换即可.


step 1: sample.txt 配置文件
-----------------------

直接使用您integrate步骤使用的sample.txt配置文件即可,无需进行更改.

.. code-block:: text
  
   sample_id input_path
   sample_id data/sample_id

step 2: 参数选择与配置
---------------

此步骤我们包含了许多重要参数,请根据您的需求进行调整,以下是部分参数及其功能的展示:

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--cluster_algorithm``
     - ``leiden``
     - Clustering algorithm; supported values include ``leiden``, ``louvain``, and ``Kmeans``
   * - ``--resolution``
     - ``0.8``
     - Community detection granularity for ``leiden`` or ``louvain``, controlling clustering resolution
   * - ``--n_clusters``
     - ``15``
     - Number of clusters used only for ``Kmeans``
   * - ``--pcs``
     - ``25``
     - Number of PCA dimensions used for clustering; adjust according to dataset size and computational resources, or use the value suggested in ``preprocess``
   * - ``--tsene``
     - ``False``
     - Whether to generate an additional tSNE visualization

配置建议:
   1.对于所有情况: 我们建议您根据 ``preprocess`` 步骤中的pca_variance_ratio以及终端中的recommend pcs的输出进行 ``pcs``的调整,我们的推荐值为 ``20``,仅供参考.同时根据研究的目的 选择聚类的resolution,建议选择 ``0.8`` 作为默认值,既不会过拟合也不会欠拟合.
   
   2.clustering模块主要进行聚类与降维操作,为了适应准确的分析需求,我们提供了不同的聚类算法,包括 ``leiden``，``louvain``，``Kmeans``.降维算法则包括 ``UMAP``，``tSNE``.您可以通过 ``--cluster_algorithm`` 进行聚类算法的选择,默认值为 ``leiden``.也可以通过 ``--tsene`` 进行降维可视化算法的选择,默认umap必须进行tsene False.
   
   3.若您在上一preprocess步骤选择了使用sketch,则建议您在后续clustering步骤继续使用 --sketch True 保持一致的下采样策略将聚类信息映射为所有spot/cell.


参数配置方法:
   1.The parameters listed above are commonly used settings that can be passed directly on the command line. 
   If you are comfortable tuning spatial transcriptomics workflows, you can append them to the command as needed, for example ``--resolution 0.8``.

   2.Optional parameters through a configuration file.正如我们在教程Usage中所介绍的一样,我们可以通过修改yaml文件中的参数配置信息进行所有参数的自定义修改后再进行使用.用以下命令获取该步骤的yaml文件并修改.

.. code-block:: bash

   spatialsnake produce-file --option=clustering

After editing the configuration file, provide it on the command line with ``--configfile``.

step 3: 命令运行
------------

通过之前教程的基本命令行介绍,详细您已经熟悉对于Spatialsnake的重要参数设置逻辑,这里我们只介绍预处理命令的运行,若您为多样本整合/其他平台数据,直接修改相关参数即可.
别忘了将你选择的参数都修改为对应的值或加入到命令行末尾.
For the example dataset, we use ``--resolution 0.8 --pcs 20`` for single_analysis or visium_HD. This filters out spots or cells with fewer than 100 UMIs, fewer than 100 detected genes, or more than 30% mitochondrial signal.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --resolution=0.8 --pcs=20

Run with a YAML file. 请不要忘记保存你编辑后的yaml文件. 同时无需手动设置参数,若设置则会覆盖yaml文件中的值.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --configfile=clustering.yaml


Demo for Clustering with visium_HD
----------------------------------

我们将使用上一步摄取的Colon_Cancer_P2_008um数据进行预处理演示.
sample.txt可沿用之前的分析流程以固定core_analysis分析同一样本。

.. code-block:: text
  
   sample_id input_path bin
   Colon_Cancer_P2 data/Colon_Cancer_P2 8

我们选取常规的参数 ``--resolution 0.8 --pcs 20`` 作为聚类参数以挖掘样本中的细胞类型.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --resolution=0.8 --pcs=20

若您想进行yaml文件配置进行更丰富的参数设置
-----------------------

.. code-block:: bash
   # 获取yaml文件并编辑
   spatialsnake produce-file --option=clustering

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --configfile=clustering.yaml

Result file structure
---------------------

This example shows single-sample clustering for ``visium_HD``. After the run completes, first confirm that the clustered object can be loaded correctly, then judge whether the clustering is reasonable by combining the UMAP or tSNE view with the sample-by-cluster distribution plot.

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── clustering/
           ├── Colon_Cancer_P2.zarr/
           ├── Colon_Cancer_P2UMAP.png
           └── Colon_Cancer_P2Cell_Distribution_Across_Clusters.png

The output object ``{sample}.zarr`` (or ``concatenated_sdata`` in a multi-sample setting) contains the cluster labels in ``obs['clusters']`` and serves as the direct input for ``annotation_help``. If ``tsene=False``, the tSNE plot is not generated.



Input and output structure
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Analysis mode
     - Input
     - Output
   * - single_analysis (standard ``zarr`` mode)
     - ``sample.txt`` should contain at least ``sample_id input_path``; the input object is ``results/{sample}/preprocess/filter_{sample}.zarr``
     - ``results/{sample}/clustering/{sample}.zarr``
   * - single_analysis (``visium_HD``)
     - ``sample.txt`` should contain at least ``sample_id input_path bin``; the input object is ``results/{sample}_{bin}um/preprocess/filter_{sample}.zarr``
     - ``results/{sample}_{bin}um/clustering/{sample}.zarr``
   * - compare_analysis
     - ``sample.txt`` should contain at least ``sample_id input_path group``; for ``visium_HD``, an additional ``bin`` column is required. The input object is ``results/merge_data/preprocess/filter_concatenated_sdata``
     - ``results/merge_data/clustering/concatenated_sdata``


How to inspect the clustering results
-------------------------------------

The UMAP plot is usually the first figure to inspect. Start by checking cluster boundaries, then evaluate whether the internal structure of each cluster is continuous and whether the global layout looks biologically plausible. A good clustering result typically shows clear boundaries, coherent within-cluster structure, and a natural overall organization.

.. figure:: /_static/images/umap.png
   :width: 85%
   :align: center
   :alt: clustering umap plot


Key outputs
~~~~~~~~~~~

- Main object: ``results/{sample}_{bin}um/clustering/{sample}.zarr``
  This object now contains ``obs['clusters']`` and is the direct input for ``annotation_help``.
- Visualization files: ``{sample}UMAP.png``, ``{sample}Cell_Distribution_Across_Clusters.png``, and ``{sample}tsene.png`` (optional)
  These plots are used to judge whether the clustering structure is clear and whether sample-specific bias is present.


Other outputs
~~~~~~~~~~~~~

1. ``{sample}Cell_Distribution_Across_Clusters.png`` (sample-by-cluster distribution)

   - This plot shows whether each cluster is distributed evenly across samples.
   - If a cluster appears almost exclusively in one sample, determine whether this reflects biology or technical bias.
   - In multi-sample analyses, interpret this figure together with the preprocessing results.

2. ``{sample}tsene.png`` (tSNE embedding)

   - This plot serves as a secondary check on the conclusions suggested by the UMAP plot.
   - If the overall pattern agrees with UMAP, confidence in clustering stability is usually higher.
   - If the two views differ strongly, revisit the clustering parameters and adjust them gradually.


Next, continue to :doc:`annotation_help`.
