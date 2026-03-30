算法注释（cell2Location）
=========================

``cell2Location`` 用于将单细胞参考中的细胞类型信息映射到空间位点，输出每个位点的细胞类型丰度估计结果，并生成对应的空间可视化与统计文件。对于 Visium 等低分辨率空间数据,
该方法尤其适合用于估计每个位点的细胞组成，而不是直接给出单个位点的唯一标签,同时,cellLocation还支持多样本整合空间对象注释,避免了不同样本之间的差异导致的注释不一致问题.
 除了一般的cell2location结果,对于得到的细胞丰度结果我们的pipeline将使用Person 算法与手动非监督聚类注释区域进行相关性计算,绘制气泡图,便于用户探寻区域内的细胞类型丰度情况.



配置文件详解请见 :doc:`../config_reference/annotion_yaml`。

处理逻辑概述
------------
1. 读取空间对象（zarr）与参考单细胞对象（h5ad）。
2. 在参考数据上训练回归模型，学习细胞类型表达特征。
3. 在空间对象上拟合 cell2location 模型，估计每个位点的细胞类型丰度。
4. 对丰度结果进行下游非负矩阵分解分析并回写结果并生成可视化对象、统计图和中间质控文件。


准备输入文件
------------
``cell2Location`` 运行时需要两类输入：

1. 空间转录组对象 ``.zarr`` (若您只有空间对象的h5ad文件,请使用我们的工具转换一下 :doc:`../useful_tool/transform`).
2. 已带细胞类型注释的单细胞参考对象 ``.h5ad`` (若您只有单细胞数据的seurat对象,同理 :doc:`../useful_tool/transform`).

这里我们直接使用 :doc:`../integration_analysis/multi_sample_integration` 中输出的空间对象进行演示,并结合论文配套的 6 个单细胞数据文件构建参考对象。

1. 参考数据下载

同理在工作目录中创建并运行下载脚本，将 6 个参考单细胞文件和注释表统一下载到 ``data/sc_data`` 目录,当然也可以手动逐个下载.

创建运行脚本文件 ``touch download.sh``

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

.. code-block:: bash

  chmod +x download.sh
  ./download.sh


2. 注释数据写入创建 ``touch annotate.py`` 并通过 ``python annotate.py`` 运行:

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



3. sample.txt 配置

``sample.txt`` 需要同时提供空间对象和单细胞参考对象。
.. code-block:: text
  
   sample_id           input_path                                      sc_reference
   concatenated_sdata  results/merge_data/annotion/concatenated_sdata  data/MTAB/merged_sc_with_annotation.h5ad


参数说明
--------

运行可选的参数设置
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - ``--anno_algorithm``
     - ``cell2Location``
     - 指定注释算法为 cell2location（必填核心参数）
   * - ``--device``
     - ``cuda`` / ``cpu``
     - 控制模型训练设备，影响训练速度
   * - ``--image_type``
     - ``hires``
     - 指定空间图像图层用于渲染可视化
   * - ``--shape_type``
     - ``cell_boundaries``
     - 指定空间分割形状图层用于叠加展示
   * - ``--max_cores``
     - ``16``
     - 控制并行资源上限（流程级资源参数）
   * - ``max_epochs_reference``
     - ``250``
     - 参考单细胞回归模型训练轮次
   * - ``max_epochs_st``
     - ``30000``
     - 空间模型训练轮次
   * - ``remove_mt``
     - ``True``
     - 是否在训练前过滤线粒体基因
   * - ``N_cells_per_location``
     - ``30``
     - 预设每个空间位点的细胞数先验
   * - ``labels_key_reference``
     - ``annotation_1``
     - 参考单细胞对象中表示细胞类型标签的列名
   * - ``batch_key_reference``
     - ``sample``
     - 参考单细胞对象中表示批次或样本来源的列名
   * - ``batch_key_st``
     - ``sample``
     - 空间对象中表示样本来源的列名，用于多样本整合场景
   * - ``cell_count_cutoff``
     - ``15``
     - 参考数据基因过滤时的细胞数阈值
   * - ``cell_percentage_cutoff2``
     - ``0.05``
     - 参考数据基因过滤时的细胞占比阈值
   * - ``nonz_mean_cutoff``
     - ``1.12``
     - 参考数据基因过滤时的非零表达均值阈值
   * - ``detection_alpha``
     - ``20``
     - 空间模型的检测率先验参数
   * - ``save_models``
     - ``True``
     - 是否保存参考模型与空间模型目录

