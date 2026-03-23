合并工具（merge）
==================

``merge`` 用于把多个 ``zarr`` 对象整合成一个对象，或把外部注释结果回填到基准对象。
对于无代码基础的分析员，可把它理解为“多对象拼接 + 注释字段回写”工具。

配置文件详解请见 :doc:`../config_reference/merge_yaml`。

适用场景
--------

1. 您想把多个样本的分析结果拼接成一个联合对象做比较分析。
2. 您想把多个子对象（按簇拆分后）再合并回一个对象继续下游流程。
3. 您已完成亚群注释，想将 ``celltype_annotations.csv`` 回填到原始大类对象。


运行前准备
----------

请先确认：

1. 输入对象均为可读的 ``.zarr`` 路径。
2. 若做 reannotation 回填，CSV 至少包含“细胞 ID 列 + 注释标签列”。
3. 命令执行目录与数据路径一致，或在命令中使用绝对路径。


命令模板
----------------

.. code-block:: bash

   spatialsnake useful_tool --option=merge <INPUT1> <INPUT2> ... --merge_by=<mode> --output_dir=results/useful_results


场景 1：按样本拼接（多样本整合常用）
----------------------------------

用于把多个样本对象拼接为一个 ``concatenated_sdata.zarr``。

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/S1/annotion/S1.zarr results/S2/annotion/S2.zarr --merge_by=sample --re_sample=True --output_dir=results/useful_results

说明：

- ``--re_sample=True`` 时，若对象里缺少 ``sample`` 列，工具会自动按文件名补充样本标识。
- 输出文件固定为 ``results/useful_results/concatenated_sdata.zarr``。


场景 2：按聚类标签拼接并重排
----------------------------

用于把多个对象按簇标签拼接，并将簇编号重排为连续编号，避免不同对象簇号冲突。

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/S1/annotion/S1.zarr results/S2/annotion/S2.zarr --merge_by=clusters --cluster_key=clusters --reordering=True --output_dir=results/useful_results

如果您希望按其他列重排（例如 ``celltype``），可改 ``--cluster_key``：

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/subset1.zarr results/subset2.zarr --merge_by=clusters --cluster_key=celltype --reordering=True --output_dir=results/useful_results

说明：

- ``--reordering=True`` 时，脚本会按输入顺序将每个对象中的标签映射到新的连续标签。
- ``--reordering=False`` 时，保留原标签，适合标签体系已统一的对象。


场景 3：将外部 reannotation 回填到基准对象
---------------------------------------

用于把外部 CSV 注释结果写回原始 zarr 对象（常用于亚群注释回灌）。

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/Colon_Cancer_P2_008um/annotion/Colon_Cancer_P2.zarr --merge_by=reannotation --annotation_csv=results/reclustering/celltype_annotations.csv --csv_cell_col=Barcode --csv_label_col=Grouped_Annotation --input_cell_col=cell_id --target_col=sub_celltype --original_celltype_col=celltype --output_dir=results/useful_results

说明：

- ``--annotation_csv`` 可传入单个 CSV、目录，或逗号分隔的多个 CSV 路径。
- 工具会按细胞 ID 匹配并更新 ``target_col``。
- 若某细胞在 CSV 中找不到标签，会保留 ``target_col`` 旧值；若旧值不存在，回退使用 ``original_celltype_col``。


关键参数说明（实操版）
----------------------

.. list-table::
   :header-rows: 1
   :widths: 24 20 56

   * - 参数
     - 常用值
     - 作用
   * - ``--merge_by``
     - ``sample`` / ``clusters`` / ``reannotation``
     - 选择合并模式。
   * - ``--re_sample``
     - ``True`` / ``False``
     - ``merge_by=sample`` 时，是否自动补充 ``sample`` 列。
   * - ``--reordering``
     - ``True`` / ``False``
     - ``merge_by=clusters`` 时，是否重排簇标签避免冲突。
   * - ``--cluster_key``
     - ``clusters`` / ``celltype`` / ``leiden``
     - 指定按哪一列做聚类标签合并或重排。
   * - ``--annotation_csv``
     - ``anno.csv`` / ``anno_dir`` / ``a.csv,b.csv``
     - reannotation 模式下的注释来源。
   * - ``--csv_cell_col``
     - ``Barcode`` / ``cell_id``
     - CSV 中用于匹配细胞 ID 的列名。
   * - ``--csv_label_col``
     - ``Grouped_Annotation`` / ``celltype``
     - CSV 中注释标签列名。
   * - ``--input_cell_col``
     - ``cell_id``
     - 基准 zarr 中用于匹配的细胞 ID 列。
   * - ``--target_col``
     - ``sub_celltype``
     - 注释写入列名。
   * - ``--original_celltype_col``
     - ``celltype``
     - 当 ``target_col`` 不存在时的回退参考列。
   * - ``--output_dir``
     - ``results/useful_results``
     - 输出目录。


结果如何检查
------------

1. 检查输出目录中是否生成 ``concatenated_sdata.zarr``。
2. 用下游流程读取该对象，确认可正常运行。
3. 若为 reannotation 模式，检查 ``target_col`` 是否出现预期新标签。


常见报错与处理
--------------

1. ``annotation csv not found``

   - 原因：``--annotation_csv`` 路径错误。
   - 处理：改为绝对路径，或确认目录下确有 CSV 文件。

2. ``required columns not found in <csv>``

   - 原因：CSV 中缺少细胞 ID 列或标签列。
   - 处理：检查 ``--csv_cell_col`` 与 ``--csv_label_col`` 是否与真实列名一致。

3. ``no tables found in base zarr``

   - 原因：输入对象异常或路径不是有效 zarr。
   - 处理：先确认对象可在上游流程中被正常读取。


下一步建议
----------

- 合并后可进入下游差异分析或可视化模块做跨样本比较。
- 若完成 reannotation 回填，建议继续执行注释相关结果导出与复核流程。
