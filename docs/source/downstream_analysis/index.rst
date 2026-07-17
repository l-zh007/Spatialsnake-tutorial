Downstream Analysis Modules
===========================

After completing the core analysis and annotation steps, the major cell types in the dataset should already be defined. The next step is to choose downstream tools that align with the biological question of interest and support more informative interpretation.
Each downstream module exports method-specific tables and a focused set of figures for interpretation and reproducible review.
The modules share a common command structure, allowing users to select an
analysis method without rebuilding input handling, result directories, or
parameter-management code for each external package.

Commonly used downstream analysis modules for spatial transcriptomics
---------------------------------------------------------------------------

1. Spatial domains and microenvironment analysis: focuses on spatial domain identification, microenvironment structure, and tissue spatial organization.
2. Ligand-receptor analysis: focuses on intercellular communication through ligand-receptor interactions.
3. Regulatory factor analysis: focuses on transcriptional regulators and inferred functional states.
4. Multi-sample comparison: focuses on between-group differences and cross-sample communication changes.

.. note::
   Spatial transcriptomics, and transcriptomics more broadly, continues to evolve rapidly. New analysis tools are introduced and refined on a regular basis, so Spatialsnake focuses on widely adopted modules rather than attempting to cover every available method.
   The workflow therefore emphasizes established methods and explicit intermediate outputs rather than attempting to cover every available tool.

There are two entry points for downstream analysis:

1. ``--option=advance_analysis``: run a selected module with ``--runpipe=`` (``cellPhoneDB``, ``pysenic``, ``liana``, ``cellcharter``, ``banksy``, or ``cellchat``).
2. ``--option=compare_stage``: run between-group comparisons with ``--runpipe=`` for ``compare_gene`` or comparative ``cellchat`` analysis.

.. code-block:: text

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=<module>

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=<module>


Prepare ``sample.txt``
-------------------------

``advance_analysis`` is modular. You can choose the specific module according to your research question, so the corresponding ``sample.txt`` file only needs to include the sample information and input path required for that module.
For illustration, we use the output of ``reannotation`` and run selected downstream analyses on the annotated tumor subclusters. If you are using your own dataset, replace the example paths with your own files.

.. code-block:: text

   sample_id data_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/reannotation/Colon_Cancer_P2_008um.zarr

.. important::
   ``sample_id`` specifies the output directory for your results files. For example, if the sample ID is ``Colon_Cancer_P2_008um``, the results will typically be placed under ``results/Colon_Cancer_P2_008um/<module>/``. If the directory does not already exist under ``results/``, it will be created automatically. You may customize the naming according to your own convention.


Configuration details follow the same pattern as in the previous sections:

- For ``advance_analysis``, see :doc:`../config_reference/advance_analysis_yaml`
- For ``compare_stage``, see :doc:`../config_reference/compare_stage_yaml`


The following pages describe the intended scope, inputs, parameters, and outputs of each available module.


Select downstream analysis modules
----------------------------------------

Spatial domains and microenvironments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   step5_cellcharter
   step6_banksy


Ligand-receptor analysis
~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   step2_cellphonedb
   step4_liana
   step7_cellchat


Regulatory factor analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   step3_pysenic


Multi-sample comparison
~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   step8_compare_stage_deg
   step9_compare_stage_cellchat
