Downstream Analysis Modules
================

在空间转录组分析中,我们虽然成功的完成了核心分析与注释,识别出了不同的细胞类型,但仍需根据研究问题选择合适的下游各种工具来得出更有意义的生物学结论。
在每个下游分析中,我们都提供了丰富的可视化结果,利用图表结合的方式,帮助研究人员更直观地理解数据,发现潜在的生物学机制,以及后续的可视化复现。

我们精心挑选了以下常用且经久不衰的空间转录组分析模块
----------------------------

1. 空间域和微环境探寻：关注空间域识别、微环境结构与组织空间模式。
2. 配受体分析：关注细胞间配体-受体通讯关系。
3. 细胞因子分析：关注调控因子活性与潜在功能状态。
4. 多样本对比分析：关注组间差异与跨样本通讯变化。

.. note::
   正如我们所知道的,空间转录组分析 甚至说转录组学 直至今日,都在不断的发展与完善,所开发的分析工具也在不断的更新与完善,所以我们仅提供最常用的分析模块,其他工具请参考相关文献
   我们目的是在当下,为您提供一个简单易用的空间转录组分析工具,帮助研究人员快速完成基础且冗杂的分析,专注于生物学机制的探寻与挖掘。
   我们只能尽可能保证我们的工具能够满足大多数研究问题的需求,但时代的车轮在不断的旋转,新的分析模块不断的涌现,我们也会不断的更新我们的工具,扩展常用的分析功能,与时代的步伐并进。


下游分析分为两类入口：

1. ``--option=advance_analysis``：使用 ``--runpipe=``运行（cellPhoneDB / pysenic / liana / cellcharter / banksy / cellchat）。
2. ``--option=compare_stage``：组间比较（ ``--runpipe=`` 进行 compare_gene 或 cellchat 比较）。


准备 ``sample.txt``
-------------------

我们的advance_analysis是一个多模块运行的步骤,您可以根据研究问题选择运行哪些模块,所以我们的sample.txt文件只需输入样本信息和对应模块的输入文件路径即可。

例如
.. code-block:: text

   sample_id   input_path
   S1          results/S1/annotion/S1.zarr


配置文件详解,配置方法与前文相同

- ``advance_analysis`` 参见 :doc:`../config_reference/advance_analysis_yaml`
- ``compare_stage`` 参见 :doc:`../config_reference/compare_stage_yaml`


统一命令入口
------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=<module>

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=<module>

我们的内容包含:

空间域和微环境探寻
~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   step5_cellcharter
   step6_banksy


配受体分析
~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   step2_cellphonedb
   step4_liana
   step7_cellchat


细胞因子分析
~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   step3_pysenic


多样本对比分析
~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   step8_compare_stage_deg
   step9_compare_stage_cellchat
