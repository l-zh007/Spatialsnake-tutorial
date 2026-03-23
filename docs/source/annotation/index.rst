细胞注释模块
============

本模块对应 ``option=annotion`` 下不同 ``anno_algorithm`` 分支,为用户提供了多种注释算法,包括手动注释、重新注释、cell2location、RCTD等。
请确保您已经完成preprocess,clustering和annotation_help流程,并获得了注释辅助文件。

统一注释配置模板详解请见 :doc:`../config_reference/annotion_yaml`。


对于注释方法的选择我们建议用户根据自己的需求和数据特点进行选择。
若您对细胞类型的注释比较熟悉,且数据量较小,则手动注释可能是一个不错的选择。
若您的数据量较大,或对注释结果有较高的要求,则可以考虑使用cell2location或RCTD等方法。

cell2location适用于低分辨率的空间转录组数据,而RCTD适用于高分辨率的空间转录组数据。

对于配套单细胞数据，若您做的是多模态转录组分析，可以使用自己测序的单细胞数据进行注释。
若您没有自己的单细胞数据,则可以考虑使用公开的单细胞数据集进行注释。

但请确保公开数据集的质量和可靠性,并根据自己的需求进行筛选，我们需要您提供其细胞类型注释列名和注释结果的存储路径。

.. toctree::
   :maxdepth: 1

   mannul
   cell2location
   RCTD
