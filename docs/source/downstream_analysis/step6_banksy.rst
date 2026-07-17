Module 5: Spatially Enhanced Clustering (BANKSY)
================================================

``banksy`` performs spatially enhanced clustering for niche and tissue-domain
discovery using the pyBANKSY implementation. BANKSY augments the expression
profile of each spot or cell with features derived from its local spatial
neighborhood, and then applies standard dimensionality reduction and graph-based
clustering. In Spatialsnake, the final BANKSY labels are written to
``obs["spatial_cluster"]``.

For the complete parameter configuration reference, see
:doc:`../config_reference/advance_analysis_yaml`.


1. Analysis content and workflow
--------------------------------

The module follows the official BANKSY analysis logic:

1. Read a processed ``.zarr`` or ``.h5ad`` object.
2. Verify spatial coordinates.
3. Select a lightweight feature set for the BANKSY matrix.
4. Build the BANKSY spatial neighborhood graph using ``k_geom``.
5. Generate the neighborhood-augmented BANKSY matrix using ``lambda_list``.
6. Run PCA and Leiden clustering.
7. Save the selected labels to ``obs["spatial_cluster"]``.
8. Export result tables and spatial visualization.

The input expression matrix is expected to be already processed. In particular,
``adata.X`` should contain log-normalized expression values. This module does
not perform additional normalization or log transformation.

BANKSY clusters should be interpreted as spatially informed domains or niches,
rather than as pure cell types. A single BANKSY domain may contain multiple
cell types if they share a coherent local microenvironment.


2. Input preparation
--------------------

The recommended ``sample.txt`` format is:

.. code-block:: text

   sample_id   input_path
   {sample_id} results/{sample_id}/annotation/{sample_id}.zarr

For Visium HD, Xenium, Stereo-seq, or other high-resolution spatial data, the
input object should contain:

1. A processed expression matrix in ``adata.X``.
2. Spatial coordinates in ``adata.obsm["spatial"]`` or in
   ``obs["array_row"]`` and ``obs["array_col"]``.
3. Optional ``obs["celltype"]`` annotations if cell-type composition across
   BANKSY domains should be summarized.


3. Essential parameters
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - Parameter
     - Default
     - Description
   * - ``k_geom``
     - ``15``
     - Number of spatial neighbors used to construct the BANKSY graph.
   * - ``max_m``
     - ``1``
     - Maximum harmonic order. ``1`` captures first-order spatial structure and is the recommended default.
   * - ``nbr_weight_decay``
     - ``scaled_gaussian``
     - Spatial neighbor weighting scheme used by pyBANKSY.
   * - ``lambda_list``
     - ``[0.8]``
     - Spatial neighborhood contribution. Larger values emphasize tissue-domain or niche structure.
   * - ``banksy_max_features``
     - ``2000``
     - Maximum number of genes used to construct the BANKSY matrix. Set ``0`` to use all genes.
   * - ``banksy_feature_col``
     - ``highly_variable``
     - Optional ``adata.var`` column used before variance-based feature selection.
   * - ``banksy_n_comps``
     - ``20``
     - Number of principal components used after BANKSY matrix generation.
   * - ``banksy_resolution``
     - ``[0.5]``
     - Leiden resolution values tested by BANKSY.
   * - ``banksy_num_nn``
     - ``50``
     - Number of expression-neighbors used for the Leiden graph.
   * - ``banksy_plot_full``
     - ``false``
     - Generate full pyBANKSY figures. Disabled by default for large datasets.
   * - ``banksy_run_nonspatial``
     - ``false``
     - Run non-spatial baseline clustering. Use only when benchmarking spatial contribution.
   * - ``banksy_sample_col``
     - ``region``
     - Sample or slice column used to avoid cross-sample spatial neighbors in merged inputs.


4. Recommended settings
-----------------------

For a first-pass spatial niche analysis on Visium HD-scale data, use:

.. code-block:: yaml

   runpipe: "banksy"
   k_geom: 15
   max_m: 1
   nbr_weight_decay: "scaled_gaussian"
   lambda_list: [0.8]
   banksy_max_features: 2000
   banksy_n_comps: 20
   banksy_resolution: [0.5]
   banksy_num_nn: 50
   banksy_add_umap: false
   banksy_plot_full: false
   banksy_run_nonspatial: false

This configuration keeps all spots or cells in the analysis while restricting
the number of genes used to construct the dense BANKSY matrix. This is the main
lightweight strategy for large spatial transcriptomics datasets.

The following feature settings are commonly useful:

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Setting
     - Recommended use
   * - ``banksy_max_features: 1000``
     - Fast preview on very large data.
   * - ``banksy_max_features: 2000``
     - Default balance between biological detail and computational cost.
   * - ``banksy_max_features: 3000``
     - More complete analysis on high-memory servers.
   * - ``banksy_max_features: 0``
     - Use all genes. Recommended only for small datasets or very high-memory servers.

When multiple ``lambda`` or resolution values are provided, all combinations
are recorded in ``banksy_results.csv``. By default, the first BANKSY result is
written to ``obs["spatial_cluster"]``. To select a specific result, set:

.. code-block:: yaml

   banksy_selected_lambda: "0.8"
   banksy_selected_resolution: "0.5"


