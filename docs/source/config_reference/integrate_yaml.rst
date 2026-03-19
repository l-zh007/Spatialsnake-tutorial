integrate.yaml 参数说明
=======================

该配置文件对应 ``--option=integrate``，用于定义数据读入与跨样本整合阶段的输入组织方式。其默认值如下。

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - 参数
     - 默认值
     - 作用
   * - ``option``
     - ``integrate``
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
     - 平台类型，如 ``visium``、``visium_HD``、``xenium``。
   * - ``channel``
     - ``compare_analysis``
     - 分析通道（单样本或多样本）。
   * - ``cells_boundaries``
     - ``False``
     - Xenium 中是否加载细胞边界图层。
   * - ``nucleus_boundaries``
     - ``False``
     - Xenium 中是否加载细胞核边界图层。
   * - ``nucleus_labels``
     - ``False``
     - Xenium 中是否加载细胞核标签图层。
   * - ``morphology_mip``
     - ``False``
     - Xenium 中是否加载形态学 MIP 图像。
   * - ``geojson``
     - ``cell_segmentations.geojson``
     - Visium segment 的分割文件名。
   * - ``image``
     - ``tissue_hires_image.png``
     - Visium segment 的组织图像文件名。
   * - ``scale_factors``
     - ``scalefactors_json.json``
     - 缩放系数文件名。
   * - ``coor_file``
     - ``BeadLocationsForR.csv``
     - Slide-seq 坐标文件名。

调参建议
--------

1. 绝大多数项目仅需修改 ``run_type``、``channel`` 与 ``sample_list``。
2. 仅在 Xenium 或 Visium segment 场景下开启/调整对应图层参数。
3. 团队协作中建议固定 ``results_folder``，保证后续步骤路径稳定可复现。
