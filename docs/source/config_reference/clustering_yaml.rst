clustering.yaml 参数说明
========================

该配置文件对应 ``--option=clustering``，用于低维嵌入、邻域构图与聚类分群。

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - 参数
     - 默认值
     - 作用
   * - ``option``
     - ``clustering``
     - 固定分析阶段标识。
   * - ``results_folder``
     - ``results``
     - 结果输出根目录。
   * - ``data_fold``
     - ``data``
     - 原始数据根目录。
   * - ``sample_list``
     - ``sample.txt``
     - 样本清单路径。
   * - ``run_type``
     - ``visium``
     - 平台类型。
   * - ``channel``
     - ``compare_analysis``
     - 分析通道。
   * - ``tsene``
     - ``False``
     - 是否额外输出 tSNE。
   * - ``MIN_DIST``
     - ``0.3``
     - UMAP 最小距离参数。
   * - ``SPREAD``
     - ``2``
     - UMAP spread 参数。
   * - ``cluster_algorithm``
     - ``leiden``
     - 聚类算法选择。
   * - ``resolution``
     - ``0.5``
     - Leiden/Louvain 分辨率。
   * - ``n_clusters``
     - ``15``
     - KMeans 的簇数。
   * - ``n_comps``
     - ``20``
     - 降维主成分数。
   * - ``k_geom``
     - ``15``
     - BANKSY 几何邻居参数。
   * - ``max_m``
     - ``1``
     - BANKSY 邻域阶数。
   * - ``nbr_weight_decay``
     - ``scaled_gaussian``
     - 邻域权重衰减策略。
   * - ``lambda_list``
     - ``0.2``
     - 空间增强权重。
   * - ``sketch``
     - ``False``
     - 是否使用抽样对象进行聚类标签传播。
   * - ``pcs``
     - ``25``
     - 聚类主成分维度。
   * - ``NEIGHBORS``
     - ``10``
     - 邻域图近邻数。

调参建议
--------

1. 常规流程先固定 ``cluster_algorithm=leiden``，再调 ``resolution`` 与 ``pcs``。
2. 关注空间连续性时可结合 ``k_geom``、``lambda_list`` 进行空间增强试验。
3. 若 preprocess 已开启 ``sketch``，该阶段应同步开启 ``sketch``。
