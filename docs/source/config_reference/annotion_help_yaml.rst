annotion_help.yaml 参数说明
===========================

该配置文件对应 ``--option=annotion_help``，用于 marker 统计、空间渲染和通路富集辅助。

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - 参数
     - 默认值
     - 作用
   * - ``option``
     - ``advance_analysis``
     - 文件中的阶段标识字段。
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
   * - ``markers_algorithm``
     - ``wilcoxon``
     - marker 基因统计方法。
   * - ``shape_type``
     - ``False``
     - shape 图层名筛选关键字。
   * - ``image_type``
     - ``False``
     - image 图层名筛选关键字。
   * - ``spacies``
     - ``human``
     - GO/KEGG 富集物种背景。
   * - ``image_slice``
     - ``False``
     - 是否进行图像裁剪。
   * - ``x1`` / ``x2`` / ``y1`` / ``y2``
     - ``0``
     - 裁剪窗口坐标。

调参建议
--------

1. 算法层面优先确认 ``markers_algorithm`` 与物种 ``spacies``。
2. 仅在局部组织复核时开启 ``image_slice`` 并设定坐标。
3. 跨样本对比时尽量统一 ``image_type`` 与 ``shape_type``。
