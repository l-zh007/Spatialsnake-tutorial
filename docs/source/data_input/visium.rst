Start with 10x Genomics Visium
==============================

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
   * - ``spatial/tissue_positions_list.csv``/ ``tissue_positions_list.csv``
     - Yes
     - CSV
     - Spot coordinates and tissue location information
   * - ``spatial/scalefactors_json.json``
     - Yes
     - JSON
     - Tissue image scale factors
   * - ``spatial/tissue_{hires/lowres}_image.png``
     - Yes
     - PNG
     - High/Low-resolution tissue image
   * - ``<dataset_id>_filtered_feature_bc_matrix.h5``
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


For standard Visium data, the directory layout must follow the Space Ranger
output structure shown below.

Example directory layout
------------------------

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── {sample_id}/
   ├── sample.txt (key sample description file)
   └── results/ (stores analysis outputs)

   data/
   └── {sample_id}/
       ├── filtered_feature_bc_matrix.h5
       └── spatial/
           ├── tissue_positions_list.csv
           ├── scalefactors_json.json
           ├── tissue_lowres_image.png
           └── tissue_hires_image.png


A Demo for Visium Ingestion
---------------------------

``run_type: visium``. In this tutorial, we use a public 10x Genomics Visium dataset as an example:
`Adult Mouse Brain FFPE <https://www.10xgenomics.com/datasets/adult-mouse-brain-ffpe-1-standard-1-3-0>`_

Before running Spatialsnake, create the project directory, place the downloaded files under ``data/``, and extract the spatial image archive so that the sample folder matches the standard Space Ranger-style layout.
Make sure you have already set up the basic working-directory structure as described in the earlier tutorial.

Download the dataset manually from `10x Genomics <https://www.10xgenomics.com/datasets/adult-mouse-brain-ffpe-1-standard-1-3-0>`_
or run the following commands from your working directory:

.. code-block:: bash

   mkdir -p project_root/data/Visium_FFPE_Mouse_Brain
   cd project_root/data/Visium_FFPE_Mouse_Brain
   curl -O https://cf.10xgenomics.com/samples/spatial-exp/1.3.0/Visium_FFPE_Mouse_Brain/Visium_FFPE_Mouse_Brain_filtered_feature_bc_matrix.h5
   curl -O https://cf.10xgenomics.com/samples/spatial-exp/1.3.0/Visium_FFPE_Mouse_Brain/Visium_FFPE_Mouse_Brain_spatial.tar.gz
   tar -xf Visium_FFPE_Mouse_Brain_spatial.tar.gz


Example directory layout and command
------------------------------------

Make sure the directory layout and data filenames match the example below.

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

Then run the command:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=integrate


After extraction, the sample directory should match the layout shown above.


Example ``sample.txt``
----------------------

``single_analysis``:

.. code-block:: text

   sample_id input_path
   Visium_FFPE_Mouse_Brain data/Visium_FFPE_Mouse_Brain

``sample_id`` is the identifier used to create the result directory.
``input_path`` is the path to the corresponding Space Ranger output directory.

Run the command
---------------

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
- Additional output for comparison analysis: ``results/merge_data/integrate/concatenated_sdata.zarr``
- Additional QC plots: the ingestion script writes five descriptive QC figures into the ``integrate`` directory (``total.png``, ``total_umi_by_sample.png``, ``total_genes_by_sample.png``, ``genes_by_sample.png``, and ``scatter.png``). No fixed count cutoff is drawn during ingestion; select filtering thresholds in ``preprocess``. These files are produced during execution even though they are not individually declared in the Snakemake ``output`` section.


.. note::

   The figures generated at this stage are mainly intended for QC inspection. Reviewing them before ``preprocess`` helps you understand the overall quality of the data in advance.

Next steps
----------

You have now ingested your data into a SpatialData Zarr object. For the subsequent core analysis, refer to :doc:`/core_analysis/index`. If you proceed directly with your own data, each step page begins with a concise summary of the essential parameters.
Simply follow the tutorial to update the sample name and platform-specific parameters, then continue with the next step: :doc:`/core_analysis/preprocess`.
If you want to run multi-sample integration analysis, continue to :doc:`/integration_analysis/multi_sample_integration`.
