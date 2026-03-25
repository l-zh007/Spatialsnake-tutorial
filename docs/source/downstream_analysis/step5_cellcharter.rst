模块 4：空间域建模（cellcharter）
==================================

``cellcharter`` 用于结合表达信息与空间邻域结构进行空间域建模，得到更贴近组织结构的空间分区, 同时我们也会利用其工具中的富集分析步骤进行样本内或者样本间的细胞类型富集分析比较
这里我们使用之前注释好的示例数据进行空间域建模分析

此部分可使用GPU进行加速，若只使用cpu运行时间可能较长


配置文件详解请见 :doc:`../config_reference/advance_analysis_yaml`。

运行步骤与内容
------------------------

1. **读取与预处理输入**
   支持 ``.zarr`` 与 ``.h5ad``，统一整理表达矩阵并构建 ``counts`` 层，为后续空间建模提供可比较的输入基础。
2. **构建空间邻域特征**
   基于空间坐标建立邻接关系，整合“自身表达 + 邻域上下文”得到 ``X_cellcharter``，用于刻画局部微环境结构。
3. **自动选簇并写回标签**
   在 ``(2, max_cluster)`` 范围内自动评估聚类稳定性，识别最合适的空间域数量，并将每个 spot/cell 归入对应空间域。
4. **按单样本/多样本分支出图**
   - 单样本：重点分析各空间域之间的邻接富集关系，识别共定位或互斥的空间组织模式。
   - 多样本（``compare_analysis``）：在各条件内分别评估邻域结构，并进一步比较条件间差异，定位发生重塑的关键空间域连接。

准备输入文件
------------

``sample.txt`` 推荐格式：

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

输入要求：

1. 输入对象需包含空间坐标信息（``obsm['spatial']`` 或可转换坐标）。
2. 推荐输入为已注释对象（包含 ``celltype``），以便输出富集解释图。
3. 多样本比较时建议输入整合对象，并在对象中保留样本列与条件列（例如 ``sample_col=region``、``condition_col=condition``）。


运行可选的参数设置
------------------------------------------------------------

.. code-block:: bash

   image_type: "hires"
   shape_type: "cell_boundaries"
   significance: 0.05
   max_cluster: 10
   condition_col: "condition"
   sample_col: "region"
   celltype_col: "celltype"
   cellcharter_col: "spatial_cluster"


Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellcharter



结果文件结构
------------

单样本输出（默认模式）：

.. code-block:: text

   results/
   └── cellcharter/
       ├── {sample}_cellcharter.zarr/
       ├── {sample}_celchar.png
       ├── {sample}_enrichment.png
       ├── {sample}_nhood_enrichment.png
       ├── {sample}_{image}_Clusters.png
       └── {sample}_cell_clusters.csv

多样本输出（``channel=compare_analysis``）：

.. code-block:: text

   results/
   └── cellcharter/
       ├── {sample}_cellcharter.zarr/
       ├── {sample}_celchar.png
       ├── {sample}_enrichment.png
       ├── {sample}_{conditionA}_enrichment.png
       ├── {sample}_{conditionB}_enrichment.png
       ├── {sample}_diff_enrichment.png
       ├── {sample}_Clusters_proportion.png
       ├── {sample}_{image}_Clusters.png
       └── {sample}_cell_clusters.csv

多样本差异富集图何时输出
------------------------

``{sample}_diff_enrichment.png`` 仅在以下条件同时满足时生成：

1. 运行于多样本比较分支（``channel=compare_analysis``）。
2. 输入对象中存在 ``condition_col`` 且至少包含两个条件分组。
3. 输入对象中存在 ``sample_col``（用于库/样本层面的邻域比较）。

结果文件展示与解释
----------------

1. 聚类稳定性图（单样本/多样本都会输出）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_celchar.png
   :width: 85%
   :align: center
   :alt: cellcharter autok stability

解释：
用于查看候选簇数在重复运行中的稳定性，帮助判断最终空间域数量是否可靠。

2. 邻域富集图（单样本输出）
~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_nhood_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter neighborhood enrichment

解释：
展示空间域之间的邻接富集/排斥关系，帮助识别组织微环境中的共定位模式。

3. 条件内邻域富集图（多样本输出）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter per-condition enrichment

解释：
多样本模式下会按 ``condition_col`` 分组分别作图，便于在每个条件内部观察空间域邻域结构。

4. 差异邻域富集图（多样本输出，条件满足时）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_enrichment.png
   :width: 85%
   :align: center
   :alt: cellcharter differential neighborhood enrichment

解释：
对不同条件的邻域富集进行统计比较，突出显著变化的空间域连接关系，是多样本对比最核心的结果图之一。

5. 空间叠加图（单样本/多样本都会输出）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2_008um_Colon_Cancer_P2_hires_image_Clusters.png
   :width: 85%
   :align: center
   :alt: cellcharter spatial overlay

解释：
将空间域标签叠加到组织图像，验证分区结果与组织结构的一致性，并辅助人工解释空间域生物学意义。
