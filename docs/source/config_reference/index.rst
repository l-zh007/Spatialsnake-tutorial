Configuration reference
=======================

.. _practical-tips:

Practical tips
--------------

Use these tips to adjust parameters, combine analyses, and reuse existing results.

Scenario 1: choose the analysis channel from the experimental design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For core analysis, ``single_analysis`` processes samples independently;
``compare_analysis`` integrates them. See :doc:`../usage` for sample tables and
:doc:`../integration_analysis/multi_sample_integration` for the cohort example.
Check downstream input rules: several modules accept one object per invocation.


Scenario 2: make parameter changes explicit and inspect the workflow first
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the :ref:`configuration rules <cli-configuration>` when editing several
settings. Inspect the selected stage with a dry run before executing:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --min_counts=100 -d


Scenario 3: treat quality control, clustering, and annotation as an iterative process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use QC plots to choose filtering thresholds, and markers plus spatial patterns
to assess clustering resolution. Preview parameter changes before running:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=clustering --resolution=0.7 -d
   spatialsnake single_analysis sample.txt visium_HD --option=clustering --resolution=0.7

For CRC P2, retain the other :doc:`../core_analysis/clustering` settings.
After changing QC or clustering, rerun affected stages in order:
clustering → annotation_help → annotation. Update the annotation mapping if
clusters change. Back up results before overwriting; ``-r`` deletes outputs
and is not needed for normal parameter tuning.


Scenario 4: preserve counts and sample metadata for statistical comparisons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Retain raw counts and biological sample IDs for pseudobulk ``compare_gene``.
``compare_sample_col`` must match ``sample_id`` in the sample table. Two-group
comparisons test the second group against the first; for more groups, specify
``compare_contrasts``. Select a relevant ``cell_focus`` to reduce computation.
The same-condition E-MTAB-11114 mouse-brain demo demonstrates usage, not a biological contrast.

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage \
     --runpipe=compare_gene --cell_focus=all --compare_algorithm=DESeq2


Scenario 5: reduce computational load without discarding the biological design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add ``--sketch=True --sample_rate=0.1`` to preprocessing and ``--sketch=True``
  to clustering. Labels are mapped to the full table; check rare populations.
  Initial preprocessing still loads the full object.
- Use ``banksy_max_features`` to select fewer features for BANKSY.
- For pySCENIC or focused analysis, select a relevant cell class or region and
  retain the parent object for label overlay.


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

This preserves ``celltype`` and writes refined labels to ``sub_celltype``.
Use the merged object with ``--celltype_col=sub_celltype`` for downstream modules
that accept this option. See the CRC :doc:`../subcluster_annotation/reclustering`,
:doc:`../subcluster_annotation/reannotation`, and :doc:`../useful_tool/merge` examples.


Scenario 7: select the appropriate spatial-subsetting behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``subset_mode=table`` retains spatial elements for reclustering/reannotation.
- ``subset_mode=spatial`` also filters linked Shapes/Points, but retains images.
- Use ``split_by=image`` to crop images, or ``split_by=ROI`` with an exported ROI CSV.
- For integrated data, select the correct region or coordinate system.
  See :doc:`../useful_tool/splitting` for platform-specific inputs.

In the CRC :ref:`tumor–myeloid distance example <splitting-celltype-distance>`,
the output includes both tumor targets and myeloid neighbors. To recluster
only the neighboring myeloid bins, first select their recorded role:

.. code-block:: bash

   spatialsnake useful_tool --option=splitting \
     results/useful_results/data_splitting/celltype_Tumor_to_Myeloid_Cells_distance_0_50um.zarr \
     --split_by=selection_role --barcodes=neighbor

Use the subset for reclustering, or retain both populations for communication
analysis. Proximity alone does not demonstrate signaling.


Scenario 8: distinguish sample concatenation from annotation overlay
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``merge_by=sample`` for independent slides, such as separate RCTD outputs;
use ``merge_by=annotation`` to return subset labels to a parent object.
Concatenation does not perform joint clustering: harmonize biological labels
before comparing independently analyzed samples.


