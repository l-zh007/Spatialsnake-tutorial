模块 2：调控网络（pysenic）
============================

``pysenic`` 用于从表达矩阵推断转录因子调控网络（regulon），并计算每个细胞/spot 的 regulon 活性（AUCell）
同时我们丰富了输出结果的展示 既包含经典的热图展示,又增加了气泡图,活性csv表格等,方便用户进行数据的挖掘和复现。
pysenic是一个及其耗时的过程,在这里我们使用目录中操作过的Conlon_cancer_P1的子集进行演示,若想进行对自己感兴趣的细胞类型进行分析请参考教程 :doc:`../useful_tool/splitting`。

为了节省时间和运行内存,我们可以先切分两个占比较小的数据进行pysenic分析,切分结果保存于results/useful_results目录下
Smooth_Muscle_Cells和Endothelial_Cells:  cell 44396,gene 15450, 使用64cores参数下 耗时4h 请注意自己的内存是否足够

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotion/Colon_Cancer_P2.zarr  --split_by celltype --barcodes Smooth_Muscle_Cells,Endothelial_Cells

配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。

运行步骤与内容
--------------

1. **数据读取与格式转换**
   读取空间转录组对象（支持 ``.zarr`` 或 ``.h5ad``），并将其转换为 pySCENIC 分析流程所需的 ``.loom`` 格式，作为后续基因调控网络推断的基础输入。
2. **共表达网络推断 (GRNBoost2)**
   利用随机森林算法（GRNBoost2）基于基因表达矩阵，推断出潜在的转录因子（TF）与其靶基因之间的共表达网络，生成初始的候选模块。
3. **基序富集与模块过滤 (CisTarget)**
   加载 TF-motif 数据库，对上一步生成的候选靶基因集合进行顺式调控元件（cis-regulatory elements）的富集分析。过滤掉没有对应基序支持的基因，最终形成高置信度的转录调控单元（Regulons）。
4. **细胞级活性打分 (AUCell)**
   使用 AUCell 算法计算每个 Regulon 在单个细胞/点位（spot）中的活性得分（AUC）。该得分反映了特定转录因子在当前微环境中的相对活跃程度。
5. **多维特征计算与可视化**
   将 AUC 得分整合回原始数据对象，并进一步计算 Regulon 特异性得分（RSS）以寻找细胞类型特异性 TF。最终计算各细胞群的 Z-score，并自动生成点图、热图、小提琴图等丰富的可视化图表。

准备输入文件
------------

``sample.txt`` 推荐格式：

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

关键输入要求：

1. ``input_path`` 需包含可用表达矩阵；建议对象中保留 ``celltype`` 列，便于后续按细胞类型展示 regulon 活性。
2. 运行前必须准备 3 类官方资源：``tfs_input``（TF 列表）、``feather_input``（cisTarget rankings 数据库）、``motifs_input``（motif2tf 注释表）。
3. 三类资源必须使用同一物种和同一版本体系（推荐 v10），避免 TF 命名和基因注释不一致导致 regulon 数量异常偏低。

官方资源下载路径（人类 / 小鼠）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``tfs_input``（TF 列表）

   - Human（hg38）：
     ``https://resources.aertslab.org/cistarget/tf_lists/allTFs_hg38.txt``
   - Mouse（mm）：
     ``https://resources.aertslab.org/cistarget/tf_lists/allTFs_mm.txt``

2. ``motifs_input``（motif2tf 注释表，推荐 v10）

   - Human（HGNC）：
     ``https://resources.aertslab.org/cistarget/motif2tf/motifs-v10nr_clust-nr.hgnc-m0.001-o0.0.tbl``
   - Mouse（MGI）：
     ``https://resources.aertslab.org/cistarget/motif2tf/motifs-v10nr_clust-nr.mgi-m0.001-o0.0.tbl``

