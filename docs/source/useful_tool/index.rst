旁路分析与实用工具
==================

本模块对应命令 ``spatialsnake useful_tool``，用于在主流程外进行数据重组与格式转换。

配置文件详解：

- splitting 参见 :doc:`../config_reference/splitting_yaml`
- merge 参见 :doc:`../config_reference/merge_yaml`
- transform 参见 :doc:`../config_reference/transform_yaml`

使用情景指南:

1.当您想对多个大类细胞进行亚群注释,需将其按照celltype拆分spatialdata对象,推荐使用 spliting ,其中内置了许多使用的拆分参数和方法。
2.当您需要根据 图像位置信息 样本信息 进行拆分 选取ROI 请使用splitting
3.若您想通过10x Genomics官方开发的 Loupe,Xenium Explorer 工具进行互作分析,您可以将套索选取后的csv文件导入spliting模块进行ROI的选取,也可以将我们切割后的csv信息进行输入获取更可观的可视化结果.

4.若您想将亚群细胞注释信息字段整合进原始大类数据spatialdata对象中,我们推荐用户将亚群注释同步输出的celltype_annotations.csv 与spatialdata对象路径同步输入 进行字段整合
5.同时我们也允许用户将两个子集或并行的spatialdata对象 根据样本列 cluster列 进行整合，输出为一个整合 zarr对象进行后续分析

6.我们的pipeline 是基于python进行编写的,所以我们的工具基本都选择在python生态下的软件包,当然，现在也存在多种空间转录组分析工具编写于R生态下，
所以我们提供了transform部分,用户可以进行zarr(Spatialdata)，h5ad(scanpy),rds(seurat) 三个数据格式的转换

我们的转换脚本适用于单样本数据与整合的多样本数据，单当转换数据量极高的空转对象 在转为seurat时会内存溢出，请谨慎使用，或使用原始矩阵进行转换

.. toctree::
   :maxdepth: 1

   splitting
   merge
   transform
