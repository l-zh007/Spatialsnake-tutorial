Spatialsnake Pipeline for Spatial Transcriptomics
=============================================

Spatialsnake is an automated analysis pipeline for ``spatial transcriptomics``.

Implemented in ``Python`` on top of the ``scverse`` ecosystem, Spatialsnake uses SpatialData to convert spatial transcriptomics datasets from different platforms into a unified zarr-based object format.
This design provides a consistent computational framework from data ingestion through preprocessing, clustering, annotation, and downstream analysis, while preserving compatibility with platform-specific inputs.
By combining a command-line interface with workflow-based parameter control, Spatialsnake emphasizes reproducibility, operational clarity, and ease of adoption, allowing users to perform end-to-end spatial transcriptomics analysis without extensive custom scripting or repeated environment reconstruction.

.. note::

   This tutorial assumes basic familiarity with the Linux command line.
   All example commands can be used directly after adapting paths and sample names to your own project.
   Our goal is to provide a practical, reproducible entry point for users with different levels of computational experience who want to perform spatial transcriptomics analysis within the scverse ecosystem.

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
   integration_analysis/multi_sample_integration

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
