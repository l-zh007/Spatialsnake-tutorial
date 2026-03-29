模块 7：差异表达比较（compare_stage）
======================================

在多样本空间转录组研究中，研究者往往最关心两个问题：**哪些基因在不同实验组之间发生了显著变化**，以及 **这些变化反映了哪些生物学过程或信号通路**。``compare_stage`` 模块正是为这一目的设计，用于在整合分析完成后，对指定细胞群体或指定组织区域进行跨样本差异表达比较，并自动给出统计结果、可视化图像以及功能富集分析。

这里我们继续使用 :doc:`../integration_analysis/multi_sample_integration` 中已经完成整合和注释的小鼠脑空间转录组对象作为示例。

配置文件详解请见 :doc:`../config_reference/compare_stage_yaml`。

模块会做什么
------------

1. **按生物学分组进行比较**
   模块会读取 ``sample.txt`` 中设置的分组信息，将同一分组下的样本作为一个实验条件进行比较。因此，``sample.txt`` 里填写的分组名称不仅决定统计模型中的分组关系，也会直接显示在后续的结果表、目录名称和图例中。
2. **聚焦目标细胞类型或区域**
   若设置 ``cell_focus``，模块会优先提取感兴趣的细胞类型或区域，例如 ``cortex``、``CAF``、``T_cell`` 等，专门比较该群体在不同实验条件下的表达变化。
3. **进行差异表达统计**
   当每个条件下具有足够重复样本时，模块优先采用 DESeq2 风格的伪 bulk 差异分析；当样本数较少时，会自动切换到 edgeR，以提高小样本条件下的稳定性。
4. **自动生成可解释的结果图**
   模块会自动输出火山图、差异基因柱状图、log2FC 分布图、MA 图和多对比热图，帮助用户从不同角度理解表达变化。
5. **自动进行功能富集**
   对显著高表达基因分别进行 GO、KEGG 与 GSEA 分析，用于揭示某一分组中更活跃的生物学功能、代谢通路和分子网络。

准备输入文件
------------

``compare_stage`` 建议直接复用 ``compare_analysis`` 主流程的样本表。与单样本分析不同,这里的第三列建议填写**真实的生物学分组名称**.

.. code-block:: text

   sample_id   input_path       group
   ST8059048  data/ST8059048   Group1
   ST8059049  data/ST8059049   Group1
   ST8059050  data/ST8059050   Group1
   ST8059051  data/ST8059051   Group2
   ST8059052  data/ST8059052   Group2

输入要求：

1. 进入本步骤前，应已完成 ``compare_analysis`` 下的 ``annotion``。
2. ``group`` 至少应包含两个真实实验条件，例如 ``Control``、``Disease``、``WT``、``KO``、``Tumor``、``Normal``。
3. 该分组名称会直接写入差异结果主表、比较名称、图例和富集结果目录中，因此建议使用清晰、可直接解释的生物学命名。
4. ``cell_focus`` 可指定重点比较的细胞类型或区域；留空时则对聚合后的全部目标群体进行比较。

运行前常用参数
--------------

.. list-table::
   :header-rows: 1
   :widths: 22 24 54

   * - 参数
     - 常用值
     - 作用
   * - ``runpipe``
     - ``compare_gene``
     - 指定运行差异表达比较分支
   * - ``compare_algorithm``
     - ``DEseq2`` / ``edgeR``
     - 设置优先采用的差异分析算法
   * - ``cell_focus``
     - ``cortex``、``CAF``、``T_cell``
     - 指定关注的细胞类型或组织区域
   * - ``spacies``
     - ``human`` / ``mouse``
     - 指定富集分析的物种背景，应与数据来源一致
   * - ``cut_off_pvalue``
     - ``0.05``
     - 控制火山图显著性划分与差异基因筛选阈值
   * - ``cut_off_logFC``
     - ``1.5``
     - 控制差异倍数阈值，数值越高筛选越严格

在本示例中，我们选择 ``cortex`` 区域进行组间差异分析，用于比较不同实验条件下同一区域的表达变化。若您的研究对象为某一类细胞群体，也可将 ``cell_focus`` 替换为对应细胞类型名称，从而专门分析这一群体在不同条件下的变化方向。


