数据整合（Ingesting）
=========================

``run_type: visium`` 这里我们使用   等人的 visium HD  数据进行全过程的使用演示，若您存在别的空转数据和多样本请跳转到对应页面进行Ingesting部分的运行。

配置文件详解请见 :doc:`../config_reference/integrate_yaml`。

若您仅仅想依照我们的教程，使用示例数据对Spatialsnake进行一个全面的了解
请在https://www.10xgenomics.com/platforms/visium/product-family/dataset-human-crc  中下载示例数据 Visium HD, Sample P2 CRC

在Download in browser中下载Binned outputs 解压在刚刚的data/目录下,以 Conlon_cancer_P1 为目录名

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


数据内容
--------------------------------

Visium HD 数据根据网格分辨率进行分块，每个分块目录下包含表达矩阵和空间信息，其分辨率包括2um,8um,16um。
我们使用其中的 ``square_008um`` 目录进行演示。

目录结构示例
------------

.. code-block:: text

  project_root/ (当前工作目录文件夹)
   ├── data/ (存放你的原始数据)
   │   ├── sampleA/
   │   └── sampleB/
   ├── sample.txt (重要样本参数文件)
   ├── results/ (存放分析结果,自动生成)
   └── <analysis_option>.yaml (配置文件 可选)

   data/
   └── Conlon_cancer_P1/
       └── binned_outputs/
           └── square_008um/
               ├── filtered_feature_bc_matrix.h5
               └── spatial/
                   ├── tissue_positions.parquet
                   ├── scalefactors_json.json
                   └── tissue_lowres_image.png

sample.txt 示例
---------------

single_analysis（第三列是 bin，自动补零成 3 位） 请确保样本名称和你的data目录下存放数据的文件夹名称对应相同：

.. code-block:: text
  
   sample_id input_path bin
   Conlon_cancer_P1 data/Conlon_cancer_P1 8


Run the command (make sure the sample.txt file is in your current working directory)
-------------------------------------------------------------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option integrate

读取后结果结构
--------------

.. code-block:: text

   results/
   ├── Conlon_cancer_P1_008um/
       └── integrate/
           ├── Conlon_cancer_P1.zarr #  zarr 格式数据
           ├── total.png  # 总表达量分布直方图
           ├── total_umi_by_sample.png # 每个样本的总 UMI 分布直方图
           ├── total_genes_by_sample.png  # 每个样本的总基因分布直方图
           ├── genes_by_sample.png  # 每个样本的线粒体基因分布直方图
           └── scatter.png  # 总表达量与基因数散点图

How to explore the results of Ingesting?
--------------------------------

核心输出
~~~~~~~~

- 主对象：``results/<sample>_<bin>um/integrate/<sample>.zarr``  
  这是后续 ``preprocess``、``clustering`` 等步骤直接读取的标准化对象，包含表达矩阵、空间坐标与样本注释信息。
- 质控图：同目录下的 ``total.png``、``total_umi_by_sample.png``、``total_genes_by_sample.png``、``genes_by_sample.png``、``scatter.png``  
  这些图由流程自动生成，用于帮助您在“过滤前”先理解样本整体状态。


细节探寻
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``total.png`` （总体分布图）

   - 图中主要对应两个分布：每个 spot/cell 的总转录本数（``total_counts``）与检测到的基因数（``n_genes_by_counts``）。
   - 若分布极端偏向低值，通常提示文库深度不足或组织区域信号较弱。
   - 若出现“非常长的右尾”，常见于局部高表达区域，不一定是错误，但建议后续结合空间位置复核。

2. ``total_umi_by_sample.png`` （按样本比较总 UMI）

   - 使用 ``log1p_total_counts`` 按 ``sample`` 分组绘制小提琴图。
   - 图中红线（约在 4 与 8）是经验参考线，用于快速感知低信号与高信号区间。
   - 若某一组样本整体显著低于其他样本，后续比较分析中需警惕“测序深度差异驱动的假阳性”。

3. ``total_genes_by_sample.png`` （按样本比较基因复杂度）

   - 使用 ``log1p_n_genes_by_counts`` 展示每个样本的检测基因数分布。
   - 基因数整体偏低，通常意味着有效转录信息不足；偏高且离散很大，则可能存在组织异质性或区域混合。
   - 这张图与 UMI 图联合判断，能帮助您区分“低深度”与“低复杂度”两类问题。

4. ``genes_by_sample.png`` （线粒体相关信号）

   - 使用 ``log1p_total_counts_mt`` 绘制，反映线粒体相关计数水平。
   - 线粒体信号整体偏高时，常见于低质量细胞/spot 比例升高或局部应激状态。
   - 该图用于帮助设置后续 ``preprocess`` 阶段的 ``mt_threshold``，不是在本步骤直接删除数据。

5. ``scatter.png`` （综合关系散点图）

   - 横轴：``log1p_total_counts_mt``；纵轴：``log1p_n_genes_by_counts``；颜色：``pct_counts_mt``。
   - 若出现“高线粒体比例 + 低基因数”的聚集区域，通常是优先关注的低质量群体。
   - 若大部分点形成连续、平滑分布，通常说明数据质量结构较稳定，可进入下一步过滤与标准化。


结果图展示（占位符）
~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: visium hd result placeholder

   Visium HD ``integrate`` 阶段结果示意图（占位符）。



请继续探索 :doc:`preprocess`。