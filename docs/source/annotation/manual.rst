Manual annotation
=================

``manual`` is the manual annotation branch under ``annotation``. It maps ``clusters`` to interpretable ``celltype`` labels and writes the result back to the analysis object.
``annotation_help`` provides marker and enrichment evidence; ``manual`` applies
a researcher-defined mapping and exports the annotated object and figures.

The main evidence used for manual annotation is the ``marker_genes_pval.csv`` table generated in ``annotation_help``. You can combine that table with the marker dotplot and the literature to evaluate whether canonical marker genes are strongly expressed in the expected clusters.

Workflow overview
-----------------
1. Reuse the core sample table; the workflow reads the completed clustering object from its standard result directory.
2. Read the annotation mapping file and parse the relationship from ``cluster`` to ``celltype``.
3. Map ``obs['clusters']`` to ``obs['celltype']`` and write the result back into the object.
4. Export the UMAP plot, composition plot, spatial overlay plot, and annotation table.
5. Generate the ``annotation``-stage object for downstream comparison or further analysis.

Complete ``clustering`` and ``annotation_help`` first. Assign labels from the
actual marker expression and tissue context, then provide the mapping below.

Demo: CRC P2 manual annotation
------------------------------

The current implementation skips the first line and reads the second line as the annotation content. The second line is comma-separated, and the order corresponds to ``cluster 0,1,2...``.
Complete CRC P2 clustering and annotation_help first. Reuse this sample table and save the mapping below as annotation.txt. You may download :download:`crc_annotation.txt </config/demo_resources/crc_annotation.txt>` and rename it to annotation.txt.

.. code-block:: text

   sample_id input_path bin_size
   Colon_Cancer_P2 data/Colon_Cancer_P2 8

.. code-block:: text

   sample 0 1 2 3 4 5.........please input anno by order of cluster
   Endothelial_Cells,Smooth_Muscle_Cells,Myeloid_Cells,Unknown,NK_T_Cells,Fibroblasts,Tumor,Tumor,Tumor,Tumor,B_Cells,Fibroblasts,Intestinal_Epithelial_Cells,Tumor

The mapping is specific to this demo's clusters. For your own data, assign
labels from the actual marker and spatial results. If cluster numbering differs,
rebuild the correspondence rather than extending or truncating this label list.

.. note::

   Recomputed clusters can differ in membership, number, or numbering across
   parameters, software versions, and numerical backends. A rotated or flipped
   UMAP alone does not require different labels. Check the actual cluster IDs and
   markers before applying the demo mapping; do not pad or truncate the list.
   To reproduce later modules with the demonstrated labels, use the completed
   annotation object from
   `Zenodo <https://doi.org/10.5281/zenodo.23374838>`__:

   ``03_tutorial_results.zip`` contains
   ``results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr``.

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
           ├── Colon_Cancer_P2_annotation_summary.png
           ├── Colon_Cancer_P2_hires_image_Clusters.png
           ├── Colon_Cancer_P2_cell_clusters.csv
           └── ...

``Colon_Cancer_P2.zarr`` is the main object reused in downstream analysis. ``Colon_Cancer_P2_cell_clusters.csv`` is the exported label table used for external review or other downstream tools.
The current exporter uses ``*_cell_clusters.csv`` for all platforms.
``*_annotation_summary.png`` shows detected genes by annotation; if this QC
field is absent, it shows observation counts. Older archives use the filename
``*_gene_enrich.png`` for this figure.


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

The CRC P2 UMAP shows the assigned labels in expression space. Overlap alone
is not evidence of incorrect annotation. Review the marker table if different
labels share indistinguishable profiles, or if one label combines incompatible
lineage signatures.

2. Spatial overlay plot
~~~~~~~~~~~~~~~~~~~~~~~

Example output:

.. figure:: /_static/images/Colon_Cancer_P2_hires_image_celltype.png
   :width: 85%
   :align: center
   :alt: Spatial distribution of manually annotated cell types

   Spatial cell-type map used to evaluate whether the annotations show coherent spatial organization and plausible tissue boundaries.

Compare the labels with tissue morphology and marker expression. Dispersed
immune populations can be biologically plausible; spatial continuity is not a
requirement for a valid cell type. Review unexpected patterns before renaming
clusters or changing parameters.

3. Composition plot
~~~~~~~~~~~~~~~~~~~

Example output:

.. figure:: /_static/images/celltype_proportion.png
   :width: 85%
   :align: center
   :alt: Cell-type proportions across regions or samples

   Cell-type proportion plot used to compare cell-type composition across regions or samples.

This plot summarizes the fraction of observations assigned to each label.
For CRC P2 these are bin fractions, not measured cell fractions. Between-sample
differences also depend on captured tissue area, filtering, and annotation.

Suggestion:
In multi-sample studies, first account for differences in sample size and sequencing depth before interpreting changes in composition.

4. Exported annotation table (``*_cell_clusters.csv``)

This file provides the direct mapping from barcode to annotation label and serves as a standard exchange format for downstream differential analysis, visualization platforms, and manual review.


The annotation shown here is performed at the major cell-type level. To resolve finer subpopulations, select the population of interest and recompute PCA and clustering within that subset, as described in :doc:`../subcluster_annotation/reclustering`.
