MERFISH Input Tutorial
======================

``run_type: Merfish``. This tutorial demonstrates how to prepare MERFISH data for Spatialsnake.

Required files
--------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - Filename / pattern
     - Required
     - Format
     - Description
   * - ``**/cell_by_gene.csv``
     - At least one
     - CSV
     - Cell-by-gene expression matrix, commonly found in MERSCOPE outputs
   * - ``**/*transcripts*.csv*``
     - At least one
     - CSV/CSV.GZ
     - Transcript coordinate file
   * - ``**/*transcripts*.parquet``
     - At least one
     - Parquet
     - Transcript coordinate file in Parquet format
   * - ``cell_feature_matrix.h5`` / ``filtered_feature_cell_matrix.h5`` / ``raw_feature_cell_matrix.h5`` / ``filtered_feature_bc_matrix.h5`` / ``raw_feature_bc_matrix.h5``
     - No
     - H5
     - Alternative compatible matrix filenames that can be recognized if present

Validation rule: ``cell_by_gene.csv`` and ``transcripts`` files are not both mandatory, but at least one key input must be found in the directory or the workflow will stop.

Where these files come from
---------------------------

- Official download: standard Vizgen MERSCOPE/MERFISH output directory
- Experimental output: cell and transcript files exported by a laboratory MERFISH pipeline
- Placeholder usage: you can first write ``/path/to/merfish_sample`` and replace it later with the real directory

Input validation logic
----------------------

- Directory validation: the workflow recursively searches for ``cell_by_gene.csv``, ``*transcripts*.csv*``, and ``*transcripts*.parquet``. At least one of these inputs must be present.
- Post-ingestion handling: if transcript points are missing from the points layer, the reader attempts to inject a ``transcripts`` points layer so the downstream workflow remains usable.

Example directory layout
------------------------

.. code-block:: text

   data/
   └── M1/
       ├── region_0/
       │   ├── cell_by_gene.csv
       │   └── detected_transcripts.csv.gz
       └── images/
           └── morphology_mip.ome.tif

Example ``sample.txt``
----------------------

``single_analysis``:

.. code-block:: text

   sample_id input_path
   M1 data/M1
   M2 data/M2

``compare_analysis``:

.. code-block:: text

   sample_id input_path group
   M1 data/M1 tumor
   M2 data/M2 normal

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt Merfish --option=integrate

Output structure after ingestion
--------------------------------

.. code-block:: text

   results/
   ├── M1/
   │   └── integrate/
   │       ├── M1.zarr
   │       ├── total.png
   │       ├── total_umi_by_sample.png
   │       ├── total_genes_by_sample.png
   │       ├── genes_by_sample.png
   │       └── scatter.png
   └── merge_data/
       └── integrate/
           └── concatenated_sdata


Output summary
--------------

- Main output: ``results/<sample>/integrate/<sample>.zarr``
- Additional output for comparison analysis: ``results/merge_data/integrate/concatenated_sdata``
- Additional QC plots: single-sample ingestion writes five QC figures into the ``integrate`` directory. These files are generated in practice even though they are not explicitly declared in the Snakemake ``output`` section.

Suggested figure content
------------------------

When you add a real result figure to this page, we recommend emphasizing whether the transcript points layer was injected successfully, the quality of the cell-by-gene matrix, and the agreement between spatial coordinates and imaging data.

If you want to run multi-sample integration analysis, continue to :doc:`/integration_analysis/multi_sample_integration`.
Otherwise, return to :doc:`index`.
