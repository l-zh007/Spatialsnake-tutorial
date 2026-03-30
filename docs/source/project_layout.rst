How to use Spatialsnake?
=========================

如何使用命令行？
------------------------------
我们的命令行使用多通道流程, 主流程通道 工具流程通道 生成配置文件通道 安装包通道 帮助通道 版本通道。
 <> 表示必填参数 [] 表示可选参数 [options] 表示其他参数设置 参数需符合描述 例如是否前缀为 ``--`` 或 ``=``

.. code-block:: bash

  spatialsnake <command> <INPUT> <TYPE> [--option=<analysis_option>] [options] # 主流程通道
  spatialsnake useful_tool [--option=<ways>] <INPUT> [options] # 提供一些有用的工具
  spatialsnake produce-file [--option=<analysis_option>]  # 生成配置文件模板
  spatialsnake install-packages # 安装必要的R包
  spatialsnake (-h | --help)  # 查看帮助文档
  spatialsnake --version      # 查看版本号

参数间请用空格相隔
--------

- ``<command>``：主流程通道，根据分析策略选择 ``single_analysis`` 或 ``compare_analysis``
- ``<INPUT>``：输入样本文件。主流程中通常为 ``sample.txt``，通常存放着重要的分析样本id 和 分析数据路径 ``useful_tool`` 中为一个或多个数据对象路径。
- ``<TYPE>``：数据类型，支持 ``visium``、``visium_segment``、``visium_HD``、``xenium``、``Merfish``、``slide_seq``。
- ``--option=<analysis_option>``：分析模块选择，主流程为 ``integrate``、``preprocess``、``clustering``、``reclustering``、``annotion_help``、``annotion``、``advance_analysis``、``compare_stage``；工具流程为 ``splitting``、``merge``、``transform``。

[options] 其他参数设置
------------------------------

在空间转录组分析中存在多种重要的参数需要我们手动设置 这些参数直接影响分析结果的质量和可靠性 因此在使用Spatialsnake进行分析时 我们需要根据具体情况合理设置这些参数


1.直接通过--参数设置,例如下列命令 除了一般性命令，我们在末尾可以通过 ``--参数名称 参数数值``的方式加入

(哪些参数可用命令行设置? 使用 ``spatialsnake -h``查看) 

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess --min_cells=3 --min_genes=200 --mt_threshold=50
   spatialsnake compare_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat --celltype_col=celltype --threads=16
   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=ROI --roi_csv=roi_tables

参数文件（configfile）配置方法
-------------------------------

由于分析的参数众多,我们仅选择了最重要且常用的参数可供在命令行直接配置,对于其他参数我们可以使用 ``.yaml``文件配置


如何获取yaml文件?

.. code-block:: bash

   spatialsnake produce-file --option=preprocess
   spatialsnake produce-file --option=advance_analysis
   spatialsnake produce-file --option=splitting

将生成对应模板文件（如 ``preprocess.yaml``），可在此基础上修改。

查看yaml文件我们可以发现,每个yaml文件都在参数旁添加注释和默认参数 解释了参数的作用 我们希望您通过此可以快速理解每个参数的含义 掌握空间转录组分析
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   option: "preprocess"           # 分析阶段 与命令行--option一致
   channel: "compare_analysis"    # 分析模式 单样本或多样本比较
   run_type: "visium"             # 空间转录组平台类型
   sample_list: "sample.txt"      # 样本描述文件路径
   results_folder: "results"      # 结果输出根目录
   min_cells: 3                   # 每个样本最小细胞数 过滤掉小于此数的样本
   min_genes: 3                   # 每个样本最小基因数 过滤掉小于此数的样本
   mt_threshold: 80.0             # 线粒体基因阈值 过滤掉线粒体基因占比超过此阈值的细胞
   batch_method: "harmony"        # 批次校正方法 可选harmony或combat

通过 ``--configfile`` 修改配置后加入命令行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile preprocess.yaml
   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile preprocess.yaml --mt_threshold=60

.. note::
   通过 --configfile 配置的参数优先级低于直接使用命令行参数配置,例如第二条命令中的--mt_threshold 若preprocess.yaml也修改了数值,以 命令行中的60为最终输入
   初学者建议先使用命令行参数


请先进行工作目录准备(必做步骤)
------------

.. code-block:: text

   project_root/ (当前工作目录文件夹)
   ├── data/ (存放你的原始数据)
   │   ├── sampleA/ (样本数据)
   │   └── sampleB/
   ├── sample.txt (重要样本参数文件)
   ├── results/ (存放分析结果,自动生成)
   └── <analysis_option>.yaml (配置文件 可选)

样本清单 ``sample.txt`` 最小示例(后续会教学如何填写)
------------------------------------------

单样本分析（非 visium_HD）:

.. code-block:: text

   sample_id    data_path
   sampleA           /project_root/data/sampleA

多样本比较（非 visium_HD）：

.. code-block:: text

   sample_id    data_path                      group
   sampleA           /project_root/data/sampleA      Control
   sampleB           /project_root/data/sampleB      Treat

visium_HD 示例：

.. code-block:: text

   sample_id    data_path                      bin    group
   HD1          /project_root/data/HD_sample1   8     A
   HD2          /project_root/data/HD_sample2   8     B

Analysis Pipeline
------------------------------
空转分析的基本流程

.. code-block:: text

   integrate -> preprocess -> clustering -> annotion_help -> annotation -> advance_analysis -> compare_stage
                                                                      -> reclustering -> reannotation
``--option``
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

   ``useful_tool`` 不属于主流程阶段，可在任意阶段用于切分（splitting）、合并（merge）和格式转换（transform），若需使用请跳转 :doc:`useful_tool/index`。

Start your analysis
------------------------------------------------------------
我们推荐您使用我们提供的示例数据进行分析，以熟悉空转分析流程 :doc:`core_analysis/index`
若您想使用自己的空间转录组数据进行分析，请跳转 :doc:`data_input/index`
