transform.yaml 参数说明
=======================

该配置文件对应 ``spatialsnake useful_tool --option=transform``，用于 zarr/h5ad/seurat 格式互转。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 参数
     - 默认值
     - 作用
   * - ``output_dir``
     - ``results/useful_results``
     - 转换结果目录。
   * - ``save_image``
     - ``True``
     - zarr 转 h5ad 时是否导出图像数据。
   * - ``transform_from``
     - ``h5ad``
     - 输入格式。
   * - ``transform_to``
     - ``h5ad``
     - 输出格式（h5ad/zarr/seurat）。

调参建议
--------

1. 跨生态互操作时建议保留 ``save_image=True``，方便空间可视化复现。
2. 大对象转换前建议预留充足磁盘空间。
3. 对外共享建议优先输出 ``h5ad`` 或 ``seurat``，便于下游团队直接读取。
