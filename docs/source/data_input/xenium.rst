Xenium Input Tutorial
=====================

``run_type: xenium``. In this tutorial, we use the public breast cancer dataset provided by 10x Genomics.

Dataset link: https://www.10xgenomics.com/datasets/xenium-prime-ffpe-human-breast-cancer


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
   * - ``morphology.ome.tif``
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

Where these files come from
---------------------------

- Official download: directory exported from 10x Xenium on-board analysis
- Experimental output: complete sample directory delivered by the platform


Example directory layout
------------------------

.. code-block:: text

   data/
   └── breast_cancer/
       ├── experiment.xenium
       ├── cells.parquet
       ├── transcripts.parquet
       ├── morphology.ome.tif
       └── cell_feature_matrix.h5
       └──  ........

Example ``sample.txt``
----------------------

``single_analysis``:

.. code-block:: text

   sample_id input_path
   breast_cancer data/breast_cancer


Run the command
---------------

Make sure ``sample.txt`` is located in your current working directory.

.. code-block:: bash

   spatialsnake single_analysis sample.txt xenium --option=integrate

Output structure after ingestion
--------------------------------

.. code-block:: text

   results/
   ├── breast_cancer/
   │   └── integrate/
   │       ├── breast_cancer.zarr
   │       ├── total.png
   │       ├── total_umi_by_sample.png
   │       ├── total_genes_by_sample.png
   │       ├── genes_by_sample.png
   │       └── scatter.png

Output summary
--------------

- Additional QC plots: the ingestion script writes five QC figures into the ``integrate`` directory.


If you want to run multi-sample integration analysis, continue to :doc:`/integration_analysis/multi_sample_integration`.
Otherwise, return to :doc:`index`.
