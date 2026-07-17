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

A typical ``single_analysis`` table contains ``sample_id`` and ``input_path``.
For a new project, proceed through ``integrate``, ``preprocess``, ``clustering``,
``annotation_help``, and ``annotation`` in order. Inspect each stage before
starting downstream analysis. Explicit ``--option`` commands are particularly
useful while learning because the input and output of each stage remain clear.

For a standard condition-aware analysis, prepare a whitespace-delimited table
with one row per biological sample:

.. code-block:: text

   sample_id   input_path       group
   Control_1   data/Control_1   Control
   Control_2   data/Control_2   Control
   Treated_1   data/Treated_1   Treated
   Treated_2   data/Treated_2   Treated

The ``sample_id`` should identify the biological replicate, whereas ``group``
should identify the experimental condition. Do not use spots or cells as
replicates. Platform-specific fields, such as Stereo-seq ``input_spec``, should
be configured as described in the corresponding input tutorial.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess
   spatialsnake compare_analysis sample.txt visium --option=preprocess


Scenario 2: make parameter changes explicit and inspect the workflow first
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate a module-specific template before changing several parameters. Store
the edited YAML file with the project so that the effective settings remain
reviewable.

.. code-block:: bash

   spatialsnake produce-file --option=preprocess
   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile=preprocess.yaml -d

The ``-d`` option performs a Snakemake dry run and does not execute the analysis.
An explicitly supplied command-line value overrides the corresponding YAML
value, which is convenient for testing one parameter without creating another
configuration file.


Scenario 3: treat quality control, clustering, and annotation as an iterative process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inspect QC distributions before tightening ``min_counts``, ``min_cells``, or
``mt_threshold``. After clustering, evaluate marker genes and spatial coherence
alongside UMAP separation before selecting a final ``resolution``. Cluster number
alone is not sufficient evidence for a biologically meaningful partition.

If an existing output prevents a revised module from running, ``-r`` invokes
Snakemake ``--delete-all-output`` for the selected workflow. Review the dry-run
plan and preserve any required results before using it:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=clustering --resolution=0.7 -d
   spatialsnake single_analysis sample.txt visium --option=clustering --resolution=0.7 -r
   spatialsnake single_analysis sample.txt visium --option=clustering --resolution=0.7

The second command deletes outputs; the third command performs the revised
analysis. Avoid using ``-r`` as a general-purpose rerun flag.


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
mode and ``sample_rate`` can reduce the number of observations used by supported
steps. For BANKSY, ``banksy_max_features`` limits the genes used to construct
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

Use ``subset_mode=spatial`` only when the output should contain physically
cropped spatial elements. ROI CSV files exported by Loupe Browser or Xenium
Explorer can be passed to ``--split_by=ROI``. Rectangular coordinate cropping is
also available when an approximate tissue region is sufficient. For integrated
objects with repeated instance IDs, specify the region or coordinate system
rather than matching IDs across samples implicitly.


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

Read the timestamped file under ``log/`` before changing parameters. If Snakemake
reports a stale lock after a terminated process, unlock the workflow and then
rerun the original command:

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
