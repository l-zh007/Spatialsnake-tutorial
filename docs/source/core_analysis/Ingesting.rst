Data Ingestion and QC
=====================

Complete the CRC P2 download and input layout in :doc:`../data_input/visium_HD`.
This page explains the ingestion QC used by the core Demo. If ``integrate`` has
already completed, do not repeat it; inspect the figures and continue to
:doc:`preprocess`. For another platform, use its :doc:`../data_input/index`
entry and retain its sample-table format and TYPE.

Demo: CRC P2 at 8 µm
--------------------

Run from the project root after preparing the raw data:

In this workflow, ``sample.txt`` is the key input configuration file and stores sample names together with source data paths.
For this example, we use the ``single_analysis`` channel and specify the resolution in the third column. The ``bin`` value is automatically zero-padded to three digits. The table identifies the raw data directory and the chosen bin size:

.. code-block:: text
  
   sample_id input_path bin_size
   Colon_Cancer_P2 data/Colon_Cancer_P2 8

Make sure ``sample.txt`` is located in your current working directory.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=integrate

Result file structure
---------------------

.. code-block:: text

   results/ (under project_root)
   └── Colon_Cancer_P2_008um/
       └── integrate/
           ├── Colon_Cancer_P2.zarr # SpatialData Zarr object
           ├── total.png # histogram of total expression
           ├── total_umi_by_sample.png # violin plot of log-transformed total counts
           ├── total_genes_by_sample.png # violin plot of log-transformed detected genes
           ├── genes_by_sample.png # violin plot of mitochondrial signal
           └── scatter.png # scatter plot of total expression versus gene counts

How to inspect the ingestion results
------------------------------------

Core outputs
~~~~~~~~~~~~

- Main object: ``results/<sample>_<bin>um/integrate/<sample>.zarr``
  This standardized object is used directly by subsequent steps such as ``preprocess`` and ``clustering``. It contains the expression matrix, spatial coordinates, and sample annotation metadata.
- QC plots: ``total.png``, ``total_umi_by_sample.png``, ``total_genes_by_sample.png``, ``genes_by_sample.png``, and ``scatter.png`` in the same directory
  These figures are generated automatically to help you assess the overall sample state before filtering.


How to interpret the QC plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``total.png`` (overall distribution)

   - This figure is the first overall quality snapshot and helps you assess whether the sample has a clear expression signal.
   - If most observations are concentrated in the low-value range, the effective signal may be weak and the filtering thresholds in later preprocessing should be chosen carefully.
   - A small number of high-value observations can reflect locally active regions and should not automatically be treated as outliers without checking the spatial map.

2. ``total_umi_by_sample.png`` (compare total UMI across samples)

   - This violin plot displays ``log1p_total_counts`` and compares whether signal intensity is in a similar range across samples or regions.
   - No fixed filtering line is drawn during ingestion because appropriate count thresholds depend on platform, resolution, and sample quality. Use the observed distribution to choose ``min_counts`` in ``preprocess``.
   - If one sample is consistently much lower than the others, downstream cross-sample comparison may be strongly affected by technical differences.
   - Large differences between samples suggest that batch correction and normalization should be examined carefully in later steps.

3. ``total_genes_by_sample.png`` (compare gene complexity across samples)

   - This plot reflects how many genes are detected in each sample and can be interpreted as a measure of information richness.
   - A globally low value often suggests limited data complexity, whereas strong dispersion may indicate substantial intra-sample heterogeneity.
   - It is best interpreted together with the UMI plot rather than in isolation.

4. ``genes_by_sample.png`` (mitochondrial-related signal)

   - This plot helps identify whether the sample contains a high proportion of potentially low-quality observations.
   - If the overall level is high, more careful filtering may be required during preprocessing.
   - At the ingestion stage, the goal is to detect potential issues; actual filtering happens in the next step.

5. ``scatter.png`` (summary scatter plot)

   - This plot is useful for locating suspicious groups of observations, especially regions with low gene counts and high mitochondrial signal.
   - If most points form a continuous distribution without clear separation, the overall structure is usually relatively stable.
   - If obvious abnormal clusters appear, start with conservative filtering parameters during preprocessing and adjust gradually.


Example figures
~~~~~~~~~~~~~~~

In this example dataset, the QC plots show that some cells have very low or nearly absent expression. Based on this observation, we can apply appropriate filtering in the next step.

.. figure:: /_static/images/total_umi_by_sample.png
   :width: 85%
   :align: center
   :alt: Total UMI counts per sample after ingestion


.. figure:: /_static/images/total_genes_by_sample.png
   :width: 85%
   :align: center
   :alt: Detected genes per sample after ingestion



You have now completed the data ingestion step. Continue to :doc:`preprocess`.
