模块 2：调控网络（pysenic）
============================

``pysenic`` 用于从表达矩阵推断转录因子调控网络（regulon），并计算每个细胞/spot 的 regulon 活性（AUCell）
同时我们丰富了输出结果的展示 既包含经典的热图展示,又增加了气泡图,活性csv表格等,方便用户进行数据的挖掘和复现。
pysenic是一个及其耗时的过程,在这里我们使用目录中操作过的Conlon_cancer_P1的子集进行演示,若想进行对自己感兴趣的细胞类型进行分析请参考教程 :doc:`../useful_tool/splitting`。


配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。

处理逻辑概述
------------

1. 将输入对象（``.zarr`` 或 ``.h5ad``）转换为 ``.loom``。
2. 运行 ``grnboost2`` 生成候选 TF-靶基因网络（``*.grn.tsv``）。
3. 使用 motif 数据库进行 ``ctx`` 过滤，得到 regulon 集（``*.regulons.csv``）。
4. 计算 AUCell 活性并输出分组可视化与统计表。

准备输入文件
------------

``sample.txt`` 推荐格式：

.. code-block:: text

   sample_id   input_path
   S1          results/S1/annotion/S1.zarr

关键输入要求：

1. ``input_path`` 需包含可用表达矩阵与细胞注释列（用于后续按 ``celltype`` 聚合展示）。
2. 必须准备 3 个 PySCENIC 资源文件：``tfs_input``、``feather_input``、``motifs_input``。
3. 若使用人类数据，建议与官方 hg38 资源版本保持一致，避免基因 ID 不匹配导致 regulon 数量偏低。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=pysenic

运行可选的参数设置(配置文件版)
------------------------------------------------------------

先生成模板：

.. code-block:: bash

   spatialsnake produce-file --option=advance_analysis

在 ``advance_analysis.yaml`` 中，pysenic 常用参数如下：

.. list-table::
   :header-rows: 1
   :widths: 26 24 50

   * - 参数
     - 常用值
     - 作用
   * - ``runpipe``
     - ``pysenic``
     - 进入 pysenic 分支
   * - ``senic_input``
     - ``results/S1/annotion/S1.zarr``
     - 指定待分析对象路径
   * - ``tfs_input``
     - ``data/hs_hgnc_tfs.txt``
     - TF 列表文件
   * - ``feather_input``
     - ``data/hg38_...rankings.feather``
     - cisTarget ranking 数据库
   * - ``motifs_input``
     - ``data/motifs-v9-...tbl``
     - motif 注释文件
   * - ``senic_workers``
     - ``8`` 或 ``16``
     - 并行线程数，影响运行时长
   * - ``celltype_col``
     - ``celltype``
     - 分组展示 regulon 活性的标签列

结果文件结构
------------

主要结果位于 ``results/pysenic_results/``：

.. code-block:: text

   results/
   └── pysenic_results/
       ├── {sample}.loom
       ├── {sample}.grn.tsv
       ├── {sample}.regulons.csv
       ├── {sample}.aucell.loom
       ├── {sample}.auc.csv
       ├── {sample}_regulon_genes.csv
       ├── {sample}_auc_mean_by_celltype.csv
       ├── {sample}_rss.csv
       ├── {sample}_rss_top10.csv
       ├── {sample}_dotplot_regulons.png
       ├── {sample}_violin_regulons.png
       ├── {sample}_auc_heatmap.png
       ├── {sample}_rss.png
       ├── {sample}_zscore_matrix.csv
       ├── {sample}_zscore_heatmap.png
       └── {sample}_stacked_violin.png

图表与结果解释
--------------

1. ``*_auc_heatmap.png``：展示细胞类型层面的 regulon 活性全局模式，用于识别主导调控轴。
2. ``*_dotplot_regulons.png`` / ``*_violin_regulons.png``：比较不同 celltype 的 regulon 活性分布差异。
3. ``*_rss.png`` 与 ``*_rss_top10.csv``：给出各细胞类型特异 regulon，常用于定义细胞状态标志。
4. ``*_regulon_genes.csv``：记录 regulon 与靶基因关系，便于后续可复现与机制整理。
