Annotation refinement
=====================

``reannotation`` is the reannotation branch under ``annotation``. It remaps ``celltype`` labels based on existing ``clusters`` or ``recluster`` labels.
Unlike ``manual``, which reads the standard core clustering output, ``reannotation`` reads an explicit subset object. It applies labels to ``recluster`` IDs when available, or to ``clusters`` otherwise, and exports the refined annotations.

For the configuration reference, see :doc:`../config_reference/annotation_yaml`.

Workflow overview
-----------------
1. Read the SpatialData ``.zarr`` object listed in the second column of the subset table.
2. Read the annotation mapping file and parse the relationship from ``cluster`` or ``recluster`` to ``celltype``.
3. Use ``obs['recluster']`` if it exists; otherwise fall back to ``obs['clusters']``.
4. Write the mapped result to ``obs['celltype']`` and assign ``Unknown`` to unmatched labels.
5. Export the reannotated object together with ``celltype_annotations.csv`` for downstream analysis or delivery.

.. note::

   Inspect marker expression and cluster membership after ``clustering`` or
   ``reclustering`` before assigning labels. Reannotation changes labels; it does
   not correct an unsupported clustering result.
   Reuse stable parent IDs and the actual platform TYPE. The same two-column
   subset table works for a selected single-sample or integrated object; do not
   carry core bin/group columns into this table.


Demo: CRC P2 Tumor reannotation
-------------------------------

.. code-block:: text

   samples path_to_dir
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/reclustering/Tumor/Tumor.zarr

The first column retains the parent sample ID. The reannotation subset name is inferred from the input zarr name, so multiple subsets from the same sample can be listed in separate rows and written to separate subdirectories.

The current implementation skips the first line and reads the second line as the mapping definition. The second line is comma-separated, and the order corresponds to cluster or recluster IDs ``0,1,2...``.

.. code-block:: text

   celltype
   Tumor_I,Tumor_II,Tumor_III,Tumor_IV

The demo maps ``0->Tumor_I``, ``1->Tumor_II``, ``2->Tumor_III``,
and ``3->Tumor_IV``. Use the mapping only after checking the
recluster IDs and markers.

.. note::

   Recomputed subclusters can differ in membership, number, or numbering across
   parameters and software environments. Check the actual IDs and markers before
   applying this mapping; a rotated UMAP alone does not require different labels.
   ``03_tutorial_results.zip`` on
   `Zenodo <https://doi.org/10.5281/zenodo.23374838>`__ provides the annotated
   parent at ``results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr``,
   not the completed Tumor reannotation object. To start from that parent,
   follow :doc:`reclustering` and review the new subcluster-to-label mapping.


Run the command
---------------

For the YAML alternative, download
:download:`tumor_reannotation.yaml </config/demo_resources/tumor_reannotation.yaml>`
as ``annotation.yaml``. It explicitly selects reannotation; the unedited
annotation template selects manual annotation instead.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotation --anno_algorithm=reannotation --annotation-file=annotation.txt

or

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotation --anno_algorithm=reannotation --configfile annotation.yaml


Result file structure
---------------------

This example shows Visium HD Tumor reannotation. Before continuing to downstream analysis, first confirm that ``{subset}.zarr`` and ``celltype_annotations.csv`` have been generated.

.. code-block:: text

   results/
   └── {sample}/
       └── reannotation/
           └── {subset}/
               ├── {subset}.zarr/
               ├── celltype_annotations.csv
               ├── celltype_proportion.png
               ├── umap_annotations.png
               └── spatial_annotations.png

The updated ``{subset}.zarr`` contains the revised ``obs['celltype']`` field. ``celltype_annotations.csv`` is the standardized export table used for external review and data sharing.


Interpreting the results
------------------------

In this demo, four recluster IDs are mapped to four Tumor labels. These are
example annotations; use your own marker evidence to name refined populations.
Gray spatial barcodes show the remaining tissue context, not additional cells
assigned to the refined Tumor classes.

The workflow also exports UMAP plots, spatial mapping figures, and cell-proportion plots after reannotation, allowing the revised labels to be evaluated from multiple perspectives.

A cell ID-to-``celltype`` CSV file is also exported to support subsequent visualization and annotation transfer.


.. figure:: /_static/images/umap_recelltype.png
   :width: 85%
   :align: center
   :alt: UMAP colored by refined subcluster annotations

.. figure:: /_static/images/reannotation_spatial_context.png
   :width: 85%
   :align: center
   :alt: Spatial distribution of refined subcluster annotations


.. figure:: /_static/images/recelltype_proportion.png
   :width: 85%
   :align: center
   :alt: Proportions of refined subcluster annotations

If you are building atlas-style annotations, you may need to annotate each subcluster in detail and then merge the results.
Spatialsnake provides optional data operations for this step; see :doc:`../useful_tool/index`.

In the next step, we merge the annotated tumor subcluster labels back into the original larger dataset; see :doc:`../useful_tool/merge`.
