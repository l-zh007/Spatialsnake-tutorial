二次聚类（reclustering）
========================

由于空间转录组需对细胞类型进行更详细的亚群注释，先前的聚类结果由于分辨率和pcs的限制，对亚群聚类效果不佳，无法探寻亚群细胞的细微分类。
因此我们提供 ``reclustering``  用于在已有聚类结果基础上执行亚群细分，适合对目标细胞群体进行更高分辨率的结构解析。
与 ``preprocess`` 或 ``clustering`` 不同，该步骤不读取原始平台目录，而是直接读取上游分析对象路径，通常为经过useful_tool处理后的 ``.zarr`` 文件。


.. note::

   进行此流程前请确保您的数据已经根据感谢兴趣的细胞类型进行拆分。 若您还未进行拆分请先阅读 :doc:`../useful_tool/index` 中的 ``split`` 流程。

输入与输出
----------
该步骤的输入来自 ``sample.txt`` 第二列给出的下游对象路径，核心前提是输入对象可被 ``spatialdata.read_zarr`` 正常读取。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 分析模式
     - 输入
     - 输出
   * - single_analysis（推荐）
     - ``sample.txt`` 至少包含 ``sample_id input_path``；``input_path`` 建议指向 ``results/{sample}/clustering/{sample}.zarr`` 或 ``results/{sample}/annotion/{sample}.zarr``
     - ``results/{sample}/reclustering/`` 下输出 ``{sample}.zarr``、``umap_recluster.png``、``spatial_clusters.png``、``marker_genes.csv``、``cluster_assignments.csv``
   * - compare_analysis（可运行但需谨慎）
     - ``sample.txt`` 至少包含 ``sample_id input_path group``；当前实现仅读取第一条输入路径进行重聚类
     - 输出仍落在 ``results/{sample}/reclustering/``，其中 ``sample`` 为 ``sample.txt`` 第一列样本名

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=reclustering
   spatialsnake compare_analysis sample.txt visium --option=reclustering

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

   spatialsnake single_analysis sample.txt visium --option=reclustering --configfile reclustering.yaml


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


多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - 场景
     - 推荐命令
   * - 单样本重聚类（推荐）
     - ``spatialsnake single_analysis sample.txt visium --option=reclustering``
   * - 多样本通道下重聚类
     - ``spatialsnake compare_analysis sample.txt visium --option=reclustering``

尽管命令层面可写入不同 ``run_type``，``reclustering`` 实际读取的是 ``sample.txt`` 中提供的下游对象路径，不直接依赖原始平台目录结构。


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


输入输出结构的差异
------------------
重聚类阶段使用下游对象路径作为输入，因此 ``sample.txt`` 的第二列应填写待重聚类对象位置，而非原始测序数据目录。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 分析模式
     - 输入
     - 输出
   * - single_analysis
     - ``sample.txt`` 至少包含 ``sample_id input_path``；``input_path`` 推荐为 ``results/{sample}/clustering/{sample}.zarr`` 或 ``results/{sample}/annotion/{sample}.zarr``
     - ``results/{sample}/reclustering/{sample}.zarr`` 与 ``results/{sample}/reclustering/marker_genes.csv``
   * - compare_analysis
     - ``sample.txt`` 至少包含 ``sample_id input_path group``；当前实现仅使用第一条 ``input_path`` 执行重聚类
     - ``results/{sample}/reclustering/{sample}.zarr`` 与 ``results/{sample}/reclustering/marker_genes.csv``


How to explore the results of reclustering?
-----------------------------------------------------------------

核心输出
~~~~~~~~

- 主对象：``results/{sample}/reclustering/{sample}.zarr``
  新增 ``obs['recluster']`` 标签，表示亚群划分结果。
- 图像结果：``umap_recluster.png`` 与 ``spatial_clusters.png``
  分别对应低维结构视角与空间分布视角。
- 表格结果：``marker_genes.csv`` 与 ``cluster_assignments.csv``
  分别用于亚群命名证据与细胞标签映射。


细节探寻
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. umap_recluster.png（亚群结构图）

   - 来源于重聚类后的 ``recluster`` 标签可视化。
   - 若出现大量碎裂小簇，常见于 ``recluster_resolution`` 偏高。
   - 若分群过粗，可在保证稳定性的前提下小步提高分辨率。

2. spatial_clusters.png（空间亚群图）

   - 脚本优先尝试在空间图像上渲染亚群；若失败会回退到坐标散点绘制。
   - 该图用于验证亚群是否具有空间连续性与组织学合理性。
   - 若同一亚群在空间上高度离散且无生物学依据，建议回调参数重跑。

3. marker_genes.csv（亚群 marker 总表）

   - 基于 ``rank_genes_groups`` 生成，并按 ``min_pct``、``logfc_threshold`` 做阈值筛选。
   - 常见字段包括 ``gene``、``p_val``、``avg_log2FC``、``pct_nz_group`` 等。
   - 读表时可优先关注“显著性 + 效应量 + 文献一致性”三者同时满足的基因。

4. cluster_assignments.csv（标签映射表）

   - 由导出函数生成后重命名，记录每个细胞/spot 对应的 ``recluster`` 标签。
   - 该文件是后续手动注释、分组比较与可复现记录的关键入口。
   - 在进入下一步前，建议先检查是否存在极小簇导致统计不稳定。

5. 输入要求与常见误区

   - 脚本输入必须是 ``.zarr`` 路径，若传入 ``.h5ad`` 会直接报错。
   - 当前流程读取输入对象中的第一个 table 执行重聚类。
   - 因此建议先确保上游对象结构清晰，再开始亚群精细化分析。


结果图展示（占位符）
~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: reclustering result placeholder

   ``reclustering`` 阶段结果示意图（占位符）。
