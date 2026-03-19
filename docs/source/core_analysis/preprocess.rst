预处理（preprocess）
=====================

在 ``Ingesting`` 步骤完成之后 ``preprocess`` 用于空间转录组数据的质量控制、过滤、标准化与降维准备。
对于空间转录组数据,由于测序技术的误差和dropout,在预处理阶段我们通常需要对数据进行过滤,以去除低质量的基因和spot(cell)，并进行标准化处理，如总量标准化、对数转换等。
同时,我们还可以根据数据的高变基因特征进行选择,以减少噪声对后续分析的影响，同时也可以根据数据的批次效应进行校正，以提高分析的准确性，同时也可以根据数据的样本间差异进行校正，以提高分析的准确性。

配置文件详解请见 :doc:`../config_reference/preprocess_yaml`。

处理逻辑概述
------------
1. 计算 QC 指标，并基于阈值进行基因/spot(cell)过滤。
2. 进行总量标准化与对数转换。
3. 根据设置执行高变基因选择（可选）。
4. 执行缩放与 PCA，并可在多样本场景进行批次效应校正。
5. 输出过滤后的对象，并保存预处理阶段的质控图。

总之，此步骤是对测序所得到的 spot x gene 基因表达矩阵进行质量控制、过滤、标准化与降维准备，以提高后续分析的准确性和效率。

.. note::

   若您的数据并非Visium HD平台或为多样本整合数据 请阅读完后查看文末,学习不同平台和样本数量下的输入与输出的差异。


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

以上命令为 我们精心选取的一些常用参数设置,若您对空间转录组有一定的了解，想进行参数的设置，可直接在命令行中添加参数 如 ``--min_cells 5`` 以空格隔开。加入到命令中即可。

运行可选的参数设置(配置文件版)
------------------------------------------------------------
若您已经熟练掌握 Spatialsnake, 且对空间转录组参数设置有一定的了解, 或您想了解更多参数设置, 请参考 [yaml解释]。

运行下列命令进行yaml文件获取

.. code-block:: bash

   spatialsnake produce-file --option=preprocess

在yaml文件中,您可以根据自己的需求进行参数设置,每个文件注释都有详细的说明,请根据自己的需求进行修改，或更方便的，您可在文档中查看 【yaml解释】。

运行最终运行命令吧
----------------------------

.. code-block:: bash

   # 确保您的yaml文件与sample.txt在当前同一工作目录下
   spatialsnake single_analysis sample.txt visium --option=preprocess --config preprocess.yaml


结果文件结构
------------

当前示例为 ``visium_HD`` 单样本预处理。完成运行后，建议优先检查 ``filter_{sample}.zarr`` 是否生成，再结合质控图判断阈值设置是否合理。

.. code-block:: text

   results/
   └── {sample}_{bin}um/
       └── preprocess/
           ├── filter_{sample}.zarr/
           ├── {sample}filtered_Total_UMI.png
           ├── {sample}filtered_Total_Genes.png
           ├── {sample}_Mitochondrial_Genes.png
           ├── {sample}_scatter.png
           ├── {sample}pca_variance_ratio.png
           ├── {sample}_highly_variable.png
           └── sketch.h5ad

其中，``filter_{sample}.zarr`` 为后续聚类与注释的核心输入对象；其余图像用于评估 UMI 分布、基因数分布、线粒体比例、离群点与 PCA 解释度。若关闭高变基因选择或抽样流程，则对应文件不会生成。


多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------

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


多样本整合时，于单样本类似``sample.txt`` 需要包含分组列。

.. code-block:: text

   sample    input_path                 group  min_cells min_genes mt_threshold
   Colon_Cancer_P2   data/Colon_Cancer_P2   Tumor  50  50  30
   Colon_Normal_P5  data/Colon_Normal_P5 Normal  50  50  30

其他参数

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


分析结果解释与实用建议
--------------------------------

1. 总 UMI 分布（``{sample}filtered_Total_UMI.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/core_analysis/preprocess/filtered_Total_UMI.png]

解释：
不同样本（或区域）中位数过低通常提示捕获效率或测序深度不足；分布过宽常提示组织异质性较强或存在批次差异。若低 UMI 区域占比过高，后续聚类容易受到低质量点干扰。

建议：
若低 UMI 区域集中出现，可适度提高 ``min_genes`` 或 ``min_cells``；若整体信号较弱但组织真实稀疏，优先小步调整阈值并结合后续聚类稳定性复核，避免过度过滤。

2. 基因数分布（``{sample}filtered_Total_Genes.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/core_analysis/preprocess/filtered_Total_Genes.png]

解释：
基因数偏低常对应低复杂度 spot/cell；若出现长尾极高值，需警惕局部异常信号或潜在双细胞/分割异常。多样本时若某一组整体偏移明显，后续需重点评估批次校正必要性。

建议：
单样本可围绕分布主体设置阈值；多样本建议先使用相对保守阈值保证群体可比性，再在下游按目标亚群进行细化筛选。

3. 线粒体比例（``{sample}_Mitochondrial_Genes.png``）与计数-基因散点（``{sample}_scatter.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/core_analysis/preprocess/Mitochondrial_Genes.png]
   [在此插入图片路径：/_static/images/core_analysis/preprocess/scatter.png]

解释：
线粒体比例显著偏高通常提示细胞损伤或低质量区域。散点图中若出现“高 counts 但低 genes”或“高 mt% 聚集”的异常群，需要结合组织背景判断是否应过滤。

建议：
``mt_threshold`` 不建议一次性大幅收紧。优先采用梯度调整（例如分阶段下调）并观察异常群是否稳定消失，再确定最终阈值。

4. 高变基因图（``{sample}_highly_variable.png``，当 ``variable=True`` 时）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/core_analysis/preprocess/highly_variable.png]

解释：
高变基因选择用于提升后续降维与聚类对生物学变异的敏感性。若高变基因数量过少，可能损失细粒度结构；过多则可能引入噪声。

建议：
通常以 ``n_top_genes=2000-4000`` 作为起始区间。跨样本比较时建议各批次保持一致策略，以减少由特征选择差异引入的偏移。

5. PCA 方差解释图（``{sample}pca_variance_ratio.png``）与推荐 PC 数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/core_analysis/preprocess/pca_variance_ratio.png]
   [终端日志占位：******* recommand pcs : <N>]

解释：
PCA 方差解释图用于观察主成分信息衰减趋势；终端日志会给出推荐 PC 数（``recommand pcs``），用于辅助确定后续邻域图与聚类使用的维度范围。

建议：
- 若拐点与推荐值接近，可优先采用推荐 PC 数作为基线方案。
- 若研究目标偏向稀有亚群识别，可在推荐值基础上适度上调并比较聚类稳定性。
- 若目标偏向大类群稳健分层，可在推荐值附近小范围下调以降低噪声敏感性。
- 建议在 clustering 阶段以“推荐值、推荐值±5”进行并行试验，综合轮廓清晰度、空间连续性与 marker 一致性选择最终维度。
