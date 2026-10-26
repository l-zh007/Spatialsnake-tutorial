Spatialsnake: spatial transcriptomics analysis
==============================================

.. image:: /_static/images/spatialsnake-logo.png
   :width: 68%
   :align: center
   :alt: Spatialsnake logo
   :class: ss-home-logo

What is Spatialsnake?
---------------------

Spatialsnake is a command-line tool for analysing processed spatial
transcriptomics data. It starts from platform-specific processed outputs and uses SpatialData
to retain expression measurements, available spatial elements, and sample metadata
across analysis stages. Snakemake manages dependencies between stages, while
CLI options and YAML configuration files specify analysis settings.

What can Spatialsnake do?
-------------------------

Spatialsnake supports data ingestion, QC, preprocessing, clustering, annotation,
focused analysis, and selected downstream methods for individual samples and
assembled multi-sample datasets. Researchers can inspect intermediate results and revise
parameters or annotations before continuing.

What is distinctive about Spatialsnake?
---------------------------------------

- **A shared workflow across platforms and resolutions:** dedicated readers
  convert processed sequencing- and imaging-based inputs into SpatialData
  objects stored in Zarr, reducing repeated format conversion between analysis stages.
- **Analysis guided by intermediate results:** QC plots, PC diagnostics, marker
  expression, and enrichment results support dataset-specific filtering,
  clustering, and annotation decisions.
- **Reusable analysis stages:** saved intermediate objects and Snakemake
  dependencies support selected reruns and transitions between whole-tissue,
  sample-specific, and population-specific analyses.
- **Integrated research workflow:** cell or region selection, subcluster
  refinement, and downstream reuse form a continuous workflow. Supported format
  conversions connect these results to AnnData- and Seurat-based analyses.

Where to start
--------------

Read :doc:`usage` for command syntax and working-directory conventions, then
choose your :doc:`data_input/index` platform. Follow :doc:`core_analysis/index`
for a single-sample walkthrough or :doc:`integration_analysis/index` for
multi-sample data assembly. After annotation, continue with focused analysis,
further analyses or optional data operations as needed.

For analysis shortcuts and troubleshooting, see :ref:`practical-tips` and
:ref:`common-errors`.

.. note::

   The main examples use the 10x Genomics colorectal cancer P2 dataset (CRC P2)
   and five mouse-brain Visium samples from
   `E-MTAB-11114 <https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-11114>`_.
   For your own data, replace sample-table entries and choose suitable
   parameters; retain the platform-specific input and coordinate requirements.


Tutorial contents
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
