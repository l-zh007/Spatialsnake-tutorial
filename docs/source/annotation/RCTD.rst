Algorithm-Based Annotation (RCTD)
=================================

模块介绍
----

``RCTD`` 使用已注释的单细胞参考数据对空间转录组数据进行细胞类型解卷积，在空间分辨率与细胞类型分辨率之间提供了较为实用的平衡。
在 ``full`` 模式下，RCTD 估计每个空间位置的细胞类型组成，因此尤其适用于 Visium 等较低分辨率平台。
在 ``doublet`` 与 ``singlet`` 模式下，RCTD 则输出 ``first_type``、``second_type`` 等主导细胞类型标签，这类结果在较高分辨率数据中通常更具解释性。

由于 RCTD 结果在空间转录组研究中常与无监督聚类结果联合解读，本流程除输出标准解卷积结果外，还保留与聚类结构相关的比较性汇总结果。
这些结果包括基于相关性与比例重叠的辅助统计，有助于评估 RCTD 推断结果与无监督聚类结构的一致程度。

.. note::
   1. RCTD 需要原始计数矩阵，因此单细胞与空间输入均应为未经归一化的整数计数数据。若数据已通过 Spatialsnake 流程处理，原始表达矩阵通常仍保留在对象中并可被恢复调用。
   2. 单细胞参考中建议每种细胞类型至少包含 25 个细胞。极少见细胞类型会被流程自动移除，因此推荐使用高质量且注释可靠的参考数据。


基本 workflow
-----------

1. 从 ``sample.txt`` 中读取空间对象路径与单细胞参考路径。
2. 提取参考数据中的细胞类型注释信息，并构建 RCTD 所需的参考对象。
3. 在空间数据上运行 ``create.RCTD`` 与 ``run.RCTD`` 完成解卷积分析。
4. 输出主结果表、权重矩阵、空间图像及其他辅助汇总文件。

简而言之，该模块的核心目标是利用高质量单细胞参考，为每个空间位置估计细胞组成或主导细胞类型，并为后续空间解释与聚类比较提供依据。


基本运行步骤
------

``RCTD`` 运行通常需要以下两类输入：

1. 空间转录组对象，格式为 ``.h5ad``。由于 RCTD 不适用于直接多样本整合分析，多样本空间数据通常需先按样本拆分后分别运行。
2. 单细胞参考对象，格式为 ``.rds``。在示例数据中，公开数据以注释表和 HDF5 文件形式提供，因此需要先组装为一个带注释的 ``.rds`` 参考对象。

这里以 :doc:`../integration_analysis/multi_sample_integration` 中生成的空间对象为例，并使用研究中配套发表的 6 个单细胞文件构建参考对象。

若当前使用的是多样本整合后的空间对象，请先使用我们的utility-tools进行数据拆分，再将 ``zarr`` 转换为 ``h5ad`` 以便传入基于 R 的 RCTD 流程：

step 1: ``sample.txt`` 配置文件
---------------------------

``sample.txt`` 需至少包含空间对象路径与单细胞参考路径。

.. code-block:: text

   sample_id   input_path                                      sc_reference
   ST8059052   results/useful_results/ST8059052.h5ad           data/merged_sc_with_annotation.rds


step 2: 参数选择与配置
---------------

以下参数通常是运行 RCTD 时最需要优先确认的设置：

.. list-table::
   :header-rows: 1
   :widths: 28 18 54

   * - Parameter
     - Example
     - Description
   * - ``RCTD_mode``
     - ``full`` / ``doublet``
     - 指定 RCTD 的预测模式；``full`` 更适合低分辨率空间数据，``doublet`` 更适合关注主导细胞类型组合的场景
   * - ``sc_cell_type_col``
     - ``annotation_1``
     - 单细胞参考对象中存储细胞类型标签的列名
   * - ``spatial_cell_type_col``
     - ``celltype``
     - 空间对象中已有注释列名，用于对照展示或下游比较
   * - ``group_by``
     - ``sample``
     - 用于分组汇总或比较的列名，常用于样本层面的组织
   * - ``max_cores``
     - ``8``
     - 并行计算核心数上限
   * - ``threads``
     - ``64``
     - 后端线程数量设置，会影响整体运行速度
   * - ``zarr_input``
     - ``results/useful_results/ST8059052.zarr``
     - 若可提供原始 ``zarr`` 对象，通常更利于后续空间可视化结果写回与展示

配置建议：

1. ``RCTD_mode`` 是最关键的参数之一。若目标是估计每个 spot 的细胞组成，通常优先使用 ``full``；若更关注主导细胞类型及双细胞型推断，可考虑 ``doublet``。
2. ``sc_cell_type_col`` 必须与参考对象中的真实注释列名一致，否则 RCTD 无法正确识别参考细胞类型。
3. 若后续仍需在空间对象中进行结果可视化，建议保留或补充 ``zarr_input``，便于结果回写到更适合空间展示的对象中。

常见配置示例如下：

