Spatialsnake Pipeline for Spatial Transcriptomics
=============================================

Spatialsnake is an automated analysis pipeline for ``spatial transcriptomics`` analysis.

Implemented in ``Python`` on top of the ``scverse`` ecosystem, Spatialsnake uses SpatialData to convert spatial transcriptomics datasets from different platforms into a unified zarr-based object format.
This design provides a consistent computational framework from data ingestion through preprocessing, clustering, annotation, and downstream analysis, while preserving compatibility with platform-specific inputs.
By combining a command-line interface with workflow-based parameter control, Spatialsnake emphasizes reproducibility, operational clarity, and ease of adoption, allowing users to perform end-to-end spatial transcriptomics analysis without extensive custom scripting or repeated environment reconstruction.

.. note::

   此教程默认您已经具备简单的linux命令行操作基础,能很好的通过替换路径/参数/样本名称等,进行基础的命令 ``执行``操作,
   若您对空间转录组学分析的步骤不熟悉,请详细阅读教程中每个模块概要与解析
   Spatialsnake致力于打破生物信息学分析的技术壁垒，通过用户友好的命令行架构为所有技术背景的研究人员提供无障碍的分析入口，确保科学探索不受技术能力的限制。


Tutorial Contents
-----------------

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   environment_setup
   usage

.. toctree::
   :maxdepth: 1
   :caption: Data Ingestion

   data_input/index
   integration_analysis/multi_sample_integration

.. toctree::
   :maxdepth: 1
   :caption: Main Analysis

   core_analysis/index
   annotation/index
   subcluster_annotation/index
   downstream_analysis/index
   useful_tool/index

.. toctree::
   :maxdepth: 1
   :caption: Reference

   api
   config_reference/index
