模块 6：细胞通讯网络（cellchat）
=================================

``cellchat`` 用于从细胞类型间配体-受体关系推断细胞通讯网络，并量化通讯数量、强度与通路信息流。
在空间模式下，流程会结合细胞/spot 空间距离计算通讯概率，因此建议提供缩放因子文件以获得更稳定的空间距离标定。

本模块支持单样本与多样本整合，也支持单细胞输入：

1. 多样本整合仅建议用于**相同实验处理条件**下的生物学重复样本。
2. 若需比较不同实验条件，请先分别运行本模块，再在后续 ``compare_analysis`` 的 ``compare_cellchat`` 中进行差异比较。
3. 单细胞输入可通过 ``is_single_cell=True`` 启用，不依赖空间距离参数。

我们将使用 ``Colon_Cancer_P2_008um.h5ad`` 数据集进行 cellchat 分析。请先提前将reannotation后的数据转换为传统h5ad格式以节省内存消耗

.. code-block:: bash
   spatialsnake useful_tool --option=transform results/Colon_Cancer_P2_008um/reannotation/Colon_Cancer_P2_008um.zarr --transform_from=zarr --transform_to=h5ad


运行步骤与内容
--------------

1. **读取输入与数据结构转换**
   自动识别 ``.h5ad`` 或 ``.rds`` 输入，并整理为 CellChat 可用对象，同时按 ``celltype_col`` 建立细胞群分组。
2. **数据库选择与信号筛选**
   根据 ``species`` 选择 ``CellChatDB.human`` 或 ``CellChatDB.mouse``，并筛选 Secreted Signaling 相关信号集合。
3. **空间坐标与尺度校正（空间模式）**
   读取坐标后结合 ``scale_factors`` 或 ``scale_factors_list`` 进行尺度换算，并自动修正 ``scale.distance`` 到合理区间，避免距离尺度异常影响概率估计。
4. **通讯概率与通路层级推断**
   依次执行过表达基因/互作识别、通讯概率计算、低细胞数过滤、通路概率计算与网络聚合，得到细胞群间通讯主干结构。
5. **网络与机制解释**
   从细胞群网络、通路信息流、热图与 LR 统计多个维度描述通讯格局，支持后续机制挖掘与复现。

.. note::
   本模块只会输出基本的图和csv表文件来展示 运行数据集的基本L-R通讯情况,若想进行更深度的可视化 或者 在多样本情况下对不同实验条件对象进行配受体强度差异分析以及可视化请跳转 :doc:`step9_compare_stage_cellchat`
   在这个模块中我们将会进行更丰富以及个性化的结果展示,但此模块需要本章节的输出文件 cellchat.rds 作为元数据输入，请先完成本章节运行，若为不同实验条件下的多样本数据，请以
   分两次依次运行,此模块只支持同一实验条件即生物学重复的样本进行整合分析。

准备输入文件
------------

情景 1：单样本空间数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   input_path  scale_factor_path
   Colon_Cancer_P2_008um  results/Colon_Cancer_P2_008um/annotion/Colon_Cancer_P2.h5ad  results/Colon_Cancer_P2_008um/scale_factor.json

情景 2：多样本整合（仅相同实验条件生物学重复）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   input_path  scale_factor_path
   SampleA_Rep1  results/SampleA_Rep1/annotion/SampleA_Rep1.h5ad  results/SampleA_Rep1/scale_factor.json
   SampleA_Rep2  results/SampleA_Rep2/annotion/SampleA_Rep2.h5ad  results/SampleA_Rep2/scale_factor.json

情景 3：单细胞输入（非空间模式）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   input_path
   sc_sample   results/sc_sample/annotion/sc_sample.rds

说明：

1. 输入可为 ``.h5ad`` 或 ``.rds``，脚本自动识别格式。
2. 输入对象需包含细胞类型列（默认 ``celltype``）。
3. 多样本整合仅用于相同条件样本；跨条件比较请转 ``compare_cellchat``。
4. 空间模式建议提供 scale factor 文件；单细胞模式可不提供。


运行可选的参数设置(配置文件版)
------------------------------------------------------------
配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。


