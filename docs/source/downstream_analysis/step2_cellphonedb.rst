模块 1：细胞通讯（cellPhoneDB）
===============================

``cellPhoneDB`` 用于在细胞类型之间推断配体-受体通讯关系。这里以 ``Colon_Cancer_P2`` 的流程结果为例演示；若需先筛选感兴趣细胞亚群，请先参考 :doc:`../useful_tool/splitting`。

为了节省空间我们使用 ``reannotation``步骤亚聚类的肿瘤细胞的四个分群使用cellphoneDB的statistical方法进行分析。

处理逻辑概述
------------
1. 读取输入对象并抽取 ``cell_id`` + 细胞类型列，生成 ``{sample}_cellid_cell_type.txt``。
2. 根据 ``cpdb_method``  ``statistical`` 或 ``degs`` 推断。
3. 输出 means/pvalues/deconvoluted/interaction_scores 等表格结果文件。
4. 自动绘制热图、点图、家族点图，并在条件满足时绘制弦图。

情景 1：标准统计模式（statistical）
------------------------------------
适用于常规探索，或直接用带注释列的 ``.zarr/.h5ad`` 对象完成通讯推断。

配置说明
~~~~~~~~
``sample.txt`` 至少包含样本 ID 与输入对象路径：

.. code-block:: text

   samples path_to_dir
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/reannotation/Colon_Cancer_P2_008um.zarr

推荐关键参数：

 :doc:`../config_reference/advance_analysis`

.. code-block:: bash

   cellPhoneDB_input: ""
   cpdb_method: "statistical"
   counts_data: "hgnc_symbol"
   output_name: "Colon_Cancer_P2"
   threshold: 0.1
   threads: 16
   pvalue: 0.05
   iterations: 500
   microenvs_file_path: ""
   active_tf_path: ""
   degs_file_path: ""
   niche_col: "None"
   is_singlecell: False
   cpdb_de_method: "wilcoxon"
   celltype_col: "celltype"
   cell_type1: "Tumor_II"
   cell_type2: "Tumor_I"
   gene_family: ""

运行命令
~~~~~~~~
.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=cellPhoneDB  --threads 8 --output_name Colon_Cancer_P2

结果文件层级
~~~~~~~~~~~~
.. code-block:: text

   results/
   └── {sample}/
       └── cellPhoneDB_results/
           ├── adata.h5ad
           ├── {sample}_cellid_cell_type.txt
           ├── {sample}_heatmap.png
           ├── {sample}_dot_plot.png
           ├── {sample}_dot_family_plot.png
           ├── {sample}_chord_plot.png                # 条件满足时生成
           └── cellphonedb_output/
               ├── statistical_analysis_means_{output_name}.txt
               ├── statistical_analysis_pvalues_{output_name}.txt
               ├── statistical_analysis_deconvoluted_{output_name}.txt
               ├── statistical_analysis_interaction_scores_{output_name}.txt
               └── statistical_analysis_relevant_interactions_{output_name}.txt

可视化自动选择说明（本情景同样适用）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. 若未指定 ``celltype`` 列名，工具会按 ``celltype`` → ``cell_type`` → ``celltypes`` → ``cell_type_annotation`` 自动匹配。
2. 若 ``cell_type1/cell_type2`` 缺失或填写无效，工具会自动选择样本中出现频次最高的前两个细胞类型作点图默认展示。
3. 若 ``gene_family`` 缺失或不在支持集合内，家族点图默认回退为默认的 ``chemokines`` 
4. 热图和点图依赖 ``means + pvalues``，只要这两者存在就会绘制。
5. 弦图仅在同时满足“可解析的 interaction 列表 + deconvoluted 文件存在”时生成；若条件不满足会跳过弦图，不影响其他图件。



情景 2：空间微环境约束模式（spatial）
--------------------------------------
适用于需要将空间分区信息纳入通讯推断
例如利用 banksy 或者 cellcharter 运行的结果注释``spatial_cluster`` 或 自行手动书写的microenvs_file 文件,请确保书写的格式符合官方文档要求。
若您是使用我们的工具进行空间域的探索,则可直接进行空间微环境约束模式的分析无需手动书写microenvs_file 文件。

例如

.. code-block:: bash
  cell_type	microenvironment
  NKcells_1	location_1
  NKcells_0	location_2
  Tcells	location_1
  Myeloid	location_2


配置说明
~~~~~~~~
先生成模板：

.. code-block:: bash

   spatialsnake produce-file --option=advance_analysis

再在 ``advance_analysis.yaml`` 中设置：

.. code-block:: yaml

   cellPhoneDB_input: ""
   counts_data: "hgnc_symbol"
   threshold: 0.1
   threads: 16
   pvalue: 0.05
   output_name: "Colon_Cancer_P2"
   iterations: 500
   microenvs_file_path: "" # 若为手动输入  请在此配置
   active_tf_path: ""
   degs_file_path: ""
   niche_col: "spatial_cluster"    # 确定空间域的列名 我们的pipeline默认为spatial_cluster
   is_singlecell: False # 确定为空转数据
   cpdb_method: "statistical"
   cpdb_de_method: "wilcoxon"
   celltype_col: "celltype"
   cell_type1: "Tumor_II"
   cell_type2: "Tumor_I"
   gene_family: ""

解释：

