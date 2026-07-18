Algorithm-Based Annotation (RCTD)
==================================================================

``RCTD`` uses annotated single-cell reference data to perform cell-type deconvolution on spatial transcriptomics data, offering a practical balance between spatial resolution and cell-type resolution.
In ``full`` mode, RCTD estimates the relative cell-type composition at each spatial location, making it particularly suitable for lower-resolution platforms such as Visium.
In ``doublet`` mode, RCTD reports ``first_type`` and ``second_type`` predictions together with a confidence class. ``second_type`` is interpreted only for ``doublet_certain`` spots.

Because RCTD results are often interpreted together with unsupervised spatial regions, regional summaries report full-mode normalized weights or doublet-mode first-type proportions and their descriptive enrichment relative to the tissue-wide mean.

.. note::
   1. RCTD requires raw count matrices, so both single-cell and spatial inputs should be unnormalized integer count data. If the data have been processed through the Spatialsnake pipeline, the raw expression matrix is typically preserved in the object and can be recovered.
   2. It is recommended that each cell type in the single-cell reference contains at least 25 cells. Extremely rare cell types are automatically removed by the pipeline, so it is advisable to use high-quality, reliably annotated reference data.


In short, the goal of this module is to estimate relative cell-type composition in ``full`` mode or confidence-aware first/second cell-type assignments in ``doublet`` mode.


``RCTD`` requires the following two inputs:

1. A spatial transcriptomics object stored as a SpatialData ``.zarr`` directory. This is the only spatial input supplied by the user. Because RCTD is not suitable for direct multi-sample integrated analysis, multi-sample spatial data should typically be split by sample and run individually first.
2. A single-cell reference object in ``.h5ad`` or ``.rds`` format. In the example data, the public data are provided as an annotation table and HDF5 files, so they need to be assembled into an annotated ``.rds`` reference object first.


Step 1: ``sample.txt`` configuration file
------------------------------------------------------

``sample.txt`` uses exactly one spatial input path per sample. The second column is the SpatialData Zarr directory and the third column is the single-cell reference:

.. code-block:: text

   sample_id   spatial_zarr                                    sc_reference
   sample_id   results/useful_results/sample_id.zarr           data/merged_sc_with_annotation.rds


Step 2: Parameter Selection and Configuration
------------------------------------------------------------------------------------------

The following parameters are usually the highest priority to confirm when running RCTD:

.. list-table::
   :header-rows: 1
   :widths: 28 18 54

   * - Parameter
     - Example
     - Description
   * - ``RCTD_mode``
     - ``full`` / ``doublet``
     - Specifies the RCTD prediction mode; ``full`` is better suited for lower-resolution spatial data, ``doublet`` is more appropriate when focusing on dominant cell-type combinations
   * - ``sc_cell_type_col``
     - ``celltype``
     - Column name storing cell-type labels in the single-cell reference object
   * - ``spatial_cell_type_col``
     - ``celltype``
     - Existing unsupervised spatial-region column used by the full- and doublet-mode regional dotplots
   * - ``group_by``
     - ``sample``
     - Sample column used to compute sample-balanced regional summaries
   * - ``rctd_dotplot_max_cell_types``
     - ``30``
     - Maximum number of cell types displayed in a regional dotplot; use ``0`` to display all
   * - ``rctd_dotplot_enrichment_clip``
     - ``2.5``
     - Symmetric display limit for the regional log2-enrichment colour scale
   * - ``threads``
     - ``8``
     - Number of threads passed to RCTD and the postprocessing rule

Configuration recommendations:

1. ``RCTD_mode`` is one of the most critical parameters. If the goal is to estimate cell-type composition at each spot, ``full`` is usually the preferred choice; if the focus is on dominant cell types and doublet inference, ``doublet`` may be considered.
2. ``sc_cell_type_col`` must match the actual annotation column name in the reference object; otherwise RCTD cannot correctly identify reference cell types.
3. The second column of ``sample.txt`` must point to an existing ``.zarr`` directory. The same object is used for conversion, visualization, and result write-back, so no additional spatial input parameter is needed.

A typical configuration example:

.. code-block:: yaml

   threads: 8
   RCTD_mode: "full"                    # RCTD prediction mode
   sc_cell_type_col: "celltype"         # Column name of cell-type labels in the single-cell reference object
   spatial_cell_type_col: "celltype"    # Existing unsupervised spatial-region column
   group_by: "sample"
   rctd_dotplot_max_cell_types: 30      # Maximum number of cell types displayed in the regional dotplot; use 0 to display all
   rctd_dotplot_enrichment_clip: 2.5    # Symmetric display limit for the regional log2-enrichment colour scale


Step 3: Run the Command
----------------------------------------------

Ensure that ``annotation.yaml`` and ``sample.txt`` are ready in the working directory, then run:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=RCTD --configfile=annotation.yaml


Demo for RCTD
----------------------------------------------


Here we use the spatial object generated in :doc:`../integration_analysis/multi_sample_integration` as an example, together with the six accompanying single-cell files from the published study.
If you are using a multi-sample integrated spatial object, first use the splitting utility to create one Zarr object per sample. If a prepared annotation file is available in the project resources, it can be used to retain consistent labels across the resulting sample objects.

Using the six single-cell files from the example study, the following demonstrates how to build the reference object required for RCTD and run the pipeline.


1. Prepare the spatial transcriptomics data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash


   # If the data are already single-sample, the splitting step can be skipped
   spatialsnake useful_tool --option=splitting results/merge_data/annotation/concatenated_sdata.zarr --split_by=sample

