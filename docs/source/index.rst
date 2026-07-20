Spatialsnake Pipeline for Spatial Transcriptomics
=================================================

.. image:: /_static/images/spatialsnake-logo.png
   :width: 68%
   :align: center
   :alt: Spatialsnake logo
   :class: ss-home-logo

What is Spatialsnake?
---------------------

Spatialsnake is a command-line workflow for reproducible spatial transcriptomics
analysis. It is designed to help users with different computational backgrounds
process spatial datasets through concise commands and transparent YAML
configuration files.

What can Spatialsnake do?
-------------------------

Spatialsnake supports data ingestion, preprocessing, clustering, cell-type
annotation, subcluster refinement, and downstream analysis for single-sample and
integrated spatial transcriptomics projects.

What is distinctive about Spatialsnake?
---------------------------------------

Spatialsnake is built on the scverse ecosystem and uses SpatialData Zarr objects
to organize platform-specific expression, image, shape, label, and coordinate
information in a unified data structure. It also provides reusable utilities for
sample or region splitting, annotation overlay, sample merging, and controlled
conversion to AnnData H5AD or Seurat RDS.

Why use Spatialsnake?
---------------------

Spatial transcriptomics projects often require repeated data restructuring as
analytical questions change. Spatialsnake reduces ad hoc file handling while
preserving identifiers, metadata, and spatial relationships across analysis
steps, making routine workflows easier to reproduce and transfer between
projects.

.. note::

   This tutorial assumes basic familiarity with the Linux command line. Replace
   example paths, parameters, and sample names with values appropriate for your
   own project. If spatial transcriptomics workflows are new to you, read the
   module overview and input requirements before running each command.


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
