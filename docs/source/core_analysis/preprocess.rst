预处理（preprocess）
=====================

在 ``Ingesting`` 步骤完成之后 ``preprocess`` 用于空间转录组数据的质量控制、过滤、标准化与降维准备。

对于空间转录组数据,由于测序技术的误差和dropout,在预处理阶段我们通常需要对数据进行过滤,以去除低质量的基因和spot(cell)，并进行标准化处理，如总量标准化、对数转换等。
同时,我们还可以根据数据的高变基因特征进行选择,以减少噪声对后续分析的影响，同时也可以根据数据的批次效应进行校正，以提高分析的准确性，同时也可以根据数据的样本间差异进行校正，以提高分析的准确性。


处理逻辑概述
------------
1. 计算 QC 指标，并基于阈值进行基因/spot(cell)过滤。
2. 进行总量标准化与对数转换。
3. 根据设置执行高变基因选择（可选）。
4. 执行缩放与 PCA，并可在多样本场景进行批次效应校正。
5. 输出过滤后的对象，并保存预处理阶段的质控图。

总之，此步骤是对测序所得到的 spot x gene 基因表达矩阵进行质量控制、过滤、标准化与降维准备，以提高后续分析的准确性和效率。

.. note::

   若您的数据并非Visium HD平台或为多样本整合数据 请阅读完后查看文末,学习不同平台和不同样本数量下的输入与输出的差异。
   同理,将sample.txt样本文件中的样本名称更换为您自身数据的样本即可得到相同的结果，在此之前请确保您的数据已经严格根据对应平台的要求进行了读取和设置。

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess
   spatialsnake compare_analysis sample.txt visium --option=preprocess

运行可选的参数设置(命令行版)
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--min_cells`` / ``--min_genes``
     - ``3`` / ``200``
     - 控制基因与 spot(cell) 过滤阈值
   * - ``--mt_threshold``
     - ``40``
     - 线粒体占比过滤阈值
   * - ``--batch_method``
     - ``harmony``
     - 多样本整合时用于批次校正
   * - ``--n_top_genes``
     - ``3000``
     - 高变基因数量
   * - ``--n_comps``
     - ``50``
     - PCA 维度数
   * - ``--variable``
     - ``True``
     - 是否执行高变基因选择
   * - ``--NEIGHBORS``
     - ``10``
     - 邻域图参数
   * - ``--sketch`` / ``--sample_rate``
     - ``True`` / ``0.30``
     - 大样本抽样分析设置

以上命令为 我们精心选取的一些常用参数设置可直接通过命令行设置,若您对空间转录组有一定的了解，想进行参数的设置，可直接在命令行中添加参数 如 ``--min_cells 5`` 以空格隔开。加入到命令中即可。

运行可选的参数设置(配置文件版)
------------------------------------------------------------
若您已经熟练掌握 Spatialsnake, 且对空间转录组参数设置有一定的了解, 或您想了解更多参数设置

请参考配置文件并根据下述说明进行设置  :doc:`../config_reference/preprocess_yaml`。。

可运行下列命令进行yaml文件获取

.. code-block:: bash

   spatialsnake produce-file --option=preprocess

在yaml文件中,您可以根据自己的需求进行参数设置,每个文件注释都有详细的说明,请根据自己的需求进行修改，或更方便的，您可在文档中查看 【yaml解释】。

配置完成后在命令行使用configfile加入配置文件路径

运行最终运行命令
----------------------------

.. code-block:: bash

   # 确保您的yaml文件与sample.txt在当前同一工作目录下
   spatialsnake single_analysis sample.txt visium --option=preprocess --configfile preprocess.yaml


结果文件结构
------------

当前示例为 ``visium_HD`` 单样本预处理。完成运行后，建议优先检查 ``filter_{sample}.zarr`` 是否生成，再结合质控图判断阈值设置是否合理。

.. code-block:: text

   results/
   └── Conlon_cancer_P1_008um/
       └── preprocess/
           ├── filter_Conlon_cancer_P1.zarr # 过滤后的zarr对象
           ├── Conlon_cancer_P1filtered_Total_UMI.png # 过滤后的UMI分布图
           ├── Conlon_cancer_P1filtered_Total_Genes.png # 过滤后的基因数分布图
           ├── Conlon_cancer_P1_Mitochondrial_Genes.png # 线粒体基因占比图
           ├── Conlon_cancer_P1_scatter.png # 过滤后的UMI与基因数散点图
           ├── Conlon_cancer_P1pca_variance_ratio.png # PCA方差解释度图
           ├── Conlon_cancer_P1_highly_variable.png # 高变基因选择图

其中，``filter_{sample}.zarr`` 为后续聚类与注释的核心输入对象；其余图像用于评估 UMI 分布、基因数分布、线粒体比例、离群点与 PCA 解释度。若关闭高变基因选择或抽样流程，则对应文件不会生成。


多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------
在特定位置根据自身数据平台和样本数量更换不同的命令参数即可，其他基本不变

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - 场景
     - 推荐命令
   * - 单样本（Visium HD，本节演示）
     - ``spatialsnake single_analysis sample.txt visium_HD --option=preprocess``
   * - 单样本（常规 zarr 平台：将visium_HD更改为您所使用的平台数据字段即可）
     - ``spatialsnake single_analysis sample.txt xenium --option=preprocess``
   * - 多样本联合预处理 将channel改为compare_analysis 整合分析
     - ``spatialsnake compare_analysis sample.txt visium_HD --option=preprocess``


重要参数设置的差异
--------------------------------------------


