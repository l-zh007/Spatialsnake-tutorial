Cell-type composition estimation (RCTD)
=======================================

``RCTD`` uses annotated single-cell reference data to perform cell-type deconvolution on spatial transcriptomics data, offering a practical balance between spatial resolution and cell-type resolution.
In ``full`` mode, RCTD estimates the relative cell-type composition at each spatial location, making it particularly suitable for lower-resolution platforms such as Visium.
In ``doublet`` mode, RCTD reports ``first_type`` and ``second_type`` predictions together with a confidence class. ``second_type`` is interpreted only for ``doublet_certain`` spots.

Because RCTD results are often interpreted together with unsupervised spatial regions, regional summaries report full-mode normalized weights or doublet-mode first-type proportions and their descriptive enrichment relative to the tissue-wide mean.

.. note::
   1. RCTD requires raw count matrices, so both single-cell and spatial inputs should be unnormalized integer count data. If the data have been processed through the Spatialsnake pipeline, the raw expression matrix is typically preserved in the object and can be recovered.
   2. It is recommended that each cell type in the single-cell reference contains at least 25 cells. Extremely rare cell types are automatically removed by the pipeline, so it is advisable to use high-quality, reliably annotated reference data.


``RCTD`` requires the following two inputs:

1. A spatial transcriptomics object stored as a SpatialData ``.zarr`` directory. This is the only spatial input supplied by the user. Because RCTD is not suitable for direct multi-sample integrated analysis, multi-sample spatial data should typically be split by sample and run individually first.
2. A single-cell reference object in ``.h5ad`` or ``.rds`` format. In the example data, the public data are provided as an annotation table and HDF5 files, so they need to be assembled into an annotated ``.rds`` reference object first.


Step 1: ``sample.txt`` configuration file
-----------------------------------------

``sample.txt`` uses exactly one spatial input path per sample. The second column is the SpatialData Zarr directory and the third column is the single-cell reference:

.. code-block:: text

   sample_id   spatial_zarr                                    sc_reference
   sample_id   results/useful_results/data_splitting/sample_id.zarr           data/merged_sc_with_annotation.rds


Step 2: Select parameters
-------------------------

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


Step 3: Run the analysis
------------------------

The basic command uses the packaged defaults. Replace ``visium`` with your
actual platform and prepare the three-column result-object table above:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=RCTD

For the full-mode configuration shown above, save it as ``annotation.yaml``
and use this alternative command:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=RCTD --configfile=annotation.yaml


Demo: ST8059052 full-mode deconvolution
---------------------------------------

.. note::
   ``04_tutorial_essential_resources.zip`` on
   `Zenodo <https://doi.org/10.5281/zenodo.23374838>`__ includes
   ``data/MTAB/merged_sc_with_annotation.rds`` and
   ``results/useful_results/data_splitting/ST8059052.zarr``.
   Extract the archive, run from ``test/``, and proceed directly
   to the sample table to skip input preparation.

Run from your project root. ST8059052 is one of the E-MTAB-11114 samples.
To prepare inputs from scratch, complete :doc:`../integration_analysis/multi_sample_integration` first. Split the annotated object by sample:

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/merge_data/annotation/concatenated_sdata.zarr --split_by=sample

Download :download:`download_reference.sh </config/demo_resources/download_reference.sh>`
and :download:`merge_anno.R </config/demo_resources/merge_anno.R>` into the project root.
The following commands prepare the reference RDS locally:

``Read10X_h5()`` requires ``hdf5r`` for this preparation step. If missing, run
``Rscript -e 'install.packages("hdf5r", repos="https://cloud.r-project.org")'``.
Skip reference preparation if a compatible annotated reference RDS is already available.

.. code-block:: bash

   bash download_reference.sh
   cd data/MTAB
   Rscript ../../merge_anno.R
   cd ../..

Save this as ``sample.txt`` (or download
:download:`rctd_sample.txt </config/demo_resources/rctd_sample.txt>`):

.. code-block:: text

   sample_id spatial_zarr sc_reference
   ST8059052 results/useful_results/data_splitting/ST8059052.zarr data/MTAB/merged_sc_with_annotation.rds

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=RCTD --RCTD_mode=full

The demo writes ``results/ST8059052/RCTD/`` in ``full`` mode. Doublet mode is
an alternative (``--RCTD_mode=doublet``), not an additional demo step. Both
modes use the same output directory; preserve an existing run before switching.


Results and interpretation
--------------------------

Result file structure
~~~~~~~~~~~~~~~~~~~~~

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


Primary result tables
~~~~~~~~~~~~~~~~~~~~~

The main outputs are fitted weights, confidence classes, and a SpatialData
object that retains the input observations and spatial elements.

1. ``{sample}_RCTD_results.csv``
   In ``doublet`` mode, this file contains ``spot_class``, ``first_type``, ``second_type``, and the remaining official RCTD result fields. In ``full`` mode, spacexr does not produce ``results_df``; the file therefore retains the fitted spot identifiers only.

2. ``{sample}_RCTD_weights.csv``
   This file stores row-normalized cell-type weights for each fitted spatial location. The values are relative mixture proportions, not absolute cell counts. Spots filtered by RCTD remain missing rather than being forced into a cell type when the matrix is written back to Zarr.

3. ``{sample}.zarr``
   This result is based on the original SpatialData object, so its complete expression matrix, images, shapes, coordinate systems, and pre-existing metadata are retained. In both modes, ``obsm["RCTD_weights"]`` stores the continuous row-normalized proportions, and ``uns["RCTD"]`` records ``mode``, ``weight_key``, ``weight_scale``, ``cell_types``, ``n_input_spots``, and ``n_fitted_spots``. The weight scale is explicitly recorded as ``row_normalized_proportion``.

   In ``full`` mode, no dominant cell type or other discrete annotation is created. In ``doublet`` mode, all fields from the official ``results_df`` are aligned to spot identifiers and written to ``obs``, including ``spot_class``, ``first_type``, and ``second_type``; the plotting-friendly ``RCTD_first_type`` and ``RCTD_second_type`` fields are retained as well.

Demo result: regional cell-type composition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/ST8059052_RCTD_full_dotplot.png
   :width: 90%
   :align: center
   :alt: RCTD full-mode relative cell-type composition across ST8059052 regions

This is a preview of the original ``ST8059052_RCTD_full_dotplot.pdf`` from the
completed full-mode run (2,576 spots, 58 reference types). The plot displays the
top 30 reference types by tissue-wide mean weight. Dot area represents the
regional mean normalized weight; color represents log2 enrichment relative to
the tissue mean. Weights describe relative mixture composition, not absolute
cell counts. Full mode does not produce the doublet-mode spot-class plot.

Inspect ``*_RCTD_weights.csv`` and ``*_RCTD_full_dotplot_source.tsv`` for the
underlying values. Region labels are the coarse E-MTAB-11114 annotations from
the integration demo, not new discrete labels inferred by RCTD.
