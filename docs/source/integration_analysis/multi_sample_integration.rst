Spatialsnake for multi-sample integration
=========================================

Before reading this section, make sure you have completed at least one tutorial in :doc:`../data_input/index` so that you already know how to prepare ``sample.txt`` and run Spatialsnake.
This tutorial is intended for studies with multiple spatial transcriptomics datasets from one or more experimental conditions, such as control and disease tissues with biological replicates.
The integrated object produced here can be used for the same downstream analyses as a single-sample object, although some result files and interpretations differ.


What changes in a multi-sample analysis?
------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 36 42

   * - Setting
     - Independent samples
     - Integrated analysis
   * - Channel
     - ``single_analysis``
     - ``compare_analysis``
   * - Core table
     - One row per sample
     - One row per sample, with ``group`` before any platform selector
   * - Output
     - ``results/<sample>/`` (HD adds the bin suffix)
     - ``results/merge_data/``
   * - Batch handling
     - No between-sample correction
     - Consider ``harmony`` or ``bbknn`` during preprocessing

``sample_id`` identifies the sample; ``group`` identifies the study condition.
Batch correction uses sample identity, not condition. Visium HD adds
``bin_size`` and Stereo-seq adds ``input_spec``; see :ref:`sample-tables` for
exact headers. This page demonstrates the changed commands, while
:doc:`../core_analysis/index` explains QC, PC selection, markers, and annotation.


Demo Walkthrough
----------------

.. note::
   To begin with downstream analyses, use the annotated five-brain object at
   ``results/merge_data/annotation/concatenated_sdata.zarr`` in
   ``04_tutorial_essential_resources.zip`` on
   `Zenodo <https://doi.org/10.5281/zenodo.23374838>`__.
   Extract the archive and run commands from ``test/``; the workflow below
   describes preparation from raw data.

Multi-sample analysis typically combines several datasets. For a concise demonstration, we use multiple Visium mouse brain sections from a public dataset:

`E-MTAB-11114 (ArrayExpress) <https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-11114>`_

We use the demo data for a minimal ``core_analysis`` walkthrough that covers data ingestion, preprocessing, and annotation. This tutorial helps you intuitively understand the key differences between multi-sample and single-sample analyses. For detailed module functionality, parameter settings, and implementation of analysis features, please read the introductory tutorial at the beginning of each module. You can also use our Visium HD example dataset for a more comprehensive hands-on learning experience.

The five sections were collected under the same experimental condition.
``Group1`` and ``Group2`` are illustrative teaching groups, not control/disease
assignments. For your own study, use real condition labels and biological
replicates.

This tutorial uses five public samples:

- Group 1: ``ST8059048``, ``ST8059049``, ``ST8059050``
- Group 2: ``ST8059051``, ``ST8059052``

If you are using your own dataset rather than the example shown here, the main fields you need to replace are:

- the sample IDs in the download script and in ``sample.txt``
- the ``input_path`` values in ``sample.txt``
- the biological group labels in the ``group`` column
- the platform type in the command if your data are not ``visium``

Step 1: create a download script in the project root
----------------------------------------------------

First make sure the current working directory contains a ``data/`` folder, then create a script named ``download.sh``.
This script downloads one expression matrix and one spatial archive for each sample and expands them directly into sample-specific directories under ``data/``.
If you are working with another public dataset, keep the same folder logic but replace the sample IDs and download URLs.

.. code-block:: bash


   #!/usr/bin/env bash
   set -euo pipefail
   ids=(ST8059048 ST8059049 ST8059050 ST8059051 ST8059052)
   for id in "${ids[@]}"; do
   mkdir -p "data/${id}"
   cd "data/${id}"
   wget -c "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/114/E-MTAB-11114/Files/${id}_filtered_feature_bc_matrix.h5"
   wget -c "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/114/E-MTAB-11114/Files/${id}_spatial.tar.gz"
   tar -xvzf "${id}_spatial.tar.gz"
   cd - >/dev/null
   done


Step 2: make the script executable and run it
---------------------------------------------

.. code-block:: bash

   chmod +x download.sh
   ./download.sh

After the script finishes, the input directory should follow the structure below.
This is the folder layout that Spatialsnake expects when reading multi-sample Visium data.

Example input directory layout
------------------------------

