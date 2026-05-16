Module 4: Spatial Domain Modeling (cellcharter)
==============================================================================================

``cellcharter`` 通过联合利用基因表达信息与局部空间邻域结构，对组织中的空间 domain 进行建模，从而识别更符合组织结构的空间区域划分。
除空间 domain 识别外，该流程还结合 CellCharter 的 enrichment 分析，用于比较单样本内部或多样本之间的细胞类型富集模式。
在本教程中，我们使用已经完成注释的示例数据集演示空间 domain 建模流程。

该模块支持 GPU 加速；若仅在 CPU 环境下运行，整体耗时通常会显著增加。

参数配置的完整说明请参见 :doc:`../config_reference/advance_analysis_yaml`。


1. 读取并预处理输入对象。
2. 构建结合空间邻域信息的特征表示。
3. 在候选聚类数范围内评估稳定性，并选择最合适的空间 domain 数量。
4. 根据运行分支输出单样本或多样本比较结果。

更具体地说，该流程会读取 ``.zarr`` 或 ``.h5ad`` 对象，标准化表达矩阵并构建 ``counts`` 层；随后建立空间邻域图，将细胞或 spot 的自身表达与邻域上下文整合为 ``X_cellcharter`` 特征；之后在 ``(2, max_cluster)`` 范围内评估聚类稳定性，确定最终空间 domain 数量；最后根据单样本或多样本分析模式输出空间分区图、邻域富集图及比较性结果。

step 1: ``sample.txt`` 配置文件
------------------------------------------------------

推荐的 ``sample.txt`` 格式如下,将{sample_id}替换为你自己的样本id：

.. code-block:: bash

   sample_id   input_path
   {sample_id} results/{sample_id}/annotation/{sample_id}.zarr


输入要求：

1. 输入对象必须包含空间坐标信息，可存储于 ``obsm['spatial']`` 或其他可转换的等价字段中。
2. 建议使用已包含 ``celltype`` 注释的对象，以保证 enrichment 结果具有明确的生物学可解释性。
3. 若进行多样本比较分析，建议使用整合后的对象，并保留样本列与实验条件处理列/分组列，例如 ``sample_col=region`` 与 ``condition_col=condition`` (若您的数据通过spatialsnake整合 使用默认参数即可)。

Step 2: Parameter Selection and Configuration
------------------------------------------------------------------------------------------

在 CellCharter 模块中，以下参数通常最值得优先理解：

.. list-table::
   :header-rows: 1
   :widths: 28 18 54

   * - Parameter
     - Example
     - Description
   * - ``runpipe``
     - ``cellcharter``
     - 指定当前高级分析分支为 CellCharter
   * - ``max_cluster``
     - ``10``
     - 候选空间 domain 数量上限，用于自动评估最优聚类数
   * - ``significance``
     - ``0.05``
     - enrichment 结果显著性阈值
   * - ``condition_col``
     - ``condition``
     - 多样本比较时用于定义条件分组的列名
   * - ``sample_col``
     - ``region``
     - 多样本比较时用于标识样本来源的列名
   * - ``celltype_col``
     - ``celltype``
     - 输入对象中细胞类型注释列名，用于 enrichment 分析
   * - ``cellcharter_col``
     - ``spatial_cluster``
     - CellCharter 输出空间 domain 标签写回对象时使用的列名
   * - ``image_type``
     - ``hires``
     - 用于空间叠加展示的图像层
   * - ``shape_type``
     - ``cell_boundaries``
     - 用于空间边界可视化的图层

配置建议：

1. ``max_cluster`` 会直接影响自动选取空间 domain 数量的范围。若组织结构较复杂，可适当上调；若样本规模较小，则不宜设得过高。
2. 若关注条件间空间组织差异，``condition_col`` 与 ``sample_col`` 必须准确设置，否则无法生成稳健的跨条件 enrichment 比较结果。
3. ``celltype_col`` 与 ``cellcharter_col`` 分别决定输入注释与输出空间 domain 标签的读写逻辑，是后续解释结果时最关键的列名参数。

常见配置示例如下：

.. code-block:: bash

   image_type: "hires"
   shape_type: "cell_boundaries"
   significance: 0.05
   max_cluster: 10
   condition_col: "condition"
   sample_col: "region"
   celltype_col: "celltype"
   cellcharter_col: "spatial_cluster"


Step 3: Run the Command
----------------------------------------------

完成输入准备与参数确认后，可运行：

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellcharter


下面以已完成注释的示例空间对象为例，演示 CellCharter 的标准运行思路。

1. Prepare the input object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

我们使用core_analysis注释分析完成的Colon_Cancer_P2_008um作为示例,请确保你已经完成了先前的core_analysis与注释步骤。

sample.txt:

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

2. Set the key parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

为了方便演示,使用默认参数即可,若为其他样本请注意修改合适的参数。

3. Run CellCharter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellcharter


Spatialsnake将会自动选择使用GPU加速计算,若未检测到GPU,则使用CPU计算,请确保你的显存足够。

Result file structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

单样本输出（默认模式）：

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
         └── cellcharter/
               ├── Colon_Cancer_P2_008um_cellcharter.zarr/
               ├── Colon_Cancer_P2_008um_celchar.png
               ├── Colon_Cancer_P2_008um_enrichment.png
               ├── Colon_Cancer_P2_008um_nhood_enrichment.png
               ├── Colon_Cancer_P2_008um_Clusters.png
               └── Colon_Cancer_P2_008um_cell_clusters.csv


其中，``{sample}_diff_enrichment.png`` 仅在以下条件同时满足时生成：

1. 当前运行在多样本比较分支（``channel=compare_analysis``）。
2. 输入对象中 ``condition_col`` 至少包含两个条件分组。
3. 输入对象中存在 ``sample_col``，以支持样本层面的邻域比较。


1. Clustering stability plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_celchar.png
   :width: 85%
   :align: center
   :alt: cellcharter autok stability

该图展示不同候选聚类数在重复运行中的稳定程度，用于判断最终选择的空间 domain 数量是否可靠。


2. Neighborhood enrichment plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_nhood_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter neighborhood enrichment

该图用于展示不同空间 domain 之间的邻接富集或排斥关系，有助于识别组织微环境中的共定位模式或互斥结构。


3. Condition-specific enrichment plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter per-condition enrichment

在多样本模式下，CellCharter 会分别为不同 ``condition_col`` 条件组生成 enrichment 图，以便观察各条件内部的空间组织结构。


4. Differential neighborhood enrichment plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter differential neighborhood enrichment

该图比较不同条件之间的邻域富集差异，并突出发生显著变化的 domain-domain 关系，是比较性空间分析中最重要的结果之一。


5. Spatial overlay plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_Colon_Cancer_P2_hires_image_Clusters.png
   :width: 85%
   :align: center
   :alt: cellcharter spatial overlay

该图将空间 domain 标签叠加到组织图像上，可用于判断推断得到的空间分区是否与组织形态结构一致，并进一步赋予每个 domain 生物学解释。
