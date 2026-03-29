Visium Segment 输入教程
=======================

``run_type: visium_segment`` 这里我们使用 10xgenomics 官网公开数据集 中的 CRC P2 数据集的细胞分割数据进行演示,此数据由spaceranger v4自动生成

link: https://cf.10xgenomics.com/supp/spatial-exp/analysis-workshop/multisample_raw_data.tar.gz

在Download in browser中下载Segmented outputs 通过 ``tar -xzf`` 解压在刚刚的data/目录下,以 ``Colon_Cancer_P2`` 为目录名存储所有数据,结构如下文.


必需文件清单
------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - 文件名/通配
     - 必选
     - 格式
     - 说明
   * - ``segmented_outputs/spatial/tissue_hires_image.png``
     - 是
     - PNG
     - 分割坐标对应的高分辨率图像
   * - ``segmented_outputs/spatial/scalefactors_json.json``
     - 是
     - JSON
     - 图像缩放系数
   * - ``segmented_outputs/cell_segmentations.geojson``
     - 是
     - GeoJSON
     - 细胞分割多边形
   * - ``segmented_outputs/filtered_feature_bc_matrix.h5`` 或 ``segmented_outputs/raw_feature_bc_matrix.h5``
     - 是
     - H5
     - 主表达矩阵
   * - ``segmented_outputs/cell_feature_matrix.h5`` / ``segmented_outputs/filtered_feature_cell_matrix.h5`` / ``segmented_outputs/raw_feature_cell_matrix.h5``
     - 否
     - H5
     - 兼容候选矩阵名

文件来源与获取方式
------------------------

- 官方下载：10x Visium + segmentation 流程导出的 ``segmented_outputs``。
- 实验输出：图像分割流程产物。
- 占位符写法：先写 ``data/S1``，等你整理好后替换为真实样本目录。


目录结构示例
------------

.. code-block:: text

   data/
   └── colon_Cancer_P2/
       └── segmented_outputs/
           ├── filtered_feature_bc_matrix.h5
           ├── cell_segmentations.geojson
           └── spatial/
               ├── tissue_hires_image.png
               └── scalefactors_json.json

sample.txt 示例
---------------

single_analysis：

.. code-block:: text

   sample_id input_path
   colon_Cancer_P2 data/colon_Cancer_P2


Run the command (make sure the sample.txt file is in your current working directory)
-------------------------------------------------------------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_segment --option integrate

结果文件层次
--------------

.. code-block:: text

   results/ (存在于project_root工作目录中)
   ├── colon_Cancer_P2/
       └── integrate/
           ├── colon_Cancer_P2.zarr #  zarr 格式数据
           ├── total.png  # 总表达量分布直方图
           ├── total_umi_by_sample.png # 每个样本的总 UMI 分布直方图
           ├── total_genes_by_sample.png  # 每个样本的总基因分布直方图
           ├── genes_by_sample.png  # 每个样本的线粒体基因分布直方图
           └── scatter.png  # 总表达量与基因数散点图

输出解释
--------------------

- 主输出：``results/<sample>/integrate/<sample>.zarr``。
- 比较分析附加输出：``results/merge_data/integrate/concatenated_sdata``。
- 附加 QC 图：读取脚本会在 ``integrate`` 目录写入 5 张质控图；这些文件不在 Snakemake ``output`` 声明中，但会实际生成。



If you want to run multi-sample integration analysis, please jump to :doc:`/integration_analysis/multi_sample_integration`.
else continue to :doc:`data_input/index`