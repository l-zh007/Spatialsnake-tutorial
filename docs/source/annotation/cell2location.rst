Algorithm-Based Annotation (``cell2Location``)
==============================================

``cell2Location`` maps cell-type information from a single-cell reference onto spatial locations, producing estimated cell-type abundances for each location together with spatial visualizations and summary tables.
For lower-resolution spatial data such as Visium, this method is particularly useful because it estimates cell composition per spot rather than forcing each spot into a single label.
It also supports annotation of integrated multi-sample spatial objects, which helps reduce annotation inconsistency across samples.
In addition to the standard cell2location outputs, the pipeline further correlates abundance results with manually defined or unsupervised cluster regions and generates bubble plots to help interpret local cell-type composition.



For the configuration reference, see :doc:`../config_reference/annotation_yaml`.

Workflow overview
-----------------
1. Read the spatial object (``zarr``) and the annotated single-cell reference object (``h5ad``).
2. Train the regression model on the reference data to learn cell-type-specific expression signatures.
3. Fit the cell2location model on the spatial object and estimate cell-type abundance for each spatial location.
4. Perform downstream non-negative matrix factorization on the abundance matrix, write the results back to the object, and generate visualization outputs, summary plots, and intermediate QC files.


Prepare the input files
-----------------------
``cell2Location`` requires two input types:

1. A spatial transcriptomics object in ``.zarr`` format. If you only have a spatial ``.h5ad`` object, convert it first with :doc:`../useful_tool/transform`.
2. A single-cell reference object in ``.h5ad`` format that already contains cell-type annotations. If you only have a Seurat object, convert it first in the same way with :doc:`../useful_tool/transform`.

Here we use the spatial object generated in :doc:`../integration_analysis/multi_sample_integration` together with six matching single-cell files from the study to build the reference object.

1. Download the reference data

Create and run a download script in the working directory to retrieve the six single-cell reference files and the annotation table into ``data/sc_data``. You can also download them manually if preferred.

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

.. code-block:: bash

  chmod +x download.sh
  ./download.sh


2. Build the annotated reference object

Create ``annotate.py`` and run it with ``python annotate.py``:

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

``sample.txt`` must contain both the spatial object path and the single-cell reference path.
.. code-block:: text
  
   sample_id           input_path                                      sc_reference
   concatenated_sdata  results/merge_data/annotation/concatenated_sdata  data/MTAB/merged_sc_with_annotation.h5ad


Key parameters
--------------

Optional settings
-----------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - ``--anno_algorithm``
     - ``cell2Location``
     - Selects cell2location as the annotation algorithm
   * - ``--device``
     - ``cuda`` / ``cpu``
     - Training device, which affects runtime
   * - ``--image_type``
     - ``hires``
     - Image layer used for spatial rendering
   * - ``--shape_type``
     - ``cell_boundaries``
     - Shape layer used for overlay visualization
   * - ``--max_cores``
     - ``16``
     - Upper limit on parallel resources
   * - ``max_epochs_reference``
     - ``250``
     - Number of training epochs for the reference regression model
   * - ``max_epochs_st``
     - ``30000``
     - Number of training epochs for the spatial model
   * - ``remove_mt``
     - ``True``
     - Whether to remove mitochondrial genes before training
   * - ``N_cells_per_location``
     - ``30``
     - Prior on the number of cells per spatial location
   * - ``labels_key_reference``
     - ``annotation_1``
     - Column name in the reference object that stores cell-type labels
   * - ``batch_key_reference``
     - ``sample``
     - Column name in the reference object that stores batch or sample identity
   * - ``batch_key_st``
     - ``sample``
     - Column name in the spatial object that stores sample identity, used especially for integrated multi-sample analyses
   * - ``cell_count_cutoff``
     - ``15``
     - Cell-count threshold used when filtering genes in the reference data
   * - ``cell_percentage_cutoff2``
     - ``0.05``
     - Cell-percentage threshold used when filtering genes in the reference data
   * - ``nonz_mean_cutoff``
     - ``1.12``
     - Non-zero mean expression threshold used when filtering genes in the reference data
   * - ``detection_alpha``
     - ``20``
     - Detection-rate prior parameter for the spatial model
   * - ``save_models``
     - ``True``
     - Whether to save the reference and spatial model directories

The most important parameters are usually ``labels_key_reference``, ``batch_key_reference``, and ``batch_key_st``.
If the reference data are integrated across multiple samples, it is usually best to set both batch-related parameters to ``sample`` so that the model can recognize sample origin correctly.

If you prefer to manage these settings in a configuration file, use ``annotation.yaml``:


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

Setting both ``batch_key_reference`` and ``batch_key_st`` to ``sample`` makes cross-sample comparison more reliable.

Run the workflow
----------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=cell2Location


Result file structure
---------------------

In single-sample mode, the main results are usually written to ``results/{sample}/cell2Location/``:

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

The file ``{sample}.zarr`` is the main object for downstream analysis. ``Cell2Loc_inf_aver.csv`` and ``figure/cluster_abundance_stats.csv`` are the most frequently used tabular outputs, while the figures are mainly used to assess training quality, spatial abundance patterns, and compositional differences.

How to interpret the results
----------------------------

1. Main result tables
~~~~~~~~~~~~~~~~~~~~~

After cell2location finishes, the most commonly used tables include the following:

1. ``Cell2Loc_inf_aver.csv``
   This file stores the cell-type expression signatures learned by the reference model and serves as the basis for spatial mapping.

2. ``figure/cluster_abundance_stats.csv``
   This file summarizes cell-type abundance statistics across clusters or sample groups and supports downstream barplots and group comparisons.

3. Additional intermediate or model directories
   ``Reference_model/``, ``Spatial_model/``, ``CoLocatedComb/``, and ``test.h5ad`` are primarily used for model persistence, colocalization review, and reproducibility tracking rather than as the first entry point for biological interpretation.

In summary, ``{sample}.zarr`` stores the abundance results written back into the spatial object, ``Cell2Loc_inf_aver.csv`` describes the learned reference signatures, and ``cluster_abundance_stats.csv`` is especially useful for region-level or group-level composition comparisons.

2. Training convergence curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/ELBO_sc_model.png
   :width: 82%
   :align: center
   :alt: cell2location training curve

Interpretation:
This ELBO curve visualizes model training. The x-axis shows training iterations and the y-axis shows the objective value, allowing you to judge whether the reference model or spatial model is converging stably.

3. Bubble plot relating abundance to unsupervised regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/dotplot.png
   :width: 90%
   :align: center
   :alt: cell2location spatial abundance

Interpretation:
This plot summarizes how different cell types are distributed across tissue regions. Different panels correspond to different cell types and help you identify spatial enrichment, continuity, and region-specific patterns.


4. Cell composition barplot (``cluster_abundance_stacked_bar.png``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/cluster_abundance_stacked_bar.png
   :width: 82%
   :align: center
   :alt: cell2location abundance barplot

Interpretation:
This stacked barplot shows the relative abundance of each cell type across clusters or samples and is useful for comparing compositional differences between regions.

5. NMF-based decomposition analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/n_fact12.png
   :width: 76%
   :align: center
   :alt: cell2location reconstruction qc


6. Spatial visualization of decomposition factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MNF_spatial.png
   :width: 76%
   :align: center
   :alt: cell2location reconstruction qc


7. Spatial map of dominant predicted cell abundance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/max_cell.png
   :width: 90%
   :align: center
   :alt: cell2location spatial abundance

For low-resolution data, cell2location returns abundance weights rather than a single hard label. Here we visualize only the maximum-abundance cell type for each spot as a coarse summary.
