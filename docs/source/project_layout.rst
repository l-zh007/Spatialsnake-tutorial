How to use Spatialsnake?
=========================

How does the command line work?
-------------------------------
The command-line interface provides several entry points: the main workflow, utility tools, configuration template generation, package installation, help, and version display.
``<>`` indicates required arguments, ``[]`` indicates optional arguments, and ``[options]`` indicates additional parameter settings. Arguments must follow the documented syntax, including prefixes such as ``--`` and ``=`` where required.

.. code-block:: bash

  spatialsnake <command> <INPUT> <TYPE> [--option=<analysis_option>] [options] # main workflow
  spatialsnake useful_tool [--option=<ways>] <INPUT> [options] # utility tools
  spatialsnake produce-file [--option=<analysis_option>] # generate configuration templates
  spatialsnake install-packages # install required R packages
  spatialsnake (-h | --help) # show help
  spatialsnake --version # show version

Separate arguments with spaces
------------------------------

- ``<command>``: main workflow channel. Choose ``single_analysis`` or ``compare_analysis`` according to your analysis strategy.
- ``<INPUT>``: input sample file. In the main workflow, this is usually ``sample.txt``, which stores sample IDs and data paths. In ``useful_tool``, it is one or more object paths.
- ``<TYPE>``: data type. Supported values are ``visium``, ``visium_segment``, ``visium_HD``, ``xenium``, ``Merfish``, and ``slide_seq``.
- ``--option=<analysis_option>``: analysis module selection. Main workflow options include ``integrate``, ``preprocess``, ``clustering``, ``reclustering``, ``annotation_help``, ``annotation``, ``advance_analysis``, and ``compare_stage``. Utility workflow options include ``splitting``, ``merge``, and ``transform``.

Additional parameter settings
-----------------------------

Spatial transcriptomics analysis involves many important parameters, and these settings directly affect result quality and reliability. When running Spatialsnake, you should adjust parameters according to your specific dataset and study design.

1. You can set supported parameters directly on the command line. In addition to the standard command structure, append arguments in the form ``--parameter_name=value``.

(To see which parameters are available from the command line, run ``spatialsnake -h``.)

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess --min_cells=3 --min_genes=200 --mt_threshold=50
   spatialsnake compare_analysis sample.txt visium --option=advance_analysis --runpipe=cellchat --celltype_col=celltype --threads=16
   spatialsnake useful_tool --option=splitting results/merge_data/integrate/concatenated_sdata --split_by=ROI --roi_csv=roi_tables

How to configure a parameter file (``configfile``)
-------------------------------------------------

Since the workflow contains many parameters, only the most important and commonly used ones are exposed directly on the command line. All other settings can be configured through a ``.yaml`` file.

How do you obtain a YAML template?

.. code-block:: bash

   spatialsnake produce-file --option=<analysis_option> #analysis_option can be preprocess, advance_analysis, splitting, merge, transform......

These commands generate the corresponding template files, such as ``preprocess.yaml``, which you can then edit.

Each YAML template includes default values and inline explanations for the parameters. This is intended to help you understand the purpose of each setting and become familiar with the analysis workflow more quickly.

.. code-block:: yaml

   option: "preprocess"           # analysis stage, consistent with --option
   channel: "compare_analysis"    # analysis mode single sample or multi-sample comparison
   run_type: "visium"             # spatial transcriptomics platform type
   sample_list: "sample.txt"      # path to the sample description file
   results_folder: "results"      # root output directory
   min_cells: 50                  # minimum cells per sample; samples below this threshold are filtered
   min_genes: 50                  # minimum genes per sample; samples below this threshold are filtered
   mt_threshold: 30.0             # mitochondrial gene threshold; cells above this proportion are filtered
   batch_method: "harmony"        # batch correction method, choose from harmony or combat

Apply the YAML file with ``--configfile``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile=preprocess.yaml
   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile=preprocess.yaml --mt_threshold=60

.. note::
   Parameters provided through ``--configfile`` have lower priority than parameters set directly on the command line.
   For example, in the second command, if ``preprocess.yaml`` also defines ``mt_threshold``, the final value used is ``60`` from the command line.
   For beginners, we recommend starting with direct command-line parameters.


Prepare the working directory first
----------------------------------

.. code-block:: text

   project_root/ (current working directory)
   ├── data/ (stores your raw data)
   │   ├── sampleA/ (sample data)
   │   └── sampleB/
   ├── sample.txt (key sample description file)
   ├── results/ (stores analysis outputs; generated automatically)
   └── <analysis_option>.yaml (optional configuration file)

Minimal examples of ``sample.txt``
----------------------------------

Single-sample analysis (non-``visium_HD``):

.. code-block:: text

   sample_id    data_path
   sampleA           /project_root/data/sampleA

Multi-sample comparison (non-``visium_HD``):

.. code-block:: text

   sample_id    data_path                      group
   sampleA           /project_root/data/sampleA      Control
   sampleB           /project_root/data/sampleB      Treat

``visium_HD`` example:

.. code-block:: text

   sample_id    data_path                      bin    group
   HD1          /project_root/data/HD_sample1   8     A
   HD2          /project_root/data/HD_sample2   8     B

Analysis Pipeline
-----------------
Basic spatial transcriptomics workflow

.. code-block:: text

   integrate -> preprocess -> clustering -> annotation_help -> annotation -> advance_analysis -> compare_stage
                                                                      -> reclustering -> reannotation
``--option``
------------

.. list-table:: Description of analysis stages
   :header-rows: 1
   :widths: 20 80

   * - option
     - Description
   * - integrate
     - Read raw data from supported platforms and standardize it into a unified object
   * - preprocess
     - Perform quality control, filtering, normalization, batch handling, and dimensionality reduction preparation
   * - clustering
     - Perform clustering and generate cluster visualizations
   * - annotation_help
     - Provide marker and enrichment guidance to support manual interpretation
   * - annotation
     - Perform manual or algorithm-based annotation
   * - advance_analysis
     - Run advanced downstream modules such as CellPhoneDB, PySCENIC, and LIANA
   * - compare_stage
     - Run multi-sample differential analysis and CellChat comparison

.. note::

   ``useful_tool`` is not part of the main workflow and can be used at any stage for splitting, merging, or format conversion. See :doc:`useful_tool/index` for details.

Start your analysis
------------------------------------------------------------
We recommend starting with the example dataset provided in :doc:`core_analysis/index` to become familiar with the workflow.
If you want to analyze your own spatial transcriptomics data, continue to :doc:`data_input/index`.
