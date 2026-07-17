Core Analysis Workflow
======================

Following the standard spatial transcriptomics workflow, Spatialsnake organizes the core analysis into four stages:

1. Data integration (``integrate``)
2. Preprocessing (``preprocess``)
3. Clustering (``clustering``)
4. Annotation support (``annotation_help``)


Following the usual analytical order in spatial transcriptomics, the core workflow is divided into the four stages listed above. Together, these steps transform raw spatial data into clusters supported by marker, enrichment, and spatial evidence for subsequent cell-type or tissue-region annotation.
Because the outputs are largely consistent across platforms, this section uses a single-sample Visium HD dataset to illustrate the workflow from ingestion through annotation support. The resulting object and evidence tables provide the inputs required for the annotation and downstream-analysis modules.

If you are working with another spatial transcriptomics platform, or with an already integrated multi-sample dataset, we recommend reading the documentation for each step in full. The individual pages describe any required differences in commands and parameter settings.


.. toctree::
   :maxdepth: 1

   Ingesting
   preprocess
   clustering
   annotation_help