.. list-table::
   :header-rows: 1
   :widths: 24 24 52

   * - 参数
     - 常用值
     - 作用
   * - ``runpipe``
     - ``cellchat``
     - 进入 cellchat 分支
   * - ``celltype_col``
     - ``celltype``
     - 细胞类型列名
   * - ``species``
     - ``human`` / ``mouse``
     - 选择通讯数据库物种
   * - ``assay``
     - ``Spatial``
     - 分析类型标签
   * - ``min_cells``
     - ``10``
     - 过滤细胞数量过少的群体
   * - ``workers``
     - ``32``
     - 并行线程数
   * - ``scale_factors``
     - ``results/S1/scale_factor.json``
     - 单样本空间尺度文件，用于距离换算
   * - ``scale_factors_list``
     - ``sf1.json,sf2.json``
     - 多样本时按样本顺序提供尺度文件列表
   * - ``sample_names``
     - ``SampleA_Rep1,SampleA_Rep2``
     - 与 ``scale_factors_list`` 一一对应的样本名
   * - ``spot_size``
     - ``65``
     - 多样本空间尺度标准化参考直径
   * - ``trim``
     - ``0.1``
     - truncatedMean 截尾比例，影响稳健性
   * - ``interaction_length``
     - ``150``
     - 空间通讯距离阈值
   * - ``is_single_cell``
     - ``False``
     - ``True`` 时按单细胞模式运行，不使用空间距离

.. code-block:: bash

   celltype_col: "celltype"
   assay: "Spatial"  # 指定你的分析策略
   species: "human"
   min_cells: 10
   workers: 32
   is_single_cell: FALSE
   trim: 0.1
   interaction_length: 250


Run the command
------------------------------

.. code-block:: bash
   #单样本
   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat
   #多样本
   spatialsnake compare_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat


单样本与多样本的结果差异
------------------------

1. 单样本与多样本都会输出网络图、信息流、热图与 LR 统计表。
2. 多样本整合结果反映“同条件重复样本合并后”的整体通讯格局，不用于直接表达跨条件差异。
3. 若需比较条件 A 与条件 B，请先分别运行 cellchat，再进入 ``compare_cellchat`` 做差异比较。

结果文件结构
------------

.. code-block:: text

   results/
   └── {sample}/
       └── cellchat/
           ├── cellchat.rds
           ├── {sample}_cellchat_network.png
           ├── {sample}_cellchat_network.pdf
           ├── {sample}_cellchat_infoflow_bar.png
           ├── {sample}_cellchat_count_heatmap.png
           ├── {sample}_cellchat_heatmap.png
           ├── {sample}_cellchat_signaling_role_network.png
           ├── {sample}_cellchat_signaling_role_scatter.png
           ├── {sample}_cellchat_signaling_role_outgoing.png
           ├── {sample}_cellchat_signaling_role_incoming.png
           ├── {sample}_cellchat_stats.csv
           ├── {sample}_cellchat_lr.csv
           ├── {sample}_cellchat_lr_summary.csv
           ├── {sample}_cellchat_pathway_pairs.csv
           ├── {sample}_cellchat_pathway_summary.csv
           └── {sample}_cellchat_pathway_net.csv

图表与结果解释
--------------

1. 网络总览图（``{sample}_cellchat_network.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_network.png
   :width: 85%
   :align: center
   :alt: cellchat network

解释：
左图展示细胞群间通讯数量，右图展示通讯强度。可先快速识别通讯枢纽细胞群与主要发送/接收关系。

2. 信息流条形图（``{sample}_cellchat_infoflow_bar.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_infoflow_bar.png
   :width: 85%
   :align: center
   :alt: cellchat info flow

解释：
用于比较不同通路的信息流强弱，帮助优先锁定最活跃或最具生物学意义的通讯通路。

3. 通讯热图（``{sample}_cellchat_count_heatmap.png`` / ``{sample}_cellchat_heatmap.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_cellchat_heatmap.png
   :width: 85%
   :align: center
   :alt: cellchat heatmap

解释：
``count_heatmap`` 反映细胞群通讯数量，``cellchat_heatmap`` 反映通讯权重（强度）。两者结合可区分“连接多但弱”与“连接少但强”的通讯模式。

4. 信号角色图（``{sample}_cellchat_signaling_role_*.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
自动选取一个可用通路，分别输出 signaling role network / scatter / outgoing / incoming 图，用于快速观察各细胞群在该通路中的发送与接收角色分布。

5. LR 明细与聚合统计（``*_cellchat_lr.csv`` / ``*_cellchat_lr_summary.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
``lr.csv`` 提供逐条配体-受体证据，``lr_summary.csv`` 提供按 LR 对聚合后的强度与显著性统计，是机制阐释与复现分析的关键依据。
