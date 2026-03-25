注释辅助（annotion_help）
=========================

``annotion_help`` 在聚类结果基础上执行 marker 基因统计与富集分析 和 空间聚类可视化输出，用于为后续 ``annotion`` 提供可解释的生物学证据。
在单样本场景中，该步骤用于确定各 cluster 的候选细胞类型；在多样本联合场景中，还需要评估 marker 与通路结果是否受样本构成影响。

该部分包含python 和 R 两部分工具,若还未配置R环境请使用命令

.. code-block:: bash

   spatialsnake install-packages

处理逻辑概述
------------
1. 读取 ``clustering`` 阶段输出对象与 ``clusters`` 标签。
2. 按 cluster 计算差异 marker 基因并导出总表与分簇子表。
3. 绘制 marker dotplot、样本-簇比例图与空间叠加图。
4. 基于 marker 基因执行 KEGG 富集分析并输出通路结果。
5. 将注释辅助结果统一写入 ``clustering`` 目录，供 ``annotion`` 直接调用。

.. note::

   若您的数据并非Visium HD平台或为多样本整合数据，请阅读完后查看文末，学习不同平台和样本数量下的输入与输出差异。


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


Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotion_help



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
我们的分析结果将会对每个聚类都生成一个子目录，包含该聚类的差异 marker 基因表、KEGG 富集分析结果、空间可视化图等,以方便用户探寻每个细胞类型的差异特征。

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── clustering/
           ├── marker_genes_pval.csv
           ├── kegg_data.csv
           ├── Colon_Cancer_P2rank_genes_groups_dotplot.png
           ├── Clusters_proportion.png
           ├── Colon_Cancer_P2_hires_image_cluster.png
           ├── [cluster_id]/
           │   └── cluster_[cluster_id].csv
           └── clusters.csv

.. note::

   core_analysis中关于空间转录组的大体分析流程已经完结了，得到的注释辅助结果已经存储在 ``clustering`` 目录下，后续请跳转 :doc:`../annotation/index` 进行人工注释或其他注释对注释信息进行探索吧！




多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------

若您使用的数据非Visium_HD平台,请将visium_HD更改为您所使用的平台数据字段即可。
.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion_help

若您使用的数据为整合样本,请将channel改为compare_analysis 整合分析,同时sample.txt文件需符合前文教程中的格式路径
.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotion_help

同理在末尾你也可以进行命令行型参数设置或者在yaml文件中进行参数设置,步骤和我们的演示数据一致。


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

这里我们得到了聚类的空间映射图，用于可视化每个簇在组织中的分布
我们将子图设置为原始H&E染色图像和映射后的细胞聚类图像,若您有染色图像分析经验即可挖掘其中的生物学信息

.. figure:: /_static/images/Colon_Cancer_P2_hires_image_cluster.png
   :width: 85%
   :align: center
   :alt: annotation help spatial clusters

marker dotplot：用于查看不同簇的代表性基因表达强弱与特异性,后续可以结合csv文件来确定每个cluster的具体marker进行注释

.. figure:: /_static/images/Colon_Cancer_P2rank_genes_groups_dotplot.png
   :width: 85%
   :align: center
   :alt: annotation help marker dotplot



同时我们在每个聚类的目录下也得到了差异 marker 基因表与 GO/KEGG 富集分析结果 以柱状体和桑基图展示各个cluster的高富集通路。

.. figure:: /_static/images/kegg_cluster.png
   :width: 85%
   :align: center
   :alt: annotation help remaining plots placeholder

.. figure:: /_static/images/GO_cluster.png
   :width: 85%
   :align: center
   :alt: annotation help remaining plots placeholder



其他结果
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. marker_genes_pval.csv（marker 总表）

   - 这是注释阶段最核心的证据表，用于判断每个簇最有代表性的基因特征。
   - 判读时建议优先关注“稳定出现、与已知细胞特征一致”的基因组合。
   - 这张表通常作为命名细胞类型的基础依据。

2. <cluster_id>/cluster_<cluster_id>.csv（分簇子表）

   - 该文件把每个簇单独拆开，便于逐簇精读。
   - 对单簇进行细读时，更容易发现是否存在混合特征。
   - 若一个簇同时呈现多类信号，通常要回看上游聚类是否过粗。

3. kegg_data.csv（通路富集）

   - 该表用于补充说明每个簇可能关联的生物过程。
   - 通路结果应与 marker 一起看，而不是单独作为注释结论。
   - 若两者明显冲突，建议先复核聚类质量再命名。

4. {sample}rank_genes_groups_dotplot.png（表达模式总览）

   - 该图用于快速查看“哪些基因在哪些簇更强”。
   - 若某些基因只在目标簇明显增强，注释置信度通常更高。
   - 若多个簇共享相似高表达模式，常提示还可进一步细分。

5. Clusters_proportion.png 与 [image]_Clusters.png（构成 + 空间）

   - 簇占比图用于查看不同样本或区域中的组成差异。
   - 空间叠加图用于验证簇在组织中的位置是否连贯、是否符合组织结构。
   - 当“组成差异”和“空间分布”两者一致时，更适合进入人工注释。


请继续探索 :doc:`../annotation/index`。



.. note::

   core_analysis中关于空间转录组的大体分析流程已经完结了,得到的注释辅助结果已经存储在 ``clustering`` 目录下,
   在此步骤完成后我们通常先通过输出结果的每个cluster的差异基因和富集结果进行探索,根据其表达信息研究其具体的细胞类型,用户可以通过cellmarker 或panglaoDB进行查询.
   后续请跳转 :doc:`../annotation/index` 进行人工注释或其他注释对注释信息进行探索吧！
