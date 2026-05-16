Module 5: Spatially Enhanced Clustering (banksy)
================================================

模块介绍
----

``banksy`` 在表达特征的基础上引入空间邻域加权，从而提升聚类结果与组织结构的一致性。
相较于仅依赖表达矩阵的传统聚类方法，BANKSY 更适合用于识别具有连续空间结构的组织 domain。
在本教程中，我们使用已完成注释的示例数据集，演示 BANKSY 如何更清晰地揭示空间 domain 结构。

参数配置的完整说明请参见 :doc:`../config_reference/advance_analysis_yaml`。


基本 workflow
-----------

1. 读取输入对象并检查空间坐标是否完整。
2. 构建 BANKSY 邻域图与空间加权矩阵。
3. 在加权特征矩阵上执行降维与空间增强聚类。
4. 若已存在参考注释，则与非空间基线聚类进行比较评估。
5. 输出图像、汇总表格与最佳聚类标签。

更具体地说，该流程会读取 ``.zarr`` 或 ``.h5ad`` 对象，并确认可用的空间坐标；若 ``spatial`` 层缺失，则尝试从其他坐标字段重建。随后根据 ``k_geom`` 与邻域衰减策略构建空间邻域图，生成结合邻域信息的加权特征；之后在不同 ``lambda_list`` 与分辨率参数下执行 PCA、UMAP 与 Leiden 聚类；若输入对象中已有 ``celltype`` 标签，还会同时运行非空间基线聚类，并通过 ARI、AMI 与 MCC 等指标进行比较。


基本运行步骤
------

推荐的 ``sample.txt`` 格式如下：

输入要求：

1. 输入对象应包含空间坐标信息。若缺失，流程会尝试利用 ``array_row`` 与 ``array_col`` 等字段进行重建。
2. 建议使用已包含 ``celltype`` 注释的对象，以便自动比较 BANKSY 结果与已有生物学标签之间的一致性。


step 1: ``sample.txt`` 配置文件
---------------------------

通常只需提供样本 ID 与输入对象路径即可开始运行 BANKSY 分析。

.. code-block:: bash

   sample_id   input_path
   {sample_id} results/{sample_id}/annotation/{sample_id}.zarr

step 2: 参数选择与配置
---------------

BANKSY 模块中最值得优先理解的参数如下：

.. list-table::
   :header-rows: 1
   :widths: 24 24 52

   * - Parameter
     - Typical values
     - Description
   * - ``runpipe``
     - ``banksy``
     - 指定当前高级分析分支为 BANKSY
   * - ``k_geom``
     - ``15``
     - 几何邻居数，决定空间平滑的局部范围
   * - ``max_m``
     - ``1``
     - 邻域阶数；数值越大，越强调更远距离的邻域信息
   * - ``nbr_weight_decay``
     - ``scaled_gaussian``
     - 邻域权重衰减策略，影响空间邻居对特征构建的贡献方式
   * - ``n_comps``
     - ``[20]``
     - 用于降维的主成分数量
   * - ``lambda_list``
     - ``[0.8]``
     - 空间加权系数；值越大，越强调空间结构信息
   * - ``RES``
     - ``[0.5]``
     - Leiden 聚类分辨率，控制聚类粒度

配置建议：

1. ``k_geom`` 与 ``lambda_list`` 是影响 BANKSY 结果最核心的两个参数。前者决定空间邻域范围，后者决定空间信息在聚类中的权重。
2. 若希望更强地突出组织空间连续性，可适当提高 ``lambda_list``；若更重视表达差异本身，则可降低其取值。
3. ``RES`` 会明显影响最终空间 domain 数量，应结合组织复杂度和下游解释需求进行选择。

示例配置如下：

.. code-block:: bash

  k_geom: 15
  max_m: 1
  nbr_weight_decay: "scaled_gaussian"
  lambda_list: [0.8]


step 3: 命令运行
------------

完成输入与参数设置后，可运行：

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=banksy


Demo 演示流程
---------

下面以已完成注释的示例对象为例，展示 BANKSY 的标准分析流程。

1. 准备输入对象
~~~~~~~~~

确认对象中存在空间坐标，并尽量保留 ``celltype`` 注释列，以便后续比较空间增强聚类与已有标注之间的一致性。

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

2. 设置关键参数
~~~~~~~~~

优先关注 ``k_geom``、``lambda_list`` 与 ``RES``。这些参数分别对应邻域范围、空间加权强度与聚类粒度，是决定结果形态的关键因素。
这里为了节省时间我们选择自带默认参数即可

3. 运行 BANKSY
~~~~~~~~~~~~

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=banksy


结果展示与解读
-------

Result file structure
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   results/
   └── banksy/
       ├── {sample}_banksy.zarr/
       ├── banksy_results/
       │   ├── banksy_results.csv
       │   ├── BANKSY-Results*.png/pdf
       │   ├── BANKSY-Results-Nonspatial*.png/pdf
       │   ├── scatter.png
       │   └── bar.png
       └── *_cell_clusters.csv


1. BANKSY 空间聚类图
~~~~~~~~~~~~~~~

.. figure:: /_static/images/BANKSY_scaled_gaussian_pc50_nc0.80_r0.50_full_figure.png
   :width: 85%
   :align: center
   :alt: banksy spatial clustering results

该图展示纳入空间邻域加权后的聚类结果。不同颜色对应不同空间 domain，主要用于评估空间区域的连续性、边界清晰度以及与组织形态结构的一致性。


2. 组织散点图
~~~~~~~~

.. figure:: /_static/images/BANKSY-Nonspatial_nonspatial_pc50_nc0.00_r0.50_full_figure.png
   :width: 85%
   :align: center
   :alt: banksy tissue scatter

该图将已有 ``celltype`` 注释重新映射回组织坐标中，为 BANKSY 聚类结果提供一个生物学参照。


3. 非空间聚类比较图
~~~~~~~~~~~

该图展示空间权重设为 0 时的聚类结果，即仅使用表达信息进行聚类。它有助于直观比较空间信息对边界平滑度与噪声抑制的提升程度。


4. 指标比较柱状图
~~~~~~~~~~

.. figure:: /_static/images/bar.png
   :width: 85%
   :align: center
   :alt: banksy metrics comparison

该柱状图基于 ARI、AMI 与 MCC 等指标比较空间增强聚类与非空间聚类的表现。数值越高，通常表示推断得到的聚类结果与参考细胞类型或预期组织结构的一致性越好。


5. 聚类标签汇总表
~~~~~~~~~~

该表保存所有测试参数组合下的聚类标签结果，例如不同 ``lambda`` 与 ``resolution`` 组合对应的输出，是比较不同空间 domain 粒度与保证结果可复现性的核心文件。