3. ``feather_input``（cisTarget rankings 数据库，推荐下载 2 个 gene-based rankings）

   - Human（hg38）：
     ``https://resources.aertslab.org/cistarget/databases/homo_sapiens/hg38/refseq_r80/mc_v10_clust/gene_based/hg38_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather``
     ``https://resources.aertslab.org/cistarget/databases/homo_sapiens/hg38/refseq_r80/mc_v10_clust/gene_based/hg38_500bp_up_100bp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather``
   - Mouse（mm10）：
     ``https://resources.aertslab.org/cistarget/databases/mus_musculus/mm10/refseq_r80/mc_v10_clust/gene_based/mm10_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather``
     ``https://resources.aertslab.org/cistarget/databases/mus_musculus/mm10/refseq_r80/mc_v10_clust/gene_based/mm10_500bp_up_100bp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather``



运行可选的参数设置
------------------------------------------------------------

先生成模板：

.. code-block:: bash

   spatialsnake produce-file --option=advance_analysis


.. code-block:: bash

   senic_input: ""    # sample.txt中写入即可
   sample_type: "Colon_Cancer_P2" #样本名称
   tfs_input: "data/hs_hgnc_tfs.txt" # 
   feather_input: "data/hg38_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather"
   motifs_input: "data/motifs-v10nr_clust-nr.hgnc-m0.001-o0.0.tbl"
   senic_workers: 64 # 注意核心数最大限制
   gene_attr: "var_names"  # 若您是根据我们的教程读取的数据默认值即可正常运行，若不是请自行查看数据中的表达矩阵基因名 和 obs中对应的细胞列名
   cell_attr: "cell_id"    # 同上



Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=pysenic --configfile advance_analysis.yaml

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

1. Regulon 活性热图（``*_auc_heatmap.png`` / ``*_zscore_heatmap.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_auc_heatmap.png
   :width: 85%
   :align: center
   :alt: pysenic auc heatmap

解释：
``*_auc_heatmap.png`` 使用 AUC 矩阵展示主要 regulon 在各细胞群的活性格局；``*_zscore_heatmap.png`` 基于按细胞群均值计算的 Z-score 矩阵排序后绘制，更适合识别“相对特异激活”的调控轴。

2. Regulon 活性点图（``*_dotplot_regulons.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_dotplot_regulons.png
   :width: 85%
   :align: center
   :alt: pysenic dotplot

解释：
以点大小表示 regulon 在细胞群中的平均活性，颜色深浅反映该活性在群体中的相对水平，适合快速比较不同细胞类型的核心调控差异。

3. 活性分布小提琴图（``*_violin_regulons.png`` / ``*_stacked_violin.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_violin_regulons.png
   :width: 85%
   :align: center
   :alt: pysenic violin regulons

解释：
``*_violin_regulons.png`` 展示前 12 个 regulon 的分布，``*_stacked_violin.png`` 展示按活性排序的前 20 个 regulon。两者用于观察细胞群内变异度、偏态分布与异质性。

4. 细胞类型特异性得分图（``*_rss.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_rss.png
   :width: 85%
   :align: center
   :alt: pysenic rss

解释：
基于 Regulon Specificity Score（RSS）绘制。每个细胞类型会输出本群体最特异的 regulon 排名，可用于定义细胞状态标志与候选关键 TF。

5. 关键结果表（``*.auc.csv`` / ``*_auc_mean_by_celltype.csv`` / ``*_zscore_matrix.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
``*.auc.csv`` 是逐细胞/spot 的 regulon 活性原始矩阵；``*_auc_mean_by_celltype.csv`` 为按细胞类型聚合后的均值矩阵；``*_zscore_matrix.csv`` 为标准化后矩阵，通常与 zscore 热图配套用于筛选特异调控轴。

6. 特异性与网络详情表（``*_rss.csv`` / ``*_rss_top10.csv`` / ``*_regulon_genes.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
``*_rss.csv`` 记录全部细胞类型的 regulon 特异性得分，``*_rss_top10.csv`` 提供每个细胞类型 Top10 regulon 摘要；``*_regulon_genes.csv`` 给出 regulon-靶基因对应关系，是机制复核和下游实验验证的核心依据表。
