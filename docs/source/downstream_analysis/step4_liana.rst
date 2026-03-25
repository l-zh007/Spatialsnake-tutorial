模块 3：细胞通讯（liana）
=========================

虽然我们已经在 :doc:`step2_cellphonedb` 中介绍了 ``cellPhoneDB``,并且也有在R生态下的CellChat两种配受体分析工具

 但我们还是想要提供 ``liana`` , 此工具提供了更全面的配体-受体通讯分析功能。
``liana`` 用于在统一接口下执行多种配体-受体打分方法，并将结果写回对象，便于后续继续分析,这种多样的分析方法可以帮助我们更好更深度的理解和挖掘细胞之间的通讯机制，而不仅仅拘泥于一种算法工具。
但需要注意的是,``liana`` 分析并不像先前的工具样存在空间距离的限制,若您需要考虑细胞之间的空间距离,请先进行切割,将数据分为一个小区域研究,再进行 ``liana`` 分析.

更有意义的是,在空间转录组与单细胞组合分析中,``liana`` 的加入可以让我们输入对相似实验条件的单细胞转录组数据，与空间转录组数据的结果相印证,从而更稳健的揭示细胞之间的通讯机制.


运行步骤与内容
--------------

1. **读取输入与参数解析**
   读取空间转录组或单细胞数据对象（支持 ``.zarr`` 和 ``.h5ad``），并提取指定的细胞类型标注列作为后续通信分析的分组依据。
2. **多算法通信推断 (LIANA Execution)**
   根据配置中指定的通信推断方法（如 ``cellphonedb``、``connectome``、``cellchat`` 等）以及资源数据库（如 ``consensus``），调用 LIANA 框架进行配体-受体（Ligand-Receptor）交互强度的打分。过程中会结合表达比例阈值和最小细胞数对低表达特征进行过滤。
3. **显著性过滤与结果聚合**
   提取各细胞类型间高置信度的配体-受体对，计算相互作用的强度（magnitude）和特异性（specificity）等关键指标，并将计算结果保存在数据对象的无结构字典（``.uns``）中。
4. **多维图表自动生成**
   基于上一步提取的显著交互结果，自动生成展示特定细胞对通信细节的点图（Dotplot）、展示高分互作排名的热图（Tileplot），以及总览全细胞群通信流向与强度的圆环网络图（Circle plot）。
5. **结果对象导出**
   将包含完整通信推断信息的数据对象保存为新的 ``.zarr`` 或 ``.h5ad`` 文件，供后续提取原始表格或进行个性化二次作图。

准备输入文件
------------

``sample.txt`` 推荐格式。若您想输入单细胞数据，直接将路径更改即可，支持传统 ``.h5ad`` 格式：

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

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

1. 配受体交互点图（``dotplot.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_dot_plot.png
   :width: 85%
   :align: center
   :alt: liana dotplot

解释：
展示特定来源细胞（Source）与目标细胞（Target）之间具体的配体-受体交互对。通常点的大小代表该互作的显著性（如 p-value 负对数），颜色深浅代表互作的强度（如表达量乘积），是分析具体分子机制的最核心图表。

2. 高分互作热图（``tileplot.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_heatmap.png
   :width: 85%
   :align: center
   :alt: liana tileplot

解释：
以平铺网格的形式直观展示全样本或特定细胞对中排名靠前（Top N）的配受体交互。填充颜色代表相互作用的强度得分，便于快速抓取关键的通信候选轴。

3. 细胞群通信网络圆环图（``circle.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_chord_plot.png
   :width: 85%
   :align: center
   :alt: liana circle plot

解释：
从宏观视角呈现所有细胞类型之间的整体通信网络。圆环上的节点代表细胞群，连线的粗细与颜色代表细胞群之间交互对的数量和总体通信强度。用于识别在组织微环境中占据通信枢纽地位的细胞类型。

4. 通信推断结果对象（``{sample}.zarr`` / ``.h5ad``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
LIANA 生成的完整推断表格已写入对象的 ``.uns`` 字典中。高级用户可加载该对象，提取原始数值用于更复杂的定制化筛选或通过 Scanpy/SpatialData 生态进行其他二次开发。
