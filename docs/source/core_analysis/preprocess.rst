Preprocessing
==============================

After ``Ingesting`` is complete, ``preprocess`` performs quality control, filtering, normalization, and preparation for dimensionality reduction.

Because spatial transcriptomics data are affected by technical noise and dropout, preprocessing is usually required to remove low-quality genes and spots or cells, followed by normalization steps such as library-size normalization and log transformation.
At this stage, you can also select highly variable genes to reduce noise, and in multi-sample settings you can correct batch effects to improve the reliability of downstream analysis.


Workflow overview
-----------------
1. Compute QC metrics and filter genes and spots or cells according to the selected thresholds.
2. Apply total-count normalization and log transformation.
3. Perform highly variable gene selection if enabled.
4. Run scaling and PCA, and optionally apply batch correction in multi-sample analyses.
5. Export the filtered object and save QC figures generated during preprocessing.

In short, this step prepares the spot-by-gene expression matrix for downstream analysis by improving data quality, standardizing values, and reducing technical noise.

.. note::

   If your data are not from the Visium HD platform, or if you are analyzing integrated multi-sample data, read the notes at the end of this page to understand the differences in input and output across platforms and analysis modes.
   You can reproduce the same workflow with your own dataset by replacing the sample names in ``sample.txt``, provided that your data have already been ingested according to the platform-specific requirements.

Optional parameters from the command line
-----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--min_cells`` / ``--min_genes``
     - ``3`` / ``200``
     - Control gene and spot/cell filtering thresholds
   * - ``--mt_threshold``
     - ``40``
     - Mitochondrial proportion threshold for filtering
   * - ``--batch_method``
     - ``harmony``
     - Batch correction method for integrated multi-sample analysis
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
     - Neighbor graph parameter
   * - ``--sketch`` / ``--sample_rate``
     - ``True`` / ``0.30``
     - Sampling settings for very large datasets

The parameters listed above are commonly used settings that can be passed directly on the command line. If you are comfortable tuning spatial transcriptomics workflows, you can append them to the command as needed, for example ``--min_cells 5``.

For the example dataset, we use ``--min_cells 100 --min_genes 100 --mt_threshold 30``. This filters out spots or cells with fewer than 100 UMIs, fewer than 100 detected genes, or more than 30% mitochondrial signal.

Run the command
------------------------------
.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --min_cells=100 --min_genes=100 --mt_threshold=30





Optional parameters through a configuration file
------------------------------------------------

If you are already familiar with Spatialsnake and want to manage more settings in a structured way, use a YAML configuration file.

See :doc:`../config_reference/preprocess_yaml` for the full parameter reference.

Generate a YAML template with:

.. code-block:: bash

   spatialsnake produce-file --option=preprocess

The YAML file contains inline comments describing each parameter. You can adjust the settings according to your analysis needs, or consult the documentation for the YAML explanation directly.

After editing the configuration file, provide it on the command line with ``--configfile``.

Run with a YAML file
--------------------

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

The file ``filter_{sample}.zarr`` is the core input for downstream clustering and annotation. The remaining figures are used to evaluate UMI distribution, gene complexity, mitochondrial proportion, outliers, and PCA variance explained. If highly variable gene selection or sketch-based sampling is disabled, the corresponding files will not be generated.


Cross-platform notes
--------------------

Differences in command usage
----------------------------

If your dataset is not from ``visium_HD``, replace ``visium_HD`` with the appropriate platform type:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess --min_cells 100 --min_genes 100 --mt_threshold 30

If you are analyzing integrated samples, switch to ``compare_analysis`` and make sure ``sample.txt`` follows the format described earlier:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium_HD --option=preprocess

You can add command-line parameters at the end of the command or manage them through a YAML file in exactly the same way as in the example above.

Differences in parameters
----------------------------

In multi-sample integration, different samples may require different thresholds such as ``min_cells``, ``min_genes``, or ``mt_threshold``.
You can add these sample-specific settings directly to ``sample.txt``, and the workflow will read them automatically and apply the corresponding filtering strategy.

.. code-block:: text

   sample    input_path                 group  min_cells min_genes mt_threshold
   Colon_Cancer_P2   data/Colon_Cancer_P2   Tumor  50  50  30
   Colon_Normal_P5  data/Colon_Normal_P5 Normal  50  50  30

