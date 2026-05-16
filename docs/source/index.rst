Spatialsnake Pipeline for Spatial Transcriptomics
=================================================

Spatialsnake is an automated analysis pipeline for ``spatial transcriptomics`` analysis.

Implemented in ``Python`` on top of the ``scverse`` ecosystem, Spatialsnake uses SpatialData to convert spatial transcriptomics datasets from different platforms into a unified zarr-based object format.
This design provides a consistent computational framework from data ingestion through preprocessing, clustering, annotation, and downstream analysis, while preserving compatibility with platform-specific inputs.
By combining a command-line interface with workflow-based parameter control, Spatialsnake emphasizes reproducibility, operational clarity, and ease of adoption, allowing users to perform end-to-end spatial transcriptomics analysis without extensive custom scripting or repeated environment reconstruction.

.. note::

   This tutorial assumes that you have basic familiarity with the Linux command line and can run standard commands after replacing paths, parameters, and sample names as needed.
   If you are not yet familiar with the standard workflow of spatial transcriptomics analysis, please read the overview and explanatory notes in each module carefully.
   Spatialsnake aims to lower the technical barrier to bioinformatics analysis through a user-friendly command-line framework, ensuring that scientific exploration is not constrained by computational background.


Tutorial Contents
-----------------

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   environment_setup
   usage

.. toctree::
   :maxdepth: 1
   :caption: Data Ingestion

   data_input/index
   integration_analysis/index

.. toctree::
   :maxdepth: 1
   :caption: Main Analysis

   core_analysis/index
   annotation/index
   subcluster_annotation/index
   downstream_analysis/index
   useful_tool/index

.. toctree::
   :maxdepth: 1
   :caption: Reference

   api
   config_reference/index
