Module 7: Differential Expression Comparison (compare_stage)
============================================================

The ``compare_gene`` branch of ``compare_stage`` performs replicate-aware
differential expression analysis for multi-sample spatial transcriptomics data.
For each selected cell type or spatial label, raw integer counts are aggregated
into sample-level pseudobulk profiles, formal group contrasts are tested, and
directional GO and KEGG enrichment summaries are generated.

For the complete parameter reference, see :doc:`../config_reference/compare_stage_yaml`.

Analysis logic
--------------

The workflow follows four steps:

1. Select labels from ``obs[compare_celltype_col]`` using ``cell_focus``.
2. Aggregate raw counts by ``sample_id`` within each selected label.
3. Compare biological groups with ``DESeq2`` or ``edgeR``.
4. Visualize differential genes and perform directional GO/KEGG enrichment.

Each label and contrast is analysed independently. Labels are not pooled, because
their abundance, library size, and dispersion may differ substantially.

For standard Visium data, a spot may contain several cells. Therefore, a
``celltype`` label in spot-level data should be interpreted as a label-enriched
region or dominant cell-state region. Cell-type-specific interpretation is most
appropriate for cell-resolved data or segmented single-cell observations.

Prepare ``sample.txt``
----------------------

``sample.txt`` contains three columns:

.. code-block:: text

   sample_id   input_path   group
   S1          data/S1      Control
   S2          data/S2      Control
   S3          data/S3      Disease
   S4          data/S4      Disease

Spaces and tabs are both accepted. ``sample_id`` must match
``obs[compare_sample_col]`` in the annotated merged Zarr. The third column,
``group``, is the authoritative biological condition used by ``compare_gene``.

The default input Zarr is:

.. code-block:: text

   results/merge_data/annotation/concatenated_sdata.zarr

This can be overridden with ``compare_input_zarr`` when necessary.

Configure a two-group comparison
--------------------------------

For a two-group study, ``compare_contrasts`` may be left empty. In that case,
the workflow compares the second group appearing in ``sample.txt`` against the
first group.

For example:

.. code-block:: text

   sample_id   input_path   group
   S1          data/S1      Control
   S2          data/S2      Control
   S3          data/S3      Disease
   S4          data/S4      Disease

With an empty contrast list, the default contrast is:

.. code-block:: text

   Disease_vs_Control

For clarity and reproducibility, an explicit contrast is recommended:

.. code-block:: yaml

   compare_contrasts:
     - comparison: Disease
       reference: Control

In this contrast, positive ``log2FoldChange`` values indicate higher expression
in ``Disease`` relative to ``Control``.

Configure three or more groups
------------------------------

When ``sample.txt`` contains three or more groups, ``compare_contrasts`` is
required. The workflow does not automatically run all pairwise comparisons,
because the intended reference group is a biological design choice.

Example:

.. code-block:: yaml

   compare_contrasts:
     - comparison: TreatmentA
       reference: Control
     - comparison: TreatmentB
       reference: Control
     - comparison: TreatmentB
       reference: TreatmentA

The equivalent command-line form is:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium \
     --option=compare_stage \
     --runpipe=compare_gene \
     --compare_contrasts TreatmentA:Control,TreatmentB:Control,TreatmentB:TreatmentA

Each contrast produces an independent result directory, such as
``TreatmentA_vs_Control``.

Biological replicates
---------------------

Each ``sample_id`` is treated as one biological replicate. The default
``min_replicates`` is ``2``, meaning that both the comparison and reference
groups must retain at least two valid samples after label-specific filtering.

Balanced designs, such as two replicates per group, are supported. Unequal
designs, such as three controls and two disease samples, are also supported if
both groups satisfy ``min_replicates``. If one side of a contrast has too few
valid biological replicates, that label/contrast task is skipped. If no
requested task remains executable, the workflow stops with a clear error.

``min_cells_per_sample`` controls how many cells or spots from the selected
label must be present in each sample before that sample is retained for the
label-specific pseudobulk test.

Minimal YAML example
--------------------

