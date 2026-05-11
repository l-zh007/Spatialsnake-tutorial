Contribution/Software Version/Citation
=================================

Our automated workflow is built on top of Snakemake and follows a layered architecture of ``Python CLI + Snakemake workflow + scverce ecosystem``.
If you want to contribute code or add a new module, we recommend forking the repository and creating a dedicated feature branch.

GitHub Contribution and Module Extension
----------------------------------------

Project homepage and issue tracker:

- Homepage: https://github.com/l-zh007/spatialsnake
- Issues: https://github.com/l-zh007/spatialsnake/issues

Architecture Overview
---------------------

1. The command-line entry point (``spatialsnake/command_line.py``) parses arguments, loads configuration, and constructs the Snakemake command.
2. The scheduling layer (``spatialsnake/workflow/Snakefile``) selects rule files according to ``option`` and ``runpipe``.
3. The execution layer (``spatialsnake/workflow/rules/*.smk`` + ``spatialsnake/workflow/scripts/*``) performs the actual analysis tasks.
4. The environment and configuration layer (``environment.yml`` + ``requirements.txt`` + ``requirements-extended.txt`` + ``spatialsnake/workflow/envs/*.yaml``) defines the runtime environment and step-specific configuration.

This design decouples parameter management, workflow orchestration, and algorithm implementation, making it easier to extend the project while preserving reproducibility.


How Snakemake organized
--------------------------

In the current implementation, the command line automatically performs the following core steps:


1. Spatialsnake 命令行是基于docopt进行构建的，用户可以通过命令行参数指定分析选项和运行类型，通过入口文件command_line.py解析。
2. 命令行解析后会根据用户指定的分析选项和运行类型，自动选择对应的调度分支，运行相应的snakemake规则[Snakefile]。
3. 命令行参数会自动加载对应步骤的默认配置文件 ``spatialsnake/workflow/envs/{option}.yaml``，用户也可以通过 ``--configfile`` 参数指定自定义配置文件。
3. 不同的模块的输入输出文件会自动根据配置文件中的参数进行处理，若有新增分析模块需求，可在snakefile中查看相关路径配置函数进行迭代修改。
4. 若您想新增一个调度分支，请注意修改各个模块中输入输出路径的参数配置逻辑。

The main scheduling branches can be summarized as:

- integrate / preprocess / clustering / reclustering / annotation_help / annotation
- advance_analysis (dispatched through ``runpipe`` to ``cellPhoneDB``, ``pysenic``, ``liana``, ``cellcharter``, ``banksy``, or ``cellchat``)
- compare_stage (differential expression comparison and comparative CellChat analysis)



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
