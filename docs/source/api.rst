参数与命令速查
==============

本页用于快速查找常用命令、关键参数和推荐取值。

命令骨架
--------

.. code-block:: bash

   spatialsnake <channel> <INPUT_FILE> <TYPE> --option=<step> [更多参数]

核心参数
--------

.. list-table:: 核心参数说明
   :header-rows: 1
   :widths: 20 20 60

   * - 参数
     - 示例
     - 说明
   * - ``<channel>``
     - ``single_analysis``
     - 运行模式，可选 ``single_analysis`` 或 ``compare_analysis``
   * - ``<INPUT_FILE>``
     - ``sample.txt``
     - 样本清单文件，定义样本名与数据路径
   * - ``<TYPE>``
     - ``visium``
     - 数据类型：``visium`` / ``visium_segment`` / ``visium_HD`` / ``xenium`` / ``Merfish`` / ``slide_seq``
   * - ``--option``
     - ``clustering``
     - 分析阶段，如 integrate、preprocess、clustering、annotion_help、annotion、advance_analysis

高频阶段参数
------------

.. list-table:: 常用参数与推荐设置
   :header-rows: 1
   :widths: 20 20 60

   * - 阶段
     - 参数
     - 典型用法
   * - preprocess
     - ``--min_cells --min_genes --mt_threshold``
     - 根据组织质量调整过滤阈值
   * - clustering
     - ``--cluster_algorithm --resolution --pcs``
     - 优先用 ``leiden``，再按分群粒度调 ``resolution``
   * - annotion
     - ``--anno_algorithm --annotation-file``
     - 先用 ``mannul``，再尝试 ``reannotation`` / ``cell2Location`` / ``RCTD``
   * - advance_analysis
     - ``--runpipe --threads --workers``
     - 选择下游模块，如 ``cellPhoneDB`` / ``pysenic`` / ``liana``
   * - useful_tool
     - ``--option=splitting|merge|transform``
     - 主流程外的数据切分、合并、格式转换

示例命令片段
------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --batch_method=harmony
   spatialsnake single_analysis sample.txt xenium --option=clustering --cluster_algorithm=leiden --resolution=0.6
   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellPhoneDB --threads=16
   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=sample
   spatialsnake useful_tool --option=merge results/S1/annotion/S1.zarr results/S2/annotion/S2.zarr --merge_by=sample
