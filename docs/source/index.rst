Spatialsnake 空间转录组实战教程
========================================

Spatialsnake 是一个用于空间转录组自动化分析Pipeline.

　我们的工具基于 python 依赖于scverver生态,使用spatialdata将不同平台空间转录组数据转换为统一的对象格式 ``zarr``.
您只需进行命令行和参数的简单配置即可上手,我们提供了从数据读取、预处理、分群、注释到下游分析的完整且多样性的分析流程.
spatialsnake的易操作性和可重复性极大的加快了分析和研究速度, 帮助您快速上手空转分析, 避免了复杂代码的编写和环境配置.

.. note::

   教程默认你已具备简单的 Linux 命令行基础。
   所有示例命令均可按需替换路径与样本名后直接运行。
   我们希望无论您的背景和经验水平,都能通过本教程快速上手空间转录组分析，通过scverver生态进行数据处理和分析！

教程目录
--------

.. toctree::
   :maxdepth: 2
   :caption: 分析准备

   environment_setup
   usage

.. toctree::
   :maxdepth: 2
   :caption: 核心流程

   data_input/index
   core_analysis/index
   annotation/index
   subcluster_annotation/index
   integration_analysis/multi_sample_integration
   useful_tool/index
   downstream_analysis/index

.. toctree::
   :maxdepth: 1
   :caption: 参考

   api
   config_reference/index
