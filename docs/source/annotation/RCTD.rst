算法注释（RCTD）
================

``RCTD`` 用于基于参考单细胞数据对空间位点进行细胞类型解卷积,我们选择这一算法是因为它在空间分辨率与细胞类型分辨率之间提供了平衡,
其 ``full``模块输出空间位点的细胞类型分布,适用于visium低分辨率数据,而 ``doublet`` 和 ``singlet``模块分别输出空间位点的first_type second_type细胞类型标签,适用于高分辨率数据。
我们根据不同分辨率数据设置了不同的输出结果,通过阅读现在的空转分析文献不难发现,RCTD结果往往需要与非监督聚类进行对比,以评估其在空间分辨率下的表现。
因此我们的输出内容既包含了传统的反卷积预测结果,同时使用Person score,用于评估解卷积结果与非监督聚类结果的匹配程度与相关性.或直接计算解卷积结果与非监督聚类结果的比例以探究其注释准确性.

.. note::
  1.对于RCTD算法功能,请保证 1.输入的单细胞和空转数据需未经正则化等预处理,基因表达矩阵需为原始整数矩阵(若您是通过我们的工具进行数据处理,可直接使用任意输出的zarr数据,其中会自动保存原始表达矩阵在 ``.obs.raw`` 中) 
  
  2.配套的单细胞注释数据需保证每个celltype均至少有25个cell/spot,稀少的细胞类型我们的pipeline会自动剔除,请确保注释的高质量,最好使用经过同行评定的数据集进行注释.

处理逻辑概述
------------
1. 从 ``sample.txt`` 读取空间对象路径与单细胞参考路径。
2. 在单细胞对象中提取细胞类型标签，构建 RCTD 参考。
3. 在空间对象上运行 ``create.RCTD`` 与 ``run.RCTD`` 完成解卷积。
4. 导出主结果表、权重矩阵、可视化图与补充统计文件。

准备输入文件
------------
``RCTD`` 运行时需要两类输入：

1. 空间转录组对象 ``.h5ad``,由于RCTD并未有多样本分析功能,为了避免在多样本情况下出现生物学逻辑错误,我们先进行样本的拆分,每个样本对应一个空间对象。
2. 已带细胞类型注释的单细胞参考对象 ``.rds``,由于原论文中给出的数据为注释信息和h5文件,我们需要先整合为一个rds文件才能使用

这里可直接使用 :doc:`../integration_analysis/multi_sample_integration` 中输出的空间对象，并结合论文配套的 6 个单细胞数据文件构建参考对象。


.. code-block:: bash
  #若为单样本可跳过此步骤
  spatialsnake useful_tool --option=splitting results/merge_data/annotion/concatenated_sdata.zarr  --split_by sample
  #必须步骤,将zarr数据转换为h5ad格式,以方便程序转化为seurat对象,若您的数据为h5ad格式,或为seurat对象,可直接跳过此步骤.
  spatialsnake useful_tool --option=transform results/useful_results/ST8059052.zarr --transform_from=zarr --transform_to=h5ad --save_image=True --output_dir=results/useful_results

1. 参考数据下载

同理在工作目录中创建并运行下载脚本，将 6 个参考单细胞文件和注释表统一下载到 ``data/sc_data`` 目录：

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

运行
.. code-block:: bash

  chmod +x download.sh
  ./download.sh

2. 创建单细胞注释整合脚本 ``touch merge_anno.R``

.. code-block:: bash

  library(Seurat)
  library(dplyr)
  h5_files <- c(
    "5705STDY8058285_filtered_feature_bc_matrix.h5",
    "5705STDY8058284_filtered_feature_bc_matrix.h5",
    "5705STDY8058283_filtered_feature_bc_matrix.h5",
    "5705STDY8058282_filtered_feature_bc_matrix.h5",
    "5705STDY8058281_filtered_feature_bc_matrix.h5",
    "5705STDY8058280_filtered_feature_bc_matrix.h5"
  )
  obj_list <- list()
  for (f in h5_files) {
    sample_id <- sub("_filtered_feature_bc_matrix\\.h5$", "", basename(f))
    counts <- Read10X_h5(f)
    colnames(counts) <- paste0(sample_id, "_", colnames(counts))
    obj <- CreateSeuratObject(counts = counts, project = sample_id)
    obj$sample <- sample_id
    obj_list[[sample_id]] <- obj
  }
  merged_obj <- obj_list[[1]]
  if (length(obj_list) > 1) {
    for (i in 2:length(obj_list)) {
      merged_obj <- merge(merged_obj, y = obj_list[[i]])
    }
  }
  anno <- read.csv("cell_annotation.csv", stringsAsFactors = FALSE, check.names = FALSE)
  colnames(anno) <- trimws(colnames(anno))
  anno$`Cell ID` <- trimws(as.character(anno$`Cell ID`))
  anno$sample <- trimws(as.character(anno$sample))
  anno$annotation_1 <- trimws(as.character(anno$annotation_1))
  anno <- anno[!duplicated(anno$`Cell ID`), c("Cell ID", "sample", "annotation_1")]
  rownames(anno) <- anno$`Cell ID`
  meta <- merged_obj@meta.data
  meta$sample <- ifelse(
    rownames(meta) %in% rownames(anno),
    anno[rownames(meta), "sample"],
    meta$sample
  )
  meta$annotation_1 <- ifelse(
    rownames(meta) %in% rownames(anno),
    anno[rownames(meta), "annotation_1"],
    NA
  )
  merged_obj@meta.data <- meta
  before_n <- ncol(merged_obj)
  matched_cells <- rownames(merged_obj@meta.data)[!is.na(merged_obj@meta.data$annotation_1) & merged_obj@meta.data$annotation_1 != ""]
  merged_obj <- subset(merged_obj, cells = matched_cells)
  after_n <- ncol(merged_obj)
  DefaultAssay(merged_obj) <- "RNA"
  merged_obj <- JoinLayers(merged_obj, assay = "RNA")
  meta <- merged_obj@meta.data
  meta$annotation_1 <- as.character(meta$annotation_1)
  meta$sample <- as.character(meta$sample)
  merged_obj@meta.data <- meta
  saveRDS(merged_obj, file = "merged_sc_with_annotation.rds")

