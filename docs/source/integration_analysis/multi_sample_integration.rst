Spatialsnake for multi-sample integration
=========================================

Before reading this section, make sure you have completed at least one tutorial in :doc:`../data_input/index` so that you already know how to prepare ``sample.txt`` and run Spatialsnake.
This tutorial is intended for studies with multiple spatial transcriptomics datasets from different experimental conditions, such as different tumor types or different normal tissue types.
The integrated object produced here can be used for the same downstream analyses as a single-sample object, although some result files and interpretations differ.


Multi-sample Integration Workflow
---------------------------------

This page provides a basic multi-sample integration tutorial. For detailed ``core_analysis`` guidance, please refer to the corresponding tutorial pages. This section applies to data from all supported platforms. Please ensure you have already read the ingestion tutorial for your target platform and have a basic understanding of the ingestion step; this tutorial will not repeat that content.

Step 1: Data download and storage paths
   The Spatialsnake multi-sample ingestion step supports integrating samples from two different experimental conditions. The data path and ``sample_id`` for each sample must match the corresponding entries in ``sample.txt``.
   Multiple biological replicates are supported within each group.
   Regardless of the platform, the correct directory layout is:


.. code-block:: text

   # Sample IDs can be customized and are independent of group assignment
   project_root/
   ├── data/
   │   ├── Normal_1/
   │   ├── Normal_2/
   │   ├── Normal_3/
   │   ├── cancer_1/
   │   ├── cancer_2/
   │   └── cancer_3/
   ├── sample.txt
   └── results/

Step 2: Configure ``sample.txt``
   Similarly, we use the sample file table to record the sample ID, input directory, and group information.


.. code-block:: bash

   sample_id   input_path         group
   Normal_1   data/Normal_1     Group1
   Normal_2   data/Normal_2     Group1
   Normal_3   data/Normal_3     Group1
   cancer_1   data/cancer_1     Group2
   cancer_2   data/cancer_2     Group2
   cancer_3   data/cancer_3     Group2


Step 3: Run the command
   Unlike ``single_analysis``, multi-sample analysis requires multiple sample directories and a ``sample.txt`` with corresponding entries, and some command parameters differ.

For example, the ``compare_analysis`` integration command for Visium:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=integrate

Summary:

This concludes the basic overview of multi-sample integration in Spatialsnake. For specific analysis steps, ``compare_analysis`` supports different parameter configurations, such as ``batch_method``, to accommodate various experimental analysis needs.
The most important takeaway is: once ``sample.txt`` is correctly configured, run the ``compare_analysis`` command with the appropriate platform type, and you can proceed with multi-sample integration just as smoothly as with the single-sample workflow.

Below, we provide a detailed demonstration using Visium platform data. If you have already completed this step with your own data, you may skip this demo and proceed directly to the ``core_analysis`` and ``preprocess`` steps.

.. important::
   The demo dataset used in this section will also be used in subsequent analyses; please use it as appropriate.


Demo Walkthrough
----------------

Multi-sample analysis typically combines several datasets. For a concise demonstration, we use multiple Visium mouse brain sections from a public dataset:

`E-MTAB-11114 (ArrayExpress) <https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-11114>`_

We use the demo data for a minimal ``core_analysis`` walkthrough that covers data ingestion, preprocessing, and annotation. This tutorial helps you intuitively understand the key differences between multi-sample and single-sample analyses. For detailed module functionality, parameter settings, and implementation of analysis features, please read the introductory tutorial at the beginning of each module. You can also use our Visium HD example dataset for a more comprehensive hands-on learning experience.

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
           └── concatenated_sdata
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
Because the data are integrated, manual annotation is usually performed on the shared cluster identities across all samples.

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=clustering --resolution=0.5 --pcs=15
   spatialsnake compare_analysis sample.txt visium --option=annotation_help --species=mouse

For this mouse brain example, we provide only a coarse broad-region annotation. The labels are for tutorial demonstration only and are not intended as a formal reproduction of the original study annotation.

.. code-block:: bash

   sample 0 1 2 3 4 5.........please input anno by order of cluster
   thalamus,cortex,cortex,amygdala,hypothalamus,hypothalamus,striatum,cortex,cortex,white matter,hypothalamus,thalamus,hippocampus,hippocampus,hippocampus,piriform_cortex,cortex,cortex,cortex,cortex,cortex,cortex,cortex,amygdala,thalamus,thalamus

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=manual --annotation-file=annotation.txt

For your own data, replace these example labels with the cell types or tissue regions inferred from your own clustering and marker results.


You have now generated an integrated spatial transcriptomics object. The remaining analysis steps are similar to the single-sample workflow, with a few multi-sample-specific details explained on each step page.

Continue to :doc:`../core_analysis/index`.

Example visualizations are discussed in the downstream tutorial pages.
