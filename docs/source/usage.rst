Usage of Spatialsnake
=====================

If you encounter any problems while using Spatialsnake, or if you have suggestions for extending its functionality, please open an issue on GitHub:
https://github.com/l-zh007/spatialsnake/issues

.. _quick_start:

Available Platforms
-------------------

- Sequencing-based:

  1. ``visium``: 10x Genomics spatial transcriptomics data
  2. ``visium HD``: high-resolution 10x Genomics spatial transcriptomics data
  3. ``visium segment``: cell segmentation outputs from 10x Genomics Space Ranger
  4. ``stereo-seq``: BGI Stereo-seq spatial transcriptomics data

- Imaging-based:

  1. ``xenium``: image-based 10x Genomics Xenium spatial transcriptomics data
  2. ``Merfish``: Vizgen MERFISH spatial transcriptomics data

.. note::
   Many excellent spatial transcriptomics platforms are currently available. Spatialsnake focuses on six widely used platforms chosen based on technical categories and practical relevance.
   For platforms not listed here, the official SpatialData documentation provides multiple interfaces for loading data into ``zarr`` format, after which you can continue the analysis with Spatialsnake.

Basic Analysis Pipeline
-----------------------
We simplify the full analysis into several modules. Each stage has its own parameters and recommended settings, covering the complete workflow from raw data to biological interpretation.

1. ``Ingesting``: read raw spatial transcriptomics data and standardize it into a unified object
2. ``preprocess``: quality control, filtering, normalization, and dimensionality reduction preparation
3. ``clustering``: clustering and visualization
4. ``annotation_help``: automatic marker and enrichment guidance
5. ``annotation``: manual or algorithm-based annotation
6. ``reclustering``: secondary subclustering of clusters of interest
7. ``advance_analysis``: advanced downstream analyses such as cell communication and regulatory network inference
8. ``compare_stage``: differential and communication comparison across samples

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
Linux

- Memory: 16 GB or more is recommended
- Disk space: 100 GB or more is recommended, depending on dataset size and analysis scope
- CPU: multi-core processor
- GPU: optional, for accelerating selected analyses


How to use the command line to run Spatialsnake
-----------------------------------------------


.. include:: project_layout.rst
   :start-line: 6
