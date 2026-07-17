Algorithm-Based Annotation (``cell2location``)
==============================================

``cell2location`` maps cell-type information from a single-cell reference onto spatial transcriptomic locations, thereby estimating cell-type abundance at each spatial position and generating corresponding spatial visualizations and summary tables.

For lower-resolution spatial data such as Visium, this method is particularly well suited because it does not force a single label onto each spot, but instead estimates the continuous abundance of different cell types within each spot.
The method also supports annotation of spatially integrated objects from multiple samples, helping to reduce annotation inconsistency across samples.
In addition to the standard cell2location outputs, the pipeline further relates the abundance results to manually defined or unsupervised clustering-derived regions, generating bubble plots and other figures to facilitate interpretation of local cell-composition patterns.
In short, the goal of this step is to use a single-cell reference to construct cell-type expression priors and map them robustly onto the spatial data, yielding cell-composition estimates for regional comparison, spatial pattern discovery, and downstream biological interpretation.

``cell2location`` generally requires the following two input files:

1. A spatial transcriptomics object in ``.zarr`` format. If you currently have only a spatial ``.h5ad`` object, please first use :doc:`../useful_tool/transform` to complete the format conversion.
2. A single-cell reference object that already contains cell-type annotation information, in ``.h5ad`` format. If you currently have only a Seurat object, please also use :doc:`../useful_tool/transform` to perform the conversion first.


Step 1: Configure ``sample.txt``
--------------------------------

``sample.txt`` must contain at least the spatial object path and the single-cell reference object path.

.. code-block:: text

   sample_id           input_path                                      sc_reference
   concatenated_sdata  results/merge_data/annotation/concatenated_sdata.zarr  data/MTAB/merged_sc_with_annotation.h5ad


Step 2: Parameter Selection and Configuration
------------------------------------------------------------------------------------------

The following table lists the commonly used parameters and their descriptions:

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--anno_algorithm``
     - ``cell2Location``
     - Specifies the current annotation algorithm as cell2location
   * - ``--device``
     - ``cuda`` / ``cpu``
     - Computing device used for model training; directly affects runtime
   * - ``--threads``
     - ``16``
     - Threads allocated to each workflow rule; ``--max_cores`` remains a compatibility alias
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
     - Prior estimate of the number of cells per spatial location
   * - ``labels_key_reference``
     - ``celltype``
     - Column name storing cell-type labels in the reference object
   * - ``batch_key_reference``
     - ``sample``
     - Column name storing batch or sample information in the reference object
   * - ``batch_key_st``
     - ``sample``
     - Column name storing batch or sample information in the spatial object, especially important for multi-sample integrated analyses
   * - ``cell_count_cutoff``
     - ``15``
     - Cell count threshold for filtering genes in the reference data
   * - ``cell_percentage_cutoff2``
     - ``0.05``
     - Cell proportion threshold for filtering genes in the reference data
   * - ``nonz_mean_cutoff``
     - ``1.12``
     - Non-zero mean expression threshold for filtering genes in the reference data
   * - ``detection_alpha``
     - ``20``
     - Prior parameter for the detection rate in the spatial model
   * - ``save_models``
     - ``True``
     - Whether to save the reference model and spatial model directories
   * - ``celltype_col``
     - ``celltype``
     - Existing spatial grouping column used by the regional-abundance dotplot
   * - ``cell2location_microenvironment_threshold``
     - ``0.10``
     - Minimum n_fact=12 cell-type fraction included in the CellPhoneDB microenvironment table

Configuration recommendations:

1. ``labels_key_reference``, ``batch_key_reference``, and ``batch_key_st`` are usually the parameters that should be confirmed first, as they respectively determine how cell-type labels and sample origin information are read by the model.
2. If the reference data comes from a multi-sample integration, it is generally recommended to set both ``batch_key_reference`` and ``batch_key_st`` to ``sample`` so that the model can correctly identify sample origins and improve cross-sample comparison reliability.
3. ``device``, ``max_epochs_reference``, and ``max_epochs_st`` significantly affect training time and can be adjusted according to hardware conditions and data scale.

If you prefer to manage parameters centrally through a configuration file, you can use ``annotation.yaml``.

.. code-block:: yaml

   anno_algorithm: "cell2Location"
   device: "cuda"
   max_epochs_reference: 250
   remove_mt: True
   N_cells_per_location: 30
   max_epochs_st: 30000
   labels_key_reference: "celltype"
   batch_key_reference: "sample"
   batch_key_st: "sample"
   cell_count_cutoff: 15
   cell_percentage_cutoff2: 0.05
   nonz_mean_cutoff: 1.12
   detection_alpha: 20
   save_models: True
   celltype_col: "celltype"
   cell2location_microenvironment_threshold: 0.10

For further YAML parameter details, see :doc:`../config_reference/annotation_yaml`.


Step 3: Run the Command
----------------------------------------------

Once ``sample.txt`` and the parameters are ready, run the cell2location annotation pipeline.

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=cell2Location
   # To use a custom file, append --configfile=annotation.yaml


