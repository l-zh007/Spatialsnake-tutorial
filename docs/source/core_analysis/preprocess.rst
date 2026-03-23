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

对于示例数据我们选择--min_cells 100 --min_genes 100 --mt_threshold 30 作为默认参数设置,过滤掉UMI数小于100或基因数小于100的spot(cell)，以及线粒体基因占比大于30%的spot(cell)。

Run the command
------------------------------
.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --min_cells 100 --min_genes 100 --mt_threshold 30





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
   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --configfile preprocess.yaml


结果文件结构
------------

当前示例为 ``visium_HD`` 单样本预处理。完成运行后，建议优先检查 ``filter_{sample}.zarr`` 是否生成，再结合质控图判断阈值设置是否合理。

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── preprocess/
           ├── filter_Colon_Cancer_P2.zarr # 过滤后的zarr对象
           ├── Colon_Cancer_P2filtered_Total_UMI.png # 过滤后的UMI分布图
           ├── Colon_Cancer_P2filtered_Total_Genes.png # 过滤后的基因数分布图
           ├── Colon_Cancer_P2_Mitochondrial_Genes.png # 线粒体基因占比图
           ├── Colon_Cancer_P2_scatter.png # 过滤后的UMI与基因数散点图
           ├── Colon_Cancer_P2pca_variance_ratio.png # PCA方差解释度图
           └── Colon_Cancer_P2_highly_variable.png # 高变基因选择图

其中，``filter_{sample}.zarr`` 为后续聚类与注释的核心输入对象；其余图像用于评估 UMI 分布、基因数分布、线粒体比例、离群点与 PCA 解释度。若关闭高变基因选择或抽样流程，则对应文件不会生成。


多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------

若您使用的数据非Visium_HD平台,请将visium_HD更改为您所使用的平台数据字段即可。
.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess --min_cells 100 --min_genes 100 --mt_threshold 30

若您使用的数据为整合样本,请将channel改为compare_analysis 整合分析,同时sample.txt文件需符合前文教程中的格式路径
.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium_HD --option=preprocess

同理在末尾你也可以进行命令行型参数设置或者在yaml文件中进行参数设置,步骤和我们的演示数据一致。


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

1. {sample}filtered_Total_UMI.png（总 UMI 分布）

.. figure:: /_static/images/Colon_Cancer_P2filtered_Total_UMI.png
   :width: 85%
   :align: center
   :alt: preprocess umi plot

   过滤后 UMI 分布图,我们可以看到低质量的细胞已经被过滤

2. {sample}filtered_Total_Genes.png（检测基因数分布）

.. figure:: /_static/images/Colon_Cancer_P2filtered_Total_Genes.png
   :width: 85%
   :align: center
   :alt: preprocess genes plot

   过滤后基因数分布图。

   - 这张图反映过滤后每个区域的基因复杂度是否合理。
   - 若整体仍偏低，常提示有效信息不足，后续分群可能不稳定。
   - 若局部特别高，建议结合空间位置确认是否存在局部异常或特殊组织区。

6. {sample}pca_variance_ratio.png 与终端推荐 PC 数

   - 这张图用于判断“保留多少维度”更合适。
   - 曲线明显变缓的位置通常是较好的维度参考点。
   - 实操中可围绕推荐值做小范围对比，再选择最稳定的一组。

.. figure:: /_static/images/Colon_Cancer_P2pca_variance_ratio.png
   :width: 85%
   :align: center
   :alt: preprocess pca variance ratio

   PCA 方差解释度图：用于辅助确定后续聚类时的主成分维度范围,用户可以参考这一图和终端输出中的算法计算出的推荐pcs 来进行后续的pcs选择


3. {sample}_Mitochondrial_Genes.png(线粒体信号分布)

   - 这张图用于评估线粒体相关信号是否仍偏高。
   - 若某些区域整体偏高，通常需要在保证数据量的前提下适度收紧过滤策略。
   - 建议小步调整，不要一次性过滤过多，避免丢失真实生物信号。

4. {sample}_scatter.png（综合散点图）

   - 这张图帮助快速识别潜在低质量点群。
   - 重点观察“低基因数且线粒体比例偏高”的聚集区域。
   - 建议与前面三张分布图联合判断，结论更稳健。

5. {sample}_highly_variable.png（高变基因图，可选）

   - 这张图用于确认后续分群将聚焦于信息量更高的基因。
   - 若筛选范围过窄，可能丢失结构信息；范围过宽，则可能引入噪声。
   - 建议先使用默认设置，再根据聚类效果微调。



请继续探索 :doc:`clustering`。
