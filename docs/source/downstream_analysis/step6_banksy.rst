模块 5:空间聚类增强(banksy)
==============================

``banksy`` 在表达特征基础上引入空间邻域权重进行聚类，重点用于提升空间域边界与组织结构一致性。
我们使用注释好的示例数据进行banksy空间域的聚类分析以挖掘不同的空间域结构。

配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。

运行步骤与内容
--------------

1. **读取输入与空间坐标校验**
   自动读取输入对象(支持 ``.zarr`` 或 ``.h5ad``)，并检查是否包含有效的空间坐标信息。若缺失 ``spatial`` 层，则尝试从观测指标中提取并构建空间坐标系。
2. **构建空间邻域图与权重矩阵**
   根据设定的几何邻居数(``k_geom``)和权重衰减方式（如高斯衰减），初始化 BANKSY 邻域图，计算每个细胞/spot 的邻域特征，生成包含空间信息的 BANKSY 加权矩阵。
3. **降维与空间增强聚类**
   对加权特征矩阵执行 PCA 降维和 UMAP 投影，随后在指定的 ``lambda_list``（空间权重）和 ``resolution``（分辨率）下进行 Leiden 聚类，得到融合了空间结构信息的聚类标签。
4. **性能评估与指标对比**
   若输入数据已包含细胞类型（``celltype``）注释，流程将自动执行无空间权重的标准聚类，并计算两种结果与已知注释的一致性指标（如 ARI、AMI、MCC），生成性能对比图表。
5. **结果可视化与导出**
   输出带有空间坐标的聚类散点图、指标对比条形图，以及汇总了所有参数组合聚类结果的 ``banksy_results.csv``，并将最终的最佳聚类标签写回对象中供后续复用。

准备输入文件
------------

``sample.txt`` 推荐格式：

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

输入要求：

1. 输入对象需具备空间坐标信息；缺失时流程会尝试从 ``array_row/array_col`` 自动构建。
2. 建议输入已注释对象（包含 ``celltype`` 列），以便自动输出空间聚类与已有注释的一致性评估对比图。


运行可选的参数设置
------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 24 52

   * - 参数
     - 常用值
     - 作用
   * - ``runpipe``
     - ``banksy``
     - 进入 banksy 分支
   * - ``k_geom``
     - ``15``
     - 邻域图几何邻居数，控制空间平滑范围
   * - ``max_m``
     - ``1``
     - 邻域阶数，越大越强调更远邻域信息
   * - ``nbr_weight_decay``
     - ``scaled_gaussian``
     - 邻域权重衰减方式
   * - ``n_comps``
     - ``[20]``
     - 降维主成分数量
   * - ``lambda_list``
     - ``[0.8]``
     - 空间信息权重，越大越偏空间结构
   * - ``RES``
     - ``[0.5]``
     - Leiden 分辨率列表，控制簇粒度


.. code-block:: bash

  k_geom: 15
  max_m: 1
  nbr_weight_decay: "scaled_gaussian"
  lambda_list: [0.8]

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=banksy


结果文件结构
------------

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

图表与结果解释
--------------

1. BANKSY 空间聚类结果图（``BANKSY-Results_*.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/BANKSY_scaled_gaussian_pc50_nc0.80_r0.50_full_figure.png
   :width: 85%
   :align: center
   :alt: banksy spatial clustering results

解释：
展示加入空间邻域权重后的聚类结果，颜色代表不同的空间域。该图重点用于验证空间域的连续性、边界的清晰度以及与组织形态学结构的一致性。

2. 组织原位散点图（``scatter.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/BANKSY-Nonspatial_nonspatial_pc50_nc0.00_r0.50_full_figure.png
   :width: 85%
   :align: center
   :alt: banksy tissue scatter

解释：
将已有注释（``celltype``）映射在空间坐标上，作为真实生物学结构的参考基准，用于与 BANKSY 聚类结果进行直观对比。

3. 无空间权重聚类对比图（``BANKSY-Results-Nonspatial_*.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
展示在空间权重为 0（即纯基于表达特征）的情况下的聚类结果，用于凸显加入空间信息后对聚类边界平滑度和噪声消除的提升效果。

4. 性能评估对比条形图（``bar.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/bar.png
   :width: 85%
   :align: center
   :alt: banksy metrics comparison

解释：
直观比较空间增强聚类与非空间聚类在 ARI、AMI 和 MCC 等指标上的得分差异。柱状图越高，说明该聚类方法得出的标签与真实细胞类型（或预期分区）的一致性越好。

5. 聚类标签汇总表（``banksy_results.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释：
保存不同参数组合（如不同 ``lambda`` 和 ``resolution``）下的所有聚类标签结果，是后续复现实验和进一步探索不同粒度空间域的核心数据表。
