annotion.yaml 参数说明
======================

该配置文件对应 ``--option=annotion``，统一管理手动注释、重注释、cell2location、RCTD 四类注释分支。

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - 参数
     - 默认值
     - 作用
   * - ``option``
     - ``advance_analysis``
     - 文件中的阶段标识字段。
   * - ``results_folder`` / ``data_fold`` / ``sample_list``
     - ``results`` / ``data`` / ``sample.txt``
     - 结果目录、数据目录与样本表。
   * - ``run_type`` / ``channel``
     - ``visium`` / ``compare_analysis``
     - 平台类型与分析通道。
   * - ``anno_algorithm``
     - ``mannul``
     - 注释算法分支选择。
   * - ``annotion_list``
     - ``annotion.txt``
     - 手动映射文件路径。
   * - ``device``
     - ``cuda``
     - 模型训练设备。
   * - ``max_epochs_reference``
     - ``250``
     - cell2location 参考模型训练轮数。
   * - ``remove_mt``
     - ``True``
     - 是否过滤线粒体基因。
   * - ``N_cells_per_location``
     - ``30``
     - cell2location 位点细胞数先验。
   * - ``max_epochs_st``
     - ``30000``
     - cell2location 空间模型训练轮数。
   * - ``shape_type`` / ``image_type``
     - ``False`` / ``False``
     - 空间图层筛选关键字。
   * - ``image_slice``
     - ``False``
     - 是否裁剪图像区域。
   * - ``x1`` / ``x2`` / ``y1`` / ``y2``
     - ``0``
     - 裁剪窗口坐标。
   * - ``threads``
     - ``64``
     - RCTD 线程数配置。
   * - ``RCTD_mode``
     - ``doublet``
     - RCTD 运行模式。
   * - ``cell_type_col``
     - ``celltype``
     - RCTD 参考对象细胞类型列名。
   * - ``group_by``
     - ``sample``
     - RCTD 分组展示列名。
   * - ``max_cores``
     - ``8``
     - RCTD 并行核心数上限。

调参建议
--------

1. 先固定 ``anno_algorithm``，再调整对应分支参数，避免跨算法混调。
2. 深度学习分支优先校准 ``device`` 与训练轮数参数。
3. RCTD 分支优先确认 ``cell_type_col`` 与 ``RCTD_mode`` 的一致性。
