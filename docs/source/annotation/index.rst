Annotation
==========

This section corresponds to different ``anno_algorithm`` branches under ``option=annotation`` and provides several annotation strategies, including manual annotation, reannotation, cell2location, and RCTD.
Manual annotation follows ``clustering`` and ``annotation_help``. Reference-based
methods require spatial counts and an annotated single-cell reference; existing
spatial labels are useful for regional summaries but are not the inferred
abundances themselves. Each method page gives its exact input requirements.

For a detailed explanation of the shared annotation configuration template, see :doc:`../config_reference/annotation_yaml`.

We recommend choosing the annotation method according to your dataset characteristics and analysis goals.

- Use **manual annotation** to assign cluster labels using marker and spatial
  evidence.
- Use **cell2location** to estimate continuous cell-type abundances from a
  reference, particularly for mixed spatial locations.
- Use **RCTD** for reference-based deconvolution in full mode or dominant
  first/second-type predictions in doublet mode.

Choose according to observation resolution, reference quality, and the required
output, not dataset size alone. Subcluster relabeling is covered in
:doc:`../subcluster_annotation/reannotation`.

If matched single-cell data are available, use an annotated count object as the reference for cell-type composition estimation.
If you do not have matched single-cell data, you may instead use a suitable public single-cell reference dataset. In that case, verify that the reference is well annotated and biologically appropriate, and provide the correct cell-type annotation column together with the path to the reference object.

.. toctree::
   :maxdepth: 1

   manual
   cell2location
   RCTD
