Using Spatialsnake
==================

This page introduces the Spatialsnake workflow, command-line interface, and
working-directory layout.
The interface is designed to expose common spatial transcriptomics operations
through short commands, while YAML configuration files retain the parameters
needed to reproduce or adapt an analysis.
If you encounter any problems while using Spatialsnake, or if you have suggestions for extending its functionality, please `open an issue on GitHub <https://github.com/l-zh007/spatialsnake/issues>`_.
After reviewing the available modules, follow the working-directory setup in
the command-line section below.

.. _quick_start:

Available Platforms
-------------------

- Sequencing-based:

  - ``visium``: 10x Genomics Visium data
  - ``visium_HD``: 10x Genomics Visium HD data
  - ``visium_segment``: cell-segmented Visium outputs from Space Ranger
  - ``stereoseq``: BGI Stereo-seq tissue-bin, cell-bin, and adjusted cell-bin data

- Imaging-based:

  - ``xenium``: 10x Genomics Xenium data
  - ``Merfish``: Vizgen MERFISH/MERSCOPE data

Basic Analysis Pipeline
-----------------------
Spatialsnake organizes the analysis into modules with explicit inputs, outputs,
parameters, and recommended settings. Users can run the complete workflow or
start from a compatible intermediate object when only selected stages are
required.

- ``ingestion`` (Data ingestion): read platform outputs and standardize them into spatial objects; multi-sample mode also assembles the samples
- ``preprocess``: quality control, filtering, normalization, and dimensionality reduction preparation
- ``clustering``: clustering and visualization
- ``annotation_help``: automatic marker and enrichment guidance
- ``annotation``: manual or algorithm-based annotation
- ``reclustering``: secondary subclustering of clusters of interest 
- ``annotation --anno_algorithm=reannotation``: assign revised labels to refined clusters
- ``advanced_analysis``: selected downstream analyses, including ligand–receptor,
  regulatory-network, spatial-domain, and niche analyses
- ``compare_stage``: differential expression or CellChat comparison between
  experimental conditions

Diverse Analysis Modes
----------------------
To support different experimental designs and analysis goals, Spatialsnake provides multiple workflow modes, including a convenient solution for multi-sample analysis.

- ``single_analysis``: analyze each listed sample independently without creating
  a joint object
- ``compare_analysis``: integrate multiple samples and support analyses that use
  sample and condition information


Useful Tools
------------
Spatial transcriptomics workflows frequently require samples, regions, or cell
classes to be separated for method-specific analysis and subsequently restored
to a complete object. Spatialsnake provides reusable utilities for these data
management operations and for exchanging results with external ecosystems.

- ``splitting``: split objects, suitable for breaking large datasets into smaller subsets, selecting ROIs, or interacting with Xenium Explorer and Loupe Browser
- ``merge``: merge objects, suitable for combining multiple subsets or subcluster annotation results back into a larger dataset
- ``transform``: export Zarr/H5AD to AnnData or Seurat and import H5AD to Zarr;
  Seurat is an output format, not an input to this utility


Hardware recommendations
------------------------

Use Linux. Suggested resources depend on dataset size:

- **Memory:** 32 GB RAM for routine projects; 64–128 GB for larger datasets.
- **CPU:** 8–16 cores recommended.
- **Storage:** at least 100 GB of free SSD space; allow more for larger projects.
- **GPU:** optional for cell2location and CellCharter. ``device=auto`` uses
  available CUDA with a CUDA-enabled PyTorch build, otherwise CPU.


Command-line use
----------------


.. include:: project_layout.rst
   :start-after: .. _usage-body:

Compatibility
-------------

``ingestion`` and ``advanced_analysis`` are the recommended option names.
The legacy names ``integrate`` and ``advance_analysis`` remain supported;
``--runpipe=pysenic`` is an alias for ``--runpipe=pyscenic``.
Both spellings use the same workflow. Configuration filenames remain
``integrate.yaml`` and ``advance_analysis.yaml``; ingestion results remain in
``integrate/``.
