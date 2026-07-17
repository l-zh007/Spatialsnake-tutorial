Reannotation (``reannotation``)
===============================

``reannotation`` is the reannotation branch under ``annotation``. It remaps ``celltype`` labels based on existing ``clusters`` or ``recluster`` labels.
Compared with ``manual``, ``reannotation`` is designed for quickly revising existing labels and exporting the updated annotations in a standardized format, making it well suited to small naming adjustments after clustering has stabilized.

For the configuration reference, see :doc:`../config_reference/annotation_yaml`.

Workflow overview
-----------------
1. Read the downstream object listed in the second column of ``sample.txt`` (``.zarr`` or ``.h5ad``).
2. Read the annotation mapping file and parse the relationship from ``cluster`` or ``recluster`` to ``celltype``.
3. Use ``obs['recluster']`` if it exists; otherwise fall back to ``obs['clusters']``.
4. Write the mapped result to ``obs['celltype']`` and assign ``Unknown`` to unmatched labels.
5. Export the reannotated object together with ``celltype_annotations.csv`` for downstream analysis or delivery.

.. note::

   We recommend completing ``clustering`` or ``reclustering`` and confirming that the cluster structure is stable before running ``reannotation``. If the clustering itself is unreliable, reannotation will only amplify the existing bias.
   Because this module repeats the step of integrating annotation information, we use the example data directly here. For other scenarios, adjust the required parameters as appropriate.


Prepare ``sample.txt`` and the mapping file ``annotation.txt``
--------------------------------------------------------------

.. code-block:: text

   samples path_to_dir
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/reclustering/Tumor/Tumor.zarr

The first column retains the parent sample ID. The reannotation subset name is inferred from the input zarr name, so multiple subsets from the same sample can be listed in separate rows and written to separate subdirectories.

The current implementation skips the first line and reads the second line as the mapping definition. The second line is comma-separated, and the order corresponds to cluster or recluster IDs ``0,1,2...``.

.. code-block:: text

   celltype
   Tumor_I,Tumor_II,Tumor_III,Tumor_IV,Tumor_IV

In this example, the mapping is ``0->Tumor_I``, ``1->Tumor_II``, ``2->Tumor_III``, ``3->Tumor_IV``, and ``4->Tumor_IV``. If more IDs are present, continue listing them on the same line.


Run the command
---------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotation --anno_algorithm=reannotation --annotation-file=annotation.txt

or

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --configfile annotation.yaml


Result file structure
---------------------

This example shows single-sample ``visium`` reannotation. Before continuing to downstream analysis, first confirm that ``{subset}.zarr`` and ``celltype_annotations.csv`` have been generated.

.. code-block:: text

   results/
   └── {sample}/
       └── reannotation/
           └── {subset}/
               ├── {subset}.zarr/
               ├── celltype_annotations.csv
               ├── celltype_proportion.png
               ├── umap_recluster.png
               └── spatial_clusters.png

The updated ``{subset}.zarr`` contains the revised ``obs['celltype']`` field. ``celltype_annotations.csv`` is the standardized export table used for external review and data sharing.



Interpreting the results
------------------------

In this example, the reclustered tumor population is reannotated into four distinct malignant subpopulations based on differences in their marker profiles.

The workflow also exports UMAP plots, spatial mapping figures, and cell-proportion plots after reannotation, allowing the revised labels to be evaluated from multiple perspectives.

A cell ID-to-``celltype`` CSV file is also exported to support subsequent visualization and annotation transfer.


.. figure:: /_static/images/umap_recelltype.png
   :width: 85%
   :align: center
   :alt: UMAP colored by refined subcluster annotations

.. figure:: /_static/images/respatial_clusters.png
   :width: 85%
   :align: center
   :alt: Spatial distribution of refined subcluster annotations


.. figure:: /_static/images/recelltype_proportion.png
   :width: 85%
   :align: center
   :alt: Proportions of refined subcluster annotations

If you are building atlas-style annotations, you may need to annotate each subcluster in detail and then merge the results.
Spatialsnake provides utility modules to make this process easier; see :doc:`../useful_tool/index`.

In the next step, we merge the annotated tumor subcluster labels back into the original larger dataset; see :doc:`../useful_tool/merge`.
