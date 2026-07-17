Spatialsnake Pipeline for Spatial Transcriptomics
=================================================

Spatialsnake is a workflow for reproducible spatial transcriptomics analysis.

Implemented in Python and built on the scverse ecosystem, Spatialsnake uses
SpatialData to represent multiple spatial transcriptomics platforms as unified
Zarr objects. The workflow covers data ingestion, preprocessing, clustering,
annotation, subcluster refinement, and downstream analysis while retaining
platform-specific spatial elements. A command-line interface, Snakemake
orchestration, and module-specific YAML files provide consistent parameter and
output management across independent-sample and integrated analyses.

.. note::

   This tutorial assumes basic familiarity with the Linux command line. Replace
   all example paths, parameters, and sample names with values appropriate for
   your project. If spatial transcriptomics workflows are new to you, read each
   module overview and its input requirements before running the example command.


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
