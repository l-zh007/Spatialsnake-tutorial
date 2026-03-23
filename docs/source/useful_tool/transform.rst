格式转换工具（transform）
==========================

``transform`` 用于 ``zarr``、``h5ad``、``seurat(rds)`` 之间的数据格式转换,以方便使用不同生态的工具进行后续的空间转录组分析

配置文件详解请见 :doc:`../config_reference/transform_yaml`。


适用场景
--------

1. 您需要把 Spatialsnake 的 zarr 结果交给 Scanpy 生态继续分析（转 h5ad）。
2. 您已有 h5ad 对象，想转回 zarr 接入 Spatialsnake 流程（转 zarr）。
3. 您需要把对象转为 Seurat 使用的 rds（转 seurat）。


运行前准备
----------

请先确认：

1. 输入路径正确，且与 ``--transform_from`` 一致。
2. 若输出为 ``seurat``，运行环境中可用 ``Rscript``，且依赖脚本可执行。
3. 建议先预留足够磁盘空间；``zarr -> seurat`` 会产生中间 ``h5ad`` 文件。


命令模板（通用）
----------------

.. code-block:: bash

   spatialsnake useful_tool --option=transform <INPUT> --transform_from=<src> --transform_to=<dst> --output_dir=results/useful_results


场景 1：zarr -> h5ad（含图像可选）
--------------------------------

将 zarr 转为 h5ad，便于在 Scanpy 中继续分析。

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotion/S1.zarr --transform_from=zarr --transform_to=h5ad --save_image=True --output_dir=results/useful_results

说明：

- ``--save_image=True`` 会尽量保留空间图像相关信息。
- 支持多个输入 zarr，一次整合后输出单个 h5ad。
- 输出文件名默认取第一个输入的 basename，例如 ``S1.h5ad``。


场景 2：h5ad -> zarr
-------------------

将 h5ad 转回 zarr，用于接回 Spatialsnake 的后续分析。

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/useful_results/S1.h5ad --transform_from=h5ad --transform_to=zarr --output_dir=results/useful_results

说明：

- 实际实现更适合单个 h5ad 输入。
- 若传入多个 h5ad，当前脚本会以最后一个读取对象写出结果，建议避免多输入。


场景 3：h5ad -> seurat(rds)
--------------------------

将 h5ad 转为 Seurat 的 rds 文件（调用 R 脚本）。

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/useful_results/S1.h5ad --transform_from=h5ad --transform_to=seurat --type=st --output_dir=results/useful_results

``--type`` 可选：

- ``st``：空间转录组（默认）
- ``sc``：单细胞


场景 4：zarr -> seurat(rds)
--------------------------

该模式会先把 zarr 转成中间 h5ad，再继续转 rds。

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotion/S1.zarr --transform_from=zarr --transform_to=seurat --save_image=True --type=st --output_dir=results/useful_results

输出通常包含：

- ``S1.h5ad``（中间文件）
- ``S1.rds``（最终 Seurat 文件）


关键参数说明（实操版）
----------------------

.. list-table::
   :header-rows: 1
   :widths: 24 20 56

   * - 参数
     - 常用值
     - 作用
   * - ``--transform_from``
     - ``zarr`` / ``h5ad``
     - 指定输入格式。
   * - ``--transform_to``
     - ``h5ad`` / ``zarr`` / ``seurat``
     - 指定目标格式。
   * - ``--save_image``
     - ``True`` / ``False``
     - zarr 转 h5ad 或 zarr 转 seurat 的第一步中，是否保留图像信息。
   * - ``--type``
     - ``st`` / ``sc``
     - 转 seurat 时的数据类型，默认 ``st``。
   * - ``--output_dir``
     - ``results/useful_results``
     - 输出目录。


结果如何检查
------------

1. 检查输出目录下是否生成目标文件（``.h5ad`` / ``.zarr`` / ``.rds``）。
2. 若目标为 seurat，同时确认中间 ``.h5ad`` 是否成功生成。
3. 用下游工具尝试读取一次，确认对象可正常打开。


常见报错与处理
--------------

1. 输入输出格式相同后直接退出

   - 原因：``--transform_from`` 与 ``--transform_to`` 设为相同值。
   - 处理：修改其中一个参数，保证源格式与目标格式不同。

2. ``Rscript`` 执行失败（转 seurat）

   - 原因：R 环境缺失或依赖未安装。
   - 处理：先在命令行测试 ``Rscript --version``，再补齐相关 R 包。

3. 中间 h5ad 未生成（zarr -> seurat）

   - 原因：zarr 到 h5ad 第一步失败。
   - 处理：先单独运行 ``zarr -> h5ad``，确认输入对象和图像信息可正常转换。


下一步建议
----------

- 若您要继续在 Python 生态分析，推荐优先使用 ``h5ad``。
- 若您要与 Seurat 工作流联动，优先使用 ``seurat`` 并保留中间 ``h5ad`` 便于回溯。
