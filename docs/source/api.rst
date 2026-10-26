About and citation
==================

Our automated workflow is built on top of Snakemake and follows a layered architecture of ``Python CLI + Snakemake workflow + scverse ecosystem``.
If you want to contribute code or add a new module, we recommend forking the repository and creating a dedicated feature branch.

Contributing and extending modules
----------------------------------

Project homepage and issue tracker:

- `Homepage <https://github.com/l-zh007/spatialsnake>`_
- `Issues <https://github.com/l-zh007/spatialsnake/issues>`_

Or contact us directly at ``2400507123@stu.gdpu.edu.cn``

Architecture overview
---------------------

1. The command-line entry point (``spatialsnake/command_line.py``) parses arguments, loads configuration, and constructs the Snakemake command.
2. The scheduling layer (``spatialsnake/workflow/Snakefile``) selects rule files according to ``option`` and ``runpipe``.
3. The execution layer (``spatialsnake/workflow/rules/*.smk`` + ``spatialsnake/workflow/scripts/*``) performs the actual analysis tasks.
4. The environment and configuration layer (``environment.yml`` + ``requirements.txt`` + ``requirements-extended.txt`` + ``spatialsnake/workflow/envs/*.yaml``) defines the runtime environment and step-specific configuration.

This design decouples parameter management, workflow orchestration, and algorithm implementation, making it easier to extend the project while preserving reproducibility.


How Snakemake is organized
--------------------------

For main analysis commands, the CLI performs the following steps; optional
data operations under ``useful_tool`` call Python functions directly:

1. The Spatialsnake CLI is built on top of docopt. Users specify analysis options and run types via command-line arguments, which are parsed through the entry-point file ``command_line.py``.
2. After parsing, the CLI automatically selects the appropriate scheduling branch according to the specified analysis option and run type, and executes the corresponding Snakemake rules (``Snakefile``).
3. The CLI loads the corresponding template from ``spatialsnake/workflow/envs/`` or a user file supplied with ``--configfile``. The recommended options ``ingestion`` and ``advanced_analysis`` use the legacy template filenames ``integrate.yaml`` and ``advance_analysis.yaml``.
4. Input and output paths for each module are automatically resolved from the parameters defined in the configuration file. If you need to add a new analysis module, consult the path-resolution helper functions in the Snakefile and adapt them accordingly.
5. If you wish to add a new scheduling branch, be sure to also update the parameter configuration logic for the module's input and output paths. For a new platform branch, we recommend reading the data with a standalone Python script and bypassing the integration step initially, to avoid extensive logic refactoring.


Software versions
-----------------

The tables below summarize the **user-facing software stack** of Spatialsnake.
The documentation version displayed in the sidebar is distinct from the installed
software version, which is reported by ``spatialsnake --version``.
The tables list selected workflow and analysis packages; some are optional and are installed only for the corresponding modules. Low-level dependencies are omitted.
The listed versions are reference versions from the documented environment.
Installation routes and dependency updates can produce different versions;
record those actually installed for your analysis. The current Bioconda
completion configuration pins PyDESeq2 to 0.5.4 and Seurat to 5.5.1.

.. list-table:: Core runtime
   :header-rows: 1
   :widths: 34 18 48

   * - Component
     - Version
     - Role in the workflow
   * - Spatialsnake
     - ``spatialsnake --version``
     - Command-line workflow for analysis of processed spatial transcriptomics data
   * - Python
     - 3.12.11
     - Main runtime for the CLI, workflow logic, and Python analysis modules
   * - R
     - 4.4.0 (PyPI/source); 4.4.3 (Bioconda)
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
     - Readers for processed outputs from multiple spatial technologies
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
     - Reference-based cell-type abundance estimation
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
     - 1.1.0
     - Memory-efficient H5AD-to-Seurat conversion used by ``transform``


Citation
--------

If you use Spatialsnake in your study, we recommend citing both the workflow framework and the project repository in the Methods section:

Record the installed Spatialsnake version and the modules used. The project
repository is https://github.com/l-zh007/spatialsnake; cite the underlying
analysis methods as appropriate for your study.