.. code-block:: text

   project_root/
   ├── data/
   │   ├── ST8059048/
   │   │   ├── ST8059048_filtered_feature_bc_matrix.h5
   │   │   └── spatial/
   │   │       ├── tissue_positions_list.csv
   │   │       ├── scalefactors_json.json
   │   │       ├── tissue_lowres_image.png
   │   │       └── tissue_hires_image.png
   │   ├── ST8059049/
   │   │   ├── ST8059049_filtered_feature_bc_matrix.h5
   │   │   └── spatial/
   │   ├── ST8059050/
   │   │   ├── ST8059050_filtered_feature_bc_matrix.h5
   │   │   └── spatial/
   │   ├── ST8059051/
   │   │   ├── ST8059051_filtered_feature_bc_matrix.h5
   │   │   └── spatial/
   │   └── ST8059052/
   │       ├── ST8059052_filtered_feature_bc_matrix.h5
   │       └── spatial/
   ├── sample.txt
   └── results/

If you are using your own data, keep the same two-level organization:

- one folder per sample under ``data/``
- one expression matrix and one ``spatial/`` directory inside each sample folder

Step 3: prepare ``sample.txt`` with group information
-----------------------------------------------------

For multi-sample integration, ``sample.txt`` is similar to the single-sample version but must also include a group column.
The ``group`` field defines the biological condition used later in comparison-oriented analyses, so it should reflect your real experimental design rather than arbitrary batch labels.
If you are using another dataset, replace both the sample IDs and the paths, and rename ``Group1`` and ``Group2`` to meaningful condition names such as ``Control`` and ``Disease``.

.. code-block:: text

   sample_id   input_path         group
   ST8059048   data/ST8059048     Group1
   ST8059049   data/ST8059049     Group1
   ST8059050   data/ST8059050     Group1
   ST8059051   data/ST8059051     Group2
   ST8059052   data/ST8059052     Group2

Step 4: run integration and merge the samples
---------------------------------------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=integrate

At this stage, Spatialsnake reads all sample folders listed in ``sample.txt``, standardizes them into one common object representation, and writes the merged result for downstream preprocessing.
If your data come from another platform, replace ``visium`` with the corresponding ``run_type``.

The result structure is similar to the single-sample workflow:

.. code-block:: text

   results/
   └── merge_data/
       └── integrate/
           └── concatenated_sdata.zarr
               ...........



Step 5: preprocess the integrated object
----------------------------------------

Single-sample analyses often do not require explicit batch correction, but for multi-sample analysis it is usually worth considering:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --min_counts=100 --min_cells=100 --batch_method=harmony

Step 6: continue with the steps
-------------------------------

After preprocessing, the remaining steps follow the standard ``compare_analysis`` workflow.
The pipeline will generate joint visualizations and result tables across samples.
Because the data are integrated, manual annotation maps shared cluster IDs
across all samples. Save the mapping below as ``annotation.txt`` or download
:download:`brain_annotation.txt </config/demo_resources/brain_annotation.txt>`
and rename it. Review the actual markers before using different labels.

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=clustering --resolution=0.5 --pcs=15
   spatialsnake compare_analysis sample.txt visium --option=annotation_help --species=mouse

For this mouse brain example, we provide only a coarse broad-region annotation. The labels are for tutorial demonstration only and are not intended as a formal reproduction of the original study annotation.

.. code-block:: text

   sample 0 1 2 3 4 5.........please input anno by order of cluster
   thalamus,hypothalamus,white_matter,piriform_cortex,cortex,cortex,hypothalamus,cortex,hippocampus,white_matter,hippocampus,striatum,hippocampus,hypothalamus

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=manual --annotation-file=annotation.txt

For your own data, replace these example labels with the cell types or tissue regions inferred from your own clustering and marker results.


You have now generated an integrated spatial transcriptomics object. The remaining analysis steps are similar to the single-sample workflow, with a few multi-sample-specific details explained on each step page.

Continue to :doc:`../annotation/cell2location` or :doc:`../annotation/RCTD`
for reference-assisted estimates, :doc:`../subcluster_annotation/index` for
refinement, or :doc:`../downstream_analysis/index` for selected downstream
analyses. Do not restart the core Demo: its earlier stages are already complete.


.. figure:: /_static/images/concatenated_sdata_harmony_sample_UMAP.png
   :width: 85%
   :align: center
   :alt: harmony_sample_UMAP

.. figure:: /_static/images/concatenated_sdata_UMAP.png
   :width: 85%
   :align: center
   :alt: celltype_UMAP
