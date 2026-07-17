Annotation Modules
==================

This section corresponds to different ``anno_algorithm`` branches under ``option=annotation`` and provides several annotation strategies, including manual annotation, reannotation, cell2location, and RCTD.
Please make sure that you have already completed ``preprocess``, ``clustering``, and ``annotation_help``, and that the annotation support files are available.

For a detailed explanation of the shared annotation configuration template, see :doc:`../config_reference/annotation_yaml`.

We recommend choosing the annotation method according to your dataset characteristics and analysis goals.
If you are familiar with the expected cell types and your dataset is relatively small, manual annotation is often sufficient.
If your dataset is larger, or you require a more systematic annotation strategy, cell2location or RCTD may be more appropriate.

In general, cell2location is better suited to lower-resolution spatial transcriptomics data, whereas RCTD is more appropriate for higher-resolution datasets.

If matched single-cell data are available, you can use your own sequencing data as the annotation reference in a multimodal analysis setting.
If you do not have matched single-cell data, you may instead use a suitable public single-cell reference dataset. In that case, verify that the reference is well annotated and biologically appropriate, and provide the correct cell-type annotation column together with the path to the reference object.

.. toctree::
   :maxdepth: 1

   manual
   cell2location
   RCTD
