Configuration Reference and Practical Tips
==========================================

Practical tips
--------------

The scenarios below summarize common decisions that arise during a spatial
transcriptomics project. They are intended to help new users combine the main
workflow, downstream modules, and utility commands without losing sample
identity or spatial metadata.

Scenario 1: choose the analysis channel from the experimental design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``single_analysis`` when each row of ``sample.txt`` should be processed as
an independent dataset. Use ``compare_analysis`` when samples must be integrated
or compared within one experimental design.

Core table headers and output conventions are summarized in :doc:`../usage`.
Use biological sample IDs, not individual spots/cells, as replicates. For a
cohort walkthrough, see :doc:`../integration_analysis/multi_sample_integration`.


Scenario 2: make parameter changes explicit and inspect the workflow first
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the :ref:`configuration rules <cli-configuration>` when editing several
settings. Inspect the selected stage with a dry run before executing:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --min_counts=100 -d


Scenario 3: treat quality control, clustering, and annotation as an iterative process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inspect QC distributions before tightening ``min_counts``, ``min_cells``, or
``mt_threshold``. After clustering, evaluate marker genes and spatial coherence
alongside UMAP separation before selecting a final ``resolution``. Cluster number
alone is not sufficient evidence for a biologically meaningful partition.

Changing tracked rule parameters normally causes Snakemake to rerun the
selected stage. Check the dry-run plan, then run the revised command:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=clustering --resolution=0.7 -d
   spatialsnake single_analysis sample.txt visium --option=clustering --resolution=0.7

Each core command selects one stage. After changing QC or clustering, rerun the
affected downstream stages (clustering, annotation_help, annotation) in order;
old annotation mappings may no longer match the new clusters. ``-r`` deletes
workflow outputs and is not a normal parameter-tuning option.


Scenario 4: preserve counts and sample metadata for statistical comparisons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before integration, retain stable sample identifiers and raw counts in a
supported count source, such as ``layers["counts"]`` or aligned ``raw.X``.
Batch correction supports joint visualization and clustering, but it does not
create biological replication or replace raw counts in differential analysis.

The ``compare_gene`` branch performs replicate-aware pseudobulk analysis within
each selected cell type. ``compare_sample_col`` must identify biological samples,
and its values must correspond to ``sample_id`` in ``sample.txt``. With two
groups, the default comparison is the second group against the first. With three
or more groups, specify ``compare_contrasts`` explicitly.

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage \
     --runpipe=compare_gene --cell_focus=all --compare_algorithm=DESeq2


Scenario 5: reduce computational load without discarding the biological design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Large Visium HD and imaging-based datasets should remain sparse whenever
possible. Begin with standard QC, then reduce optional computation rather than
removing biological replicates. For exploratory preprocessing, the ``sketch``
mode and ``sample_rate`` reduce the clustering reference size; keep
``sketch=True`` in clustering to restore labels to the full output table. For BANKSY, ``banksy_max_features`` limits the genes used to construct
dense neighborhood matrices while preserving the complete output object.

Subsetting a biologically defined region or cell class is often more
interpretable than arbitrary downsampling. Record the selection rule and retain
the complete parent object so that refined results can later be written back.


Scenario 6: refine several cell classes with splitting, reclustering, and reannotation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``splitting`` after broad annotation to create focused inputs. A comma joins
labels into one object, whereas a pipe creates independent objects. Quote a pipe
expression so that the shell does not interpret it as a pipeline:

.. code-block:: bash

   spatialsnake useful_tool --option=splitting results/S1/annotation/S1.zarr \
     --split_by=celltype --barcodes=Tumor,T_cell

   spatialsnake useful_tool --option=splitting results/S1/annotation/S1.zarr \
     --split_by=celltype --barcodes='Tumor|T_cell'

Place separate subset Zarr objects on separate rows of the reclustering
``sample.txt`` file to process them in parallel. After reclustering and
reannotation, use annotation overlay to return the refined labels to the complete
parent object:

.. code-block:: bash

   spatialsnake useful_tool --option=merge results/S1/annotation/S1.zarr \
     --merge_by=annotation \
     --annotation_csv=results/S1/reannotation/Tumor/celltype_annotations.csv,results/S1/reannotation/T_cell/celltype_annotations.csv \
     --target_col=sub_celltype --fallback_col=celltype

