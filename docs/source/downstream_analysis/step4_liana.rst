模块 3：细胞通讯（liana）
=========================

虽然我们已经在 :doc:`step2_cellphonedb` 中介绍了 ``cellPhoneDB``,并且也有在R生态下的CellChat两种配受体分析工具

 但我们还是想要提供 ``liana`` , 此工具提供了更全面的配体-受体通讯分析功能。
``liana`` 用于在统一接口下执行多种配体-受体打分方法，并将结果写回对象，便于后续继续分析,这种多样的分析方法可以帮助我们更好更深度的理解和挖掘细胞之间的通讯机制，而不仅仅拘泥于一种算法工具。
但需要注意的是,``liana`` 分析并不像先前的工具样存在空间距离的限制,若您需要考虑细胞之间的空间距离,请先进行切割,将数据分为一个小区域研究,再进行 ``liana`` 分析.

更有意义的是,在空间转录组与单细胞组合分析中,``liana`` 的加入可以让我们输入对相似实验条件的单细胞转录组数据，与空间转录组数据的结果相印证,从而更稳健的揭示细胞之间的通讯机制.


处理逻辑概述
------------

1. 读取输入 ``.zarr`` 或 ``.h5ad`` 对象，提取细胞类型列。
2. 按 ``method`` 与 ``resource_name`` 运行 LIANA 通讯推断。
3. 将通讯结果写入 ``adata.uns``，并自动导出 dotplot / tileplot / circle 图。
4. 输出携带通讯结果的 ``.zarr`` 对象供后续复用。

准备输入文件
------------

``sample.txt`` 推荐格式  若您想输入单细胞数据，直接将路径更改即可，支持传统h5ad格式

.. code-block:: text

   sample_id   input_path
   S1          results/S1/annotion/S1.zarr

输入要求：

1. 输入对象中应包含细胞类型列（默认 ``celltype``）。
2. 建议使用已完成注释的对象，保证通讯来源/受体群体可解释。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=liana

运行可选的参数设置(配置文件版)
------------------------------------------------------------
配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。

在 ``advance_analysis.yaml`` 中常用参数如下：

.. list-table::
   :header-rows: 1
   :widths: 26 22 52

   * - 参数
     - 常用值
     - 作用
   * - ``runpipe``
     - ``liana``
     - 进入 liana 分支
   * - ``cellPhoneDB_input``
     - ``results/S1/annotion/S1.zarr``
     - 指定输入对象路径
   * - ``liana_method``
     - ``cellphonedb`` / ``connectome`` / ``cellchat``
     - 选择通讯打分方法
   * - ``liana_resource_name``
     - ``consensus``
     - 选择配体-受体数据库资源
   * - ``liana_expr_prop``
     - ``0.1``
     - 表达比例阈值，过滤低表达配体/受体
   * - ``liana_min_cells``
     - ``5``
     - 每类细胞最小数量
   * - ``liana_use_raw``
     - ``true``
     - 是否优先使用 ``adata.raw``
   * - ``celltype_col``
     - ``celltype``
     - 细胞类型分组列

结果文件结构
------------

.. code-block:: text

   results/
   └── liana_output/
       ├── {sample}.zarr
       ├── dotplot.png
       ├── tileplot.png
       └── circle.png

图表与结果解释
--------------

1. ``dotplot.png``：展示来源细胞与靶细胞间主要配体-受体对，颜色与点大小反映不同评分维度。
2. ``tileplot.png``：对重点细胞对的高分互作进行排序汇总，适合提取候选通讯轴。
3. ``circle.png``：从网络视角查看不同细胞类型的通讯强度与方向，适合总览“谁在主导通讯”。
4. ``{sample}.zarr``：包含完整通讯推断结果（写入 ``uns``），便于后续继续筛选或可视化。