Other parameters

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - Parameter category
     - Recommendation for single-sample analysis
     - Recommendation for multi-sample or cross-condition analysis
   * - Harmony batch correction
     - Usually keep the default setting or leave it disabled
     - If technical differences between samples are obvious, enable ``harmony`` or ``BBkNN`` to reduce their impact on clustering
   * - Sampling strategy (``sketch/sample_rate``)
     - Usually unnecessary for modestly sized datasets
     - For very large integrated objects, start with a small sampling rate to iterate quickly, then return to the full dataset for confirmation


Input and output structure
--------------------------

After ``Ingesting`` is complete, you can usually reuse the same ``sample.txt`` file for ``preprocess``.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Analysis mode
     - Input
     - Output
   * - single_analysis (standard ``zarr`` mode)
     - ``sample.txt`` should contain at least ``sample_id input_path``; the input object is ``results/{sample}/integrate/{sample}.zarr``
     - ``results/{sample}/preprocess/filter_{sample}.zarr``
   * - single_analysis (``visium_HD``)
     - ``sample.txt`` should contain at least ``sample_id input_path bin``; the input object is ``results/{sample}_{bin}um/integrate/{sample}.zarr``
     - ``results/{sample}_{bin}um/preprocess/filter_{sample}.zarr``
   * - compare_analysis
     - ``sample.txt`` should contain at least ``sample_id input_path group``; for ``visium_HD``, an additional ``bin`` column is required. The input object is ``results/merge_data/integrate/concatenated_sdata``
     - ``results/merge_data/preprocess/filter_concatenated_sdata``


How to inspect the preprocessing results
----------------------------------------

Key outputs
~~~~~~~~~~~

1. ``{sample}filtered_Total_UMI.png`` (total UMI distribution)

.. figure:: /_static/images/Colon_Cancer_P2filtered_Total_UMI.png
   :width: 85%
   :align: center
   :alt: preprocess umi plot

   Filtered UMI distribution. Low-quality cells have been removed.

2. ``{sample}filtered_Total_Genes.png`` (detected gene distribution)

.. figure:: /_static/images/Colon_Cancer_P2filtered_Total_Genes.png
   :width: 85%
   :align: center
   :alt: preprocess genes plot

   Distribution of detected genes after filtering.

   - This plot shows whether the post-filtering gene complexity remains reasonable across the dataset.
   - If the overall level is still low, the effective information content may be insufficient and downstream clustering may become unstable.
   - If some regions remain unusually high, check the spatial location to determine whether they represent local artifacts or biologically distinct tissue areas.

3. ``{sample}pca_variance_ratio.png`` and the recommended number of PCs printed in the terminal

   - This plot helps determine how many dimensions should be retained for downstream analysis.
   - The point where the curve clearly flattens often provides a useful reference.
   - In practice, compare a few nearby values around the recommended point and choose the most stable setting.

.. figure:: /_static/images/Colon_Cancer_P2pca_variance_ratio.png
   :width: 85%
   :align: center
   :alt: preprocess pca variance ratio

   PCA variance ratio plot. Use this figure together with the recommended PC value shown in the terminal to choose a suitable ``pcs`` setting for clustering.


4. ``{sample}_Mitochondrial_Genes.png`` (mitochondrial signal distribution)

   - This plot shows whether mitochondrial-related signal remains elevated after filtering.
   - If some regions are still globally high, consider tightening the filtering strategy while preserving sufficient data.
   - Adjust thresholds gradually to avoid removing genuine biological signal.

5. ``{sample}_scatter.png`` (summary scatter plot)

   - This plot helps identify potential low-quality clusters of observations.
   - Pay particular attention to regions with low gene counts and high mitochondrial proportion.
   - Interpret it together with the previous plots for a more reliable conclusion.

6. ``{sample}_highly_variable.png`` (highly variable gene plot, optional)

   - This plot confirms that downstream clustering will focus on the most informative genes.
   - If the selection is too narrow, structural information may be lost; if it is too broad, additional noise may be introduced.
   - Start with the default setting and refine it only if clustering results suggest it is necessary.



Continue to :doc:`clustering`.