.. code-block:: yaml

   option: compare_stage
   channel: compare_analysis
   runpipe: compare_gene

   compare_algorithm: DESeq2
   compare_input_zarr: results/merge_data/annotation/concatenated_sdata.zarr

   compare_celltype_col: celltype
   compare_sample_col: sample
   compare_condition_col: group
   count_layer: counts
   cell_focus: "T_cell,B_cell"

   compare_contrasts:
     - comparison: Disease
       reference: Control

   min_replicates: 2
   min_cells_per_sample: 30
   min_total_counts_per_gene: 10

   cut_off_pvalue: 0.05
   cut_off_logFC: 0.5
   de_top_n: 20

   species: human
   compare_gene_id_type: auto
   compare_gene_symbol_col: ""
   compare_go_ontology: BP
   compare_enrichment_top_n: 10

Use ``cell_focus: "all"`` to analyse every available label. Use a comma-separated
list to analyse a small set of labels.

Run the workflow
----------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=compare_stage --runpipe=compare_gene

The result root is:

.. code-block:: text

   results/merge_data/compare_analysis/compare_gene/{algorithm}/{celltype}/{comparison}_vs_{reference}/

Output files
------------

Each successful label/contrast task keeps only the core outputs:

.. code-block:: text

   differential_expression.csv
   volcano.pdf
   heatmap.pdf
   GO_enrichment.csv
   GO_<ontology>_enrichment.pdf
   KEGG_enrichment.csv
   KEGG_enrichment.pdf

Only the selected GO ontology plots are produced. For example,
``compare_go_ontology: BP`` creates ``GO_BP_enrichment.pdf``. When
``compare_go_ontology: ALL`` is used, BP, CC, and MF are visualized as separate
PDF files rather than as one large multi-ontology figure.

Differential-expression plots
-----------------------------

``differential_expression.csv`` contains:

.. code-block:: text

   gene  gene_symbol  base_mean  log2FoldChange  statistic  pvalue  padj  comparison  reference  celltype  algorithm

``volcano.pdf`` summarizes effect size and statistical significance for the
current label and contrast. ``heatmap.pdf`` displays the top significant genes
across the retained biological replicates; if no significant genes are
available, a placeholder heatmap PDF is still written so that the output
contract remains stable.

GO and KEGG visualization
-------------------------

Significant genes are split into two directional sets before enrichment:

* ``higher_in_comparison``: genes with ``padj < cut_off_pvalue`` and
  ``log2FoldChange >= cut_off_logFC``.
* ``higher_in_reference``: genes with ``padj < cut_off_pvalue`` and
  ``log2FoldChange <= -cut_off_logFC``.

GO enrichment is written to ``GO_enrichment.csv`` and visualized separately for
each selected ontology. Each GO PDF is a compact horizontal bar plot. The x-axis
shows the number of genes assigned to each term, and the panels separate
``Higher in <comparison>`` from ``Higher in <reference>``.

KEGG enrichment is written to ``KEGG_enrichment.csv`` and visualized in
``KEGG_enrichment.pdf``. The KEGG plot uses fold enrichment on the x-axis, point
size for gene count, and color for adjusted P value. Directional panels again
separate pathways enriched among genes higher in the comparison group from
pathways enriched among genes higher in the reference group.

Interpreting pathway direction
------------------------------

Pathway direction is determined by the ``direction`` column in the enrichment
CSV files and by the panel title in the PDF.

For a result directory named ``Disease_vs_Control``:

.. code-block:: text

   higher_in_comparison  -> enriched among genes higher in Disease
   higher_in_reference   -> enriched among genes higher in Control

For a result directory named ``TreatmentB_vs_TreatmentA``:

.. code-block:: text

   higher_in_comparison  -> enriched among genes higher in TreatmentB
   higher_in_reference   -> enriched among genes higher in TreatmentA

Thus, a GO term or KEGG pathway is interpreted as enriched in a group only when
it appears in the directional gene set corresponding to that group. The
enrichment result does not mean that every gene in the pathway is upregulated;
it means that the thresholded directional DEG set contains more pathway members
than expected from the tested gene universe.


Display the results
------------------------------

Although all five mouse brain Visium samples provided in the documentation were generated under the same experimental conditions, cortical regions were selected solely to demonstrate the differential analysis workflow. The resulting comparisons are illustrative and should not be interpreted as biologically meaningful findings.

1. DEG volcano plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/volcano.jpg
   :width: 85%
   :align: center
   :alt: DEG volcano plot


1. GO enrichment bar plot in the comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/GO_BP_enrichment.jpg
   :width: 85%
   :align: center
   :alt: GO enrichment bar plot
