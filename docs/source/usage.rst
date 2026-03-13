使用总览
========

本页给出一条最短可跑通路径，帮助你快速理解 Spatialsnake 的运行方式。

.. _quick_start:

5 分钟认识流程
--------------

Spatialsnake 的主流程按分析阶段拆分为：

1. ``integrate``：读取原始空间转录组数据并标准化到统一对象
2. ``preprocess``：质控、过滤、归一化与降维准备
3. ``clustering``：聚类与可视化
4. ``annotion_help``：自动 marker 与富集提示
5. ``annotion``：人工或算法注释
6. ``advance_analysis``：下游高级分析（如细胞通讯、调控网络等）
7. ``compare_stage``：多样本差异与通讯比较

你可以选择：

- ``single_analysis``：单样本分析
- ``compare_analysis``：多样本联合比较分析

此外提供旁路工具：

- ``useful_tool --option=splitting``：切分对象
- ``useful_tool --option=merge``：合并对象
- ``useful_tool --option=transform``：格式转换

一键式命令风格
--------------

命令格式统一为：

.. code-block:: bash

   spatialsnake <channel> <INPUT_FILE> <TYPE> --option=<step>

参数说明：

- ``<channel>``：``single_analysis`` 或 ``compare_analysis``
- ``<INPUT_FILE>``：样本清单，通常是 ``sample.txt``
- ``<TYPE>``：数据类型，如 ``visium``、``xenium``、``Merfish``、``slide_seq``、``visium_HD``
- ``--option``：当前要执行的分析阶段

最小可跑示例
------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=integrate
   spatialsnake single_analysis sample.txt visium --option=preprocess
   spatialsnake single_analysis sample.txt visium --option=clustering
   spatialsnake single_analysis sample.txt visium --option=annotion_help
   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=mannul

推荐下一步阅读 :doc:`environment_setup`、:doc:`data_input/index` 与 :doc:`core_analysis/index`。
