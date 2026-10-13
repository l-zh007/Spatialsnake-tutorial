Manual Annotation (``manual``)
==============================

``manual`` is the manual annotation branch under ``annotation``. It maps ``clusters`` to interpretable ``celltype`` labels and writes the result back to the analysis object.
Unlike ``annotation_help``, which provides evidence for interpretation, ``manual`` does not infer new annotations automatically. Instead, it implements a standardized workflow of "you provide the mapping table, and the pipeline writes the labels back and exports the results."

The main evidence used for manual annotation is the ``marker_genes_pval.csv`` table generated in ``annotation_help``. You can combine that table with the marker dotplot and the literature to evaluate whether canonical marker genes are strongly expressed in the expected clusters.

Workflow overview
-----------------
1. Reuse the core sample table; the workflow reads the completed clustering object from its standard result directory.
2. Read the annotation mapping file and parse the relationship from ``cluster`` to ``celltype``.
3. Map ``obs['clusters']`` to ``obs['celltype']`` and write the result back into the object.
4. Export the UMAP plot, composition plot, spatial overlay plot, and annotation table.
5. Generate the ``annotation``-stage object for downstream comparison or further analysis.

This is a lightweight module designed to integrate annotated cell-type information into the ``zarr`` data object. Please ensure that you have completed clustering and that the ``obs['clusters']`` field has been generated. We use the demo data for this demonstration. For other scenarios, simply adjust the necessary parameters and the ``annotation.txt`` mapping file according to your own experience.

Demo: CRC P2 manual annotation
-------------------------------------------

The current implementation skips the first line and reads the second line as the annotation content. The second line is comma-separated, and the order corresponds to ``cluster 0,1,2...``.
Complete CRC P2 clustering and annotation_help first. Reuse this sample table and save the mapping below as annotation.txt. You may download :download:`crc_annotation.txt </config/demo_resources/crc_annotation.txt>` and rename it to annotation.txt.

.. code-block:: text

   sample_id input_path bin_size
   Colon_Cancer_P2 data/Colon_Cancer_P2 8

.. code-block:: text

   sample 0 1 2 3 4 5.........please input anno by order of cluster
   Endothelial_Cells,Smooth_Muscle_Cells,Myeloid_Cells,Unknown,NK_T_Cells,Fibroblasts,Tumor,Tumor,Tumor,Tumor,B_Cells,Fibroblasts,Intestinal_Epithelial_Cells,Tumor

The mapping is specific to this Demo's clusters. For your own data, assign
labels from the actual marker and spatial results. If cluster numbering differs,
rebuild the correspondence rather than extending or truncating this label list.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotation --anno_algorithm=manual --annotation-file=annotation.txt


Result file structure
---------------------

This example shows single-sample manual annotation for ``visium_HD``. Before interpreting the results, first confirm that ``{sample}.zarr`` and ``*_cell_clusters.csv`` have been generated, then check whether the figures support your annotation decisions.

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── annotation/
           ├── Colon_Cancer_P2.zarr/
           ├── celltype_proportion.png
           ├── Colon_Cancer_P2_UMAP.png
           ├── Colon_Cancer_P2_gene_enrich.png
           ├── Colon_Cancer_P2_hires_image_Clusters.png
           ├── Colon_Cancer_P2_cell_clusters.csv
           └── ...

``Colon_Cancer_P2.zarr`` is the main object reused in downstream analysis. ``Colon_Cancer_P2_cell_clusters.csv`` is the exported label table used for external review or other downstream tools.
The current exporter uses ``*_cell_clusters.csv`` for all platforms.


.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Scenario
     - Recommended command
   * - Single sample (Visium HD, shown in this tutorial)
     - ``spatialsnake single_analysis sample.txt visium_HD --option=annotation --anno_algorithm=manual --annotation-file=annotation.txt``
   * - Single sample (Visium example; retain your own platform TYPE)
     - ``spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=manual --annotation-file=annotation.txt``
   * - Manual annotation of an integrated multi-sample object
     - ``spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=manual --annotation-file=annotation.txt``

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - Parameter category
     - Recommendation for single-sample analysis
     - Recommendation for multi-sample or cross-condition analysis
   * - Annotation mapping file (``annotation_list`` / ``--annotation-file``)
     - Fill it completely in cluster order and cover the major populations first
     - Start with a unified naming system on the integrated object, then refine sample-specific differences
   * - ``image_type`` / ``shape_type``
     - Start with the default layers to generate figures quickly
     - Keep the same layer types across all samples to reduce visualization bias
   * - ``image_slice`` + coordinates
     - Usually keep it disabled and inspect the full tissue first
     - Enable it only when reviewing a target region and record the crop coordinates for reproducibility


