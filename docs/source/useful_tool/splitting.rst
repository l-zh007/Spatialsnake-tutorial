切分工具（splitting）
======================

功能对应 ``workflow/function/splitting.py``，用于把一个空间对象拆成多个子对象。

命令模板
--------

.. code-block:: bash

   spatialsnake useful_tool --option=splitting <INPUT> --split_by=<mode> --output_dir=results/useful_results

常见模式
--------

1) 按聚类或细胞类型切分

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=clusters --barcodes=0,1,2 --output_dir=results/useful_results

2) 按样本或分组切分

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=sample --output_dir=results/useful_results

3) 按 ROI CSV 切分

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=ROI --roi_csv=roi_tables --output_dir=results/useful_results

4) 按图像坐标切分

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=image --shape_elements=sampleA --min_x=0 --max_x=2000 --min_y=0 --max_y=2000 --output_dir=results/useful_results

关键参数
--------

- ``--split_by``：``sample`` / ``group`` / ``clusters`` / ``celltype`` / ``ROI`` / ``image``
- ``--barcodes``：按 ``split_by`` 指定要保留的值，多个值逗号分隔
- ``--roi_csv``：ROI csv 文件或目录
- ``--shape_elements`` 与坐标参数：图像坐标切分时使用

输出
----

- 默认输出到 ``results/useful_results/``
- 输出类型与输入一致：zarr 输入生成 zarr，h5ad 输入生成 h5ad
