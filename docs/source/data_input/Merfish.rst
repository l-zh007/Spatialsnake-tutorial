MERFISH Input Tutorial
======================

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
     - Required
     - CSV
     - Cell-by-gene count matrix
   * - ``**/detected_transcripts.csv``
     - Required
     - CSV
     - Detected-transcript table
   * - ``**/cell_boundaries.parquet``
     - Required
     - Parquet
     - Cell boundary polygons
   * - ``**/cell_metadata.csv``
     - Required
     - CSV
     - Per-cell metadata table
   * - ``**/images/micron_to_mosaic_pixel_transform.csv``  ``**/images/**_z*.tif`` ``**/images/manifest.json``
     - No
     - TIFF/OME.TIFF/OME-XML
     - Includes TIFF image information. The exact file set may vary across MERFISH versions; please refer to the MERFISH documentation. If no image information is available, Spatialsnake will skip these files by default. Please ensure your data are from MERFISH version 2 or later.

Following the output directory structure of the Vizgen MERFISH platform, organize the downloaded files under the ``data/`` directory. Replace ``region_0`` with your own sample name.

For example:

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── region_0/
   ├── sample.txt (key sample description file)
   └── results/ (stores analysis outputs)

   data/
   └── region_0/
       ├── cell_by_gene.csv
       ├── detected_transcripts.csv.gz
       ├── ......
       └── images/
           ├── morphology_mip.ome.tif
           ├── ......
           └── manifest.json

For a routine first analysis, select one region and one relevant set of z
layers. The MERSCOPE reader options can be configured when additional regions
or z layers are required.

Where these files come from
---------------------------

- Official download: standard Vizgen MERSCOPE/MERFISH output directory
- Experimental output: cell and transcript files exported by a laboratory MERFISH pipeline
- Placeholder usage: you can first write ``/path/to/merfish_sample`` and replace it later with the real directory


Demo Walkthrough
------------------------

``run_type: Merfish``. In this tutorial, we assume a standard MERFISH output directory prepared from a public or in-house Vizgen-style dataset.
One public example release is available from the Vizgen Breast Cancer Tissue Microarray Region_R1:
`Vizgen MERFISH Breast Cancer Dataset <https://console.cloud.google.com/storage/browser/vz-merfish2-showcase/202409242358_240916JHHUBC0005XQ-V2V-HubcTMA-V2-BY_VMSC02511>`_

For this demo, we use the Region_R1 Breast Cancer Tissue Microarray data from the download link above. Because the dataset is large and contains multiple files stored in a public repository layout, please download and organize the files following the expected directory hierarchy.
Make sure you have already created the basic working directory as described in the earlier tutorial.

Example setup:

.. code-block:: bash

   mkdir -p project_root/data/Breast_Cancer
   cd project_root/data/Breast_Cancer

After download, the sample directory should match the layout shown below.

Example directory layout
------------------------

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── Breast_Cancer/
   ├── sample.txt (key sample description file)
   └── results/ (stores analysis outputs)

   data/
   └── Breast_Cancer/
       ├── cell_by_gene.csv
       ├── detected_transcripts.csv.gz
       ├── ......
       └── images/
           ├── morphology_mip.ome.tif
           ├── ......
           └── manifest.json

``single_analysis``:

.. code-block:: text

   sample_id input_path
   Breast_Cancer data/Breast_Cancer

.. note::
      If you intend to perform multi-sample analysis, please first complete the content on this page, then refer to :doc:`/integration_analysis/multi_sample_integration` for configuration and command instructions. Compared with single-sample analysis, multi-sample analysis requires multiple sample data directories and a ``sample.txt`` with additional rows. As with single-sample mode, the ``data`` path and ``sample_id`` for each sample must match the entries in ``sample.txt``.

Below is the minimal command to run the data ingestion module. For additional parameter configuration, please refer to the corresponding YAML reference at :doc:`../config_reference/integrate_yaml`.

.. code-block:: bash

   spatialsnake single_analysis sample.txt Merfish --option=integrate


Output structure after ingestion
--------------------------------

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── Breast_Cancer/
   ├── sample.txt (key sample description file)
   ├── log/
   └── results/ (stores analysis outputs)

   results/
   └── Breast_Cancer/
      └── integrate/
          ├── Breast_Cancer.zarr
          ├── total.png
          ├── total_umi_by_sample.png
          ├── total_genes_by_sample.png
          ├── genes_by_sample.png
          └── scatter.png


- Main output: ``results/<sample>/integrate/<sample>.zarr``
- Additional output for comparison analysis: ``results/merge_data/integrate/concatenated_sdata.zarr``
- Additional QC plots: single-sample ingestion writes five QC figures into the ``integrate`` directory. These files are generated in practice even though they are not explicitly declared in the Snakemake ``output`` section.

You have now ingested your data into a SpatialData Zarr object. For the subsequent core analysis, refer to :doc:`/core_analysis/index`. If you proceed directly with your own data, each step page begins with a concise summary of the essential parameters.
Simply follow the tutorial to update the sample name and platform-specific parameters, then continue with the next step: :doc:`/core_analysis/preprocess`.
If you want to run multi-sample integration analysis, continue to :doc:`/integration_analysis/multi_sample_integration`.