``manual`` reuses the original core sample table and reads the clustered
object from its standard result directory. Do not replace the sample-table
input directory with a downstream Zarr path.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Analysis mode
     - Input
     - Output
   * - single_analysis (standard ``zarr`` mode)
     - Use the exact platform core header (Stereo-seq also needs ``input_spec``); the sample table retains the original data directory; the rule reads ``results/{sample}/clustering/{sample}.zarr``
     - ``results/{sample}/annotation/{sample}.zarr`` and ``results/{sample}/annotation/*_cell_clusters.csv``
   * - single_analysis (``visium_HD``)
     - ``sample.txt`` should contain at least ``sample_id input_path bin_size``; the sample table retains the original data directory; the rule reads ``results/{sample}_{bin}um/clustering/{sample}.zarr``
     - ``results/{sample}_{bin}um/annotation/{sample}.zarr`` and ``results/{sample}_{bin}um/annotation/*_cell_clusters.csv``
   * - compare_analysis
     - ``sample.txt`` contains ``sample_id input_path group``. For Visium HD, append bin_size after group in sample.txt. The current implementation performs mapping on the integrated object.
     - ``results/merge_data/annotation/concatenated_sdata.zarr`` and ``results/merge_data/annotation/*_cell_clusters.csv``


Interpreting the results
------------------------

1. Annotated UMAP
~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/Colon_Cancer_P2UMAP.png
   :width: 85%
   :align: center
   :alt: UMAP colored by manual cell-type annotation

Interpretation:
UMAP is mainly used to inspect the separation and transitions among mapped ``celltype`` labels in low-dimensional space. If several cell types overlap strongly without a meaningful transition pattern, the annotation granularity may not match the clustering granularity.

Suggestion:
First check whether biologically distinct clusters were merged into the same ``celltype`` in the mapping file. If needed, adjust the cluster structure before reapplying the mapping.

2. Spatial overlay plot
~~~~~~~~~~~~~~~~~~~~~~~

Example output:

.. figure:: /_static/images/Colon_Cancer_P2_hires_image_celltype.png
   :width: 85%
   :align: center
   :alt: Spatial distribution of manually annotated cell types

   Spatial cell-type map used to evaluate whether the annotations show coherent spatial organization and plausible tissue boundaries.

Interpretation:
This plot helps determine whether the annotated cell types occupy biologically reasonable positions in tissue space. If one type appears as scattered noise and does not match tissue histology, misannotation or cluster noise should be considered.

Suggestion:
Evaluate spatial coherence together with the UMAP structure, and finalize the naming only when both views support the same conclusion.

3. Composition plot
~~~~~~~~~~~~~~~~~~~

Example output:

.. figure:: /_static/images/celltype_proportion.png
   :width: 85%
   :align: center
   :alt: Cell-type proportions across regions or samples

   Cell-type proportion plot used to compare cell-type composition across regions or samples.

Interpretation:
This plot compares the relative abundance of each cell type across regions or samples. If one cell type is highly enriched in only one area, interpret it in the context of tissue structure and sampling strategy before deciding whether it reflects biology or technical bias.

Suggestion:
In multi-sample studies, first account for differences in sample size and sequencing depth before interpreting changes in composition.

4. Exported annotation table (``*_cell_clusters.csv``)

This file provides the direct mapping from barcode to annotation label and serves as a standard exchange format for downstream differential analysis, visualization platforms, and manual review.



The annotation shown here is performed at the major cell-type level. If you want to annotate finer subclusters, simply increasing ``resolution`` and ``pcs`` is usually not sufficient. Instead, split out the cell type of interest and run PCA and clustering again at that level, as described in :doc:`../subcluster_annotation/reclustering`.
