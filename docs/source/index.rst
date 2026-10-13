Spatialsnake Pipeline for Spatial Transcriptomics
=================================================

.. image:: /_static/images/spatialsnake-logo.png
   :width: 68%
   :align: center
   :alt: Spatialsnake logo
   :class: ss-home-logo

What is Spatialsnake?
---------------------

Spatialsnake is a command-line application that brings spatial transcriptomics
analysis into a consistent, Snakemake-managed workflow. It helps researchers
reuse data and analysis steps as biological questions change, using concise
commands and optional YAML configuration files.

What can Spatialsnake do?
-------------------------

Spatialsnake supports data ingestion, preprocessing, clustering, cell-type
annotation, subcluster refinement, and downstream analysis for single-sample and
integrated spatial transcriptomics projects.

What is distinctive about Spatialsnake?
---------------------------------------

- **Unified spatial objects:** platform-specific readers organize expression,
  images, spatial elements, and coordinates in SpatialData Zarr objects.
- **Decision-guided analysis:** QC distributions, PC diagnostics, markers, and
  enrichment results support filtering, clustering, and annotation decisions.
- **Reusable analysis stages:** run selected stages for single samples or
  integrated datasets without rebuilding the analysis around each tool.
- **Refinement and reuse:** select spatial neighborhoods or cell populations,
  refine their annotations, and write labels back to the complete parent object.
  Export supported representations to AnnData or Seurat when needed.

Where to start
--------------

Read :doc:`usage` for command syntax and working-directory conventions, then
choose your :doc:`data_input/index` platform. Follow :doc:`core_analysis/index`
for a single-sample walkthrough or :doc:`integration_analysis/index` for
multi-sample analysis. After annotation, choose only the refinement, utility,
or downstream modules needed for your study.

.. note::

   Tutorials use CRC P2 and five mouse-brain samples to demonstrate the common
   workflow. For your own data, replace sample-table entries and choose suitable
   parameters; retain the platform-specific input and coordinate requirements.


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
