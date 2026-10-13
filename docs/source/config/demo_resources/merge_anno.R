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
