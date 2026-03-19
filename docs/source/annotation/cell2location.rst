算法注释（cell2Location）
=========================

``cell2Location`` 用于将单细胞参考信息映射到空间位点，完成细胞类型比例估计与空间可视化。对应实现为 ``workflow/rules/cell2Location_run.smk``、``workflow/scripts/cell2Location.py`` 与 ``workflow/scripts/cell2locate_visualize.py``。

配置文件详解请见 :doc:`../config_reference/annotion_yaml`。

处理逻辑概述
------------
1. 读取空间对象（zarr）与参考单细胞对象（h5ad）。
2. 在参考数据上训练回归模型，学习细胞类型表达特征。
3. 在空间对象上拟合 cell2location 模型，估计每个位点的细胞类型丰度。
4. 回写结果并生成可视化对象、统计图和中间质控文件。

该流程会同时输出“可继续下游分析的结果对象”和“便于人工复核的图表文件”。

准备输入文件
------------
``cell2Location`` 运行时需要 ``sample.txt`` 同时提供空间对象与单细胞参考。推荐格式如下：

.. code-block:: text

   sample_id   input_path                                      sc_reference
   SampleA     results/SampleA/clustering/SampleA.zarr         data/reference_sc.h5ad

说明：

1. ``input_path`` 建议填写 ``clustering`` 或 ``reclustering`` 阶段输出的 ``.zarr`` 对象。
2. ``sc_reference`` 建议填写已完成细胞类型标注的 ``.h5ad`` 参考对象。
3. 当前实现按重计算负载设计为逐样本运行，建议一次只在 ``sample.txt`` 中放置一个样本。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=cell2Location

运行可选的参数设置(命令行版)
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--anno_algorithm``
     - ``cell2Location``
     - 指定注释算法为 cell2location（必填核心参数）
   * - ``--device``
     - ``cuda`` / ``cpu``
     - 控制模型训练设备，影响训练速度
   * - ``--image_type``
     - ``hires``
     - 指定空间图像图层用于渲染可视化
   * - ``--shape_type``
     - ``cell_boundaries``
     - 指定空间分割形状图层用于叠加展示
   * - ``--max_cores``
     - ``16``
     - 控制并行资源上限（流程级资源参数）

在命令行可直接追加参数，例如：

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=cell2Location --device cuda --image_type hires

运行可选的参数设置(配置文件版)
------------------------------------------------------------
``cell2Location`` 的训练轮次和先验参数主要通过配置文件管理。先生成模板：

.. code-block:: bash

   spatialsnake produce-file --option=annotion

然后在 ``annotion.yaml`` 中重点调整以下参数：

.. list-table::
   :header-rows: 1
   :widths: 26 20 54

   * - 参数
     - 默认值
     - 作用
   * - ``max_epochs_reference``
     - ``250``
     - 参考模型训练轮次，过低可能欠拟合
   * - ``remove_mt``
     - ``True``
     - 是否在建模前过滤线粒体基因
   * - ``N_cells_per_location``
     - ``30``
     - 空间位点的先验细胞数，影响丰度估计尺度
   * - ``max_epochs_st``
     - ``30000``
     - 空间模型训练轮次，决定收敛充分程度
   * - ``device``
     - ``cuda``
     - 训练设备，建议与命令行保持一致

运行最终运行命令吧
----------------------------

.. code-block:: bash

   # 确保 annotion.yaml 与 sample.txt 位于当前工作目录
   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=cell2Location --configfile annotion.yaml

结果文件结构
------------

完成后，核心结果通常位于 ``results/{sample}/cell2Location/``：

.. code-block:: text

   results/
   └── {sample}/
       └── cell2Location/
           ├── {sample}.zarr/
           ├── Cell2Loc_inf_aver.csv
           ├── Reference_model/
           ├── Spatial_model/
           ├── CoLocatedComb/
           ├── test.h5ad
           └── figure/
               ├── ELBO_sc_model.png
               ├── ELBO_spatial_model.png
               ├── QC_reference_reconstruction_accuracy.png
               ├── QC_reference_expression signatures_vs_avg_expression.png
               ├── QC_spatial_reconstruction_accuracy.png
               ├── each_celltype.png
               ├── factor_namescelltype.png
               ├── cluster_abundance_stacked_bar.png
               └── cluster_abundance_stats.csv

其中，``{sample}.zarr`` 为后续比较分析与可视化复用的主对象；``figure/`` 下文件用于检查训练收敛与空间映射质量；``Reference_model`` 与 ``Spatial_model`` 保存模型状态，便于复现实验。

输入输出结构说明
------------------
``cell2Location`` 会读取 ``sample.txt`` 中的两类输入并生成一个最终对象：

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 阶段
     - 输入
     - 输出
   * - 模型训练
     - input_path（空间 zarr 对象）+ sc_reference（单细胞 h5ad 对象）
     - results/{sample}/cell2Location/tem.zarr（流程中间对象）
   * - 可视化与回写
     - tem.zarr
     - results/{sample}/cell2Location/{sample}.zarr 与图表/统计文件

分析结果解释与实用建议
--------------------------------

1. 训练收敛曲线（``ELBO_sc_model.png`` 与 ``ELBO_spatial_model.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/annotation/cell2location/ELBO_sc_model.png]
   [在此插入图片路径：/_static/images/annotation/cell2location/ELBO_spatial_model.png]

解释：
ELBO 随迭代下降并趋于平稳，通常表示模型收敛良好；若持续剧烈波动或长期不下降，提示训练轮次、先验参数或输入质量需要调整。

建议：
优先检查 ``max_epochs_reference`` 与 ``max_epochs_st`` 是否过小；若曲线已稳定但结果噪声高，再回到输入对象检查预处理和聚类质量。

2. 细胞类型空间分布图（``each_celltype.png`` / ``factor_namescelltype.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/annotation/cell2location/each_celltype.png]
   [在此插入图片路径：/_static/images/annotation/cell2location/factor_namescelltype.png]

解释：
该类图用于查看不同细胞类型在组织中的空间富集模式，判断是否与组织结构和已知生物学先验一致。

建议：
重点关注“空间连续性”和“组织学一致性”。若出现大面积离散噪点，可考虑回调 ``N_cells_per_location`` 并复核参考单细胞注释质量。

3. 丰度统计结果（``cluster_abundance_stacked_bar.png`` / ``cluster_abundance_stats.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（文件占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/annotation/cell2location/cluster_abundance_stacked_bar.png]
   [在此插入文件路径：results/.../cell2Location/figure/cluster_abundance_stats.csv]

解释：
该结果展示各聚类区域中的细胞类型组成比例，适合用于区域比较、富集趋势判断与结果汇报。

建议：
将统计结果与聚类标签、marker 基因表达联合验证。若某些簇被单一类型异常主导，建议先排查输入参考是否类别不平衡。

结果检查与下一步
----------------
进入后续分析前建议完成以下核查：

1. ``results/{sample}/cell2Location/{sample}.zarr`` 已生成，且对象中可见 cell2location 丰度结果。
2. ELBO 曲线整体收敛，无明显异常震荡。
3. 空间分布图与组织结构基本一致，未出现大面积随机噪声区域。
4. 丰度统计结果与已知标记和聚类结果无明显冲突。

若任一项不满足，建议按“输入对象质量 → 参考单细胞标签 → 训练参数（轮次/先验）”的顺序逐步回调，再重新运行。
