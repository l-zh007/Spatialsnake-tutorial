splitting.yaml 参数说明
=======================

该配置文件对应 ``spatialsnake useful_tool --option=splitting``，用于按样本、标签或空间范围切分对象。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 参数
     - 默认值
     - 作用
   * - ``output_zarr_path``
     - ``results``
     - 输出 zarr 根目录。
   * - ``split_by``
     - ``sample``
     - 切分模式（sample/group/clusters/celltype/ROI/image）。
   * - ``output_dir``
     - ``results/useful_results``
     - 结果目录。
   * - ``shape_elements``
     - ``None``
     - image 切分时指定 shape 元素。
   * - ``max_x`` / ``min_x`` / ``max_y`` / ``min_y``
     - ``0``
     - 图像坐标切分边界。
   * - ``barcodes``
     - ``None``
     - 指定保留标签（逗号分隔）。
   * - ``roi_csv``
     - ``""``
     - ROI 表格路径或目录。

调参建议
--------

1. 标签切分优先使用 ``split_by`` + ``barcodes``。
2. 局部组织裁剪使用 ``split_by=image`` 并联动设置坐标。
3. 多次切分时建议固定 ``output_dir`` 便于产物管理。
