Contribution and Software Version
=================================

Our automated workflow is built on top of Snakemake and follows a layered architecture of ``Python CLI + Snakemake workflow + rule/script``.
If you want to contribute code or add a new module, we recommend forking the repository and creating a dedicated feature branch.


Architecture Overview
---------------------

1. The command-line entry point (``spatialsnake/command_line.py``) parses arguments, loads configuration, and constructs the Snakemake command.
2. The scheduling layer (``spatialsnake/workflow/Snakefile``) selects rule files according to ``option`` and ``runpipe``.
3. The execution layer (``spatialsnake/workflow/rules/*.smk`` + ``spatialsnake/workflow/scripts/*``) performs the actual analysis tasks.
4. The environment layer (``environment.yml`` + ``requirements.txt`` + ``spatialsnake/workflow/envs/*.yaml``) defines the runtime environment and step-specific configuration.

This design decouples parameter management, workflow orchestration, and algorithm implementation, making it easier to extend the project while preserving reproducibility.


How Snakemake organized
--------------------------

In the current implementation, the command line automatically performs the following core steps:

1. Read the default configuration file ``spatialsnake/workflow/envs/{option}.yaml`` according to ``--option``, unless a custom ``--configfile`` is provided.
2. Pass key parameters such as ``sample_list``, ``channel``, and ``run_type`` to Snakemake through ``--config``.
3. Inside ``workflow/Snakefile``, include the appropriate ``rules/*.smk`` files according to the ``option`` and ``runpipe`` branches.
4. Use ``rule all`` to collect target outputs so that tasks are rerun only when output files are missing or outdated.

The main scheduling branches can be summarized as:

- integrate / preprocess / clustering / reclustering / annotation_help / annotation
- advance_analysis (dispatched through ``runpipe`` to ``cellPhoneDB``, ``pysenic``, ``liana``, ``cellcharter``, ``banksy``, or ``cellchat``)
- compare_stage (differential expression comparison and comparative CellChat analysis)


GitHub Contribution and Module Extension
----------------------------------------

Project homepage and issue tracker:

- Homepage: https://github.com/l-zh007/spatialsnake
- Issues: https://github.com/l-zh007/spatialsnake/issues

Suggested contribution workflow for adding or rewriting modules:

1. Fork the repository and create a feature branch such as ``feature/new_module``.
2. Add or rewrite the analysis script under ``spatialsnake/workflow/scripts/``.
3. Add a new rule file under ``spatialsnake/workflow/rules/`` and declare its inputs, outputs, logs, and shell or Python calls.
4. Register the new ``option`` or ``runpipe`` branch and its expected outputs in ``spatialsnake/workflow/Snakefile``.
5. Add a default YAML parameter template under ``spatialsnake/workflow/envs/`` so the CLI can load it automatically.
6. If the new module changes CLI behavior, update the available options and argument parsing in ``spatialsnake/command_line.py``.
7. Update the tutorial pages and configuration reference, then submit a pull request with a minimal reproducible command example.

At minimum, a pull request should document:

- Input object formats for the module, such as ``.zarr``, ``.h5ad``, or ``.rds``
- Output file list and key fields
- Default parameters and tunable parameter ranges
- Typical commands for single-sample and multi-sample execution


Software Version
----------------

The versions below are taken from the project environment files and dependency definitions.

.. list-table:: Core runtime (from ``environment.yml``)
   :header-rows: 1
   :widths: 36 20 44

   * - Component
     - Version
     - Description
   * - Python
     - 3.12.11
     - Main runtime version
   * - snakemake-minimal
     - 9.8.1
     - Core workflow scheduler
   * - snakemake-interface-common
     - 1.20.2
     - Snakemake interface layer
   * - snakemake-interface-executor-plugins
     - 9.3.8
     - Executor plugin interface
   * - snakemake-interface-storage-plugins
     - 4.2.1
     - Storage plugin interface
   * - pip
     - 25.2
     - Python package manager

.. list-table:: Key Python packages (from ``requirements.txt``)
   :header-rows: 1
   :widths: 36 20 44

   * - Package
     - Version
     - Purpose
   * - spatialdata
     - 0.5.0
     - Unified spatial transcriptomics object format
   * - spatialdata-io
     - 0.3.0
     - Multi-platform read and write support
   * - spatialdata-plot
     - 0.2.11
     - Spatial visualization
   * - scanpy
     - 1.10.4
     - Core toolkit for single-cell and spatial downstream analysis
   * - anndata
     - 0.12.0
     - Matrix and annotation data structure
   * - squidpy
     - 1.6.5
     - Spatial neighborhood and graph analysis
   * - cellphonedb
     - 5.0.1
     - Ligand-receptor communication analysis
   * - cell2location
     - 0.1.5
     - Cell localization-based annotation
   * - scvi-tools
     - 1.4.0
     - Deep generative modeling toolkit
   * - torch
     - 2.8.0
     - Deep learning backend
   * - numpy
     - 2.2.6
     - Numerical computing
   * - pandas
     - 2.2.3
     - Tabular data processing
   * - scipy
     - 1.13.1
     - Scientific computing
   * - scikit-learn
     - 1.7.2
     - Machine learning algorithms
   * - matplotlib
     - 3.9.4
     - Plotting foundation
   * - pydeseq2
     - 0.5.2
     - Differential expression analysis


Citation
--------

If you use Spatialsnake in your study, we recommend citing both the workflow framework and the project repository in the Methods section:

1. paper:
2. Spatialsnake project repository: https://github.com/l-zh007/spatialsnake
