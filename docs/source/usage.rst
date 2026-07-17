Using Spatialsnake
==================

This page introduces the Spatialsnake workflow, command-line interface, and
working-directory layout.
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

.. note::
   Spatialsnake provides dedicated ingestion paths for the six platform types
   listed above. For another platform, first convert the data to a compatible
   SpatialData Zarr object and then begin at a module that accepts an existing
   object.

Basic Analysis Pipeline
-----------------------
We simplify the full analysis into several modules. Each stage has its own parameters and recommended settings, covering the complete workflow from raw data to biological interpretation.

- ``Ingesting``: read raw spatial transcriptomics data and standardize it into a unified object
- ``preprocess``: quality control, filtering, normalization, and dimensionality reduction preparation
- ``clustering``: clustering and visualization
- ``annotation_help``: automatic marker and enrichment guidance
- ``annotation``: manual or algorithm-based annotation
- ``reclustering``: secondary subclustering of clusters of interest 
- ``reannotation``: reannotation of clusters of interest
- ``advance_analysis``: selected downstream analyses, including ligand–receptor,
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
To support different experimental scenarios, Spatialsnake also provides several utility tools that make common analysis tasks easier to handle.

- ``splitting``: split objects, suitable for breaking large datasets into smaller subsets, selecting ROIs, or interacting with Xenium Explorer and Loupe Browser
- ``merge``: merge objects, suitable for combining multiple subsets or subcluster annotation results back into a larger dataset
- ``transform``: convert supported data among SpatialData Zarr, AnnData H5AD,
  and Seurat RDS representations


The hardware requirements for Spatialsnake
------------------------------------------
Linux System

- Memory: 16 GB or more is recommended
- Disk space: 100 GB or more is recommended, depending on dataset size and analysis scope if you are using the downstream_analysis module.
- CPU: multi-core processor
- GPU: optional, for accelerating selected analyses


Step 1: Run Spatialsnake from the command line
-----------------------------------------------


.. include:: project_layout.rst
   :start-line: 6
