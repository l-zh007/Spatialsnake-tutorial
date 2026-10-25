Using Spatialsnake
==================

.. _usage-body:

How the command line works
--------------------------

The command-line interface provides several entry points: the main workflow, optional data operations, configuration template generation, package installation, help, and version display.
``<>`` indicates required arguments, ``[]`` indicates optional arguments, and ``[options]`` indicates additional parameter settings. Arguments must follow the documented syntax, including prefixes such as ``--`` and ``=`` where required.

.. code-block:: bash

  spatialsnake <command> <INPUT> <TYPE> [--option=<analysis_option>] [options] # main workflow
  spatialsnake useful_tool [--option=<ways>] <INPUT>... [options] # optional data operations
  spatialsnake produce-file [--option=<analysis_option>] # generate configuration templates
  spatialsnake install-packages # complete dependencies for your installation route
  spatialsnake --help # show help
  spatialsnake --version # show version

Separate arguments with spaces
------------------------------

- ``<command>``: main workflow channel. Choose ``single_analysis`` or ``compare_analysis`` according to your analysis design.
- ``<INPUT>``: input sample file. In the main workflow, this is usually ``sample.txt``, which stores sample IDs and data paths. In ``useful_tool``, it refers to one or more object paths.
- ``<TYPE>``: platform type. Supported values are ``visium``, ``visium_segment``, ``visium_HD``, ``xenium``, ``Merfish``, and ``stereoseq``.
- ``--option=<analysis_option>``: analysis module selector. Main workflow options include ``ingestion``, ``preprocess``, ``clustering``, ``reclustering``, ``annotation_help``, ``annotation``, ``advanced_analysis``, and ``compare_stage``. Utility workflow options include ``splitting``, ``merge``, and ``transform``.


Setting command-line parameters (``[options]``)
-----------------------------------------------

Spatial transcriptomics analysis involves many important parameters, and these settings directly affect result quality and reliability. When running Spatialsnake, you should adjust parameters according to your specific dataset and study design.
You can set supported parameters directly on the command line. In addition to the standard command structure, append arguments in the form ``--parameter_name=value``.
To see which parameters are available from the command line, run ``spatialsnake -h``.

Example 1: the following command runs ``preprocess`` on Visium data with a
minimum of three observations per gene and 200 total counts per observation:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess --min_cells=3 --min_counts=200 --mt_threshold=50

Example 2: the following command converts the ``zarr`` file in ``results/S1/annotation/S1.zarr`` to ``h5ad`` format. The default output is saved under ``results/useful_results/data_transforms``.

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotation/S1.zarr --transform_from=zarr --transform_to=h5ad --save_image=True

These commands illustrate syntax, not a complete demo. Core stages require the
preceding stage's output; each module page identifies its necessary inputs.

.. _cli-configuration:

Using a YAML file for richer parameter configuration (``--configfile``)
-----------------------------------------------------------------------

Since the workflow contains many parameters, only the most important and commonly used ones are exposed directly on the command line. All other settings can be configured through a ``.yaml`` file.

How do you generate a YAML template?

.. code-block:: bash

   spatialsnake produce-file --option=<analysis_option> # for example: preprocess, advanced_analysis, splitting, merge, or transform

These commands copy a template, such as ``preprocess.yaml``, into the current
directory. Edit it before use. Generating a template again overwrites a file
with the same name, including a downloaded demo configuration.

Each YAML template includes default values and inline explanations for the parameters. This is intended to help you understand the purpose of each setting and become familiar with the analysis workflow more quickly.

.. code-block:: yaml

   option: "preprocess"           # analysis stage, consistent with --option
   channel: "compare_analysis"    # analysis mode single sample or multi-sample comparison
   run_type: "visium"             # spatial transcriptomics platform type
   sample_list: "sample.txt"      # path to the sample description file
   results_folder: "results"      # root output directory
   min_cells: 50                  # minimum observations in which a gene must be detected
   min_counts: 50                 # minimum total counts required per observation
   mt_threshold: 30.0             # maximum mitochondrial percentage per observation
   batch_method: "harmony"        # batch correction method for integrated data

Apply the YAML file with ``--configfile``

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile=preprocess.yaml
   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile=preprocess.yaml --mt_threshold=60

