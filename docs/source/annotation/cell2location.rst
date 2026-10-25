Cell-type composition estimation (cell2location)
================================================

``cell2location`` maps cell-type information from a single-cell reference onto spatial transcriptomic locations, thereby estimating cell-type abundance at each spatial position and generating corresponding spatial visualizations and summary tables.

For lower-resolution spatial data such as Visium, this method is particularly well suited because it does not force a single label onto each spot, but instead estimates the continuous abundance of different cell types within each spot.
The same workflow can map an integrated object when sample identity is retained.
Outputs are continuous cell-type abundances, not a single cell-type label for
every location. Regional summaries help interpret these estimates alongside
existing spatial annotations.

``cell2location`` generally requires the following two input files:

1. A spatial transcriptomics object in ``.zarr`` format. If you currently have only a spatial ``.h5ad`` object, please first use :doc:`../useful_tool/transform` to complete the format conversion.
2. A single-cell reference H5AD with raw, non-negative integer counts and
   cell-type labels. Use matching species, tissue, and gene identifiers for
   spatial and reference data. The ``transform`` utility does not import Seurat
   RDS; prepare H5AD from the original matrix and annotation table instead.


Prepare your reference
----------------------

Match annotation rows by barcode, not row order. For a single 10x reference
with a CSV containing ``barcode`` and ``celltype``, an example is:

.. code-block:: python

   import scanpy as sc
   import pandas as pd

   reference = sc.read_10x_h5("data/reference_counts.h5")
   reference.var_names_make_unique()
   labels = pd.read_csv("data/reference_annotation.csv", index_col="barcode")
   reference.obs["celltype"] = labels.loc[reference.obs_names, "celltype"]
   reference.obs["sample"] = "reference_1"
   reference.write_h5ad("data/reference.h5ad")

Keep counts unnormalized. For several references, retain their real sample IDs
and unique barcodes. If your columns differ, set ``labels_key_reference`` and
``batch_key_reference`` accordingly. The E-MTAB-11114 mouse-brain demo below supplies a script
for its own multi-file reference; do not substitute this generic example for it.

Step 1: Configure ``sample.txt``
--------------------------------

``sample.txt`` must contain at least the spatial object path and the single-cell reference object path.

.. code-block:: text

   sample_id           input_path                                      sc_reference
   concatenated_sdata  results/merge_data/annotation/concatenated_sdata.zarr  data/MTAB/merged_sc_with_annotation.h5ad


Step 2: Select parameters
-------------------------

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
     - ``auto`` / ``cuda`` / ``cpu``
     - Auto uses available CUDA or falls back to CPU; explicit cuda requires usable CUDA
   * - ``--threads``
     - ``16``
     - Threads allocated to each workflow rule; ``--max_cores`` remains a compatibility alias
   * - ``max_epochs_reference``
     - ``250``
     - Number of training epochs for the reference regression model
   * - ``max_epochs_st``
     - ``20000``
     - Default spatial epochs; increase only when convergence diagnostics require it
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
2. For multi-sample inputs, set ``batch_key_reference`` and ``batch_key_st``
   to the actual sample columns in the reference and spatial objects. The column
   names need not be identical; do not use study condition as a substitute for
   sample identity.
3. ``device``, ``max_epochs_reference``, and ``max_epochs_st`` significantly affect training time and can be adjusted according to hardware conditions and data scale.

For optional customization, save the following as ``annotation.yaml`` and
append ``--configfile=annotation.yaml`` to the command. Template generation and
CLI precedence are explained in :ref:`cli-configuration`.

.. code-block:: yaml

   anno_algorithm: "cell2Location"
   device: "auto"
   max_epochs_reference: 250
   remove_mt: True
   N_cells_per_location: 30
   max_epochs_st: 20000
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


Step 3: Run the analysis
------------------------

Once ``sample.txt`` and the parameters are ready, run the cell2location annotation pipeline.

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=cell2Location
   # To use a custom file, append --configfile=annotation.yaml


Demo: E-MTAB-11114 mouse-brain cell2location
--------------------------------------------

.. note::
   The prepared reference ``data/MTAB/merged_sc_with_annotation.h5ad`` is included
   in ``04_tutorial_essential_resources.zip`` on
   `Zenodo <https://doi.org/10.5281/zenodo.23374838>`__.
   Extract the archive and run from ``test/`` to skip the
   reference preparation below.

Run from your project root, using the E-MTAB-11114 mouse-brain annotation object from
:doc:`../integration_analysis/multi_sample_integration`.
Download :download:`download_reference.sh </config/demo_resources/download_reference.sh>`
and :download:`annotate.py </config/demo_resources/annotate.py>` into the project root.
These scripts provide an alternative way to prepare the reference from E-MTAB-11115.

.. code-block:: bash

   bash download_reference.sh
   cd data/MTAB
   python ../../annotate.py
   cd ../..

Save this as ``sample.txt`` (or download
:download:`cell2location_sample.txt </config/demo_resources/cell2location_sample.txt>`
and rename it):

.. code-block:: text

   sample_id input_path sc_reference
   concatenated_sdata results/merge_data/annotation/concatenated_sdata.zarr data/MTAB/merged_sc_with_annotation.h5ad

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=cell2Location --device=auto

Outputs are stored in ``results/merge_data/cell2Location/``.
The default reference/spatial training settings are used. This is a model-based
analysis, not an instantaneous import check.


Results and interpretation
--------------------------

Result file structure
~~~~~~~~~~~~~~~~~~~~~

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


Primary result tables
~~~~~~~~~~~~~~~~~~~~~

After cell2location completes, the most commonly used result files typically fall into the following categories:

1. ``Cell2Loc_inf_aver.csv``
   This file stores the cell-type expression signatures learned by the reference model and serves as an important basis for subsequent spatial mapping.

2. ``cellphonedb_microenvironments.tsv``
   This two-column table maps reference cell-type names to n_fact=12 co-location factors whose fraction is at least ``cell2location_microenvironment_threshold``. A cell type may belong to multiple factors, and names are preserved exactly for use as CellPhoneDB ``microenvs_file_path`` input.

3. Other intermediate results and model directories
   ``Reference_model/``, ``Spatial_model/``, ``CoLocatedComb/``, and ``convert_data.h5ad`` are primarily used for model preservation, co-localization result inspection, conversion, and reproducibility tracking.

Overall, ``{sample}.zarr`` stores continuous abundance and factor results written back to the spatial object, while ``Cell2Loc_inf_aver.csv`` describes the reference expression signatures. The module does not create or update a discrete ``cellLoca_type`` annotation; an existing input column with that name is simply preserved.


Regional cell-type abundance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/dotplot.jpg
   :width: 90%
   :align: center
   :alt: Relative cell-type abundance across spatial regions

This dotplot groups spots by the pre-existing unsupervised regions in ``celltype_col`` and summarizes the conservative ``q05_cell_abundance_w_sf`` estimates. Bubble area is the mean q05 abundance of a reference cell type within a region, whereas colour is ``log2(region mean / tissue-wide mean)`` for that cell type. For multiple samples, the two values are calculated per sample and then averaged with equal sample weight. The plot therefore describes relative regional abundance, not a discrete cell-type annotation or a significance test.


In this E-MTAB-11114 demo, excitatory-neuron reference types show distinct
regional abundance patterns. Check reference compatibility and model QC before
interpreting these estimates. Neither regional enrichment nor co-location
establishes cell-cell signaling.
