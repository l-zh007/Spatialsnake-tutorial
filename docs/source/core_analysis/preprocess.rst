Preprocessing
=============

After ``ingestion`` is complete, ``preprocess`` performs quality control, filtering, normalization, and preparation for dimensionality reduction.

Preprocessing filters observations and genes using QC thresholds, then applies total-count normalization and log transformation. Observations may be spots, bins or segmented cells, depending on the platform.
At this stage, you can also select highly variable genes to reduce noise, and in multi-sample settings you can optionally adjust batch effects before clustering.


Workflow overview
-----------------
1. Compute QC metrics and filter genes and observations according to the selected thresholds.
2. Apply total-count normalization and log transformation.
3. Perform highly variable gene selection if enabled.
4. Run PCA on the log-normalized matrix and optionally apply batch correction in multi-sample analyses.
5. Export the filtered object and save QC figures generated during preprocessing.

Highly variable gene selection is optional and disabled by default (``variable=False``).


Step 1: Configure ``sample.txt``
--------------------------------

Reuse the platform-input sample table from ``ingestion``; do not replace its paths
with a downstream Zarr. The example below is for one Visium HD sample. Other
platforms and multi-sample channels use the :ref:`core table headers <sample-tables>`.

.. code-block:: text
  
   sample_id input_path bin_size
   S1 data/S1 8

Step 2: Select parameters
-------------------------

Adjust the following parameters to the platform, resolution, and study design.

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--min_cells`` / ``--min_counts``
     - ``50`` / ``50``
     - Minimum number of observations in which a gene must be detected, and minimum total counts required for each observation
   * - ``--mt_threshold``
     - ``40``
     - Mitochondrial proportion threshold for filtering
   * - ``--batch_method``
     - ``harmony``
     - Batch correction method for integrated multi-sample analysis: ``harmony``, ``bbknn``, or ``None``
   * - ``--n_top_genes``
     - ``3000``
     - Number of highly variable genes
   * - ``--n_comps``
     - ``50``
     - Number of PCA components
   * - ``--variable``
     - ``True``
     - Whether to run highly variable gene selection
   * - ``--NEIGHBORS``
     - ``10``
     - Shared workflow setting; the standard neighbor graph is constructed in ``clustering``
   * - ``--sketch`` / ``--sample_rate``
     - ``True`` / ``0.30``
     - Sampling settings for very large datasets


Configuration recommendations:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. For all scenarios: We recommend adjusting ``min_cells``, ``min_counts``, and ``mt_threshold`` based on the QC plots generated during ``ingestion``. ``min_cells`` filters genes by the number of observations in which they are detected, whereas ``min_counts`` filters observations by total counts. Choose thresholds that are appropriate for the platform and resolution; if you do not set them explicitly, the configured defaults are used.

2. For multi-sample integrated data: In addition to tuning the above parameters, select an appropriate ``batch_method``. Harmony produces ``X_pca_harmony`` for downstream graph construction, whereas BBKNN produces a batch-balanced neighbor graph that is retained by ``clustering``. The batch column is selected from ``sample`` first and ``region`` second. Batch correction is skipped automatically when only one batch is present.

3. For datasets with hundreds of thousands or even millions of cells/spots: To improve clustering efficiency, set ``--sketch`` to ``True`` and choose a suitable ``--sample_rate``. Spatialsnake uses GeoSketch within the available sample or region strata. The preprocessed Zarr contains the sketch used as the clustering reference, while ``sketch.h5ad`` retains the full preprocessed table for subsequent label and UMAP projection. Continue with the same sketch setting in ``clustering``; the final clustered Zarr is restored to the full set of spots or cells.

The requested ``n_comps`` value is used for PCA. If the filtered matrix cannot support that many components, Spatialsnake uses the largest valid value and records the adjustment in the log and output metadata.

4. In multi-sample analysis, different samples may require different thresholds such as ``min_cells``, ``min_counts``, or ``mt_threshold``.
You can add these sample-specific settings directly to ``sample.txt``, and the workflow will read them automatically and apply the corresponding filtering strategy.
Sample-table thresholds override global defaults; use filter_list only for additional YAML overrides.

``sample.txt`` can be modified as follows:

.. code-block:: text

   sample_id input_path group bin_size min_cells min_counts mt_threshold
   Colon_Cancer_P2 data/Colon_Cancer_P2 Tumor 8 50 50 30
   Colon_Normal_P5 data/Colon_Normal_P5 Normal 8 50 50 30


Run with your own data
----------------------

After ingestion, set thresholds from the QC distributions. This example shows
how to override a threshold for your own sample; the CRC P2 demo below uses a
different, explicitly recorded parameter set.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --min_counts=100 --mt_threshold=30

Keep your actual TYPE and use ``compare_analysis`` for the integrated core
workflow. For several settings, use the optional :ref:`YAML configuration
<cli-configuration>` with the :doc:`../config_reference/preprocess_yaml` reference.


Demo: CRC P2 preprocessing
--------------------------

We use the ``Colon_Cancer_P2_008um`` data ingested in the previous step for this preprocessing demonstration.
The same ``sample.txt`` can be reused from the earlier analysis steps to maintain a consistent core analysis on the same sample.