多样本整合时，我们可能需要对不同的样本进行不同的参数设置，如不同的 ``min_cells``, ``min_genes``, ``mt_threshold`` 等。
所以我们可以在sample.txt中为每个样本添加对应的参数设置，工具会自动读取参数并分类过滤

.. code-block:: text

   sample    input_path                 group  min_cells min_genes mt_threshold
   Colon_Cancer_P2   data/Colon_Cancer_P2   Tumor  50  50  30
   Colon_Normal_P5  data/Colon_Normal_P5 Normal  50  50  30

其他参数(请根据自身需要进行设置)

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - 参数类别
     - 单样本建议
     - 多样本或跨条件建议
   * - harmony 批次校正
     - 一般保持默认或关闭
     - 若样本间存在明显技术偏差，可启用 ``harmony`` 或 ``BBkNN`` 进行批次校正，以减少跨样本差异对聚类结果的影响。
   * - 抽样策略（``sketch/sample_rate``）
     - 数据规模较小时通常不需要
     - 超大规模联合对象可先小比例抽样迭代，再回到全量结果复核,若您发现运行速度极慢，可考虑增加使用此参数。


输入输出结构的差异
------------------
完成 ``Ingesting`` 后，通常可直接复用同一份 ``sample.txt`` 进入预处理。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 分析模式
     - 输入
     - 输出
   * - single_analysis（常规 zarr 类型）
     - ``sample.txt`` 至少包含 ``sample_id input_path``；输入对象为 ``results/{sample}/integrate/{sample}.zarr``
     - ``results/{sample}/preprocess/filter_{sample}.zarr``
   * - single_analysis（visium_HD）
     - ``sample.txt`` 至少包含 ``sample_id input_path bin``；输入对象为 ``results/{sample}_{bin}um/integrate/{sample}.zarr``
     - ``results/{sample}_{bin}um/preprocess/filter_{sample}.zarr``
   * - single_analysis（slide_seq）
     - ``sample.txt`` 至少包含 ``sample_id input_path``；输入对象为 ``results/{sample}/integrate/{sample}.h5ad``
     - ``results/{sample}/preprocess/filter_{sample}.h5ad``
   * - compare_analysis
     - ``sample.txt`` 至少包含 ``sample_id input_path group``（visium_HD 需额外 ``bin``）；输入对象为 ``results/merge_data/integrate/concatenated_sdata``
     - ``results/merge_data/preprocess/filter_concatenated_sdata``


How to explore the results of preprocess?
----------------------------------------------------------------

核心输出
~~~~~~~~

- 主对象：``results/{sample}_{bin}um/preprocess/filter_{sample}.zarr``
  这是后续 ``clustering`` 直接读取的预处理对象，包含过滤后的表达矩阵与元数据（如 ``region``、``cell_id``）。
- 质控图：``{sample}filtered_Total_UMI.png``、``{sample}filtered_Total_Genes.png``、``{sample}_Mitochondrial_Genes.png``、``{sample}_scatter.png``、``{sample}pca_variance_ratio.png``
  这些图由预处理脚本自动输出，用于判断过滤阈值是否合理。
- 可选输出：``{sample}_highly_variable.png`` 与 ``sketch.h5ad``
  分别对应高变基因选择（``variable=True``）与抽样流程（``sketch=True``）。


细节探寻
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. {sample}filtered_Total_UMI.png（总 UMI 分布）

   - 脚本使用 ``log1p_total_counts`` 绘制按 ``region`` 分组的小提琴图，并在 y=4 与 y=8 画参考线。
   - 若大部分区域显著低于下参考线，通常提示测序深度偏浅或捕获效率偏低。
   - 若不同样本间中位数差距过大，后续可重点评估批次校正（``batch_method``）。

2. {sample}filtered_Total_Genes.png（检测基因数分布）

   - 对应 ``log1p_n_genes_by_counts`` 的分组小提琴图。
   - 若分布整体偏低，常见于低复杂度 spot/cell 比例较高。
   - 若出现异常长尾高值，建议后续结合空间位置判断是否存在局部异常区域。

3. {sample}_Mitochondrial_Genes.png（线粒体信号分布）

   - 对应 ``log1p_total_counts_mt`` 的分组小提琴图。
   - 该图主要服务于 ``mt_threshold`` 的合理性评估。
   - 若某一组线粒体信号整体偏高，可在复核后小步收紧阈值，避免一次性过度过滤。

4. {sample}_scatter.png（综合散点图）

   - 横轴：``total_counts``；纵轴：``n_genes_by_counts``；颜色：``pct_counts_mt``。
   - 若出现“低基因数 + 高线粒体比例”的聚集点群，通常是优先关注的低质量群体。
   - 该图建议与前三张分布图联合阅读，而不是单独下结论。

5. {sample}_highly_variable.png（高变基因图，可选）

   - 仅在 ``variable=True`` 时生成；脚本随后会将对象限制到 ``highly_variable`` 基因集合。
   - 该图用于检查高变基因筛选是否处于合理范围。
   - 若您以稳健分群为目标，可先保持默认 ``n_top_genes``，再在后续聚类中微调。

6. {sample}pca_variance_ratio.png 与终端推荐 PC 数

   - 该图展示前 20 个主成分的方差解释趋势。
   - 终端会输出 ``******* recommand pcs : <N>``，用于指导 ``clustering`` 阶段的 ``pcs`` 设定。
   - 实操中建议测试 ``N``、``N-5``、``N+5`` 三组参数，再比较聚类稳定性。


结果图展示（占位符）
~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/data_input/result_placeholder.svg
   :width: 85%
   :align: center
   :alt: preprocess result placeholder

   ``preprocess`` 阶段结果示意图（占位符）。


请继续探索 :doc:`clustering`。