.. code-block:: bash

   threads: 64
   RCTD_mode: "full"
   sc_cell_type_col: "annotation_1"
   spatial_cell_type_col: "celltype"
   group_by: "sample"
   max_cores: 8
   zarr_input: ""


step 3: 命令运行
------------

请确保工作目录中已经准备好 ``annotation.yaml`` 与 ``sample.txt``，随后运行：

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=RCTD --configfile=annotation.yaml --zarr_input="results/useful_results/ST8059052.h5ad"


Demo 演示流程
---------

下面以示例研究中的 6 个单细胞文件为例，演示如何构建 RCTD 所需的参考对象并运行流程。

1. 空间转录组数据准备
~~~~~~~~~~~~

.. code-block:: bash

   # 如果当前已经是单样本数据，则可跳过拆分步骤
   spatialsnake useful_tool --option=splitting results/merge_data/annotation/concatenated_sdata.zarr --split_by=sample

   # 将 zarr 转换为 h5ad，以便传入 RCTD 工作流
   spatialsnake useful_tool --option=transform results/useful_results/ST8059052.zarr --transform_from=zarr --transform_to=h5ad --save_image=True --output_dir=results/useful_results

2. 单细胞转录组数据准备
~~~~~~~~~~~~~

同理我们使用期刊文献中配套的六个小鼠脑单细胞数据,请在工作目录中创建并运行下载脚本，将 6 个单细胞参考文件及注释表下载至 ``data/sc_data``。

创建脚本文件：

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

运行脚本：

.. code-block:: bash

   chmod +x download.sh
   ./download.sh


3. 构建单细胞参考对象 ``merge_anno.R``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

创建参考组装脚本 ``merge_anno.R``，将 6 个单细胞文件整合并写出带注释的 ``.rds`` 对象：

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

运行脚本：

.. code-block:: bash

   Rscript merge_anno.R


4. ``sample.txt`` 配置文件
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   input_path                                      sc_reference
   ST8059052   results/useful_results/ST8059052.h5ad           data/merged_sc_with_annotation.rds


5. 命令运行
~~~~~~~

默认参数即适配该demo,若为其他数据集,请务必检查细胞注释列名是否对应符合

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=RCTD


结果展示与解读
-------

Result file structure
~~~~~~~~~~~~~~~~~~~~~

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


1. 主要结果表格
~~~~~~~~~

RCTD 完成后，最重要的表格输出通常包括以下几类：

1. ``{sample}_RCTD_results.csv``
   该文件为主结果表，记录每个空间位置的主导预测细胞类型及相关分配信息，是后续解释与统计汇总的基础。

2. ``{sample}_RCTD_weights.csv``
   该文件保存每个空间位置上不同细胞类型的归一化权重矩阵。它反映的是组成结构而非单一标签，因此尤其适用于混合位置分析、丰度比较及后续热图展示。

3. ``{sample}_RCTD_results_all.csv`` 或其他补充结果表（若生成）
   这类文件通常保存更细致的中间预测信息或辅助统计，适用于追踪每个位置的预测依据。

4. 基于主结果派生的汇总文件
   这些结果通常用于生成比例热图、分类柱状图或分组统计图，对主结果表与权重矩阵进行再次整理以便解释。

简而言之，``{sample}_RCTD_results.csv`` 主要回答“每个位置最可能是什么细胞类型”，而 ``{sample}_RCTD_weights.csv`` 则更适合回答“每个位置由哪些细胞类型构成，以及各自占比如何”。


2. 空间概览图（``{sample}_RCTD_spatial_plot.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_spatial_plot.png
   :width: 88%
   :align: center
   :alt: RCTD spatial plot

该图提供 RCTD 结果的整体空间视图，通常同时展示主导预测细胞类型及其对应比例，可用于判断不同细胞类型在组织中的空间富集位置以及预测集中程度。


3. 相关性气泡图（``{sample}_RCTD_full_dotplot.png``，``full`` 模式关键输出）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_full_dotplot.png
   :width: 88%
   :align: center
   :alt: RCTD full dotplot

该图主要用于 ``RCTD_mode = full``。横轴通常表示空间聚类或用户定义分组，纵轴表示参考细胞类型，图中利用 Pearson 相关性概括不同空间组与参考细胞类型之间的对应强度。


4. 比例热图（``{sample}_RCTD_heatmap.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_heatmap.png
   :width: 88%
   :align: center
   :alt: RCTD heatmap

该图常在 ``doublet`` 模式下生成，尤其适合较高分辨率数据。其颜色强度反映预测细胞类型的相对比例，有助于比较无监督聚类结果与 RCTD 预测之间的一致性。


5. Spot 分类柱状图（``{sample}_RCTD_spot_class_bar.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_spot_class_bar.png
   :width: 80%
   :align: center
   :alt: RCTD spot class bar

该柱状图展示被分类为 singlet、doublet 或 reject 的空间位置比例，可为整体样本的分类质量提供简洁概览。
