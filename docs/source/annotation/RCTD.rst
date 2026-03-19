算法注释（RCTD）
================

``RCTD`` 用于基于参考单细胞数据对空间位点进行细胞类型解卷积。Spatialsnake 对应实现为 ``workflow/rules/RCTD.smk`` 与 ``workflow/scripts/RCTD.R``。

配置文件详解请见 :doc:`../config_reference/annotion_yaml`。

处理逻辑概述
------------
1. 从 ``sample.txt`` 读取空间对象路径与单细胞参考路径。
2. 在单细胞对象中提取细胞类型标签，构建 RCTD 参考。
3. 在空间对象上运行 ``create.RCTD`` 与 ``run.RCTD`` 完成解卷积。
4. 导出主结果表、权重矩阵、可视化图与补充统计文件。

该流程适合用于将“空间位点”映射为“细胞类型构成”，并可直接输出用于下游分析与汇报的结果文件。

准备输入文件
------------
推荐将 ``sample.txt`` 组织为以下格式：

.. code-block:: text

   sample_id   input_path                                      sc_reference
   SampleA     results/SampleA/clustering/SampleA.zarr         data/reference_sc.h5ad

说明：

1. ``input_path`` 为待解卷积的空间对象路径，建议优先使用上游标准流程输出对象。
2. ``sc_reference`` 为参考单细胞对象（通常为 ``.h5ad`` 或 ``.rds``），且必须包含细胞类型列。
3. 细胞类型列默认读取 ``celltype``，如使用其他列名可在配置文件中设置 ``cell_type_col``。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=RCTD --max_cores 16

运行可选的参数设置(命令行版)
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--anno_algorithm``
     - ``RCTD``
     - 指定注释算法为 RCTD（核心参数）
   * - ``--max_cores``
     - ``16``
     - 设置 RCTD 并行核数，影响运行速度与资源占用

对于 RCTD 分支，命令行直接可控的核心参数主要是以上两项；其余算法参数建议通过配置文件管理，便于复现与多次回调。

运行可选的参数设置(配置文件版)
------------------------------------------------------------
先生成注释流程配置模板：

.. code-block:: bash

   spatialsnake produce-file --option=annotion

随后在 ``annotion.yaml`` 中重点调整 RCTD 参数：

.. list-table::
   :header-rows: 1
   :widths: 26 20 54

   * - 参数
     - 默认值
     - 作用
   * - ``RCTD_mode``
     - ``doublet``
     - RCTD 运行模式（常用 ``doublet`` 或 ``full``）
   * - ``cell_type_col``
     - ``celltype``
     - 单细胞参考对象中用于提供细胞类型标签的列名
   * - ``group_by``
     - ``sample``
     - 结果统计图中用于分组展示的元数据列
   * - ``max_cores``
     - ``8``
     - RCTD 并行核数，配置文件中的默认值

运行最终运行命令吧
----------------------------

.. code-block:: bash

   # 确保 annotion.yaml 与 sample.txt 位于当前工作目录
   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=RCTD --configfile annotion.yaml

结果文件结构
------------

完成运行后，核心输出目录通常为 ``results/{sample}/RCTD/``：

.. code-block:: text

   results/
   └── {sample}/
       └── RCTD/
           ├── {sample}_RCTD_results.csv
           ├── {sample}_RCTD_weights.csv
           ├── {sample}.zarr/
           ├── {sample}_RCTD_spatial_plot.png
           ├── {sample}_RCTD_seurat.rds
           ├── {sample}_RCTD_sample_dist_plot.png
           ├── {sample}_RCTD_cluster_plot.png
           ├── {sample}_RCTD_heatmap.pdf
           └── {sample}_RCTD_spot_class_bar.png

其中，``{sample}_RCTD_results.csv`` 与 ``{sample}_RCTD_weights.csv`` 是最关键的解卷积结果；``{sample}.zarr`` 与各类图像文件用于空间展示与结果复核。

输入输出结构说明
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 阶段
     - 输入
     - 输出
   * - RCTD 主计算
     - 空间对象（``input_path``）+ 单细胞参考（``sc_reference``）
     - ``{sample}_RCTD_results.csv`` 与 ``{sample}_RCTD_weights.csv``
   * - 可视化与对象回写
     - RCTD 权重矩阵 + 空间对象
     - ``{sample}.zarr`` 与 ``{sample}_RCTD_spatial_plot.png`` 等图件

分析结果解释与实用建议
--------------------------------

1. 主结果表（``{sample}_RCTD_results.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（文件占位）：

.. code-block:: text

   [在此插入文件路径：results/.../RCTD/{sample}_RCTD_results.csv]

解释：
该表记录每个空间位点的主要细胞类型判定（如 ``first_type``）及相关解卷积信息，是后续统计和空间解释的主依据。

建议：
优先检查主要细胞类型是否符合组织学常识；若大面积出现不合理类型，先检查参考单细胞 ``cell_type_col`` 是否设置正确。

2. 权重矩阵（``{sample}_RCTD_weights.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（文件占位）：

.. code-block:: text

   [在此插入文件路径：results/.../RCTD/{sample}_RCTD_weights.csv]

解释：
该文件给出每个空间位点在不同细胞类型上的归一化权重，是评估混合成分和细胞比例变化的核心数据。

建议：
可结合空间位置与 marker 表达交叉验证。若多数位点权重过于平均，通常提示参考数据分辨率不足或类型定义过粗。

3. 空间图与分布统计（``{sample}_RCTD_spatial_plot.png`` 等）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/annotation/RCTD/{sample}_RCTD_spatial_plot.png]
   [在此插入图片路径：/_static/images/annotation/RCTD/{sample}_RCTD_spot_class_bar.png]

解释：
空间图用于直观看细胞类型在组织中的分布，柱状图和热图用于比较不同分组或类别下的组成差异。

建议：
重点关注空间连续性与组织结构一致性。若图中出现大面积孤立噪点或异常聚集，建议回查上游聚类对象质量与参考数据标注粒度。

结果检查与下一步
----------------
进入后续流程前，建议至少确认以下四点：

1. ``{sample}_RCTD_results.csv`` 与 ``{sample}_RCTD_weights.csv`` 均已生成且可正常读取。
2. 结果表中关键列（如 ``first_type``）无大规模缺失。
3. 空间分布图与组织结构趋势一致，无明显系统性偏差。
4. 分组统计图可解释且与生物学先验基本一致。

若结果不稳定，建议按“参考细胞类型列设置 → RCTD_mode → max_cores 与输入质量”顺序逐步回调并重跑。