This operation preserves the broad ``celltype`` field and writes refined labels
to ``sub_celltype``. Do not concatenate cell-type subsets with
``merge_by=sample`` because they are not independent samples.


Scenario 7: select the appropriate spatial-subsetting behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default ``subset_mode=table`` filters table observations but retains the
existing images, labels, shapes, points, and coordinate transformations. This
mode is compatible with reclustering and reannotation and avoids breaking
table-to-spatial-element relationships.

Use ``subset_mode=spatial`` when linked Shapes or Points should be filtered;
images are retained. Use ``split_by=image`` for a true rectangular image crop. ROI CSV files exported by Loupe Browser or Xenium
Explorer can be passed to ``--split_by=ROI``. Rectangular coordinate cropping is
also available when an approximate tissue region is sufficient. For integrated
objects with repeated instance IDs, specify the region or coordinate system
rather than matching IDs across samples implicitly. For radius-based local
analysis, use :ref:`splitting-celltype-distance` or :ref:`splitting-roi-distance`:
select from the complete parent, run the chosen analysis on the saved subset,
and use annotation overlay when refined labels should return to the parent.


Scenario 8: distinguish sample concatenation from annotation overlay
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``merge_by=sample`` to concatenate independent samples, for example after
running RCTD separately on multiple slides. Existing observation fields such as
``first_type`` and named ``obsm`` deconvolution weights are retained when their
structures are compatible.

Use ``merge_by=annotation`` when multiple outputs originate from subsets of one
parent object. In this mode, the parent remains the source of expression and
spatial elements, while CSV or subset-Zarr inputs contribute annotation values
only. Keeping these two operations separate prevents duplicated spatial elements
and increasingly long observation identifiers.


Scenario 9: reuse annotated objects in downstream and external analyses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most ``advance_analysis`` modules can be run independently after annotation by
placing the supported Zarr or H5AD object in a new ``sample.txt`` file. Check the
module page before assuming that single-cell and spatial inputs use identical
parameters. Spatial constraints, images, and coordinate requirements differ
among CellPhoneDB, LIANA, CellChat, CellCharter, BANKSY, and pySCENIC.

Use ``transform`` when another package requires AnnData H5AD or Seurat RDS:

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotation/S1.zarr \
     --transform_from=zarr --transform_to=h5ad

   spatialsnake useful_tool --option=transform results/S1/annotation/S1.zarr \
     --transform_from=zarr --transform_to=seurat --seurat_matrix=auto

For Seurat export, ``seurat_matrix=auto`` prefers validated raw counts when
available and otherwise interprets ``X`` according to its values. Review the
transform report because non-Visium platforms may use a generic Seurat fallback,
and not every SpatialData element has an equivalent H5AD or Seurat representation.


Scenario 10: separate single-condition communication from condition comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``advance_analysis --runpipe=cellchat`` to infer and visualize communication
within one sample or one experimental condition. Use
``compare_stage --runpipe=cellchat`` only after producing two condition-level
CellChat RDS objects. The comparison describes differences between the two
inferred networks and is not a replicate-level significance test.

Users who know only the cell-type annotations can leave pathway and
ligand-receptor parameters empty. The workflow selects representative results
automatically. Set ``cellchat_focus_cells`` or an exact cell-pair parameter when
a narrower biological question is already defined.


Scenario 11: recover safely from interrupted workflows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Read the timestamped file under ``log/`` before changing parameters. Unlock
only after confirming that no workflow is still running in this directory.
For a stale lock left by a terminated process, unlock and rerun:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=clustering --unlock
   spatialsnake single_analysis sample.txt visium --option=clustering

Core-analysis modules resolve inputs from the documented output of the preceding
stage. An arbitrary object placed under ``results/`` is therefore not sufficient.
Downstream modules and ``useful_tool`` commands accept explicit object paths, so
they are usually the safer entry points for analyses that begin from an existing
intermediate object.

Parameter reference:

.. toctree::
   :maxdepth: 1

   integrate_yaml
   preprocess_yaml
   clustering_yaml
   annotation_help_yaml
   reclustering_yaml
   annotation_yaml
   advance_analysis_yaml
   compare_stage_yaml
   splitting_yaml
   merge_yaml
   transform_yaml
