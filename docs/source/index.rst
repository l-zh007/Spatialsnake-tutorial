Spatialsnake Spatial Transcriptomics Tutorial
=============================================

Spatialsnake is an automated analysis pipeline for spatial transcriptomics.

Built in Python on top of the scverse ecosystem, the workflow uses SpatialData to convert spatial transcriptomics datasets from different platforms into a unified ``zarr``-based object format.
With only simple command-line execution and parameter configuration, you can run a complete and flexible workflow covering data ingestion, preprocessing, clustering, annotation, and downstream analysis.
The design of Spatialsnake emphasizes ease of use and reproducibility, helping you start spatial transcriptomics analysis quickly without writing complex code or rebuilding the analysis environment from scratch.

.. note::

   This tutorial assumes basic familiarity with the Linux command line.
   All example commands can be run directly after replacing the paths and sample names as needed.
   Our goal is to help users of different backgrounds and experience levels get started quickly with spatial transcriptomics analysis in the scverse ecosystem.

Tutorial Contents
-----------------

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   environment_setup
   usage

.. toctree::
   :maxdepth: 1
   :caption: Main Workflow

   data_input/index
   core_analysis/index
   annotation/index
   subcluster_annotation/index
   integration_analysis/multi_sample_integration
   useful_tool/index
   downstream_analysis/index

.. toctree::
   :maxdepth: 1
   :caption: Reference

   api
   config_reference/index
