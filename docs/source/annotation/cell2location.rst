Algorithm-Based Annotation (``cell2Location``)
============================================================================================

``cell2Location`` 用于将单细胞参考数据中的细胞类型信息映射到空间转录组位置中，从而估计每个空间位置的细胞类型丰度，并生成相应的空间可视化结果与汇总表格。

对于 Visium 等分辨率较低的空间数据，该方法尤其适用，因为它并不强行将每个 spot 指派为单一标签，而是估计每个 spot 内不同细胞类型的组成比例。
该方法同样支持多样本整合后的空间对象注释，有助于降低不同样本之间的注释不一致性。
除标准的 cell2location 输出外，流程还会进一步将丰度结果与人工定义或无监督聚类得到的区域进行关联分析，并生成气泡图等结果，以辅助解释局部组织区域中的细胞组成特征。

参数配置的完整说明请参见 :doc:`../config_reference/annotation_yaml`。


1. 读取空间转录组对象（``zarr``）以及已完成细胞类型注释的单细胞参考对象（``h5ad``）。
2. 在参考数据上训练回归模型，学习不同细胞类型的表达特征。
3. 在空间对象上拟合 cell2location 模型，估计每个空间位置的细胞类型丰度。
4. 对丰度矩阵执行后续非负矩阵分解（NMF）等分析，将结果写回对象，并输出可视化图像、统计汇总表及中间质量控制文件。

简而言之，该步骤的核心目标是利用单细胞参考构建细胞类型表达先验，并将其稳健地映射到空间数据中，从而获得可用于区域比较、空间模式识别及下游生物学解释的细胞组成结果。


``cell2Location`` 运行通常需要以下两类输入文件：

1. 空间转录组对象，格式为 ``.zarr``。若当前仅有空间 ``.h5ad`` 对象，请先通过 :doc:`../useful_tool/transform` 完成格式转换。
2. 已包含细胞类型注释信息的单细胞参考对象，格式为 ``.h5ad``。若当前仅有 Seurat 对象，也请先使用 :doc:`../useful_tool/transform` 完成转换。


step 1: ``sample.txt`` 配置文件
------------------------------------------------------

``sample.txt`` 需至少包含空间对象路径与单细胞参考对象路径。

.. code-block:: text

   sample_id           input_path                                      sc_reference
   concatenated_sdata  results/merge_data/annotation/concatenated_sdata  data/MTAB/merged_sc_with_annotation.h5ad


Step 2: Parameter Selection and Configuration
------------------------------------------------------------------------------------------

以下为该步骤中较常用的参数及其作用说明:

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--anno_algorithm``
     - ``cell2Location``
     - 指定当前注释算法为 cell2location
   * - ``--device``
     - ``cuda`` / ``cpu``
     - 模型训练所使用的计算设备，直接影响运行时间
   * - ``--image_type``
     - ``hires``
     - 空间可视化时使用的图像层
   * - ``--shape_type``
     - ``cell_boundaries``
     - 用于叠加展示的空间边界图层
   * - ``--max_cores``
     - ``16``
     - 并行计算资源上限
   * - ``max_epochs_reference``
     - ``250``
     - 参考回归模型训练轮数
   * - ``max_epochs_st``
     - ``30000``
     - 空间模型训练轮数
   * - ``remove_mt``
     - ``True``
     - 是否在训练前去除线粒体基因
   * - ``N_cells_per_location``
     - ``30``
     - 每个空间位置细胞数目的先验设定
   * - ``labels_key_reference``
     - ``annotation_1``
     - 参考对象中存储细胞类型标签的列名
   * - ``batch_key_reference``
     - ``sample``
     - 参考对象中存储批次或样本信息的列名
   * - ``batch_key_st``
     - ``sample``
     - 空间对象中存储批次或样本信息的列名，尤其适用于多样本整合分析
   * - ``cell_count_cutoff``
     - ``15``
     - 参考数据中过滤基因时的细胞计数阈值
   * - ``cell_percentage_cutoff2``
     - ``0.05``
     - 参考数据中过滤基因时的细胞比例阈值
   * - ``nonz_mean_cutoff``
     - ``1.12``
     - 参考数据中过滤基因时的非零均值表达阈值
   * - ``detection_alpha``
     - ``20``
     - 空间模型中检测率先验参数
   * - ``save_models``
     - ``True``
     - 是否保存参考模型与空间模型目录

配置建议：

