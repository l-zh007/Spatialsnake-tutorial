reclustering.yaml 参数说明
==========================

该配置文件对应 ``--option=reclustering``，用于目标群体的二次细分与亚群 marker 识别。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 参数
     - 默认值
     - 作用
   * - ``option``
     - ``reclustering``
     - 固定分析阶段标识。
   * - ``results_folder``
     - ``results``
     - 结果输出根目录。
   * - ``sample_list``
     - ``sample.txt``
     - 样本清单路径。
   * - ``channel``
     - ``single_analysis``
     - 分析通道。
   * - ``run_type``
     - ``visium``
     - 平台类型。
   * - ``recluster_resolution``
     - ``0.8``
     - 二次聚类分辨率。
   * - ``recluster_n_top_genes``
     - ``2000``
     - 高变基因数量。
   * - ``recluster_neighbors``
     - ``15``
     - 邻域图近邻数。
   * - ``recluster_n_pcs``
     - ``30``
     - 重聚类 PCA 维度。
   * - ``recluster_marker_method``
     - ``wilcoxon``
     - 亚群 marker 统计方法。
   * - ``recluster_min_pct``
     - ``0.1``
     - marker 最小阳性比例阈值。
   * - ``recluster_logfc_threshold``
     - ``0.25``
     - marker 最小 logFC 阈值。

调参建议
--------

1. 先调 ``recluster_resolution`` 再调 ``recluster_n_pcs``，便于解释参数效应,再聚类因数据集较小,一般维度和聚类分辨率设置较小数值即可
2. ``recluster_min_pct`` 与 ``recluster_logfc_threshold`` 同时决定 marker 严格度。
