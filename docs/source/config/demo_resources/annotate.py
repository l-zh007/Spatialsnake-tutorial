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
anno["celltype"] = anno["annotation_1"].astype(str).str.strip()
anno = anno.drop_duplicates(subset=["CellID"], keep="first")
anno = anno.set_index("CellID")

anno_aligned = anno.reindex(adata_merged.obs_names)
matched_mask = anno_aligned["celltype"].notna()
adata_merged = adata_merged[matched_mask].copy()
anno_aligned = anno_aligned.loc[matched_mask]
adata_merged.obs["sample"] = anno_aligned["sample"].values
adata_merged.obs["celltype"] = anno_aligned["celltype"].values
adata_merged.var["gene_ids"] = adata_merged.var.index
adata_merged.write_h5ad("merged_sc_with_annotation.h5ad")