Scenario 9: reuse annotated objects in downstream and external analyses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Point a new sample table to the selected Zarr/H5AD output. Choose modules
according to the question:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Analysis question
     - Suggested sequence
   * - Refine CRC tumor identities
     - Annotation → splitting → reclustering → reannotation → annotation overlay;
       use the refined column in a subsequent communication analysis.
   * - Study tumor-adjacent immune populations
     - Distance splitting → myeloid-only reclustering, or retain tumor and
       immune bins together for LIANA/CellPhoneDB.
   * - Relate tissue domains to communication
     - BANKSY or CellCharter → use its output object in CellPhoneDB with
       ``niche_col=spatial_cluster``. This restricts co-occurring cell-type
       pairs; it is not a spot-distance model.
   * - Inspect vascular regulatory programs
     - Annotated CRC → select Endothelial_Cells and Smooth_Muscle_Cells → pySCENIC,
       as in :doc:`../downstream_analysis/step3_pysenic`.

Use the preceding output, not the original object; check species, annotation
column, and spatial requirements on the module page.

Use ``transform`` when another package requires AnnData H5AD or Seurat RDS:

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotation/S1.zarr \
     --transform_from=zarr --transform_to=h5ad

   spatialsnake useful_tool --option=transform results/S1/annotation/S1.zarr \
     --transform_from=zarr --transform_to=seurat --seurat_matrix=auto

Review the transform report: H5AD/Seurat do not preserve every SpatialData element.


Scenario 10: separate single-condition communication from condition comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run ``advance_analysis --runpipe=cellchat`` within a sample; use
``compare_stage --runpipe=cellchat`` to compare two existing CellChat RDS objects.
Network differences are not replicate-level significance tests. Leave pathway
and ligand–receptor selections empty for automatic plots, or use
``cellchat_focus_cells`` to focus the question.

CellPhoneDB separates plotting from inference: after its demo, add
``--cell_pairs='Tumor_I|Tumor_II'`` to focus plots without changing inference
settings. Preview with ``-d``. Do not assume CellChat supports the same shortcut.


Scenario 11: recover safely from interrupted workflows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Read the timestamped file under ``log/`` before changing parameters. Unlock
only after confirming that no workflow is still running in this directory.
For a stale lock left by a terminated process, unlock and rerun:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=clustering --unlock
   spatialsnake single_analysis sample.txt visium --option=clustering

Core stages require the preceding stage's expected output path. To analyze an
existing object directly, use a downstream module or ``useful_tool``.

.. _common-errors:

Common errors and quick fixes
-----------------------------

Check the specific error in ``log/``, not only the final return code.

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - Error or unexpected result
     - What to check
   * - Invalid sample-table header or column count
     - Use the table for the selected platform and module; core, reference,
       and CellChat tables differ. See :ref:`sample-tables`.
   * - Missing input file
     - Check paths from the working directory and complete the required
       preceding stage. Do not move or rename its outputs.
   * - Parameter changes not applied
     - Pass YAML with ``--configfile``; explicit CLI values take precedence.
       Preview with ``-d``. See :ref:`cli-configuration`.
   * - No observations or genes remain after QC
     - Review QC plots and thresholds: ``min_counts`` filters cells/spots,
       whereas ``min_cells`` filters genes.
   * - Missing sketch query or mismatched genes
     - Rerun preprocessing with matching sketch settings; do not mix
       intermediate files from different runs.
   * - Missing annotation column, ``Cluster_*``, or ``Unknown`` labels
     - Select the correct annotated object and ``celltype_col``; update the
       annotation mapping after changing clustering.
   * - Invalid raw counts or no shared genes
     - Retain genuine counts, not rounded normalized values. Match species,
       gene identifiers, and reference annotations for deconvolution.
   * - Communication requires at least two cell types
     - Retain multiple populations or annotate subclusters first. CellChat
       also needs its platform-specific scaling inputs; see
       :doc:`../downstream_analysis/step7_cellchat`.
   * - No valid comparison tasks
     - Check sample IDs, groups, and biological replicates remaining after
       filtering. Spots/cells are not independent sample replicates.
   * - CUDA requested but unavailable
     - Use ``--device=auto`` or ``--device=cpu``; GPU use requires a
       CUDA-enabled PyTorch build and available CUDA.

Automatically reduced PC counts and skipped single-batch correction are not
failures. Communication plots may use automatic selections when custom filters
match nothing; check warnings before interpreting them. For ROI, merging, and
conversion issues, see :doc:`../useful_tool/index`.

Parameter reference
-------------------

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
