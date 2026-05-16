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
4. 若您想新增一个调度分支，请注意增加修改模块中输入输出路径的参数配置逻辑.若为新平台分支,我们建议手动使用python脚本进行读取跳过integrate步骤,以避免大量逻辑重构.


Software Version
----------------

The table below summarizes the **user-facing core software stack** of Spatialsnake.
Only major workflow and analysis modules relevant to spatial transcriptomics are shown here; low-level dependency packages are intentionally omitted.
Versions were consolidated from the installation tutorial, dependency definition files, and the validated ``spatialsnake_env`` runtime environment.

.. list-table:: Core runtime
   :header-rows: 1
   :widths: 34 18 48

   * - Component
     - Version
     - Role in the workflow
   * - Spatialsnake
     - 0.2.5
     - Command-line workflow framework for end-to-end spatial transcriptomics analysis
   * - Python
     - 3.12.11
     - Main runtime for the CLI, workflow logic, and Python analysis modules
   * - R
     - 4.4.0
     - Runtime for R-based downstream statistics, visualization, and communication analysis
   * - Snakemake
     - 9.8.1
     - Workflow scheduler and reproducibility engine

.. list-table:: Core Python analysis modules
   :header-rows: 1
   :widths: 30 18 52

   * - Package
     - Version
     - Main use in Spatialsnake
   * - spatialdata
     - 0.5.0
     - Unified object model for multi-platform spatial transcriptomics data
   * - spatialdata-io
     - 0.3.0
     - Import and export support for multiple spatial technologies
   * - spatialdata-plot
     - 0.2.11
     - Spatial visualization backend
   * - scanpy
     - 1.10.4
     - Core preprocessing, clustering, embedding, and marker analysis
   * - anndata
     - 0.12.0
     - Matrix and metadata container for single-cell and spatial analysis
   * - squidpy
     - 1.6.5
     - Spatial neighborhood, graph, and image-aware analysis
   * - cell2location
     - 0.1.5
     - Reference-assisted spatial cell type annotation
   * - scvi-tools
     - 1.4.0
     - Probabilistic deep-learning framework supporting annotation and latent modeling
   * - pydeseq2
     - 0.5.2
     - Differential expression analysis in Python-based comparison steps

.. list-table:: Optional Python downstream modules
   :header-rows: 1
   :widths: 30 18 52

   * - Package
     - Version
     - Main use in Spatialsnake
   * - cellphonedb
     - 5.0.1
     - Ligand-receptor communication analysis
   * - cellcharter
     - 0.3.5
     - Spatial clustering and niche organization analysis
   * - liana
     - 1.6.1
     - Consensus ligand-receptor inference framework
   * - pyscenic
     - 0.12.1
     - Gene regulatory network inference
   * - torch
     - 2.8.0
     - Deep-learning backend required by several probabilistic models

.. list-table:: Core R analysis modules
   :header-rows: 1
   :widths: 30 18 52

   * - Package
     - Version
     - Main use in Spatialsnake
   * - Seurat
     - 5.5.0
     - Spatial object handling, coordinate extraction, and downstream R analysis support
   * - CellChat
     - 2.2.0.9001
     - Spatially informed cell-cell communication analysis
   * - clusterProfiler
     - 4.14.0
     - Functional enrichment analysis
   * - edgeR
     - 4.4.0
     - Count-based differential analysis support
   * - ComplexHeatmap
     - 2.22.0
     - Publication-grade heatmap visualization
   * - AnnotationDbi
     - 1.68.0
     - Gene identifier mapping and annotation support
   * - org.Hs.eg.db
     - 3.20.0
     - Human gene annotation database for enrichment workflows
   * - org.Mm.eg.db
     - 3.20.0
     - Mouse gene annotation database for enrichment workflows
   * - circlize
     - 0.4.15
     - Circular visualization support for advanced downstream plots
   * - schard
     - 1.0.0
     - transform from zarr to Seurat



Citation
--------

If you use Spatialsnake in your study, we recommend citing both the workflow framework and the project repository in the Methods section:

1. paper:
2. Spatialsnake project repository: https://github.com/l-zh007/spatialsnake
