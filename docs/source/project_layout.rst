Using Spatialsnake
================================================

How the command line works
--------------------------------------------------------------

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
------------------------------------------------------------

- ``<command>``: main workflow channel. Choose ``single_analysis`` or ``compare_analysis`` according to your analysis design.
- ``<INPUT>``: input sample file. In the main workflow, this is usually ``sample.txt``, which stores sample IDs and data paths. In ``useful_tool``, it refers to one or more object paths.
- ``<TYPE>``: data type. Supported values are ``visium``, ``visium_segment``, ``visium_HD``, ``xenium``, ``Merfish``, and ``stereo_seq``.
- ``--option=<analysis_option>``: analysis module selector. Main workflow options include ``integrate``, ``preprocess``, ``clustering``, ``reclustering``, ``annotation_help``, ``annotation``, ``advance_analysis``, and ``compare_stage``. Utility workflow options include ``splitting``, ``merge``, and ``transform``.


Setting command-line parameters (``[options]``)
------------------------------------------------------

Spatial transcriptomics analysis involves many important parameters, and these settings directly affect result quality and reliability. When running Spatialsnake, you should adjust parameters according to your specific dataset and study design.
You can set supported parameters directly on the command line. In addition to the standard command structure, append arguments in the form ``--parameter_name=value``.
To see which parameters are available from the command line, run ``spatialsnake -h``.

Example 1: the following command runs ``preprocess`` on single-sample ``visium`` data in ``sample.txt`` with ``--min_cells=3`` and ``--min_genes=200``:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess --min_cells=3 --min_genes=200 --mt_threshold=50

Example 2: the following command converts the ``zarr`` file in ``results/S1/annotation/S1.zarr`` to ``h5ad`` format and saves the image in the ``results/useful_results`` directory.

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotation/S1.zarr --transform_from=zarr --transform_to=h5ad --save_image=True --output_dir=results/useful_results

The examples above cover basic CLI usage for starting an analysis. Additional CLI usage patterns and parameter combinations will be introduced within the subsequent analysis tutorials.

Using a YAML file for richer parameter configuration (``--configfile``)
-------------------------------------------------------------------------

Since the workflow contains many parameters, only the most important and commonly used ones are exposed directly on the command line. All other settings can be configured through a ``.yaml`` file.

How do you generate a YAML template?

.. code-block:: bash

   spatialsnake produce-file --option=<analysis_option> #analysis_option can be preprocess, advance_analysis, splitting, merge, transform......

These commands generate the corresponding template files, such as ``preprocess.yaml``, which can then be edited as needed.

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

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile=preprocess.yaml
   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile=preprocess.yaml --mt_threshold=60

.. note::
   Parameters provided through ``--configfile`` have lower priority than parameters set directly on the command line.
   For example, in the second command, if ``preprocess.yaml`` also defines ``mt_threshold``, the final value used is ``60`` from the command line.
   For beginners, we recommend starting with direct command-line parameters.


Step 2: Prepare the working directory
--------------------------------------------------------------------------------------------------------

.. code-block:: bash
   # command to create
   mkdir -p project_root/data project_root/results
   touch project_root/sample.txt

.. code-block:: text

   project_root/ (current working directory)
   ├── data/ (stores your raw data)
   ├── sample.txt (key sample description file)
   ├── results/ (stores analysis outputs; generated automatically)
   └── <analysis_option>.yaml (optional configuration file)


Minimal examples of ``sample.txt``
--------------------------------------------------------------------

``sample.txt`` is a space-delimited sample information table. To make the essential inputs and configuration more transparent, Spatialsnake records top-level parameters in this file, including sample ID, input path, grouping information, bin resolution, and other key input files.
This table is a required input for every module in the main workflow. Its contents are interpreted differently depending on the module, so please configure it according to your specific use case.

For example, when running a ``single_analysis`` on Stereo-seq data, configure ``sample.txt`` as follows:

.. code-block:: text

   sample_id input_path bin_size
   Mouse_Brain data/Mouse_Brain cellbin

When running the CellChat module on Visium data under ``downstream_analysis``, configure ``sample.txt`` as follows:

.. code-block:: text

   sample_id   input_path  scale_factor_path
   SampleA_Rep1  results/SampleA_Rep1/annotation/SampleA_Rep1.h5ad  results/SampleA_Rep1/scale_factor.json


About Log files
----------------------------

After each Spatialsnake run, a ``Log/xxx.log`` file is generated in the ``project_root`` directory, recording the commands and parameters used during the analysis.
It also records the underlying Snakemake command that was executed. Log files are timestamped and can be inspected in the ``log/`` directory.


About threads
-----------------------------

Spatialsnake uses ``-j`` (or ``--jobs``) to set the total number of CPU cores available to Snakemake, while ``--threads`` sets the number of cores requested by each rule. The actual number of threads used by a rule will not exceed the total cores supplied with ``-j``. If ``--threads`` is omitted, the recommended default for the selected workflow module is read from its YAML configuration file.

For example, the following command provides 16 cores to the workflow and allows each rule to use up to 8 threads:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess -j 16 --threads=8


.. important::
   If you are new to spatial transcriptomics analysis with Spatialsnake or are not yet familiar with the scverse ecosystem, we recommend starting with the example data to learn the basic workflow: :doc:`core_analysis/index`
   For consistency across the documentation, we use two datasets, Mouse_Brain (Visium multi-sample) and Colon_Cancer (Visium HD single-sample), throughout the tutorial examples. Please refer to the corresponding module page to see which dataset is used in each section. We also provide example data for single-sample ingestion on each platform, although those examples do not proceed through the full downstream workflow.
   If you are already familiar with spatial transcriptomics analysis or wish to analyze your own data, continue to :doc:`data_input/index`.
