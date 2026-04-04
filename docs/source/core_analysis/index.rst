Core Analysis Workflow
======================

Following the standard spatial transcriptomics workflow, Spatialsnake organizes the core analysis into four stages:

1. Data integration (``integrate``)
2. Preprocessing (``preprocess``)
3. Clustering (``clustering``)
4. Annotation support (``annotation_help``)

Because the outputs are largely consistent across platforms, this section uses a single-sample Visium HD dataset to demonstrate the full core workflow from start to finish. The final output is a cell annotation result that can be used as input for downstream analysis modules.

If you are working with another spatial transcriptomics platform, or with an already integrated multi-sample dataset, we recommend reading the documentation for each step in full. The individual pages explain the differences in commands and parameters where needed.


.. toctree::
   :maxdepth: 1

   Ingesting
   preprocess
   clustering
   annotation_help
