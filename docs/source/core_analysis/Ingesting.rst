Data ingestion and sample assembly
==================================

Complete the CRC P2 download and input layout in :doc:`../data_input/visium_HD`.
This page explains the ingestion QC used by the core demo. If ``ingestion`` has
already completed, do not repeat it; inspect the figures and continue to
:doc:`preprocess`. For another platform, use its :doc:`../data_input/index`
entry and retain its sample-table format and TYPE.

The command name is ``ingestion``; the output directory remains ``integrate/``.
The legacy option ``--option=integrate`` is still accepted.

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

   spatialsnake single_analysis sample.txt visium_HD --option=ingestion

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

- ``total.png`` and ``total_umi_by_sample.png`` summarize total counts; the
  latter uses ``log1p_total_counts``. Inspect the low-count tail before choosing
  ``min_counts``. High counts alone do not identify an artifact.
- ``total_genes_by_sample.png`` summarizes detected genes. Compare it with total
  counts to distinguish low-complexity observations from differences in depth.
- ``genes_by_sample.png`` summarizes mitochondrial counts. Interpret this with
  tissue context; mitochondrial gene detection differs across species and panels.
- ``scatter.png`` shows total counts versus detected genes for a single sample;
  the integrated ingestion plot uses log-transformed mitochondrial counts versus
  detected genes. Color indicates the mitochondrial fraction. Review outlying
  observations in spatial context before choosing filtering thresholds.

For multiple samples, inspect these distributions separately. Differences can
reflect tissue composition or technical quality; normalization and batch
correction do not replace appropriate QC.

Example figures
~~~~~~~~~~~~~~~

The CRC P2 plots show a low-count, low-gene tail among the 8 µm bins.
Use these distributions to choose initial filters, then inspect the retained
bins after :doc:`preprocess`. Bins are spatial observations, not individual cells.

.. figure:: /_static/images/total_umi_by_sample.png
   :width: 85%
   :align: center
   :alt: Total UMI counts per sample after ingestion


.. figure:: /_static/images/total_genes_by_sample.png
   :width: 85%
   :align: center
   :alt: Detected genes per sample after ingestion


You have now completed the data ingestion step. Continue to :doc:`preprocess`.
