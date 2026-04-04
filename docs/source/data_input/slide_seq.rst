Slide-seq Input Tutorial
========================

Required files
--------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - Filename / pattern
     - Required
     - Format
     - Description
   * - ``BeadLocationsForR.csv``
     - Yes
     - CSV
     - Bead spatial coordinates (``xcoord``/``ycoord``)
   * - ``MappedDGEForR.csv``
     - Yes
     - CSV
     - Bead-by-gene count matrix

Note: for this data type, the main count matrix is always identified as ``MappedDGEForR.csv``.

Where these files come from
---------------------------

- Official download: output directory from the standard Slide-seq processing workflow
- Experimental output: ``BeadLocations`` and ``MappedDGE`` files exported from the laboratory mapping step
- Placeholder usage: you can first write ``data/SQ1`` and replace it later with the real sample directory

``run_type: slide_seq``. In this tutorial, we use a public Slide-seq example and organize the downloaded files into the directory structure expected by Spatialsnake.

One convenient public source for the required processed files is:
https://portals.broadinstitute.org/single_cell/study/SCP354/slide-seq-study#study-summary

Example setup:

.. code-block:: bash

   mkdir -p project_root/data/SQ1
   cd project_root/data/SQ1

   curl -L -o MappedDGEForR.csv.gz ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM5713nnn/GSM5713341/suppl/GSM5713341_Puck_191112_04_MappedDGEForR.csv.gz
   curl -L -o BeadLocationsForR.csv.gz ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM5713nnn/GSM5713341/suppl/GSM5713341_Puck_191112_04_BeadLocationsForR.csv.gz

   gunzip -f MappedDGEForR.csv.gz
   gunzip -f BeadLocationsForR.csv.gz

After download, the sample directory should match the layout shown below.

Input validation logic
----------------------

- Directory validation: before loading, the workflow checks that both ``BeadLocationsForR.csv`` and ``MappedDGEForR.csv`` are present.
- Count file detection: ``MappedDGEForR.csv`` is treated as the main count matrix.
- Implementation detail: the reader constructs ``coor_file`` and ``count_file`` using the ``data/<sample>/`` layout, so keeping this directory structure is recommended.

Example directory layout
------------------------

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── SQ1/
   ├── sample.txt (key sample description file)
   ├── results/ (stores analysis outputs)
   └── <analysis_option>.yaml (optional configuration file)

   data/
   └── SQ1/
       ├── BeadLocationsForR.csv
       └── MappedDGEForR.csv

Example ``sample.txt``
----------------------

``single_analysis``:

.. code-block:: text

   sample_id input_path
   SQ1 data/SQ1
   SQ2 data/SQ2

``compare_analysis``:

.. code-block:: text

   sample_id input_path group
   SQ1 data/SQ1 tumor
   SQ2 data/SQ2 normal

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt slide_seq --option=integrate

Output structure after ingestion
--------------------------------

.. code-block:: text

   results/
   ├── SQ1/
   │   └── integrate/
   │       ├── SQ1.h5ad
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

- Main output: ``results/<sample>/integrate/<sample>.h5ad``
- Additional output for comparison analysis: ``results/merge_data/integrate/concatenated_sdata``
- Additional QC plots: the ingestion script writes five QC figures into the ``integrate`` directory. These files are generated during execution even though they are not explicitly listed in the Snakemake ``output`` declaration.

Suggested figure content
------------------------

When you add a real result figure to this page, we recommend highlighting the agreement between bead coordinates and matrix indices, the continuity of spatial coverage, and the completeness of the exported ``h5ad`` object.

If you want to run multi-sample integration analysis, continue to :doc:`/integration_analysis/multi_sample_integration`.
Otherwise, return to :doc:`index`.
