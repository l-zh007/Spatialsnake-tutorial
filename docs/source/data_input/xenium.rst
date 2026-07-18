Xenium Input Tutorial
=====================

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
   * - ``morphology.ome.tif``/ ``morphology_focus.ome.tif``
     - Yes
     - OME-TIFF
     - Morphology image
   * - ``experiment.xenium``
     - Yes
     - Xenium metadata
     - Platform metadata and file index
   * - ``cell_feature_matrix.h5`` / ``filtered_feature_cell_matrix.h5`` / ``raw_feature_cell_matrix.h5`` / ``filtered_feature_bc_matrix.h5`` / ``raw_feature_bc_matrix.h5``
     - No
     - H5
     - Alternative compatible matrix filenames that can be detected automatically

See the `Xenium Onboard Analysis Output Overview <https://www.10xgenomics.com/support/software/xenium-onboard-analysis/latest/analysis/xoa-output-at-a-glance>`_
for a complete description of the output files.

Where these files come from
---------------------------

- Official download: directory exported from 10x Xenium Ranger output
- Public dataset: published studies and official 10x Genomics demonstration repositories
- Experimental output: complete sample directory delivered by the platform


Demo Walkthrough
------------------------

``run_type: xenium``. In this tutorial, we use the public breast cancer dataset provided by 10x Genomics:
`Xenium Prime FFPE Human Breast Cancer <https://www.10xgenomics.com/datasets/xenium-prime-ffpe-human-breast-cancer>`_

Before running Spatialsnake, create the project directory, download the Xenium output files from the dataset page, and place them under a single sample folder so that the directory matches the expected Xenium export structure.

Example setup:

.. code-block:: bash

   mkdir -p project_root/data/breast_cancer
   cd project_root/data/breast_cancer

   curl -O https://s3-us-west-2.amazonaws.com/10x.files/samples/xenium/3.0.0/Xenium_Prime_Breast_Cancer_FFPE/Xenium_Prime_Breast_Cancer_FFPE_outs.zip
   unzip Xenium_Prime_Breast_Cancer_FFPE_outs.zip

After download, the sample directory should match the layout shown below.


Example directory layout
------------------------

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── breast_cancer/
   ├── sample.txt (key sample description file)
   ├── results/ (stores analysis outputs)
   └── <analysis_option>.yaml (optional configuration file)

   data/
   └── breast_cancer/
       ├── experiment.xenium
       ├── cells.parquet
       ├── transcripts.parquet
       ├── morphology.ome.tif
       └── cell_feature_matrix.h5
       └── ...

``single_analysis``:

.. code-block:: text

   sample_id input_path
   breast_cancer data/breast_cancer


Make sure ``sample.txt`` is located in your current working directory.

.. code-block:: bash

   spatialsnake single_analysis sample.txt xenium --option=integrate

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


You have now ingested your data into a SpatialData Zarr object. For the subsequent core analysis, refer to :doc:`/core_analysis/index`. If you proceed directly with your own data, each step page begins with a concise summary of the essential parameters.
Simply follow the tutorial to update the sample name and platform-specific parameters, then continue with the next step: :doc:`/core_analysis/preprocess`.
If you want to run multi-sample integration analysis, continue to :doc:`/integration_analysis/multi_sample_integration`.