2. Prepare the single-cell transcriptomics data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similarly, we use the six mouse brain single-cell data from the accompanying publication. Create and run the download script in your working directory to download the six single-cell reference files and the annotation table to ``data/sc_data``.

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


3. Build the single-cell reference object ``merge_anno.R``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create the reference assembly script ``merge_anno.R`` to integrate the six single-cell files and write an annotated ``.rds`` object:

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
  anno$celltype <- trimws(as.character(anno$annotation_1))
  anno <- anno[!duplicated(anno$`Cell ID`), c("Cell ID", "sample", "celltype")]
  rownames(anno) <- anno$`Cell ID`
  meta <- merged_obj@meta.data
  meta$sample <- ifelse(
    rownames(meta) %in% rownames(anno),
    anno[rownames(meta), "sample"],
    meta$sample
  )
  meta$celltype <- ifelse(
    rownames(meta) %in% rownames(anno),
    anno[rownames(meta), "celltype"],
    NA
  )
  merged_obj@meta.data <- meta
  before_n <- ncol(merged_obj)
  matched_cells <- rownames(merged_obj@meta.data)[!is.na(merged_obj@meta.data$celltype) & merged_obj@meta.data$celltype != ""]
  merged_obj <- subset(merged_obj, cells = matched_cells)
  after_n <- ncol(merged_obj)
  DefaultAssay(merged_obj) <- "RNA"
  merged_obj <- JoinLayers(merged_obj, assay = "RNA")
  meta <- merged_obj@meta.data
  meta$celltype <- as.character(meta$celltype)
  meta$sample <- as.character(meta$sample)
  merged_obj@meta.data <- meta
  saveRDS(merged_obj, file = "merged_sc_with_annotation.rds")

Run the script:

.. code-block:: bash

   Rscript merge_anno.R


4. Configure ``sample.txt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   sample_id   spatial_zarr                                    sc_reference
   ST8059052 results/useful_results/ST8059052.zarr data/MTAB/merged_sc_with_annotation.rds


5. Run the command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default parameters are suitable for this example. For other datasets, verify that the cell-annotation column name is correctly specified.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=RCTD


Results and Interpretation
----------------------------------------------------

Result file structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   results/
   └── {sample}/
       └── RCTD/
           ├── {sample}_RCTD_results.csv
           ├── {sample}_RCTD_weights.csv
           ├── {sample}.zarr/
           ├── {sample}_RCTD_seurat.rds
           ├── {sample}_RCTD.rds
           ├── {sample}_RCTD_full_dotplot.pdf                 # full mode
           ├── {sample}_RCTD_full_dotplot_source.tsv          # full mode
           ├── {sample}_RCTD_spatial_plot.pdf                 # doublet mode
           ├── {sample}_RCTD_spatial_plot_source.tsv          # doublet mode
           ├── {sample}_RCTD_doublet_proportion_dotplot.pdf   # doublet mode
           ├── {sample}_RCTD_doublet_proportion_dotplot_source.tsv
           ├── {sample}_RCTD_spot_class_bar.pdf               # doublet mode
           └── {sample}_RCTD_spot_class_bar_source.tsv


1. Primary result tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following RCTD analysis, Spatialsnake extends the visualizations provided in the official tutorial with additional plots informed by published studies. These outputs facilitate comparison between RCTD-based reference annotations and cell-type assignments derived from unsupervised clustering.

1. ``{sample}_RCTD_results.csv``
   In ``doublet`` mode, this file contains ``spot_class``, ``first_type``, ``second_type``, and the remaining official RCTD result fields. In ``full`` mode, spacexr does not produce ``results_df``; the file therefore retains the fitted spot identifiers only.

2. ``{sample}_RCTD_weights.csv``
   This file stores row-normalized cell-type weights for each fitted spatial location. The values are relative mixture proportions, not absolute cell counts. Spots filtered by RCTD remain missing rather than being forced into a cell type when the matrix is written back to Zarr.

3. ``{sample}.zarr``
   This result is based on the original SpatialData object, so its complete expression matrix, images, shapes, coordinate systems, and pre-existing metadata are retained. In both modes, ``obsm["RCTD_weights"]`` stores the continuous row-normalized proportions, and ``uns["RCTD"]`` records ``mode``, ``weight_key``, ``weight_scale``, ``cell_types``, ``n_input_spots``, and ``n_fitted_spots``. The weight scale is explicitly recorded as ``row_normalized_proportion``.

   In ``full`` mode, no dominant cell type or other discrete annotation is created. In ``doublet`` mode, all fields from the official ``results_df`` are aligned to spot identifiers and written to ``obs``, including ``spot_class``, ``first_type``, and ``second_type``; the plotting-friendly ``RCTD_first_type`` and ``RCTD_second_type`` fields are retained as well.

In full mode, the following figures are generated:

.. figure:: /_static/images/ST8059052_RCTD_full_dotplot_page-0001.jpg
   :width: 76%
   :align: center
   :alt: Abundance of cell types in each spatial region, normalized by the tissue-wide mean

In doublet mode, the following figures are generated:

.. figure:: /_static/images/ST8059052_RCTD_spot_class_bar_page-0001.jpg
   :width: 76%
   :align: center
   :alt: RCTD spot classification in doublet mode

.. figure:: /_static/images/ST8059052_RCTD_doublet_proportion_dotplot_page-0001.jpg
   :width: 76%
   :align: center
   :alt: RCTD proportions of first and second cell types in doublet mode

.. figure:: /_static/images/ST8059052_RCTD_spatial_plot_page-0001.jpg
   :width: 76%
   :align: center
   :alt: RCTD first and second cell-type assignments in doublet mode

