Data Integration (Ingesting)
============================

This tutorial uses a Visium HD example dataset to demonstrate the full core workflow. If you are working with another spatial transcriptomics platform or with multi-sample data, go to the corresponding input tutorial and run the ``Ingesting`` step there.

For the full configuration reference, see :doc:`../config_reference/integrate_yaml`.

If you want to follow the tutorial exactly as written, download the Visium HD CRC P2 example dataset from:
https://www.10xgenomics.com/platforms/visium/product-family/dataset-human-crc

From the "Download in browser" section, download the ``Binned outputs`` archive, extract it with ``tar -xzf`` under your ``data/`` directory, and store it in a folder named ``Colon_Cancer_P2``.

Required files
--------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - Filename / pattern
     - Required
     - Format
     - Description
   * - ``binned_outputs/square_{bin}um/spatial/tissue_positions.parquet``
     - Yes
     - Parquet
     - Bin-level coordinate information
   * - ``binned_outputs/square_{bin}um/spatial/scalefactors_json.json``
     - Yes
     - JSON
     - Image scale factors
   * - ``binned_outputs/square_{bin}um/spatial/tissue_lowres_image.png``
     - Yes
     - PNG
     - Low-resolution tissue image
   * - ``binned_outputs/square_{bin}um/filtered_feature_bc_matrix.h5`` or ``binned_outputs/square_{bin}um/raw_feature_bc_matrix.h5``
     - Yes
     - H5
     - Main expression matrix
   * - ``binned_outputs/square_{bin}um/cell_feature_matrix.h5`` / ``filtered_feature_cell_matrix.h5`` / ``raw_feature_cell_matrix.h5``
     - No
     - H5
     - Alternative compatible matrix filenames


About the data structure
------------------------

Visium HD data are organized by grid resolution. Each resolution-specific directory contains an expression matrix and the corresponding spatial metadata, typically for 2 µm, 8 µm, or 16 µm bins.
In this tutorial, we use the ``square_008um`` directory as the example input.

Example directory layout
------------------------

.. code-block:: text

  project_root/ (current working directory)
   ├── data/ (stores your raw data)
   │   └── Colon_Cancer_P2/
   ├── sample.txt (key sample description file)
   ├── results/ (stores analysis outputs; generated automatically)
   └── <analysis_option>.yaml (optional configuration file)

   data/
   └── Colon_Cancer_P2/
       └── binned_outputs/
           └── square_008um/
               ├── filtered_feature_bc_matrix.h5
               └── spatial/
                   ├── tissue_positions.parquet
                   ├── scalefactors_json.json
                   ├── tissue_hires_image.png
                   └── tissue_lowres_image.png

Example ``sample.txt``
----------------------

In Spatialsnake, ``sample.txt`` is the main input configuration file and stores sample names together with source paths.
For this example, we use the ``single_analysis`` channel and specify the resolution in the third column. The ``bin`` value is automatically zero-padded to three digits. Make sure the sample name matches the folder name under ``data/``:

.. code-block:: text
  
   sample_id input_path bin
   Colon_Cancer_P2 data/Colon_Cancer_P2 8


Run the command
---------------

Make sure ``sample.txt`` is located in your current working directory.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=integrate

Result file structure
---------------------

.. code-block:: text

   results/ (under project_root)
   ├── Colon_Cancer_P2_008um/
       └── integrate/
           ├── Colon_Cancer_P2.zarr # zarr-formatted data
           ├── total.png # histogram of total expression
           ├── total_umi_by_sample.png # histogram of total UMI counts by sample
           ├── total_genes_by_sample.png # histogram of detected genes by sample
           ├── genes_by_sample.png # histogram of mitochondrial signal by sample
           └── scatter.png # scatter plot of total expression versus gene counts

How to explore the results of Ingesting?
----------------------------------------

Core outputs
~~~~~~~~~~~~

- Main object: ``results/<sample>_<bin>um/integrate/<sample>.zarr``
  This standardized object is used directly by downstream steps such as ``preprocess`` and ``clustering``. It contains the expression matrix, spatial coordinates, and sample-level metadata.
- QC plots: ``total.png``, ``total_umi_by_sample.png``, ``total_genes_by_sample.png``, ``genes_by_sample.png``, and ``scatter.png``
  These figures are generated automatically and provide a first-pass view of sample quality before filtering.


How to interpret the QC plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``total.png`` (overall distribution)

   - This plot provides the first overall quality overview and helps you determine whether the sample has a clear expression signal.
   - If most observations are concentrated in the low-value range, the effective signal may be weak and filtering thresholds should be chosen conservatively.
   - A small number of high-value observations can reflect locally active regions and should be interpreted together with the spatial image rather than treated as outliers immediately.

2. ``total_umi_by_sample.png`` (compare total UMI across samples)

   - This plot shows whether the signal intensity is in a similar range across samples.
   - If one sample is globally much lower than the others, cross-sample comparison may be affected by technical variation.
   - Large between-sample differences indicate that batch correction and normalization should be assessed carefully in later steps.

3. ``total_genes_by_sample.png`` (compare gene complexity across samples)

   - This plot reflects how many genes are detected in each sample and can be interpreted as a measure of data richness.
   - A globally low value may indicate limited complexity, while a wide spread can suggest strong heterogeneity.
   - It is best interpreted together with the UMI plot rather than alone.

4. ``genes_by_sample.png`` (mitochondrial-related signal)

   - This plot helps identify whether the sample contains a high proportion of potentially low-quality observations.
   - If the overall level is high, stricter filtering may be needed during preprocessing.
   - At this stage, the purpose is to detect potential risk; actual filtering is performed in the next step.

5. ``scatter.png`` (summary scatter plot)

   - This plot is useful for locating suspicious groups of observations, especially regions with low gene counts and high mitochondrial signal.
   - If most points form a continuous distribution without clear discontinuities, the overall structure is usually relatively stable.
   - If obvious abnormal clusters appear, start with conservative filtering parameters during preprocessing and adjust gradually.


Example figures
~~~~~~~~~~~~~~~

In this example dataset, some cells show very low or nearly absent expression. This suggests that filtering in the next step will improve data quality.

.. figure:: /_static/images/total_umi_by_sample.png
   :width: 85%
   :align: center
   :alt: ingesting total umi by sample


.. figure:: /_static/images/total_genes_by_sample.png
   :width: 85%
   :align: center
   :alt: ingesting total genes by sample



You have now completed the data ingestion step. Continue to :doc:`preprocess`.