1. ``microenvs_file_path`` 为空时，工具会从 ``celltype_col + niche_col`` 自动生成 ``{sample}_microenvs.txt``。
2. 空间数据下若既无 ``microenvs_file_path``，又缺少 ``niche_col`` 或列不存在，会直接报错停止，避免无约束误分析。

运行命令
~~~~~~~~
.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=advance_analysis --runpipe=cellPhoneDB --configfile advance_analysis.yaml

结果文件层级
~~~~~~~~~~~~
.. code-block:: text

   results/
   └── {sample}/
       └── cellPhoneDB_results/
           ├── adata.h5ad
           ├── {sample}_cellid_cell_type.txt
           ├── {sample}_microenvs.txt
           ├── {sample}_heatmap.png
           ├── {sample}_dot_plot.png
           ├── {sample}_dot_family_plot.png
           ├── {sample}_chord_plot.png                # 条件满足时生成
           └── cellphonedb_output/
               └── statistical_analysis_*_{output_name}.txt

情景 3：DEG/TF 约束模式（degs + active TF）
-------------------------------------------
适用于已有差异基因列表，想在候选配体-受体筛选中加入先验约束,可以得到更准确的分析结果

例 DEG.txt

.. code-block:: bash

  cluster	gene	deg
  Myeloid	ENSG00000188157	1
  NKcells_0	ENSG00000230368	1
  NKcells_0	ENSG00000186350	1
  NKcells_0	ENSG00000134250	1
  Tcells	ENSG00000188976	1

例 TFs.txt

.. code-block:: bash

  cluster	TF
  NKcells_0	ID4


配置说明
~~~~~~~~
在 ``advance_analysis.yaml`` 中设置：

.. code-block:: yaml

   cellPhoneDB_input: "results/Colon_Cancer_P2_008um/reannotation/Colon_Cancer_P2_008um.zarr"
   cpdb_method: "degs" # 配置
   degs_file_path: "results/downstream/DEG_list.txt"  # 配置文件路径
   active_tf_path: "results/pysenic/tf_activity.txt"  # 配置文件路径

解释：

1. ``cpdb_method=degs`` 时，``degs_file_path`` 是必需项，不存在则流程报错。
2. ``active_tf_path`` 仅在文件真实存在时才会生效；路径无效时自动忽略，不会中断运行。
3. 为保证可视化正确读取 ``degs_analysis_*`` 文件，建议 ``degs_file_path`` 使用真实存在路径。

运行命令
~~~~~~~~
.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=advance_analysis --runpipe=cellPhoneDB --configfile advance_analysis.yaml

结果文件层级
~~~~~~~~~~~~
.. code-block:: text

   results/
   └── {sample}/
       └── cellPhoneDB_results/
           ├── {sample}_heatmap.png
           ├── {sample}_dot_plot.png
           ├── {sample}_dot_family_plot.png
           ├── {sample}_chord_plot.png                # 条件满足时生成
           └── cellphonedb_output/
               ├── degs_analysis_means_{output_name}.txt
               ├── degs_analysis_pvalues_{output_name}.txt
               ├── degs_analysis_deconvoluted_{output_name}.txt
               └── degs_analysis_relevant_interactions_{output_name}.txt


结果可视化讲解与展示
~~~~~~~~~~~~

这里我们以情景 1 的示例数据进行说明，重点查看 ``cellPhoneDB_results`` 目录中的 4 类图件。

1. 热图（``{sample}_heatmap.png``）
------------------------------------

.. figure:: /_static/images/Colon_Cancer_P2_008um_heatmap.png
   :width: 85%
   :align: center
   :alt: cellphonedb heatmap

解释：
热图用于总览“细胞类型两两之间显著互作数量”，适合先定位通讯最活跃的细胞组合。

建议：
先在热图中锁定高互作细胞对，再到点图查看具体配体-受体分子对。

2. 点图（``{sample}_dot_plot.png``）
-------------------------------------

.. figure:: /_static/images/Colon_Cancer_P2_008um_dot_plot.png
   :width: 85%
   :align: center
   :alt: cellphonedb dot plot

解释：
点图展示指定 ``cell_type1`` 与 ``cell_type2`` 之间的配体-受体关系，点大小和颜色反映互作强度与显著性。

自动选择逻辑：

1. 若未提供或提供了无效的 ``cell_type1/cell_type2``，工具会自动选取样本中频次最高的前两个细胞类型进行展示。
2. 若未显式指定 ``celltype`` 列，工具会在常见列名中自动匹配合适分组列。

3. 家族点图（``{sample}_dot_family_plot.png``）
-------------------------------------------------

.. figure:: /_static/images/Colon_Cancer_P2_008um_dot_family_plot.png
   :width: 85%
   :align: center
   :alt: cellphonedb gene family dot plot

解释：
家族点图用于聚焦某一类信号家族（如 ``chemokines``、``th1``、``th2`` 等），适合做机制层面的聚焦验证。

自动选择逻辑：
若 ``gene_family`` 缺失或不在支持集合，工具默认回退到 ``chemokines``。

4. 弦图（``{sample}_chord_plot.png``）
---------------------------------------

.. figure:: /_static/images/cord.png
   :width: 85%
   :align: center
   :alt: cellphonedb chord plot


自动化工具的可视化能力有限,用户可以查看官方文档进行个性化的可视化操作 例如使用cellphonedbviz

CellphoneDB v5: inferring cell-cell communication from single-cell multiomics data. Troule et al. Nat Protocols 2025


