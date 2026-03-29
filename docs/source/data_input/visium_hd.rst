Visium HD 输入教程
==================

``run_type: visium HD`` 这里我们使用 10xgenomics 官网公开数据集 中的 CRC P2 数据集进行演示

link: https://www.10xgenomics.com/platforms/visium/product-family/dataset-human-crc


在Download in browser中下载Binned outputs 通过 ``tar -xzf`` 解压在刚刚的data/目录下,以 ``Colon_Cancer_P2`` 为目录名

必需文件清单
------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - 文件名/通配
     - 必选
     - 格式
     - 说明
   * - ``binned_outputs/square_{bin}um/spatial/tissue_positions.parquet``
     - 是
     - Parquet
     - bin 级坐标信息
   * - ``binned_outputs/square_{bin}um/spatial/scalefactors_json.json``
     - 是
     - JSON
     - 图像缩放系数
   * - ``binned_outputs/square_{bin}um/spatial/tissue_lowres_image.png``
     - 是
     - PNG
     - 低分辨率组织图像
   * - ``binned_outputs/square_{bin}um/filtered_feature_bc_matrix.h5`` 或 ``binned_outputs/square_{bin}um/raw_feature_bc_matrix.h5``
     - 是
     - H5
     - 主表达矩阵
   * - ``binned_outputs/square_{bin}um/cell_feature_matrix.h5`` / ``filtered_feature_cell_matrix.h5`` / ``raw_feature_cell_matrix.h5``
     - 否
     - H5
     - 兼容候选矩阵名

文件来源与获取方式
------------------------

- 官方下载：10x Visium HD 输出目录（含 ``binned_outputs``）。
- 实验输出：平台下游流程导出的 ``square_XXXum`` 目录。
- 占位符写法：先填 ``data/S1`` 与 bin 数值，后续替换为真实目录与分辨率。


数据内容
--------------------------------

Visium HD 数据根据网格分辨率进行分块，每个分块目录下包含表达矩阵和空间信息，其分辨率包括2um,8um,16um。
我们使用其中的 ``square_008um`` 目录进行演示。

目录结构示例
------------

.. code-block:: text

  project_root/ (当前工作目录文件夹)
   ├── data/ (存放你的原始数据)
   │   └── Colon_Cancer_P2/
   ├── sample.txt (重要样本参数文件)
   ├── results/ (存放分析结果,自动生成)
   └── <analysis_option>.yaml (配置文件 可选)

   data/
   └── Colon_Cancer_P2/
       └── binned_outputs/
           └── square_008um/
               ├── filtered_feature_bc_matrix.h5
               └── spatial/
                   ├── tissue_positions.parquet
                   ├── scalefactors_json.json
                   ├── tissue_hires_image.png
                   └── tissue_lowres_image.png

sample.txt 示例
---------------

在我们的工具中 sample.txt是重要的文件输入参数配置文本,用于存放读取样本名或源文件路径
对于示例数据我们使用single_analysis通道分析 需要指定分辨率（第三列是 bin，自动补零成 3 位） 请确保样本名称和你的data目录下存放数据的文件夹名称对应相同：

.. code-block:: text
  
   sample_id input_path bin
   Colon_Cancer_P2 data/Colon_Cancer_P2 8


Run the command (make sure the sample.txt file is in your current working directory)
-------------------------------------------------------------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option integrate

结果文件层次
--------------

.. code-block:: text

   results/ (存在于project_root工作目录中)
   ├── Colon_Cancer_P2_008um/
       └── integrate/
           ├── Colon_Cancer_P2.zarr #  zarr 格式数据
           ├── total.png  # 总表达量分布直方图
           ├── total_umi_by_sample.png # 每个样本的总 UMI 分布直方图
           ├── total_genes_by_sample.png  # 每个样本的总基因分布直方图
           ├── genes_by_sample.png  # 每个样本的线粒体基因分布直方图
           └── scatter.png  # 总表达量与基因数散点图

How to explore the results of Ingesting?
----------------------------------------

核心输出
~~~~~~~~

- 主对象：``results/<sample>_<bin>um/integrate/<sample>.zarr``  
  这是后续 ``preprocess``、``clustering`` 等步骤直接读取的标准化对象，包含表达矩阵、空间坐标与样本注释信息。
- 质控图：同目录下的 ``total.png``、``total_umi_by_sample.png``、``total_genes_by_sample.png``、``genes_by_sample.png``、``scatter.png``  
  这些图由流程自动生成，用于帮助您在“过滤前”先理解样本整体状态。


细节探寻
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``total.png`` （总体分布图）

   - 这张图用于先看样本整体“有没有信号”，是读取阶段最先看的质量总览图。
   - 若大部分数据都堆在低值区，通常说明有效信号偏弱，后续预处理时要更谨慎设阈值。
   - 若少量点明显偏高，常见于局部高活性区域，不必直接判定为异常，建议结合空间图一起判断。

2. ``total_umi_by_sample.png`` （按样本比较总 UMI）

   - 这张图用于比较不同样本的信号强度是否在同一量级。
   - 若某一样本整体明显偏低，后续跨样本比较时容易受技术差异影响。
   - 看到样本间差距较大时，建议在后续步骤重点关注批次与归一化效果。

3. ``total_genes_by_sample.png`` （按样本比较基因复杂度）

   - 这张图反映“每个样本能检测到多少基因”，可理解为信息丰富度。
   - 若整体偏低，常提示数据复杂度不足；若离散很大，常说明样本内部差异较强。
   - 建议与上一张 UMI 图一起读，避免单看一张图就下结论。

4. ``genes_by_sample.png`` （线粒体相关信号）

   - 这张图帮助判断样本是否存在较高比例的潜在低质量点位。
   - 若整体偏高，后续预处理中通常需要更认真评估过滤强度。
   - 读取阶段主要是“发现风险”，真正过滤在下一步进行。

5. ``scatter.png`` （综合关系散点图）

   - 这张图适合定位“可疑点群”，尤其是低基因数且线粒体比例偏高的区域。
   - 若大部分点分布连续、没有明显割裂，通常说明整体结构较稳定。
   - 若出现明显异常团块，建议在预处理阶段先小步试探过滤参数。


结果图展示
~~~~~~~~~~

这里我们发现示例数据的小提琴中存在部分cell 表达量极低 甚至不表达,根据这里我们可以在下一步骤中进行过滤.

.. figure:: /_static/images/total_umi_by_sample.png
   :width: 85%
   :align: center
   :alt: ingesting total umi by sample


.. figure:: /_static/images/total_genes_by_sample.png
   :width: 85%
   :align: center
   :alt: ingesting total genes by sample



If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration`.
else continue your analysis :doc:`core_analysis/index`
