Module 3: Cell-Cell Communication (liana)
=========================================

模块介绍
--------

尽管 Spatialsnake 已通过 :doc:`step2_cellphonedb` 与 CellChat 提供配体-受体分析功能，我们仍纳入 ``liana``，因为它提供了更广泛且更灵活的细胞通讯推断框架。
``liana`` 能通过统一接口运行多种配体-受体评分方法，并将结果写回分析对象，便于后续复用。
这种多方法整合设计可较单一算法提供更稳健的细胞间通讯视角。

需要注意的是，``liana`` 并不像显式空间约束方法那样直接建模空间距离。
若空间邻近性是生物学问题的核心，建议先将分析限制在较小 ROI 内，再在该子集上运行 ``liana``。

``liana`` 也适用于在相似实验条件下联合解释空间与单细胞数据，有助于比较不同模态中的通讯模式。

参数配置的完整说明请参见 :doc:`../config_reference/advance_analysis_yaml`。


基本 workflow
-------------

1. 读取输入对象并解析分组参数。
2. 根据所选方法运行 LIANA 通讯推断。
3. 过滤并汇总高置信度配体-受体相互作用。
4. 自动生成可视化汇总图。
5. 导出包含通讯结果的对象供下游分析使用。

具体而言，该流程会读取空间或单细胞对象（``.zarr`` 或 ``.h5ad``），提取指定的细胞类型注释列作为分组依据；随后根据配置运行 ``cellphonedb``、``connectome``、``cellchat`` 等 LIANA 方法，并结合资源数据库与表达阈值过滤低表达特征；之后保留高置信度的相互作用并将重要得分写入 ``.uns``；最终自动生成 dot plot、tile plot 以及在条件允许时的 circle plot。


基本运行步骤
------------

推荐的 ``sample.txt`` 格式如下。若使用单细胞数据，只需将路径替换为相应 ``.h5ad`` 文件即可：

.. code-block:: text

   sample_id   input_path
   {sample_id} results/{sample_id}/annotation/{sample_id}.zarr

输入要求：

1. 输入对象应包含细胞类型注释列，通常为 ``celltype``。
2. 强烈建议使用已充分注释的对象，以保证发送者与接收者细胞群体在生物学上可解释。


step 1: ``sample.txt`` 配置文件
-------------------------------

准备包含样本 ID 与输入对象路径的 ``sample.txt`` 文件即可启动 LIANA 分析。


step 2: 参数选择与配置
----------------------

``advance_analysis.yaml`` 中常用且值得优先理解的参数包括：

.. list-table::
   :header-rows: 1
   :widths: 26 22 52

   * - Parameter
     - Typical values
     - Description
   * - ``runpipe``
     - ``liana``
     - 指定当前高级分析分支为 LIANA
   * - ``cellPhoneDB_input``
     - ``results/S1/annotation/S1.zarr``
     - 输入对象路径
   * - ``liana_method``
     - ``cellphonedb`` / ``connectome`` / ``cellchat``
     - 选择通讯评分方法
   * - ``liana_resource_name``
     - ``consensus``
     - 指定配体-受体资源数据库
   * - ``liana_expr_prop``
     - ``0.1``
     - 过滤低表达配体与受体时使用的表达比例阈值
   * - ``liana_min_cells``
     - ``5``
     - 每个细胞群体所需的最小细胞数
   * - ``liana_use_raw``
     - ``true``
     - 是否优先使用 ``adata.raw`` 中的表达矩阵
   * - ``celltype_col``
     - ``celltype``
     - 细胞类型分组所依据的列名

配置建议：

1. ``liana_method`` 是最核心的参数之一，决定通讯打分逻辑。若希望与经典分析流程保持一致，可优先使用 ``cellphonedb``；若希望进行多方法比较或从不同统计角度筛选候选相互作用，则可尝试其他方法。
2. ``liana_resource_name`` 决定配体-受体数据库来源。常规分析通常建议从 ``consensus`` 开始。
3. ``liana_expr_prop`` 与 ``liana_min_cells`` 共同决定过滤严格程度。若阈值过高，可能遗漏稀有但重要的信号；若过低，则可能引入噪声。
4. ``celltype_col`` 必须与输入对象中的实际注释列一致，否则无法正确构建发送者与接收者群体。