5. Important notes
------------------

1. ``adata.X`` is assumed to be log-normalized.
   The module does not normalize or transform the expression matrix.

2. BANKSY uses a dense internal matrix.
   Runtime and memory increase with the number of spots/cells and selected
   genes. For ``max_m=1``, the internal BANKSY matrix is approximately three
   times wider than the selected expression matrix.

3. ``banksy_max_features`` controls computational cost.
   Using all genes may be biologically unnecessary for domain discovery and can
   be prohibitively expensive for Visium HD-scale data.

4. ``lambda_list`` controls spatial emphasis.
   Lower values place more weight on expression similarity, whereas higher
   values emphasize local spatial microenvironment. For tissue-domain or niche
   discovery, ``lambda_list: [0.8]`` is a practical default.

5. Existing ``spatial_cluster`` labels are overwritten.
   If the input object already contains ``obs["spatial_cluster"]``, BANKSY will
   replace it with the new BANKSY labels.

6. Multi-sample inputs are handled sample-wise when possible.
   If ``banksy_sample_col`` exists and contains multiple samples or regions, the
   module runs BANKSY separately for each sample to avoid artificial cross-sample
   spatial neighbors.

7. Full diagnostic figures are optional.
   ``banksy_plot_full`` and ``banksy_run_nonspatial`` are useful for method
   benchmarking but are disabled by default to keep the workflow lightweight.


6. Run command
--------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=advance_analysis --runpipe=banksy --threads 8

If needed, parameters can be overridden from the command line:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD \
     --option=advance_analysis \
     --runpipe=banksy \
     --banksy_max_features 1000 \
     --threads 8


7. Output files
---------------

.. code-block:: text

   results/
   └── {sample}/
       └── banksy/
           ├── {sample}_banksy.zarr/
           └── banksy_results/
               ├── banksy_results.csv
               ├── banksy_cluster_assignments.csv
               ├── banksy_parameters.csv
               ├── banksy_spatial_cluster.png
               └── celltype_spatial_cluster_enrichment.png  # optional

``banksy_results.csv``
   Summary of all tested BANKSY parameter combinations.

``banksy_cluster_assignments.csv``
   Spot or cell identifiers and the selected ``spatial_cluster`` label.

``banksy_parameters.csv``
   Parameters used for the run, including the selected feature count.

``banksy_spatial_cluster.png``
   Lightweight spatial visualization of the selected BANKSY domains.

``celltype_spatial_cluster_enrichment.png``
   Optional cell-type composition or enrichment summary when ``obs["celltype"]``
   is available.


8. Visium HD demo
-----------------

This example uses an annotated Visium HD object:

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

Run from the project directory:

.. code-block:: bash
   
   spatialsnake single_analysis sample.txt visium_HD \
   --option=advance_analysis \
   --runpipe=banksy \
   --threads 8

For this Visium HD object, the matrix contains hundreds of thousands of spots.
The default ``banksy_max_features: 2000`` therefore provides a practical
first-pass analysis. If only a quick preview is needed, set
``banksy_max_features: 1000``. If a more complete analysis is required and the
server has sufficient memory, increase the value to ``3000`` or higher.

The main result is the lightweight spatial domain plot:

.. code-block:: text

   results/Colon_Cancer_P2_008um/banksy/banksy_results/banksy_spatial_cluster.png

The selected labels are also stored in:

.. code-block:: text

   results/Colon_Cancer_P2_008um/banksy/Colon_Cancer_P2_008um_banksy.zarr

A successful lightweight run produces a compact summary table similar to:

.. code-block:: text

   sample,result_key,decay,lambda_param,num_pcs,resolution,num_labels,selected
   all,scaled_gaussian_pc20_nc0.80_r0.50,scaled_gaussian,0.8,20,0.5,11,True

In this demo, BANKSY selected 2000 genes by variance, used
``lambda=0.8`` and ``resolution=0.5``, and identified 11 spatially informed
clusters. The output zarr can be reloaded, and ``obs["spatial_cluster"]``
contains one categorical label for every spot.


.. figure:: /_static/images/banksy_spatial_cluster.png
   :width: 85%
   :align: center
   :alt: BANKSY spatial clustering results

.. figure:: /_static/images/celltype_spatial_cluster_enrichment.png
   :width: 85%
   :align: center
   :alt: Cell-type enrichment across BANKSY spatial domains

If full pyBANKSY plotting is enabled, the spatial clustering can be visualized
as a multi-panel BANKSY figure:

.. figure:: /_static/images/BANKSY_scaled_gaussian_pc50_nc0.80_r0.50_full_figure.png
   :width: 85%
   :align: center
   :alt: BANKSY spatial clustering results

   Example BANKSY spatial clustering output. Colors represent spatially
   informed domains inferred from expression and local neighborhood structure.

When ``banksy_run_nonspatial`` is enabled, a non-spatial baseline can also be
generated for comparison:

.. figure:: /_static/images/BANKSY-Nonspatial_nonspatial_pc50_nc0.00_r0.50_full_figure.png
   :width: 85%
   :align: center
   :alt: BANKSY non-spatial baseline

   Example non-spatial baseline result. This comparison is useful for method
   benchmarking but is not required for routine large-scale niche analysis.