.. code-block:: text
  
   sample_id input_path bin_size
   Colon_Cancer_P2 data/Colon_Cancer_P2 8

Run the command
~~~~~~~~~~~~~~~

Based on the explanations above and the QC plots from the ``ingestion`` step, for this single-sample dataset we choose ``--min_cells 50 --min_counts 50 --mt_threshold 30`` as the preprocessing parameters.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --min_cells=50 --min_counts=50 --mt_threshold=30

Alternative YAML configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download :download:`crc_preprocess.yaml </config/demo_resources/crc_preprocess.yaml>`
as ``preprocess.yaml`` for the same demo settings (min_cells 50, min_counts 50, mt_threshold 30, sketch false).
Run the following **instead of** the preceding CLI command. Do not generate a
new template over the downloaded file.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --configfile=preprocess.yaml


Result file structure
---------------------

This example shows single-sample preprocessing for ``visium_HD``. After the run completes, first confirm that ``filter_{sample}.zarr`` has been generated, then review the QC figures to determine whether the chosen thresholds are appropriate.

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── preprocess/
           ├── filter_Colon_Cancer_P2.zarr # filtered zarr object
           ├── Colon_Cancer_P2filtered_Total_UMI.png # filtered UMI distribution
           ├── Colon_Cancer_P2filtered_Total_Genes.png # filtered gene-count distribution
           ├── Colon_Cancer_P2_Mitochondrial_Genes.png # mitochondrial signal distribution
           ├── Colon_Cancer_P2_scatter.png # scatter plot of filtered UMI versus gene counts
           ├── Colon_Cancer_P2pca_variance_ratio.png # PCA variance ratio plot
           └── Colon_Cancer_P2_highly_variable.png # highly variable gene selection plot

The file ``filter_{sample}.zarr`` is the core input for downstream clustering. The remaining figures are used to evaluate UMI distribution, gene complexity, mitochondrial proportion, outliers, and PCA variance explained. The highly variable gene figure is generated only when feature selection is enabled. When sketch-based analysis is enabled, the same directory also contains ``sketch.h5ad``, which stores the full preprocessed table for downstream projection.

Key outputs
~~~~~~~~~~~

1. ``{sample}filtered_Total_UMI.png`` (total UMI distribution)

   - When one global ``min_counts`` value is used, the dashed line marks ``log1p(min_counts)``, the actual filtering boundary applied to every observation.
   - When sample-specific thresholds are supplied, no single cutoff line is drawn because filtering boundaries may differ between samples.

.. figure:: /_static/images/Colon_Cancer_P2filtered_Total_UMI.png
   :width: 85%
   :align: center
   :alt: Total UMI distribution after preprocessing

   Count distribution of retained CRC P2 bins after applying the configured filters.

2. ``{sample}filtered_Total_Genes.png`` (detected gene distribution)

.. figure:: /_static/images/Colon_Cancer_P2filtered_Total_Genes.png
   :width: 85%
   :align: center
   :alt: Detected gene distribution after preprocessing

   Distribution of detected genes after filtering.

3. ``{sample}pca_variance_ratio.png`` and the recommended number of PCs printed in the terminal

   - This plot helps determine how many dimensions should be retained for downstream analysis.
   - The point where the curve clearly flattens often provides a useful reference.
   - In practice, compare a few nearby values around the recommended point and choose the most stable setting.

.. figure:: /_static/images/Colon_Cancer_P2pca_variance_ratio.png
   :width: 85%
   :align: center
   :alt: PCA variance ratio after preprocessing

   PCA explained-variance plot. Use it with the logged PC recommendation to choose ``pcs`` for clustering.

The logged recommendation is a heuristic based on component standard deviations,
not a threshold retaining 90% of explained variance. It selects the smaller of
two cutoffs: the first component whose cumulative contribution exceeds 90%
and individual contribution is below 5%, or the component after the last
adjacent decrease above 0.1 percentage points. The recommendation does not
automatically set the clustering parameter ``pcs``.


4. ``{sample}_Mitochondrial_Genes.png`` (mitochondrial signal distribution)

   - This plot shows whether mitochondrial-related signal remains elevated after filtering.
   - If some regions are still globally high, consider tightening the filtering strategy while preserving sufficient data.
   - Adjust thresholds gradually to avoid removing genuine biological signal.

5. ``{sample}_scatter.png`` (summary scatter plot)

   - This plot helps identify potential low-quality clusters of observations.
   - Pay particular attention to regions with low gene counts and high mitochondrial proportion.
   - Interpret it together with the previous plots for a more reliable conclusion.

6. ``{sample}_highly_variable.png`` (highly variable gene plot, optional)

   - Generated only when ``variable=True``; the default demo does not select HVGs.
   - If feature selection is enabled, check that relevant lineage markers remain
     represented before interpreting changes in clustering.


Before continuing, compare the retained data with the ingestion QC and check
whether filtering has removed entire anatomical regions or disproportionately
affected one sample. Revisit thresholds if this cannot be explained by data
quality. A filtered distribution alone does not establish that all retained
observations are high quality.

Continue to :doc:`clustering`.
