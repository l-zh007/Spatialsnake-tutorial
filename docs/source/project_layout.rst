项目结构与运行流程
==================

本章帮助你先建立全局认知，再进入每个分析步骤。

工作目录建议
------------

.. code-block:: text

   project_root/
   ├── data/
   │   ├── sampleA/
   │   └── sampleB/
   ├── sample.txt
   ├── results/
   └── config.yaml

样本清单 ``sample.txt`` 最小示例
------------------------------------------

单样本分析（非 visium_HD）：

.. code-block:: text

   sample_id    data_path
   S1           /abs/path/to/data/sampleA

多样本比较（非 visium_HD）：

.. code-block:: text

   sample_id    data_path                      group
   S1           /abs/path/to/data/sampleA      Control
   S2           /abs/path/to/data/sampleB      Treat

visium_HD 示例：

.. code-block:: text

   sample_id    data_path                      bin    group
   HD1          /abs/path/to/data/HD_sample1   8     A
   HD2          /abs/path/to/data/HD_sample2   8     B

一图理解阶段顺序
----------------

.. code-block:: text

   integrate -> preprocess -> clustering -> annotion_help -> annotion -> advance_analysis -> compare_stage

常见 ``--option`` 对应关系
--------------------------

.. list-table:: 分析阶段说明
   :header-rows: 1
   :widths: 20 80

   * - option
     - 作用
   * - integrate
     - 读取各平台原始数据并标准化输出统一对象
   * - preprocess
     - 质控过滤、归一化、批次处理与降维准备
   * - clustering
     - 聚类与聚类可视化
   * - annotion_help
     - marker 与富集提示，辅助人工判读
   * - annotion
     - 人工标注或算法注释
   * - advance_analysis
     - 下游高级模块，如 CellPhoneDB、PySCENIC、LIANA
   * - compare_stage
     - 多样本差异比较与 CellChat 比较

.. note::

   ``useful_tool`` 不属于主流程阶段，可在任意阶段用于切分（splitting）、合并（merge）和格式转换（transform）。