其中，最关键的参数通常是 ``labels_key_reference``、``batch_key_reference``、``batch_key_st``。如果参考数据是多样本整合对象，建议将后两者都设为 ``sample``，以便模型识别样本来源。

若希望通过配置文件统一管理，可在 ``annotion.yaml`` 中设置：


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

在参数中设置 batch_key_reference 与 batch_key_st 为 ``sample``，即可在不同样本间进行比较分析。

运行命令
--------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotion --anno_algorithm=cell2Location


结果文件结构
------------

单样本模式下，核心结果通常位于 ``results/{sample}/cell2Location/``：

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
其中，``{sample}.zarr`` 是后续继续分析的主结果对象，``Cell2Loc_inf_aver.csv`` 和 ``figure/cluster_abundance_stats.csv`` 是最常用的表格结果，图像文件则用于检查模型训练状态、空间分布模式和细胞组成差异。

分析结果解释
--------------------------------

1. 结果表整合说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

cell2location 运行完成后，最常用的表格结果主要包括以下几类：

1. ``Cell2Loc_inf_aver.csv``
   该文件记录参考模型学习到的细胞类型表达特征，可视为后续空间映射的参考基础。

2. ``figure/cluster_abundance_stats.csv``
   该文件汇总不同聚类区域或不同分组中的细胞类型丰度统计结果，用于支撑后续柱状图和分组比较分析。

3. 其他中间或模型结果目录
   ``Reference_model/``、``Spatial_model/``、``CoLocatedComb/`` 和 ``test.h5ad`` 主要用于模型保存、共定位结果查看和过程追溯，通常不作为结果解读的第一入口。

总体而言，``{sample}.zarr`` 保存了已经回写到空间对象中的丰度结果，``Cell2Loc_inf_aver.csv`` 说明参考特征，``cluster_abundance_stats.csv`` 则更适合用于区域和分组层面的组成比较。

2. 训练收敛曲线
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/ELBO_sc_model.png
   :width: 82%
   :align: center
   :alt: cell2location training curve

解释：
该图通过 ELBO 曲线展示模型训练过程。横轴为训练迭代过程，纵轴为目标函数变化，用于反映参考模型或空间模型是否逐步趋于稳定收敛。

3. 非监督聚类相关性气泡图
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/dotplot.png
   :width: 90%
   :align: center
   :alt: cell2location spatial abundance

解释：
该图展示不同细胞类型在组织空间中的丰度分布。不同面板对应不同细胞类型，可用于观察各类细胞在组织中的富集位置、空间连续性和区域特异性。


4. 细胞组成比例图（``cluster_abundance_stacked_bar.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/cluster_abundance_stacked_bar.png
   :width: 82%
   :align: center
   :alt: cell2location abundance barplot

解释：
该图以堆叠柱状图形式展示不同聚类区域或不同样本中各细胞类型的相对丰度构成，用于比较不同区域之间的细胞组成差异。

5. MNF 非负矩阵分解分析
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/n_fact12.png
   :width: 76%
   :align: center
   :alt: cell2location reconstruction qc


6. MNF 分解结果空间映射可视化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MNF_spatial.png
   :width: 76%
   :align: center
   :alt: cell2location reconstruction qc


7. 细胞预测丰富空间映射
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/max_cell.png
   :width: 90%
   :align: center
   :alt: cell2location spatial abundance

对于低分辨率数据,cell2location得到的是丰度权重,我们仅仅对每个spot的最大丰度进行可视化粗略展示