运行命令前，建议先确认 ``advance_analysis.yaml`` 中上述参数是否已与当前对象匹配。


step 3: 命令运行
----------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=liana


Demo 演示流程
-------------

鉴于liana为适用于单样本的分析软件包,对于空间转录组我们需尽量考虑样本中的细胞类型远近距离,对于整个样本并不适合liana的分析。
为了简单分析,在此我们使用reannotation步骤中的 Tumor细分zarr数据结果进行分析,可能对于此数据也并不适合,请根据实际情况调整。
根据您自己的数据进行拆分输入.

1. 准备输入对象
~~~~~~~~~~~~~~~

.. code-block:: text

   samples path_to_dir
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/reannotation/Colon_Cancer_P2_008um.zarr

2. 设置关键参数
~~~~~~~~~~~~~~~

优先确认 ``liana_method``、``liana_resource_name``、``liana_expr_prop``、``liana_min_cells`` 与 ``celltype_col``。这些参数决定方法选择、数据库来源、表达过滤强度以及分组逻辑。

3. 运行 LIANA
~~~~~~~~~~~~~

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=advance_analysis --runpipe=liana


附：支持的 ``liana_method`` 取值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当前流程直接支持以下方法名称：

1. ``cellphonedb``：基于均值表达与置换逻辑评估配体-受体显著性。
2. ``connectome``：更强调网络连通性与边强度。
3. ``natmi``：更关注细胞类型特异性的配体-受体特征。
4. ``singlecellsignalr``：使用 LRscore 风格排序进行快速优先级筛选。
5. ``cellchat``：在 LIANA 接口中采用类似 CellChat 的概率评分逻辑。
6. ``geometric_mean``：使用几何均值汇总，减弱极端值影响。
7. ``logfc``：更强调表达变化幅度，适合关注差异表达导向的分析场景。
8. ``rank_aggregate``：对多方法结果进行排序整合，得到共识性得分。
9. ``scseqcomm``：提供另一种统计视角以评估候选相互作用。

说明：

- ``log2fc`` 会自动映射为 ``logfc``。
- ``cellphone_db`` 会自动映射为 ``cellphonedb``。
- 其他方法名称会根据本地环境中的 LIANA 版本进行校验。


附：``liana_resource_name`` 选择建议
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``consensus``（默认）：
   为 LIANA 集成资源，适合多数常规分析与教程使用场景。
2. 其他资源名称：
   LIANA 可根据本地版本与安装资源切换不同数据库，当需要与特定论文或历史流程保持严格一致时可进行相应选择。

建议优先从 ``consensus`` 开始，仅在确有可比性需求时再切换到特定资源库。


结果展示与解读
--------------

Result file structure
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   results/
   └── liana_output/
       ├── {sample}.zarr
       ├── dotplot.png
       ├── tileplot.png
       └── circle.png

其中，``circle.png`` 仅在输入对象中的细胞类型标签能够与 LIANA 结果中的 source / target 标签稳定对应时生成；若映射不充分，流程会优先保留 ``dotplot`` 与 ``tileplot``，并跳过圆图以避免流程中断。


1. 配体-受体气泡图
~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_dot_plot.png
   :width: 85%
   :align: center
   :alt: liana dotplot

该图展示选定来源细胞与目标细胞之间的特定配体-受体相互作用。点大小通常反映显著性，例如负对数 p 值，而颜色反映相互作用强度，是机制导向解释中最重要的图之一。


2. 排名相互作用热图
~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_heatmap.png
   :width: 85%
   :align: center
   :alt: liana tileplot

该图突出全数据集或特定细胞对中排名靠前的配体-受体相互作用。填充颜色表示相互作用强度，有助于快速识别最值得关注的通讯轴。


3. 全局通讯圆图
~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_chord_plot.png
   :width: 85%
   :align: center
   :alt: liana circle plot

该图从整体上概括所有细胞类型之间的通讯网络。节点表示细胞群体，边的粗细与颜色反映相互作用数量及总体强度，尤其适用于识别组织微环境中的潜在通讯枢纽。


4. 通讯结果对象
~~~~~~~~~~~~~~~

完整的 LIANA 结果表通常写入结果对象的 ``.uns`` 槽中。高级用户可进一步加载该对象，提取原始数值结果，并在 Scanpy 或 SpatialData 生态中进行自定义筛选、可视化或扩展分析。
