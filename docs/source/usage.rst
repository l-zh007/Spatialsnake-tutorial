Usage of Spatialsnake
=====================

This page will help you learn the overview workflow and basic usage of Spatialsnake while also preparing the working directory first.
If you encounter any problems while using Spatialsnake, or if you have suggestions for extending its functionality, please `open an issue on GitHub <https://github.com/l-zh007/spatialsnake/issues>`_.
After reviewing the basic Spatialsnake functions and command-line usage described above, make sure you also complete the working-directory setup described in ``Originally Step``.

.. _quick_start:

Available Platforms
-------------------

- Sequencing-based:

- ``visium``: 10x Genomics spatial transcriptomics data
- ``visium HD``: high-resolution 10x Genomics spatial transcriptomics data
- ``visium segment``: cell segmentation outputs from 10x Genomics Space Ranger
- ``stereo-seq``: The BGI Stereo-seq spatial transcriptomics data includes different bin sizes, cellbin, and adjusted cellbin data types.

- Imaging-based:

- ``xenium``: image-based 10x Genomics Xenium spatial transcriptomics data
- ``Merfish``: Vizgen MERFISH spatial transcriptomics data

.. note::
   Many excellent spatial transcriptomics platforms are currently available. Spatialsnake focuses on six widely used platforms chosen based on technical categories and practical relevance.
   For platforms not listed here, the official SpatialData documentation provides multiple interfaces for loading data into ``zarr`` format, after which you can continue the analysis with Spatialsnake.

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
- ``advance_analysis``: advanced downstream analyses such as Ligand-receptor analysis and Regulatory factor analysis and Spatial domains and microenvironments
- ``compare_stage``: differential and communication comparison across samples to identify significant differences

Diverse Analysis Modes
----------------------
To support different experimental designs and analysis goals, Spatialsnake provides multiple workflow modes, including a convenient solution for multi-sample analysis.

- ``single_analysis``: single-sample analysis
- ``compare_analysis``: integrated multi-sample comparison, suitable for spatial transcriptomics datasets generated under the same or different experimental conditions


Useful Tools
------------
To support different experimental scenarios, Spatialsnake also provides several utility tools that make common analysis tasks easier to handle.

- ``splitting``: split objects, suitable for breaking large datasets into smaller subsets, selecting ROIs, or interacting with Xenium Explorer and Loupe Browser
- ``merge``: merge objects, suitable for combining multiple subsets or subcluster annotation results back into a larger dataset
- ``transform``: convert data between formats, such as from ``zarr`` to ``h5ad`` or Seurat-compatible outputs


The hardware requirements for Spatialsnake
------------------------------------------
Linux System

- Memory: 16 GB or more is recommended
- Disk space: 100 GB or more is recommended, depending on dataset size and analysis scope if you are using the downstream_analysis module.
- CPU: multi-core processor
- GPU: optional, for accelerating selected analyses


How to use the command line to run Spatialsnake
-----------------------------------------------


.. include:: project_layout.rst
   :start-line: 6