Demo: cell2location annotation
----------------------------------------------

Using the spatial object generated in :doc:`../integration_analysis/multi_sample_integration` as an example, together with the six accompanying single-cell files from the published study, we demonstrate how to build the reference object and perform cell2location annotation.

1. Download the reference data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create and run a download script in your working directory to download the six single-cell reference files and their annotation table to ``data/sc_data``. If you already have these files available, you can also manually organize them into the corresponding directory.

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

Create ``annotate.py`` and run ``python annotate.py`` to build the single-cell reference object for cell2location.

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


3. Configure ``sample.txt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this demonstration, ``sample.txt`` must provide both the spatial object path and the single-cell reference path.

.. code-block:: text

   sample_id           input_path                                      sc_reference
   concatenated_sdata  results/merge_data/annotation/concatenated_sdata.zarr  data/MTAB/merged_sc_with_annotation.h5ad


4. Run the workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the reference object is built and ``sample.txt`` is configured, run:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=cell2Location


Results and Interpretation
----------------------------------------------------

Result file structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In single-sample mode, the main results are typically output to ``results/{sample}/cell2Location/``:

.. code-block:: text

   results/
   └── {sample}/
       └── cell2Location/
           ├── {sample}.zarr/
           ├── Cell2Loc_inf_aver.csv
           ├── Reference_model/
           ├── Spatial_model/
           ├── CoLocatedComb/
           ├── convert_data.h5ad
           ├── cellphonedb_microenvironments.tsv
           └── figure/
               ├── ELBO_sc_model.png
               ├── ELBO_spatial_model.png
               ├── QC_reference_reconstruction_accuracy.png
               ├── QC_reference_expression signatures_vs_avg_expression.png
               ├── QC_spatial_reconstruction_accuracy.png
               ├── cell2location_relative_abundance_dotplot.pdf
               └── cell2location_relative_abundance_dotplot_source.tsv

In multi-sample ``compare_analysis`` mode, the same outputs are stored under ``results/merge_data/cell2Location/``; the final object is ``concatenated_sdata.zarr`` and the microenvironment table is ``cellphonedb_microenvironments.tsv``.

Here, ``{sample}.zarr`` is the primary object for downstream analysis. It retains the complete input expression matrix and SpatialData elements, together with the four continuous cell-abundance matrices, model metadata, and co-location factor scores. The regional-abundance dotplot is generated only when ``celltype_col`` exists in the spatial table.


1. Primary result tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After cell2location completes, the most commonly used result files typically fall into the following categories:

1. ``Cell2Loc_inf_aver.csv``
   This file stores the cell-type expression signatures learned by the reference model and serves as an important basis for subsequent spatial mapping.

2. ``cellphonedb_microenvironments.tsv``
   This two-column table maps reference cell-type names to n_fact=12 co-location factors whose fraction is at least ``cell2location_microenvironment_threshold``. A cell type may belong to multiple factors, and names are preserved exactly for use as CellPhoneDB ``microenvs_file_path`` input.

3. Other intermediate results and model directories
   ``Reference_model/``, ``Spatial_model/``, ``CoLocatedComb/``, and ``convert_data.h5ad`` are primarily used for model preservation, co-localization result inspection, conversion, and reproducibility tracking.

Overall, ``{sample}.zarr`` stores continuous abundance and factor results written back to the spatial object, while ``Cell2Loc_inf_aver.csv`` describes the reference expression signatures. The module does not create or update a discrete ``cellLoca_type`` annotation; an existing input column with that name is simply preserved.


2. Training convergence curves
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/ELBO_sc_model.png
   :width: 82%
   :align: center
   :alt: ELBO training curve for the cell2location model

The ELBO curve displays model training progress. The x-axis represents training iterations and the y-axis represents the objective-function value. Use this curve to assess whether the reference or spatial model has reached a stable regime.


3. Dot plot linking abundances to unsupervised regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/dotplot.jpg
   :width: 90%
   :align: center
   :alt: Relative cell-type abundance across spatial regions

This dotplot groups spots by the pre-existing unsupervised regions in ``celltype_col`` and summarizes the conservative ``q05_cell_abundance_w_sf`` estimates. Bubble area is the mean q05 abundance of a reference cell type within a region, whereas colour is ``log2(region mean / tissue-wide mean)`` for that cell type. For multiple samples, the two values are calculated per sample and then averaged with equal sample weight. The plot therefore describes relative regional abundance, not a discrete cell-type annotation or a significance test.


4. NMF-based decomposition analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/n_fact12.png
   :width: 76%
   :align: center
   :alt: Cell-type co-location factors identified by cell2location

This result shows the latent composition patterns derived from further decomposition of the abundance matrix, which can assist in identifying representative cell co-localization structures and regional composition features.


5. Spatial visualization of decomposition factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/MNF_spatial.png
   :width: 76%
   :align: center
   :alt: Spatial distribution of cell2location co-location factors

This figure maps the decomposed latent factors back onto spatial coordinates, helping to observe the spatial distribution of different composition patterns and their locally enriched regions.
