Xenium input
============

Required files
--------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - Filename / pattern
     - Required
     - Format
     - Description
   * - ``cells.parquet``
     - Yes
     - Parquet
     - Cell-level statistics and coordinates
   * - ``transcripts.parquet``
     - Yes
     - Parquet
     - Transcript point coordinates
   * - ``cells.zarr.zip``
     - Yes
     - Zipped Zarr
     - Cell labels and metadata loaded by the current reader
   * - ``morphology_focus.ome.tif`` / ``morphology_focus/morphology_focus_0000.ome.tif``
     - Yes
     - OME-TIFF
     - Focus image: a single file before XOA 2.0, or the complete morphology_focus directory for newer outputs
   * - ``experiment.xenium``
     - Yes
     - Xenium metadata
     - Platform metadata and file index
   * - ``cell_feature_matrix.h5``
     - Yes
     - H5
     - Cell-by-feature count matrix required by the Xenium reader

Keep the original channel filenames in ``morphology_focus/``. The reader checks
the channel set for the version recorded in ``experiment.xenium``.
``morphology.ome.tif`` alone does not replace the focus image.
If ``morphology_mip: True`` is enabled for older outputs, also provide
``morphology_mip.ome.tif``.

See the `Xenium Onboard Analysis Output Overview <https://www.10xgenomics.com/support/software/xenium-onboard-analysis/latest/analysis/xoa-output-at-a-glance>`_
for a complete description of the output files.

Where these files come from
---------------------------

- Official download: Xenium Onboard Analysis (XOA) or Xenium Ranger output directory
- Public dataset: published studies and official 10x Genomics demonstration repositories
- Experimental output: complete sample directory delivered by the platform


Demo walkthrough
----------------

``run_type: xenium``. In this tutorial, we use the public breast cancer dataset provided by 10x Genomics:
`Xenium Prime FFPE Human Breast Cancer <https://www.10xgenomics.com/datasets/xenium-prime-ffpe-human-breast-cancer>`_

Before running Spatialsnake, create the project directory, download the Xenium output files from the dataset page, and place them under a single sample folder so that the directory matches the expected Xenium export structure.

Example setup:

.. code-block:: bash

   mkdir -p data/breast_cancer
   cd data/breast_cancer

   curl -O https://s3-us-west-2.amazonaws.com/10x.files/samples/xenium/3.0.0/Xenium_Prime_Breast_Cancer_FFPE/Xenium_Prime_Breast_Cancer_FFPE_outs.zip
   unzip Xenium_Prime_Breast_Cancer_FFPE_outs.zip
   cd ../..

If the ZIP creates an extra output directory, arrange its contents so that
``experiment.xenium`` is directly under ``data/breast_cancer`` before running.
The sample directory should match the layout below.


Example directory layout
------------------------

.. code-block:: text

   project_root/
   ├── data/ (stores processed platform outputs)
   │   └── breast_cancer/
   ├── sample.txt (key sample description file)
   ├── results/ (stores analysis outputs)
   └── <analysis_option>.yaml (optional configuration file)

   data/
   └── breast_cancer/
       ├── experiment.xenium
       ├── cells.parquet
       ├── cells.zarr.zip
       ├── transcripts.parquet
       ├── morphology_focus/
       │   ├── morphology_focus_0000.ome.tif
       │   ├── morphology_focus_0001.ome.tif
       │   ├── morphology_focus_0002.ome.tif
       │   └── morphology_focus_0003.ome.tif
       ├── cell_feature_matrix.h5
       └── ...

``single_analysis``:

.. code-block:: text

   sample_id input_path
   breast_cancer data/breast_cancer


Make sure ``sample.txt`` is located in your current working directory.

.. code-block:: bash

   spatialsnake single_analysis sample.txt xenium --option=ingestion

Output structure after ingestion
--------------------------------

.. code-block:: text

   results/
   ├── breast_cancer/
      └── integrate/
          ├── breast_cancer.zarr
          ├── total.png
          ├── total_umi_by_sample.png
          ├── total_genes_by_sample.png
          ├── genes_by_sample.png
          └── scatter.png

- Additional QC plots: the ingestion script writes five descriptive QC figures into the ``integrate`` directory. No fixed count cutoff is drawn during ingestion; select filtering thresholds in ``preprocess``.


Continue to :doc:`/core_analysis/preprocess` using the same core sample table
and this page's TYPE. Choose QC thresholds for your own platform and resolution.
For a joint analysis, follow :doc:`/integration_analysis/multi_sample_integration`
instead of processing each sample independently.
