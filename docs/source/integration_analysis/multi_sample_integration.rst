Spatialsnake for multi-sample integration
=========================================

Before reading this section, make sure you have completed at least one tutorial in :doc:`../data_input/index` so that you already know how to prepare ``sample.txt`` and run Spatialsnake.
This tutorial is intended for studies with multiple spatial transcriptomics datasets from different experimental conditions, such as different tumor types or different normal tissue types.
The integrated object produced here can be used for the same downstream analyses as a single-sample object, although some result files and interpretations differ.

Multi-sample analysis typically combines several datasets. For a concise demonstration, we use multiple Visium mouse brain sections from a public dataset:

https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-11114


Prepare the demo data
---------------------

This tutorial uses five public samples:

- Group 1: ``ST8059048``, ``ST8059049``, ``ST8059050``
- Group 2: ``ST8059051``, ``ST8059052``

Step 1: create a download script in the project root
----------------------------------------------------

First make sure the current working directory contains a ``data/`` folder, then create a script named ``download.sh``.

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

Step 3: prepare ``sample.txt`` with group information
-----------------------------------------------------

For multi-sample integration, ``sample.txt`` is similar to the single-sample version but must also include a group column.

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

   spatialsnake compare_analysis sample.txt visium --option=preprocess --min_genes=100 --min_cells=100

Step 6: continue with the downstream steps
------------------------------------------

After preprocessing, the remaining steps follow the standard ``compare_analysis`` workflow.
The pipeline will generate joint visualizations and result tables across samples.
Because the data are integrated, manual annotation is usually performed on the shared cluster identities across all samples.

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=clustering --resolution=0.8 --pcs=20
   spatialsnake compare_analysis sample.txt visium --option=annotation_help
   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=manual --annotation-file=annotation.txt

For this mouse brain example, we provide only a coarse broad-region annotation. The labels are for tutorial demonstration only and are not intended as a formal reproduction of the original study annotation.

.. code-block:: bash

   sample 0 1 2 3 4 5.........please input anno by order of cluster
   thalamus,cortex,cortex,amygdala,hypothalamus,hypothalamus,striatum,cortex,cortex,white matter,hypothalamus,thalamus,hippocampus,hippocampus,hippocampus,piriform_cortex,cortex,cortex,cortex,cortex,cortex,cortex,cortex,amygdala,thalamus,thalamus


You have now generated an integrated spatial transcriptomics object. The remaining analysis steps are similar to the single-sample workflow, with a few multi-sample-specific details explained on each step page.

Continue to :doc:`../core_analysis/index`.

Example visualizations are discussed in the downstream tutorial pages.
