格式转换工具（transform）
==========================

功能对应 ``workflow/function/transform.py``，用于 zarr / h5ad / seurat 互转。

配置文件详解请见 :doc:`../config_reference/transform_yaml`。

命令模板
--------

.. code-block:: bash

   spatialsnake useful_tool --option=transform <INPUT> --transform_from=<src> --transform_to=<dst> --output_dir=results/useful_results

常见转换
--------

1) zarr -> h5ad

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotion/S1.zarr --transform_from=zarr --transform_to=h5ad --save_image=True --output_dir=results/useful_results

2) h5ad -> zarr

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/useful_results/S1.h5ad --transform_from=h5ad --transform_to=zarr --output_dir=results/useful_results

3) h5ad 或 zarr -> seurat

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/useful_results/S1.h5ad --transform_from=h5ad --transform_to=seurat --output_dir=results/useful_results

关键参数
--------

- ``--transform_from``：``zarr`` 或 ``h5ad``
- ``--transform_to``：``h5ad`` / ``zarr`` / ``seurat``
- ``--save_image``：zarr 转 h5ad 时是否带图像信息

输出
----

- 输出目录：``results/useful_results/``
- 文件名默认继承输入文件 basename
