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
Choose the object that represents your biological question: a complete tissue,
an annotated cell compartment, or a spatial subset. The Tumor object below is
used by the communication Demos, not by every downstream module.

.. code-block:: text

   sample_id data_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/reannotation/Tumor/Tumor.zarr

.. important::
   ``sample_id`` specifies the output directory for your results files. For example, if the sample ID is ``Colon_Cancer_P2_008um``, the results will typically be placed under ``results/Colon_Cancer_P2_008um/<module>/``. If the directory does not already exist under ``results/``, it will be created automatically. You may customize the naming according to your own convention.


Configuration details follow the same pattern as in the previous sections:

- For ``advance_analysis``, see :doc:`../config_reference/advance_analysis_yaml`
- For ``compare_stage``, see :doc:`../config_reference/compare_stage_yaml`

.. list-table:: Choose inputs before running a module
   :header-rows: 1
   :widths: 22 42 36

   * - Module
     - Required input
     - Demo / execution scope
   * - CellPhoneDB / LIANA
     - Annotated Zarr or H5AD; matching species/gene identifiers
     - CRC Tumor reannotation; one object per invocation
   * - pySCENIC
     - Expression object, TF list, rankings, and motif annotations
     - CRC vascular-associated subset; one object per invocation
   * - CellCharter / BANKSY
     - Spatial coordinates; counts for CellCharter, log-normalized X for BANKSY
     - Complete CRC annotation; use an integrated object for sample-aware analysis
   * - CellChat
     - Annotated H5AD/RDS; spatial scale information when required
     - CRC Tumor export; infer separately for different conditions
   * - compare_gene
     - Annotated merged counts plus biological-sample group table
     - Five-brain functional Demo; requires biological replicates for formal testing
   * - compare CellChat
     - Exactly two completed condition-level CellChat RDS objects
     - Downloaded comparison inputs; first row is the reference

Do not assume that multiple rows trigger independent jobs in every downstream
module: CellPhoneDB, LIANA, pySCENIC, CellCharter, and BANKSY currently select
one input object. Run them separately for independent inputs. For integrated
objects, retain sample identity and follow the module's channel/column settings.
Images, shapes, and points differ by platform; use the actual TYPE and available
spatial layers, not Visium layer names copied without checking.


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
