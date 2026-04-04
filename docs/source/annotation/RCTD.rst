Algorithm-Based Annotation (RCTD)
=================================

``RCTD`` performs cell-type deconvolution for spatial transcriptomics data by using an annotated single-cell reference.
We include this method because it offers a practical balance between spatial resolution and cell-type resolution.
In ``full`` mode, RCTD estimates the cell-type composition of each spatial location and is therefore well suited to lower-resolution platforms such as Visium.
In ``doublet`` and ``singlet`` modes, it assigns dominant cell-type labels such as ``first_type`` and ``second_type``, which are often more informative for higher-resolution data.

Because RCTD results are often interpreted alongside unsupervised clustering in the spatial transcriptomics literature, the workflow exports both the standard deconvolution outputs and comparison summaries against clustering-based structure.
These include correlation-based summaries and proportional overlap summaries that help assess how well the RCTD results agree with unsupervised clusters.

.. note::
   1. RCTD requires raw count matrices. The single-cell and spatial inputs should therefore be unnormalized integer-count data. If you use data processed through the Spatialsnake workflow, the raw expression matrix is retained and can be recovered from the object.
   2. The single-cell reference should contain at least 25 cells per cell type. Very rare cell types are removed automatically by the pipeline. High-quality and well-curated reference annotations are strongly recommended.

Workflow overview
-----------------
1. Read the spatial object path and the single-cell reference path from ``sample.txt``.
2. Extract the reference cell-type annotations and construct the RCTD reference object.
3. Run ``create.RCTD`` and ``run.RCTD`` on the spatial data.
4. Export the main result table, weight matrix, plots, and additional summary files.

Prepare the input files
-----------------------
``RCTD`` requires two main inputs:

1. A spatial transcriptomics object in ``.h5ad`` format. Because RCTD is not designed for direct multi-sample integration, multi-sample spatial data should first be split so that each sample is analyzed separately.
2. An annotated single-cell reference object in ``.rds`` format. In the example dataset, the published data are distributed as annotation tables plus HDF5 files, so the reference must first be assembled into one ``.rds`` object.

Here we use the spatial object generated in :doc:`../integration_analysis/multi_sample_integration` and build the reference object from the six matching single-cell files published with the study.


.. code-block:: bash

   # Skip the first step if you are already working with a single sample
   spatialsnake useful_tool --option=splitting results/merge_data/annotation/concatenated_sdata.zarr --split_by=sample

   # Convert zarr to h5ad so the object can be passed into the R-based workflow
   spatialsnake useful_tool --option=transform results/useful_results/ST8059052.zarr --transform_from=zarr --transform_to=h5ad --save_image=True --output_dir=results/useful_results

1. Download the reference data

Create and run a download script in the working directory to retrieve the six single-cell reference files and the annotation table into ``data/sc_data``:

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

2. Create the single-cell reference assembly script ``merge_anno.R``

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



Sample.txt format
-----------------

.. code-block:: text

   sample_id   input_path                                      sc_reference
   ST8059052     results/useful_results/ST8059052.h5ad         data/merged_sc_with_annotation.rds



Common parameters
-----------------

.. code-block:: bash

   threads: 64
   RCTD_mode: "full" # choose from "full" or "doublet"
   sc_cell_type_col: "annotation_1"
   spatial_cell_type_col: "celltype"
   group_by: "sample"
   max_cores: 8
   zarr_input: "" # if available, the original zarr object is recommended for spatial visualization

Run the workflow
----------------

.. code-block:: bash

   # Ensure that annotation.yaml and sample.txt are available in the working directory
   spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=RCTD --configfile=annotation.yaml --zarr_input="results/useful_results/ST8059052.h5ad"

Result file structure
---------------------

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


How to interpret the results
----------------------------

1. Main result tables
~~~~~~~~~~~~~~~~~~~~~

After RCTD completes, the most important tabular outputs are:

1. ``{sample}_RCTD_results.csv``
   This is the main result table. It records the dominant predicted cell type and related assignment information for each spatial location and serves as the foundation for downstream interpretation and summary statistics.

2. ``{sample}_RCTD_weights.csv``
   This file stores the normalized weight matrix across cell types for each spatial location. It captures compositional structure rather than a single label and is therefore especially useful for mixed-location analysis, abundance comparisons, and downstream heatmaps.

3. ``{sample}_RCTD_results_all.csv`` or analogous supplementary result tables (if generated)
   These files retain more detailed intermediate assignments or supplementary statistics and are useful when you need to trace the prediction logic for each location.

4. Additional summary tables derived from the main outputs
   These are typically used to generate proportion heatmaps, class barplots, or grouped summaries and reorganize the main result table and weight matrix into more interpretable formats.

In short, ``{sample}_RCTD_results.csv`` answers the question "what is the dominant predicted cell type at each location?", whereas ``{sample}_RCTD_weights.csv`` answers "which cell types contribute to each location, and in what proportions?".

2. Spatial summary plot (``{sample}_RCTD_spatial_plot.png``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_spatial_plot.png
   :width: 88%
   :align: center
   :alt: RCTD spatial plot

Interpretation:
This figure provides the main spatial overview of the RCTD result. It typically displays both the dominant predicted cell type and its associated proportion, allowing you to assess where each cell type is enriched in tissue and how confidently the prediction is concentrated at each location.

3. Correlation dot plot (``{sample}_RCTD_full_dotplot.png``; key output in ``full`` mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_full_dotplot.png
   :width: 88%
   :align: center
   :alt: RCTD full dotplot

Interpretation:
This figure is mainly used in ``RCTD_mode = full``. The x-axis usually represents spatial clusters or user-defined groups, and the y-axis represents reference cell types. The plot uses Pearson correlation to summarize how strongly each spatial group corresponds to each reference cell type.

4. Proportion heatmap (``{sample}_RCTD_heatmap.png``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_heatmap.png
   :width: 88%
   :align: center
   :alt: RCTD heatmap

Interpretation:
This figure is generated in ``doublet`` mode and is particularly useful for higher-resolution data. It summarizes the relative abundance of predicted cell types, with color intensity reflecting relative proportion, and therefore helps compare unsupervised clusters with RCTD-based predictions.

5. Spot-class bar plot (``{sample}_RCTD_spot_class_bar.png``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MTAB_RCTD_spot_class_bar.png
   :width: 80%
   :align: center
   :alt: RCTD spot class bar

Interpretation:
This bar plot shows the proportions of locations classified as singlet, doublet, or reject. It provides a concise overview of classification quality across the sample.