.. code-block:: bash

   compare_algorithm: 'DEseq2'          # 差异分析算法: DEseq2 或 edgeR
   cell_focus: "cortex"                    # 关注的细胞类型名称
   spacies: 'human'                     # 物种: human 或 mouse
   cut_off_pvalue: 0.05                # adjusted p value threshold for volcano plot and DEG split
   cut_off_logFC: 1.5                  # absolute log2 fold change threshold for volcano plot and DEG split

运行命令
--------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=compare_gene --cell_focus=cortex

结果文件结构
------------

当前版本统一输出 PNG 图像，并在结果目录中额外提供按真实分组命名的差异归属目录，便于用户直接判断“哪些基因更高表达于哪一组”。

.. code-block:: text

   results/
   └── merge_data/
       └── compare_analysis/
           ├── marker_genes_pval.csv
           ├── diff_all.csv
           ├── volcano.png
           ├── top_deg_barplot.png
           ├── log2fc_density.png
           ├── ma_plot.png
           ├── contrast_summary.csv
           ├── contrast_summary.png
           ├── contrast_log2fc_heatmap.png
           ├── diff/
           │   └── {groupA}_vs_{groupB}.csv
           ├── positive/
           │   ├── diff_genes.csv
           │   ├── diff_strict.csv
           │   ├── diff_loose.csv
           │   ├── GO_data.csv
           │   ├── kegg_data.csv
           │   ├── GO_enrich.png
           │   └── KEGG_enrich.png
           ├── negative/
           │   ├── diff_genes.csv
           │   ├── diff_strict.csv
           │   ├── diff_loose.csv
           │   ├── GO_data.csv
           │   ├── kegg_data.csv
           │   ├── GO_enrich.png
           │   └── KEGG_enrich.png
           ├── higher_in_{groupA}/
           │   ├── diff_genes.csv
           │   ├── diff_strict.csv
           │   ├── diff_loose.csv
           │   ├── GO_data.csv
           │   ├── kegg_data.csv
           │   ├── GO_enrich.png
           │   └── KEGG_enrich.png
           ├── higher_in_{groupB}/
           │   └── ...
           ├── gsea/
           │   ├── GSEA_GO_data.csv
           │   ├── GSEA_KEGG_data.csv
           │   ├── GSEA_GO_plot.png
           │   └── GSEA_KEGG_plot.png
           └── {contrast}/
               ├── diff_all.csv
               ├── volcano.png
               ├── top_deg_barplot.png
               ├── log2fc_density.png
               ├── ma_plot.png
               ├── positive/...
               ├── negative/...
               ├── higher_in_{groupA}/...
               ├── higher_in_{groupB}/...
               └── gsea/...

说明：

1. 若您选择的细胞类型测序质量不佳或为高分辨率数据或者实验条件相近,所得的差异基因结果可能不理想,即可能差异基因较少且富集分析结果不显著。
2. 当存在多组两两比较时，每一组比较会在 ``{contrast}`` 子目录下分别输出对应结果。
3. ``positive`` 和 ``negative`` 目录保留了算法上的上调/下调分类结果，便于兼容旧分析流程。
4. ``higher_in_{groupA}`` 和 ``higher_in_{groupB}`` 更适合实际解读，能直接说明基因更偏向哪一个实验组。

部分结果展示
--------------

1. 差异基因火山图（``volcano.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/volcano.png
   :width: 85%
   :align: center
   :alt: compare_stage volcano

解释：
火山图用于整体观察基因变化的强度和显著性。横轴表示两个分组之间的表达差异倍数，纵轴表示统计显著性。图中红色和蓝色点分别对应两个真实实验分组中更高表达的基因，灰色点表示未达到阈值的基因。被标注名称的基因通常是表达量较高且差异更明显的候选关键基因，适合进一步做验证实验或文献检索。

2. 差异基因柱状图（``top_deg_barplot.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/top_deg_barplot.png
   :width: 85%
   :align: center
   :alt: compare_stage top deg

解释：
该图聚焦展示变化最明显的一批差异基因。不同颜色对应不同实验组中更高表达的基因，适合快速识别最具代表性的候选标志物。对于无代码基础的用户来说，这张图是最直观的“重点基因清单可视化”。

3. MA 图（``ma_plot.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/ma_plot.png
   :width: 85%
   :align: center
   :alt: compare_stage ma plot

解释：
MA 图强调“表达丰度”与“表达差异”之间的关系。它能够帮助用户判断差异基因是否主要来自高表达基因，还是集中在低表达区域。若显著基因大多位于高表达区域，往往意味着结果更稳定、可信度更高。