.. code-block:: bash
    Rscript merge_anno.R



推荐将 ``sample.txt`` 组织为以下格式：
----------------------------

.. code-block:: text

   sample_id   input_path                                      sc_reference
   ST8059052     results/useful_results/ST8059052.h5ad         data/merged_sc_with_annotation.rds



参数设置
----------------------------

.. code-block:: bash

  threads: 64
  RCTD_mode: "full" # 全模式 可选值："full" 或 "doublet"
  sc_cell_type_col: "annotation_1"
  spatial_cell_type_col: "celltype"
  group_by: "sample"
  max_cores: 8
  zarr_input: "" # 我们推荐输入原始的zarr数据以进行空间可视化展示


运行最终运行命令吧
----------------------------

.. code-block:: bash

   # 确保 annotion.yaml 与 sample.txt 位于当前工作目录
   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=RCTD --configfile annotion.yaml --zarr_input "results/useful_results/ST8059052.h5ad"

结果文件结构
----------------------------

.. code-block:: text

   results/
   └── {sample}/
       └── RCTD/
           ├── {sample}_RCTD_results.csv
           ├── {sample}_RCTD_weights.csv
           ├── {sample}.zarr/
           ├── {sample}_RCTD_spatial_plot.png
           ├── {sample}_RCTD_seurat.rds
           ├── {sample}_RCTD_full_dotplot.png
           ├── {sample}_RCTD_sample_dist_plot.png
           ├── {sample}_RCTD_cluster_plot.png
           ├── {sample}_RCTD_heatmap.png
           └── {sample}_RCTD_spot_class_bar.png


部分结果展示
--------------------------------

1. 结果表整合说明（CSV 文件）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RCTD 运行结束后，最重要的表格结果主要包括以下几类：

1. ``{sample}_RCTD_results.csv``
   该文件是主结果表，记录每个空间位点的主要预测结果，例如主导细胞类型及相关判定信息。它用于概览每个位点最终被赋予了什么类型，是后续空间解释与统计汇总的基础。

2. ``{sample}_RCTD_weights.csv``
   该文件是权重矩阵，记录每个空间位点在不同细胞类型上的归一化权重。它反映的是“组成比例”而不是单一标签，因此适合用于分析混合位点、比较细胞类型丰度，以及支持热图等下游展示。

3. ``{sample}_RCTD_results_all.csv`` 或同类补充结果表（若流程输出）
   该类文件通常用于保留更完整的中间判定信息或附加统计结果，便于用户追溯每个位点在不同模式下的预测细节。

4. 由主结果进一步汇总得到的统计表
   这类文件通常用于支撑比例热图、分类柱状图或分组统计图，内容本质上是对主结果表和权重矩阵的再整理，用于展示各细胞类型在样本、区域或类别层面的分布情况。

总体而言，``{sample}_RCTD_results.csv`` 用于回答“每个位点主要是什么细胞类型”，而 ``{sample}_RCTD_weights.csv`` 用于回答“每个位点由哪些细胞类型构成，以及各自所占比例是多少”。

2. 空间主图（``{sample}_RCTD_spatial_plot.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_spatial_plot.png
   :width: 88%
   :align: center
   :alt: RCTD spatial plot

解释：
该图是 RCTD 结果的总体空间展示。图中通常同时给出主导细胞类型分布与对应主导比例，用于展示不同细胞类型在组织中的空间位置，以及各位点预测结果的集中程度。

3. 相关性气泡图（``{sample}_RCTD_full_dotplot.png``，full 模式重点结果）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_full_dotplot.png
   :width: 88%
   :align: center
   :alt: RCTD full dotplot

解释：
该图主要用于 ``RCTD_mode = full``。横轴一般表示空间聚类或用户定义的分组，纵轴表示参考细胞类型。我们使用Person correlation 来展示相关程度的大小，颜色用于展示相关方向和强弱，因此可以直观看到空间亚群与参考细胞类型之间的对应关系。

4. 比例热图（``{sample}_RCTD_heatmap.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_heatmap.png
   :width: 88%
   :align: center
   :alt: RCTD heatmap

解释：
此图只在doublet模式下生成,由于适用于高分辨率数据，比例热图用于展示预测细胞类型的相对丰度。颜色深浅对应比例大小，因此能够直接反映非监督聚类和预测结果之间的差异

5. Spot 分类柱状图（``{sample}_RCTD_spot_class_bar.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_spot_class_bar.png
   :width: 80%
   :align: center
   :alt: RCTD spot class bar

解释：
该图展示不同位点被判定为 singlet、doublet 或 reject 的比例情况，用于概览样本中不同类型判定结果的组成结构，可查看预测的质量。


