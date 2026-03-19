旁路分析与实用工具
==================

本模块对应命令 ``spatialsnake useful_tool``，用于在主流程外进行数据重组与格式转换。

配置文件详解：

- splitting 参见 :doc:`../config_reference/splitting_yaml`
- merge 参见 :doc:`../config_reference/merge_yaml`
- transform 参见 :doc:`../config_reference/transform_yaml`

推荐顺序：

1. ``splitting``：按样本、分群、ROI 或图像范围切分对象
2. ``merge``：合并多个对象，或把外部 reannotation 写回基准对象
3. ``transform``：在 zarr / h5ad / seurat 之间转换

.. toctree::
   :maxdepth: 1

   splitting
   merge
   transform
