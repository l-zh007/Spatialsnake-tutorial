Start with 10x Genomics Visium
==============================

``run_type: visium``. In this tutorial, we use a public dataset from the 10x Genomics website for demonstration.

Dataset link: https://www.10xgenomics.com/datasets/adult-mouse-brain-ffpe-1-standard-1-3-0

Download the filtered feature/barcode matrix in HDF5 format together with the Spatial imaging data archive, then extract the archive with ``tar -xfvz``.

Required files
--------------

The input directory should follow the standard 10x Genomics Space Ranger output structure.

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - Filename / pattern
     - Required
     - Format
     - Description
   * - ``spatial/tissue_positions_list.csv``
     - Yes
     - CSV
     - Spot coordinates and tissue location information
   * - ``spatial/scalefactors_json.json``
     - Yes
     - JSON
     - Tissue image scale factors
   * - ``spatial/tissue_lowres_image.png``
     - Yes
     - PNG
     - Low-resolution tissue image
   * - ``spatial/tissue_hires_image.png``
     - Yes
     - PNG
     - High-resolution tissue image
   * - ``filtered_feature_bc_matrix.h5`` or ``raw_feature_bc_matrix.h5``
     - Yes
     - H5
     - Main expression matrix; the workflow prioritizes the filtered matrix
   * - ``cell_feature_matrix.h5`` / ``filtered_feature_cell_matrix.h5`` / ``raw_feature_cell_matrix.h5``
     - No
     - H5
     - Alternative compatible matrix filenames that are detected automatically if present

Where these files come from
---------------------------

- Official download: standard 10x Genomics Space Ranger output directory
- Experimental output: Visium analysis results delivered by the sequencing or analysis platform
- Placeholder usage: you can initially write ``/path/to/visium_sample`` in ``sample.txt`` and replace it later with the real path

Example directory layout
------------------------

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── Visium_FFPE_Mouse_Brain/
   │
   ├── sample.txt (key sample description file)
   ├── results/ (stores analysis outputs)
   └── <analysis_option>.yaml (optional configuration file)

   data/
   └── Visium_FFPE_Mouse_Brain/
       ├── filtered_feature_bc_matrix.h5
       └── spatial/
           ├── tissue_positions_list.csv
           ├── scalefactors_json.json
           ├── tissue_lowres_image.png
           └── tissue_hires_image.png

Some datasets may use prefixed HDF5 filenames such as ``Visium_FFPE_Mouse_Brain_filtered_feature_bc_matrix.h5``. In that case, make sure the prefix matches the sample folder name so that the pipeline can recognize it automatically.

Example ``sample.txt``
----------------------

``single_analysis``:

.. code-block:: text

   sample_id input_path
   Visium_FFPE_Mouse_Brain data/Visium_FFPE_Mouse_Brain

``sample_id``: sample name; the result folder is created with this ID
``input_path``: path to the sample data directory

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=integrate

Output structure after ingestion
--------------------------------

.. code-block:: text

   results/
   ├── Visium_FFPE_Mouse_Brain/
   │   └── integrate/
   │       ├── Visium_FFPE_Mouse_Brain.zarr
   │       ├── total.png
   │       ├── total_umi_by_sample.png
   │       ├── total_genes_by_sample.png
   │       ├── genes_by_sample.png
   │       └── scatter.png

Output summary
--------------

- Main output: ``results/<sample>/integrate/<sample>.zarr``
- Additional output for comparison analysis: ``results/merge_data/integrate/concatenated_sdata``
- Additional QC plots: the ingestion script writes five QC figures into the ``integrate`` directory (``total.png``, ``total_umi_by_sample.png``, ``total_genes_by_sample.png``, ``genes_by_sample.png``, and ``scatter.png``). These files are produced during execution even though they are not individually declared in the Snakemake ``output`` section.


.. note::

   The figures generated at this stage are mainly intended for QC inspection. Reviewing them before ``preprocess`` helps you understand the overall quality of the data in advance.

If you want to run multi-sample integration analysis, continue to :doc:`/integration_analysis/multi_sample_integration`.
Otherwise, proceed to :doc:`../core_analysis/index`.