1. ``labels_key_reference``、``batch_key_reference`` 与 ``batch_key_st`` 通常是最需要优先确认的参数，它们分别决定细胞类型标签与样本来源信息在模型中的读取方式。
2. 若参考数据来自多样本整合结果，通常建议将 ``batch_key_reference`` 与 ``batch_key_st`` 同时设置为 ``sample``，以便模型正确识别样本来源并提高跨样本比较的可靠性。
3. ``device``、``max_epochs_reference`` 与 ``max_epochs_st`` 会显著影响训练耗时，可根据硬件条件与数据规模进行调整。

若您希望通过配置文件统一管理参数，可使用 ``annotation.yaml``。

.. code-block:: bash

  anno_algorithm: "cell2Location"
  device: "cuda"
  max_epochs_reference: 250
  remove_mt: True
  N_cells_per_location: 30
  max_epochs_st: 30000
  labels_key_reference: "annotation_1"
  batch_key_reference: "sample"
  batch_key_st: "sample"
  cell_count_cutoff: 15
  cell_percentage_cutoff2: 0.05
  nonz_mean_cutoff: 1.12
  detection_alpha: 20
  save_models: True
  celltype_col: "celltype"

如需进一步查看 YAML 参数说明，请参见 :doc:`../config_reference/annotation_yaml`。


Step 3: Run the Command
----------------------------------------------

完成 ``sample.txt`` 与参数设置后，即可运行 cell2location 注释流程。

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=cell2Location


下面以 :doc:`../integration_analysis/multi_sample_integration` 中生成的空间对象为例，结合研究中配套的 6 个单细胞文件，构建参考对象并完成 cell2location 注释演示。

1. Download the reference data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在工作目录中创建并运行下载脚本，将 6 个单细胞参考文件及其注释表下载至 ``data/sc_data``。若您已经具备这些文件，也可直接手动整理到对应目录。

Create the script file:

.. code-block:: bash


    #!/usr/bin/env bash
    set -euo pipefail

    ids=(
      5705STDY8058280
      5705STDY8058281
      5705STDY8058282
      5705STDY8058283
      5705STDY8058284
      5705STDY8058285
    )

    mkdir -p "data/sc_data"
    cd "data/sc_data"

    for id in "${ids[@]}"; do
      wget -c "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/115/E-MTAB-11115/Files/${id}_web_summary.html"
      wget -c "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/115/E-MTAB-11115/Files/${id}_filtered_feature_bc_matrix.h5"
    done

    wget -c "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/115/E-MTAB-11115/Files/cell_annotation.csv"

Run the script:

.. code-block:: bash

   chmod +x download.sh
   ./download.sh


2. Build the annotated reference object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

创建 ``annotate.py``，并运行 ``python annotate.py`` 构建用于 cell2location 的单细胞参考对象。

.. code-block:: python

    from pathlib import Path
    import scanpy as sc
    import anndata as ad
    import pandas as pd

    h5_files = [
        "5705STDY8058285_filtered_feature_bc_matrix.h5",
        "5705STDY8058284_filtered_feature_bc_matrix.h5",
        "5705STDY8058283_filtered_feature_bc_matrix.h5",
        "5705STDY8058282_filtered_feature_bc_matrix.h5",
        "5705STDY8058281_filtered_feature_bc_matrix.h5",
        "5705STDY8058280_filtered_feature_bc_matrix.h5",
    ]

    adata_list = []
    for f in h5_files:
        p = Path(f)
        sample_id = p.name.replace("_filtered_feature_bc_matrix.h5", "")
        adata_i = sc.read_10x_h5(str(p))
        adata_i.var_names_make_unique()
        adata_i.obs_names = [f"{sample_id}_{bc}" for bc in adata_i.obs_names.astype(str)]
        adata_i.obs["sample"] = sample_id
        adata_list.append(adata_i)

    adata_merged = ad.concat(
        adata_list,
        axis=0,
        join="outer",
        merge="same",
        index_unique=None
    )

    anno = pd.read_csv("cell_annotation.csv")
    anno.columns = [c.strip() for c in anno.columns]
    anno["CellID"] = anno["Cell ID"].astype(str).str.strip()
    anno["sample"] = anno["sample"].astype(str).str.strip()
    anno["annotation_1"] = anno["annotation_1"].astype(str).str.strip()
    anno = anno.drop_duplicates(subset=["CellID"], keep="first")
    anno = anno.set_index("CellID")

    anno_aligned = anno.reindex(adata_merged.obs_names)
    matched_mask = anno_aligned["annotation_1"].notna()
    adata_merged = adata_merged[matched_mask].copy()
    anno_aligned = anno_aligned.loc[matched_mask]
    adata_merged.obs["sample"] = anno_aligned["sample"].values
    adata_merged.obs["annotation_1"] = anno_aligned["annotation_1"].values
    adata_merged.var["gene_ids"] = adata_merged.var.index
    adata_merged.write_h5ad("merged_sc_with_annotation.h5ad")


