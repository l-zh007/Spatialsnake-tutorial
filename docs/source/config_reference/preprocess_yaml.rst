preprocess.yaml 参数说明
========================

该配置文件对应 ``--option=preprocess``，用于质量控制、过滤、标准化与降维前处理。

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - 参数
     - 默认值
     - 作用
   * - ``option``
     - ``preprocess``
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
     - 空间平台类型。
   * - ``channel``
     - ``compare_analysis``
     - 单样本或联合分析模式。
   * - ``seg_filter``
     - ``False``
     - 是否启用样本级差异过滤阈值。
   * - ``filter_list``
     - ``False``
     - 自定义阈值文件路径。
   * - ``min_genes``
     - ``3``
     - spot/cell 最小基因数阈值。
   * - ``min_cells``
     - ``3``
     - 基因最小出现细胞数阈值。
   * - ``mt_threshold``
     - ``80.0``
     - 线粒体比例过滤上限。
   * - ``variable``
     - ``False``
     - 是否执行高变基因筛选。
   * - ``NEIGHBORS``
     - ``10``
     - 邻域图近邻数。
   * - ``batch_method``
     - ``harmony``
     - 多样本批次校正算法。
   * - ``n_top_genes``
     - ``3000``
     - 高变基因数量。
   * - ``n_comps``
     - ``50``
     - PCA 主成分数量。
   * - ``sketch``
     - ``False``
     - 是否启用大规模抽样分析。
   * - ``sample_rate``
     - ``0.30``
     - 抽样比例。

调参建议
--------

1. 多样本整合优先关注 ``batch_method`` 与 ``n_comps`` 联动。
2. 组织质量波动较大时，先回调 ``min_genes``、``min_cells``、``mt_threshold``。
3. 百万级细胞规模可开启 ``sketch`` 以提升迭代效率。