.. note::
   Explicit CLI values override the corresponding YAML values. Without
   ``--configfile``, the selected stage's packaged defaults are used.
   For example, in the second command, if ``preprocess.yaml`` also defines ``mt_threshold``, the final value used is ``60`` from the command line.
   Sample-specific QC columns override global filtering values; see
   :doc:`core_analysis/preprocess` before mixing these settings.


Prepare the working directory
-----------------------------

``project_root`` is an example directory name; choose any name and location.
Run the analysis commands from this directory after activating your environment.
Relative paths in commands and sample tables are resolved from the current
working directory, not from the sample table's location.

.. code-block:: bash

   mkdir -p project_root/data project_root/results
   touch project_root/sample.txt
   cd project_root

.. code-block:: text

   project_root/ (current working directory)
   ├── data/ (stores processed platform outputs)
   ├── sample.txt (key sample description file)
   ├── results/ (stores analysis outputs; generated automatically)
   └── <analysis_option>.yaml (optional configuration file)


.. _sample-tables:

Choose the correct sample table
-------------------------------

``sample.txt`` is a whitespace-delimited sample information table. Depending
on the module, it records sample IDs, input paths, group assignments, spatial
resolution settings, or required reference files.
Core stages (``ingestion``, ``preprocess``, ``clustering``, ``annotation_help``,
and manual annotation) reuse the platform-input sample table. Its header and column order
must match the platform and channel:

.. list-table:: Core sample-table headers
   :header-rows: 1
   :widths: 22 36 42

   * - Platform
     - single_analysis
     - compare_analysis
   * - Visium, Segment, Xenium, MERFISH
     - ``sample_id input_path``
     - ``sample_id input_path group``
   * - Visium HD
     - ``sample_id input_path bin_size``
     - ``sample_id input_path group bin_size``
   * - Stereo-seq
     - ``sample_id input_path input_spec``
     - ``sample_id input_path group input_spec``

Use one row per sample; ``group`` denotes the study condition, not the batch
correction key. Platform pages describe platform-output layouts and resolution choices.

For example, when running a ``single_analysis`` on Stereo-seq data, configure ``sample.txt`` as follows:

.. code-block:: text

   sample_id input_path input_spec
   Mouse_Brain data/Mouse_Brain cellbin

Reclustering, reannotation, deconvolution, and downstream modules instead read
explicit result objects. Their table formats differ: deconvolution adds a
reference path, spatial CellChat may require scale information, and comparison
modules use their own sample or condition tables. Follow the target module's
input section rather than adding core ``bin_size`` or ``group`` columns blindly.

For example, a spatial Visium CellChat input is:

.. code-block:: text

   sample_id   input_path  scale_factor_path
   SampleA_Rep1  results/useful_results/data_transforms/SampleA_Rep1.h5ad  data/SampleA_Rep1/spatial/scalefactors_json.json

Keep differently structured tables under distinct names, such as
``samples_core.txt`` and ``samples_cellchat.txt``. Pass the chosen filename as
the positional input. Relative paths resolve from the working directory, not
the table's location. Core stage inputs are resolved from their standard result
directories; do not replace platform input paths with arbitrary Zarr paths.

Log files
---------

After each Spatialsnake run, a timestamped ``log/*.log`` file is generated in
the project root. It records the user command, effective parameters, and the
underlying Snakemake command.


CPU threads
-----------

Spatialsnake uses ``-j`` (or ``--jobs``) to set the total number of CPU cores available to Snakemake, while ``--threads`` sets the number of cores requested by each rule. The actual number of threads used by a rule will not exceed the total cores supplied with ``-j``. If ``--threads`` is omitted, the recommended default for the selected workflow module is read from its YAML configuration file.

For example, the following command provides 16 cores to the workflow and allows each rule to use up to 8 threads:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess -j 16 --threads=8


.. important::
   For a new project, choose :doc:`data_input/index` first. The CRC P2
   :doc:`core_analysis/index` Demo and the E-MTAB-11114 mouse-brain
   :doc:`integration_analysis/multi_sample_integration` Demo show single- and
   multi-sample analysis. After annotation, downstream modules are alternatives,
   not a sequence that must all be run. Keep the actual platform TYPE when
   substituting your data, and review each module's required metadata.
