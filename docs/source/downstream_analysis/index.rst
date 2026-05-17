Downstream Analysis Modules
===========================

After completing the core analysis and annotation steps, the major cell types in the dataset should already be defined. The next step is to choose downstream tools that align with the biological question of interest and support more informative interpretation.
For each downstream module, Spatialsnake provides a rich set of visual outputs to facilitate interpretation and improve figure reproducibility.

Commonly used downstream analysis modules for spatial transcriptomics
---------------------------------------------------------------------------

1. Spatial domains and microenvironment analysis: focuses on spatial domain identification, microenvironment structure, and tissue spatial organization.
2. Ligand-receptor analysis: focuses on intercellular communication through ligand-receptor interactions.
3. Regulatory factor analysis: focuses on transcriptional regulators and inferred functional states.
4. Multi-sample comparison: focuses on between-group differences and cross-sample communication changes.

.. note::
   Spatial transcriptomics, and transcriptomics more broadly, continues to evolve rapidly. New analysis tools are introduced and refined on a regular basis, so Spatialsnake focuses on widely adopted modules rather than attempting to cover every available method.
   Our goal is to provide a practical workflow that helps researchers complete standard but time-consuming analysis steps efficiently, so that more effort can be devoted to biological interpretation.
   We continue to expand the workflow as new widely adopted methods emerge.

There are two entry points for downstream analysis:

1. ``--option=advance_analysis``: run a selected module with ``--runpipe=`` (``cellPhoneDB``, ``pysenic``, ``liana``, ``cellcharter``, ``banksy``, or ``cellchat``).
2. ``--option=compare_stage``: run between-group comparisons with ``--runpipe=`` for ``compare_gene`` or comparative ``cellchat`` analysis.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=<module>

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=<module>


Prepare ``sample.txt``
-------------------------

``advance_analysis`` is modular. You can choose the specific module according to your research question, so the corresponding ``sample.txt`` file only needs to include the sample information and input path required for that module.
For illustration, we use the output of ``reannotation`` and run selected downstream analyses on the annotated tumor subclusters. If you are using your own dataset, replace the example paths with your own files.

.. code-block:: bash

   sample_id data_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/reannotation/Colon_Cancer_P2_008um.zarr

.. important::
   ``sample_id`` specifies the output directory for your results files. For example, if the sample ID is ``Colon_Cancer_P2_008um``, the results will typically be placed under ``results/Colon_Cancer_P2_008um/<module>/``. If the directory does not already exist under ``results/``, it will be created automatically. You may customize the naming according to your own convention.


Configuration details follow the same pattern as in the previous sections:

- For ``advance_analysis``, see :doc:`../config_reference/advance_analysis_yaml`
- For ``compare_stage``, see :doc:`../config_reference/compare_stage_yaml`


For each module, we aim to include software packages that are widely used in the literature in order to support diverse research needs. Contributions and suggestions for additional packages are welcome.


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
