Downstream Analysis Modules
===========================

After completing the core analysis and annotation steps, you have identified the major cell types in the dataset. The next step is to choose downstream tools according to your biological question so that you can derive more informative conclusions.
For each downstream module, Spatialsnake provides a rich set of visual outputs to help researchers interpret the results more intuitively and reproduce the figures more easily.

空间转录组常用下游分析模块
-------------------------------------

1. Spatial domains and microenvironment analysis: focuses on spatial domain identification, microenvironment structure, and tissue spatial organization.
2. Ligand-receptor analysis: focuses on intercellular communication through ligand-receptor interactions.
3. Regulatory factor analysis: focuses on transcriptional regulators and inferred functional states.
4. Multi-sample comparison: focuses on between-group differences and cross-sample communication changes.

.. note::
   Spatial transcriptomics, and transcriptomics more broadly, continues to evolve rapidly. New analysis tools are introduced and refined on a regular basis, so Spatialsnake currently includes the most commonly used modules rather than every available method.
   Our goal is to provide a simple and practical workflow that helps researchers complete the standard but time-consuming analysis steps efficiently, so they can focus on biological interpretation.
   We continue to expand the workflow as new widely adopted methods emerge.

There are two entry points for downstream analysis:

1. ``--option=advance_analysis``: run a selected module with ``--runpipe=`` (``cellPhoneDB``, ``pysenic``, ``liana``, ``cellcharter``, ``banksy``, or ``cellchat``).
2. ``--option=compare_stage``: run between-group comparisons with ``--runpipe=`` for ``compare_gene`` or comparative ``cellchat`` analysis.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=<module>

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=<module>


Prepare ``sample.txt``
----------------------

``advance_analysis`` is a modular step. You can choose which module to run based on your research question, so the corresponding ``sample.txt`` file only needs to contain sample information and the input file path required by that module.
For a concise demonstration, we use the output of ``reannotation`` and run selected downstream analyses on the annotated tumor subclusters. If you are using your own dataset, simply replace the paths with your own files.

.. code-block:: bash

   sample_id data_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/reannotation/Colon_Cancer_P2_008um.zarr

.. important::
   sample_id 指定了你输出文件的存放文件夹路径,例如 ``Colon_Cancer_P2_008um``.结果一般在results/Colon_Cancer_P2_008um/目录下创建对应模块结果文件夹.
   若results中不存在该文件夹名则会自动创建，您可根据你的存放习惯自定义设置


Configuration details follow the same pattern as in the previous sections:

- For ``advance_analysis``, see :doc:`../config_reference/advance_analysis_yaml`
- For ``compare_stage``, see :doc:`../config_reference/compare_stage_yaml`


每个模块我们都尽量涵盖若干个权威期刊使用频率高的软件包作为分析支持,以满足不同研究需求,对于未列举的软件包,欢迎交流与扩展.


Select downstream analysis modules
----------------------

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