3. Configure ``sample.txt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在演示中，``sample.txt`` 需要同时提供空间对象路径与单细胞参考路径。

.. code-block:: text

   sample_id           input_path                                      sc_reference
   concatenated_sdata  results/merge_data/annotation/concatenated_sdata  data/MTAB/merged_sc_with_annotation.h5ad


4. Run the workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

完成参考对象构建与 ``sample.txt`` 配置后，即可运行：

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=cell2Location


Results and Interpretation
----------------------------------------------------

Result file structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在单样本模式下，主要结果通常输出至 ``results/{sample}/cell2Location/``：

.. code-block:: text

   results/
   └── {sample}/
       └── cell2Location/
           ├── {sample}.zarr/
           ├── Cell2Loc_inf_aver.csv
           ├── Reference_model/
           ├── Spatial_model/
           ├── CoLocatedComb/
           ├── test.h5ad
           └── figure/
               ├── ELBO_sc_model.png
               ├── ELBO_spatial_model.png
               ├── QC_spatial_reconstruction_accuracy.png
               ├── each_celltype.png
               ├── cluster_abundance_stacked_bar.png
               └── cluster_abundance_stats.csv

其中，``{sample}.zarr`` 是后续分析最核心的结果对象；``Cell2Loc_inf_aver.csv`` 与 ``figure/cluster_abundance_stats.csv`` 是最常用的表格输出；其余图像文件主要用于评估训练质量、空间丰度模式及不同区域之间的组成差异。


1. Primary result tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

cell2location 完成后，最常用的结果文件通常包括以下几类：

1. ``Cell2Loc_inf_aver.csv``
   该文件保存参考模型学习到的细胞类型表达特征，是后续空间映射的重要依据。

2. ``figure/cluster_abundance_stats.csv``
   该文件汇总不同聚类区域或样本分组中的细胞类型丰度统计结果，适用于后续柱状图展示及组间比较。

3. 其他中间结果与模型目录
   ``Reference_model/``、``Spatial_model/``、``CoLocatedComb/`` 与 ``test.h5ad`` 主要用于模型保存、共定位结果检查及复现追踪，通常不是生物学解释时的第一入口文件。

总体而言，``{sample}.zarr`` 保存了写回空间对象的细胞丰度结果，``Cell2Loc_inf_aver.csv`` 描述参考表达特征，而 ``cluster_abundance_stats.csv`` 更适合进行区域层面或分组层面的组成比较。


2. Training convergence curves
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/ELBO_sc_model.png
   :width: 82%
   :align: center
   :alt: cell2location training curve

该 ELBO 曲线用于展示模型训练过程。横轴表示训练迭代次数，纵轴表示目标函数取值，可据此判断参考模型或空间模型是否达到相对稳定的收敛状态。


3. Dot plot linking abundances to unsupervised regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/dotplot.png
   :width: 90%
   :align: center
   :alt: cell2location spatial abundance

该图总结了不同细胞类型在不同组织区域中的分布特征。不同面板对应不同细胞类型，可用于识别空间富集、连续变化趋势及区域特异性模式。


4. Stacked bar plot of cell composition (``cluster_abundance_stacked_bar.png``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/cluster_abundance_stacked_bar.png
   :width: 82%
   :align: center
   :alt: cell2location abundance barplot

该堆叠柱状图展示不同聚类区域或样本中各类细胞的相对丰度，适用于比较不同区域之间的组成差异。


5. NMF-based decomposition analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/n_fact12.png
   :width: 76%
   :align: center
   :alt: cell2location reconstruction qc

该结果用于展示基于丰度矩阵进一步分解得到的潜在组成模式，可辅助识别具有代表性的细胞共定位结构与区域组合特征。


6. Spatial visualization of decomposition factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MNF_spatial.png
   :width: 76%
   :align: center
   :alt: cell2location reconstruction qc

该图将分解得到的潜在因子重新映射到空间坐标中，有助于观察不同组成模式在组织中的空间分布及其局部富集区域。


7. Spatial map of dominant cell abundance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/max_cell.png
   :width: 90%
   :align: center
   :alt: cell2location spatial abundance

对于低分辨率空间数据，cell2location 返回的是细胞丰度权重而非单一硬标签。此处仅展示每个 spot 中丰度最高的细胞类型，作为整体空间组成的粗略概览。
