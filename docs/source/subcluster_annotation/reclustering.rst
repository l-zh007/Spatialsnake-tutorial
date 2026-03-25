二次聚类（reclustering）
========================

由于空间转录组需对细胞类型进行更详细的亚群注释，先前的聚类结果由于分辨率和pcs的限制，对亚群聚类效果不佳，无法探寻亚群细胞的细微分类。
因此我们提供 ``reclustering``  用于在已有聚类结果基础上执行亚群细分，适合对目标细胞群体进行更高分辨率的结构解析。


这里我们以刚刚手动注释好的Conlon_cancer_P2 进行演示
首先我们需要选择特定感兴趣的亚群,这里我们选择Tumor 癌细胞大类进行细分，以挖掘不同的癌症分群的情况

.. note::
   进行此流程前请确保您的数据已经根据感谢兴趣的细胞类型进行拆分。 若您还未进行拆分请先阅读 :doc:`../useful_tool/index` 中的 ``split`` 流程。
   或您可以使用下列命令进行拆分选择

进行拆分

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotion/Colon_Cancer_P2.zarr  --split_by celltype --barcodes Tumor

在这里我们需要将results/useful_results结果先配置sample.txt文件,内容如下

.. code-block:: bash

   samples path_to_dir
   Colon_Cancer_P2_008um results/useful_results/celltype_selected_Tumor.zarr


Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=reclustering --resolution 0.4 --pcs 15

处理逻辑概述
------------
1. 读取输入 ``.zarr``，提取第一个 table 作为重聚类对象。
2. 基于 PCA 构建邻域图并重新执行 Leiden 聚类，聚类标签写入 ``obs['recluster']``。
3. 输出重聚类 UMAP 图与空间分布图。
4. 计算并导出亚群 marker 结果（含阈值过滤）。
5. 导出亚群分配表，并写回新的 ``{sample}.zarr`` 供后续分析复用。

.. note::

   当前 ``reclustering`` 脚本仅支持 ``.zarr`` 输入路径。若您提供 ``.h5ad``，将无法通过脚本内输入检查。


运行可选的参数设置(命令行版)
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--recluster_resolution``
     - ``0.8``
     - Leiden 重聚类分辨率，控制亚群划分粒度
   * - ``--recluster_n_top_genes``
     - ``2000``
     - 重聚类高变基因数量
   * - ``--recluster_neighbors``
     - ``15``
     - 邻域图的邻居数，影响局部结构连通性
   * - ``--recluster_n_pcs``
     - ``30``
     - 邻域图使用的 PCA 维度数
   * - ``--recluster_marker_method``
     - ``wilcoxon``
     - marker 统计方法
   * - ``--recluster_min_pct``
     - ``0.1``
     - marker 最小阳性比例阈值
   * - ``--recluster_logfc_threshold``
     - ``0.25``
     - marker 最小 log2FC 阈值

以上参数均可直接通过命令行传入。若您希望快速调整亚群分辨率与 marker 严格度，可在命令后追加参数（如 ``--recluster_resolution 1.0 --recluster_logfc_threshold 0.5``）。


运行可选的参数设置(配置文件版)
------------------------------------------------------------
若您希望固定重聚类策略并保证可复现性，建议使用 yaml 管理参数。

请参考配置文件并根据下述说明进行设置 :doc:`../config_reference/reclustering_yaml`。

运行下列命令获取 yaml 模板

.. code-block:: bash

   spatialsnake produce-file --option=reclustering

模板中可统一设置 ``recluster_resolution``、``recluster_n_pcs``、``recluster_marker_method`` 等参数，适用于多轮重聚类试验的版本化管理。


运行最终运行命令吧
----------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=reclustering --resolution 0.4 --pcs 15 --configfile reclustering.yaml


结果文件结构
------------

当前示例为单样本重聚类。建议先确认 ``marker_genes.csv`` 与 ``cluster_assignments.csv`` 已生成，再解读亚群结构。

.. code-block:: text

   results/
   └── {sample}/
       └── reclustering/
           ├── {sample}.zarr/
           ├── umap_recluster.png
           ├── spatial_clusters.png
           ├── marker_genes.csv
           └── cluster_assignments.csv

其中，``{sample}.zarr`` 中包含新的 ``recluster`` 标签；``marker_genes.csv`` 与 ``cluster_assignments.csv`` 是后续亚群注释与比较分析的核心文件。



关键参数建议
------------

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - 参数类别
     - 单样本建议
     - 多样本或跨条件建议
   * - ``recluster_resolution``
     - 从 ``0.6-1.0`` 小步试探，优先保证亚群可解释性
     - 避免一次性过高，防止将样本差异误切为技术亚群
   * - ``recluster_n_pcs`` + ``recluster_neighbors``
     - 以 ``30`` + ``15`` 作为基线，按亚群稳定性微调
     - 建议固定一组参数后比较不同条件，减少结构偏移
   * - ``recluster_marker_method``
     - 首选 ``wilcoxon``，结果稳健、解释直观
     - 跨样本比较时保持同一统计方法，避免方法学偏差
   * - ``recluster_min_pct`` + ``recluster_logfc_threshold``
     - 先用默认值获得候选 marker，再按研究目标加严
     - 联合对象建议阈值策略一致，保证 marker 可横向比较



How to explore the results of reclustering?
-----------------------------------------------------------------


1. umap_recluster.png（亚群结构图）

   - 这张图用于查看亚群是否被清晰拆分。
   - 若出现大量碎裂小簇，常提示分辨率设置过高。
   - 若亚群过于混合，则可小步提高分辨率再比较稳定性。

2. spatial_clusters.png（空间亚群图）

   - 这张图用于验证亚群在组织中的空间位置是否合理。
   - 若同一亚群在空间上过于离散且无明确依据，建议回调参数重跑。
   - 若亚群在局部区域具有连续分布，通常更具解释价值。

3. marker_genes.csv（亚群 marker 总表）

   - 该表用于支持亚群命名，是二次聚类解释的核心证据之一。
   - 建议优先关注在目标亚群中稳定增强、且与已知文献一致的基因。
   - 表格应与图像结果配合解读，避免只看单一证据。

4. cluster_assignments.csv（标签映射表）

   - 该表记录每个细胞或点位对应的亚群标签。
   - 它是后续人工命名与下游比较分析的关键连接文件。
   - 建议先检查是否存在极小亚群，避免后续统计不稳定。

5. 输入要求与常见误区

   - 重聚类前应确保输入对象来源清晰、结构完整。
   - 若输入对象本身质量不稳定，亚群结果也会受到明显影响。
   - 建议先确认上游聚类可解释，再进行亚群细化。


结果图展示
~~~~~~~~~~


.. figure:: /_static/images/umap_recluster.png
   :width: 85%
   :align: center
   :alt: reclustering umap

   重聚类 UMAP 图：用于观察亚群是否分离清晰、是否存在过度碎裂。

.. figure:: /_static/images/spatial_clusters.png
   :width: 85%
   :align: center
   :alt: reclustering spatial clusters

   空间亚群图：用于判断亚群在组织中的空间连贯性与局部富集特征。

同理我们可以使用annotation中的reannotation进行二次聚类的细胞注释，步骤和之前相同可以通过marker基因进行每个聚类的细胞信息判断
请学习 :doc:`reannotation`.
