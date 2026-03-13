合并工具（merge）
==================

功能对应 ``workflow/function/merge.py``，支持三类合并场景。

命令模板
--------

.. code-block:: bash

   spatialsnake useful_tool --option=merge <INPUT1> <INPUT2> ... --merge_by=<mode> --output_dir=results/useful_results

场景 1：按样本拼接
-------------------

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/S1/annotion/S1.zarr results/S2/annotion/S2.zarr --merge_by=sample --re_sample=True --output_dir=results/useful_results

场景 2：按聚类标签拼接并重排
-----------------------------

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/S1/annotion/S1.zarr results/S2/annotion/S2.zarr --merge_by=clusters --cluster_key=clusters --reordering=True --output_dir=results/useful_results

场景 3：把外部 reannotation 合并回基准对象
------------------------------------------

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/merge_data/annotion/concatenated_sdata --merge_by=reannotation --annotation_csv=anno_csv_dir --csv_cell_col=Barcode --csv_label_col=Grouped_Annotation --target_col=celltype --fallback_col=celltype --output_dir=results/useful_results

关键参数
--------

- ``--merge_by``：``sample`` / ``clusters`` / ``celltype`` / ``reannotation``
- ``--reordering``：聚类拼接时是否重排标签
- ``--cluster_key``：聚类列名
- ``--annotation_csv``：reannotation csv 文件、目录或逗号分隔路径
- ``--csv_cell_col --csv_label_col``：csv 中细胞 ID 与标签列
- ``--input_cell_col --target_col --fallback_col``：基准对象写入策略

输出
----

- 输出目录：``results/useful_results/``
- 产物文件：``concatenated_sdata.zarr``
