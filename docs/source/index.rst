Spatialsnake Pipeline for Spatial Transcriptomics
=================================================

.. raw:: html

   <div class="ss-hero">
     <div class="ss-hero-logo">
       <img src="_static/images/spatialsnake-logo.png" alt="Spatialsnake logo">
     </div>
     <div class="ss-hero-copy">
       <p class="ss-eyebrow">Spatial transcriptomics workflow</p>
       <div class="ss-typewriter" aria-label="Spatialsnake workflow highlights">
         <span>Unified SpatialData-based workflows across spatial platforms</span>
         <span>Decision-guided modules from ingestion to annotation</span>
         <span>Reproducible single-sample and cross-sample analysis</span>
         <span>Reusable tools for splitting, merging, transformation, and comparison</span>
       </div>
     </div>
   </div>

Spatialsnake is a command-line workflow for reproducible spatial transcriptomics
analysis. It helps users with different computational backgrounds process,
annotate, refine, compare, and export spatial datasets through concise commands
and transparent YAML configuration files.

Built on the scverse ecosystem, Spatialsnake uses SpatialData Zarr objects to
organize platform-specific spatial elements in a unified data structure. The
workflow supports data ingestion, preprocessing, clustering, cell-type
annotation, subcluster refinement, and downstream analyses for single-sample and
integrated projects.

Spatial transcriptomics projects often require repeated data restructuring.
Spatialsnake therefore includes reusable utilities for sample or region
splitting, annotation overlay, sample merging, and controlled conversion to
AnnData H5AD or Seurat RDS. These utilities reduce ad hoc file handling while
preserving identifiers, metadata, and spatial relationships across analysis
steps.

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
