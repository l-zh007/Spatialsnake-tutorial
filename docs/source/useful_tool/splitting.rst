切分工具（splitting）
======================

``splitting`` 用于把一个空间转录组对象拆分成多个更小、更容易分析的子对象。


- 按细胞类型或聚类拆分（常用于后续亚群分析）
- 按样本或实验组拆分（常用于多样本对比前的数据整理）
- 按 ROI 表格拆分（常用于 Loupe/Xenium Explorer 套索后复用）
- 按图像坐标裁剪（常用于局部区域重点分析）

本页重点讲 ``zarr`` 对象拆分。配置文件详解请见 :doc:`../config_reference/splitting_yaml`。


适用场景
--------------------

1. 您已完成 ``core_analysis``，想把某个大类细胞（如 Tumor）拆出来做二次聚类。
2. 您有多样本整合对象，想按样本或分组拆开分别查看。
3. 您在外部软件圈选了 ROI，想导入 CSV 进行不规则范围的直接批量拆分。
4. 您只关注切片局部区域，或一个玻片存在多个小样本想按坐标裁剪出独立子对象。


运行前准备
----------


1. 输入对象是 ``.zarr`` 路径（推荐来自 integrate / preprocess / clustering / annotion 结果）。
2. 您知道要按哪个字段拆分（例如 ``celltype``、``clusters``、``sample``、``group``）。
3. ``sample.txt`` 所在目录与当前工作目录一致，或命令里路径写绝对路径。


命令模板（通用）
----------------

.. code-block:: bash

   spatialsnake useful_tool --option=splitting <输入zarr路径> --split_by=<拆分模式> --output_dir=results/useful_results


场景 1：按细胞类型/聚类拆分
----------------------------------

当您希望把某几类细胞单独拿出来继续分析（例如 将示例数据中的 Tumor 亚群细分）时使用。

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotion/Colon_Cancer_P2.zarr --split_by=celltype --barcodes=Tumor

也可以一次选择多个标签（英文逗号分隔）：--barcodes=Tumor,B_cell  分别拆分(节省重复操作时间) --barcodes=Tumor|B_cell

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotion/Colon_Cancer_P2.zarr --split_by=celltype --barcodes=Tumor,Fibroblast --output_dir=results/useful_results

如果不写 ``--barcodes``，工具会把该字段下的每个类别都分别导出。

输出命名规则：

- 未指定 ``--barcodes``：``cluster_<类别名>.zarr``
- 指定 ``--barcodes``：``celltype_selected_<类别1_类别2>.zarr`` 或 ``clusters_selected_<编号>.zarr``


场景 2：按样本/分组拆分（多样本常用）
----------------------------------

用于把整合对象按 ``sample`` / ``region`` / ``group`` 拆成多个子对象。

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=sample --output_dir=results/useful_results

按实验分组拆分：

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=group --output_dir=results/useful_results

输出命名规则：

- ``split_by=sample`` 或 ``region``：按坐标系统导出 ``<样本名>.zarr``
- ``split_by=group``：导出 ``group_<分组名>.zarr``


场景 3：与Loupe,Xenium Explore互作，按 ROI CSV 拆分
----------------------------------------

如何通过Loupe进行筛选
1.使用spaceranger输出的loupe文件进行导入到Loupe软件中

2.使用套索工具筛选

.. figure:: /_static/images/step1.png
   :width: 85%
   :align: center
   :alt: preprocess pca variance ratio

2.区域命令
.. figure:: /_static/images/step2.png
   :width: 85%
   :align: center
   :alt: preprocess pca variance ratio

3.csv文件导出

.. figure:: /_static/images/step3.png
   :width: 85%
   :align: center
   :alt: preprocess pca variance ratio

如何通过Xenium Explore进行套索工具筛选

1.将xenium ranger 输出数据的文件夹导入xenium Explore

.. figure:: /_static/images/step4.png
   :width: 85%
   :align: center
   :alt: preprocess pca variance ratio

2.使用套索工具筛选并导出
.. figure:: /_static/images/step5.png
   :width: 85%
   :align: center
   :alt: preprocess pca variance ratio

用 Loupe/Xenium Explorer 等工具导出了 ROI 对应细胞表，可直接导入拆分。

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=ROI --roi_csv= [path_to_csv]

``roi_csv`` 可传入单个 CSV，也可传入一个目录（目录下多个 CSV 会自动合并处理）。

CSV 最少需要 ``cell_id`` 列；ROI 名称列可用 ``roi`` / ``region`` / ``sample`` / ``group``。
如果缺少 ROI 名称列，工具会用 CSV 文件名作为 ROI 名称。

输出命名规则：

- ``ROI_<ROI名称>.zarr``


场景 4：按图像坐标裁剪（局部区域分析）
------------------------------------

用于按坐标框裁剪某一块组织区域，我们之前annotation_help部分的图像结果均包含坐标信息可供参考，但裁剪只适合矩形范围,若需细节裁剪请使用上述官方互作工具

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/Colon_Cancer_P2_008um/annotion/Colon_Cancer_P2.zarr --split_by=image --shape_elements=Colon_Cancer_P2 --min_x=0 --max_x=2000 --min_y=0 --max_y=2000 --output_dir=results/useful_results

输出内容：

- ``spatial<min_x>_<max_x>_<min_y>_<max_y>.zarr``（裁剪后的子对象）
- ``<坐标ID>_shape.png``（该区域的图像+形状可视化）


关键参数说明（实操版）
----------------------

.. list-table::
   :header-rows: 1
   :widths: 22 20 58

   * - 参数
     - 常用值
     - 作用
   * - ``--split_by``
     - ``celltype`` / ``clusters`` / ``sample`` / ``group`` / ``ROI`` / ``image``
     - 选择拆分维度，是最核心参数。
   * - ``--barcodes``
     - ``Tumor`` 或 ``0,1,2``
     - 仅导出指定类别；不填则按该字段全部类别导出。
   * - ``--roi_csv``
     - ``roi_tables`` 或 ``roi1.csv``
     - ROI 拆分时指定 CSV 文件或目录。
   * - ``--shape_elements``
     - ``Colon_Cancer_P2``
     - 图像坐标拆分时指定目标图层/样本坐标系统。
   * - ``--min_x --max_x --min_y --max_y``
     - ``0 2000 0 2000``
     - 图像坐标裁剪范围。
   * - ``--output_dir``
     - ``results/useful_results``
     - 拆分结果输出目录。


常见报错与处理
--------------

1. ``values not found in <字段名>``

   - 原因：``--barcodes`` 里的值不在对象字段中。
   - 处理：先检查拼写和大小写，再确认字段是 ``celltype`` 还是 ``clusters``。

2. ``group column not found in table obs``

   - 原因：对象里没有 ``group`` 列。
   - 处理：改用 ``sample`` / ``region``，或先在上游流程补充分组信息。

3. ``cell_id column not found``

   - 原因：ROI CSV 中没有可识别的细胞 ID 列。
   - 处理：把列名规范为 ``cell_id``（或 ``Cell ID`` / ``barcode``）。


下一步建议
----------

- 若您拆分的是某个感兴趣细胞大类，推荐直接进入 :doc:`../subcluster_annotation/reclustering` 做亚群细分。
- 若您拆分的是多样本对象，可进入下游模块分别比较不同子对象的生物学差异。
