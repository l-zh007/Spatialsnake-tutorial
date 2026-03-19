模块 5：空间聚类增强（banksy）
==============================

``banksy`` 在表达特征基础上引入空间邻域权重进行聚类，重点用于提升空间域边界与组织结构一致性。
对应实现为 ``workflow/rules/run_banksy.smk`` 与 ``workflow/scripts/banksy.py``。

配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。

处理逻辑概述
------------

1. 读取输入对象并检查/补齐空间坐标（``array_row``、``array_col``、``obsm['spatial']``）。
2. 计算 BANKSY 邻域图与加权特征矩阵。
3. 在给定 ``lambda`` 与 ``resolution`` 下运行 Leiden 聚类，写入 ``obs['spatial_cluster']``。
4. 输出 BANKSY 结果图、标签文件与更新后的对象。

准备输入文件
------------

``sample.txt`` 推荐格式：

.. code-block:: text

   sample_id   input_path
   S1          results/S1/annotion/S1.zarr

输入要求：

1. 输入对象需具备空间坐标信息；缺失时流程会尝试从 ``array_row/array_col`` 自动构建。
2. 建议输入已注释对象，便于输出聚类与 celltype 一致性指标图。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=banksy

运行可选的参数设置(配置文件版)
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

1. ``banksy_results.csv``：保存不同参数组合下的聚类标签，是后续复现实验的核心表。
2. ``BANKSY-Results`` 图：展示加入空间邻域后的聚类结果，重点看空间连续性与边界清晰度。
3. ``BANKSY-Results-Nonspatial`` 与 ``bar.png``：比较空间增强与非空间聚类的一致性指标（ARI/AMI/MCC）。
4. ``{sample}_banksy.zarr``：包含 ``spatial_cluster`` 的对象，可直接作为后续通讯/比较分析输入。
