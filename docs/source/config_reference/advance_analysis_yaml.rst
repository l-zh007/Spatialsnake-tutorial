advance_analysis.yaml 参数说明
==============================

该配置文件对应 ``--option=advance_analysis``，统一覆盖 cellPhoneDB、pysenic、liana、cellchat、cellcharter、banksy 六个下游模块。

全局字段
--------

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - 参数
     - 默认值
     - 作用
   * - ``option``
     - ``advance_analysis``
     - 固定阶段标识。
   * - ``results_folder`` / ``data_fold`` / ``sample_list``
     - ``results`` / ``data`` / ``sample.txt``
     - 输出目录、数据目录与样本表。
   * - ``run_type`` / ``channel`` / ``runpipe``
     - ``visium_HD`` / ``single_analysis`` / ``cellPhoneDB``
     - 平台、通道与下游模块入口。

模块参数
--------

.. list-table::
   :header-rows: 1
   :widths: 32 20 48

   * - 参数
     - 默认值
     - 作用
   * - ``senic_input`` / ``tfs_input`` / ``feather_input`` / ``motifs_input``
     - 见模板
     - PySCENIC 输入对象与数据库资源路径。
   * - ``senic_workers``
     - ``128``
     - PySCENIC 并行线程数。
   * - ``cellPhoneDB_input``
     - ``results/.../Colon_Cancer_P2_cellcharter.zarr``
     - CellPhoneDB/LIANA 默认输入对象。
   * - ``counts_data`` / ``threshold`` / ``pvalue`` / ``iterations``
     - ``hgnc_symbol`` / ``0.1`` / ``0.05`` / ``500``
     - CellPhoneDB 统计阈值与置换参数。
   * - ``cpdb_method`` / ``cpdb_de_method``
     - ``statistical`` / ``wilcoxon``
     - CellPhoneDB 模式与差异方法标签。
   * - ``cell_type1`` / ``cell_type2`` / ``gene_family``
     - ``Endothelial`` / ``Tumor`` / ``""``
     - 可视化聚焦的细胞对与家族。
   * - ``liana_method`` / ``liana_resource_name``
     - ``cellphonedb`` / ``consensus``
     - LIANA 方法与数据库资源。
   * - ``liana_expr_prop`` / ``liana_min_cells`` / ``liana_use_raw``
     - ``0.1`` / ``5`` / ``true``
     - LIANA 过滤阈值与表达矩阵来源。
   * - ``assay`` / ``species`` / ``min_cells`` / ``workers`` / ``trim`` / ``interaction_length``
     - ``Spatial`` / ``human`` / ``10`` / ``32`` / ``0.1`` / ``150``
     - CellChat 物种、统计与空间距离参数。
   * - ``max_cluster`` / ``condition_col`` / ``sample_col`` / ``cellcharter_col``
     - ``10`` / ``condition`` / ``region`` / ``spatial_cluster``
     - CellCharter 分簇搜索与比较字段。
   * - ``k_geom`` / ``max_m`` / ``nbr_weight_decay`` / ``lambda_list``
     - ``15`` / ``1`` / ``scaled_gaussian`` / ``[0.8]``
     - BANKSY 邻域几何与空间权重参数。

调参建议
--------

1. 先设置 ``runpipe``，仅保留对应模块参数为重点调优对象。
2. 通讯类模块优先确认 ``celltype_col`` 与输入对象注释列一致。
3. 复杂分析建议将数据库路径参数固定为绝对路径，降低环境差异影响。
