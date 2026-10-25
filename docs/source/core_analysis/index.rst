Core analysis
=============

Following the standard spatial transcriptomics workflow, Spatialsnake organizes the core analysis into four stages:

1. Data ingestion and sample assembly (``ingestion``)
2. Preprocessing (``preprocess``)
3. Clustering (``clustering``)
4. Annotation support (``annotation_help``)


The modular design provides a consistent analytical path across supported
platforms while allowing individual stages to be rerun with revised parameters.
Together, these steps transform platform-processed spatial data into clusters supported by
marker, enrichment, and spatial evidence for subsequent cell-type or
tissue-region annotation.
The workflow uses SpatialData objects across supported platforms while retaining the spatial elements available in each dataset. This section uses the CRC P2 Visium HD dataset at 8-µm bin resolution to illustrate ingestion through annotation support (see :doc:`../data_input/visium_HD` for data preparation). The resulting object and evidence tables provide inputs for :doc:`../annotation/index` and :doc:`../downstream_analysis/index`.

If your platform's ``ingestion`` step is already complete, begin at
:doc:`preprocess`. Keep the actual TYPE and core sample table throughout these
stages. Optional batch correction is performed during preprocessing, separately from sample assembly.
For the multi-sample command differences, see
:doc:`../integration_analysis/multi_sample_integration`.

The core analysis uses fixed random seeds. Embeddings and cluster assignments can still vary across software versions and numerical backends. Review marker expression and tissue context before applying the demo annotation mapping to a new run.

.. toctree::
   :maxdepth: 1

   Ingesting
   preprocess
   clustering
   annotation_help
