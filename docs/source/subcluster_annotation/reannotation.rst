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
   由于这是一个重复进行分析的模块 重复整合注释信息,我们直接使用demo数据进行演示.若您为其他情况,请根据之前的经验更改对应必要参数.


.. code-block:: text

   samples path_to_dir
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/reclustering/Colon_Cancer_P2_008um.zarr

Prepare the mapping file ``annotation.txt``
------------------------

The current implementation skips the first line and reads the second line as the mapping definition. The second line is comma-separated, and the order corresponds to cluster or recluster IDs ``0,1,2...``.

.. code-block:: text

   celltype
   Tumor,T_cell,Fibroblast,Endothelial

In this example, the mapping is ``0->Tumor``, ``1->T_cell``, ``2->Fibroblast``, and ``3->Endothelial``. If more IDs are present, continue listing them on the same line.


Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=reannotation --annotation-file=annotation.txt
   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=reannotation --annotation-file=annotation.txt


Optional parameters from the command line
-----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--anno_algorithm``
     - ``reannotation``
     - Select the reannotation branch
   * - ``--annotation-file``
     - ``annotation.txt``
     - Path to the annotation mapping file, which is the key parameter for this step
   * - ``--results_folder``
     - ``results``
     - Root output directory

Note: in practice, the ``reannotation`` branch depends mainly on ``--anno_algorithm`` and ``--annotation-file``. Generic annotation parameters such as ``shape_type``, ``image_type``, and ``device`` are not central to the core computation in this branch.


Optional parameters through a configuration file
------------------------------------------------

If you want to keep repeated revisions reproducible, use a YAML configuration file.

Generate the YAML template with:

.. code-block:: bash

   spatialsnake produce-file --option=annotation

In ``annotation.yaml``, the most commonly used fields for ``reannotation`` are:

.. code-block:: text

   anno_algorithm: reannotation
   annotation_list: annotation.txt
   results_folder: results
   run_type: visium
   channel: single_analysis

Here, ``annotation_list`` corresponds to the command-line argument ``--annotation-file``.


Run the workflow with the configuration file
--------------------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotation --configfile annotation.yaml


Result file structure
---------------------

This example shows single-sample ``visium`` reannotation. Before continuing to downstream analysis, first confirm that ``{sample}.zarr`` and ``celltype_annotations.csv`` have been generated.

.. code-block:: text

   results/
   └── {sample}/
       └── reannotation/
           ├── {sample}.zarr/                 # for slide_seq, this becomes {sample}.h5ad
           └── celltype_annotations.csv

The updated ``{sample}.zarr`` (or ``.h5ad``) contains the revised ``obs['celltype']`` field. ``celltype_annotations.csv`` is the standardized export table used for external review and data sharing.


Differences across platforms and multi-sample analysis
------------------------------------------------------

Differences in command usage
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Scenario
     - Recommended command
   * - Single sample (standard ``zarr`` platforms: ``visium`` / ``xenium`` / ``visium_segment``)
     - ``spatialsnake single_analysis sample.txt visium --option=annotation --anno_algorithm=reannotation --annotation-file=annotation.txt``
   * - Single sample (``visium_HD``)
     - ``spatialsnake single_analysis sample.txt visium_HD --option=annotation --anno_algorithm=reannotation --annotation-file=annotation.txt``
   * - Single sample (``slide_seq``)
     - ``spatialsnake single_analysis sample.txt slide_seq --option=annotation --anno_algorithm=reannotation --annotation-file=annotation.txt``
   * - Reannotation of an integrated multi-sample object
     - ``spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=reannotation --annotation-file=annotation.txt``


Key parameter recommendations
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - Parameter category
     - Recommendation for single-sample analysis
     - Recommendation for multi-sample or cross-condition analysis
   * - Mapping file (``annotation_list`` / ``--annotation-file``)
     - Name the major populations first, then refine edge clusters
     - For integrated objects, establish a unified naming scheme before refining condition-specific details
   * - ``anno_algorithm``
     - Keep it fixed as ``reannotation`` so the correct branch is used
     - Use the same branch consistently across iterations to keep results comparable
   * - Output directory (``results_folder``)
     - The default setting is usually sufficient
     - For multiple rounds of revision, separate result directories by version for traceability


Input and output structure
--------------------------

``reannotation`` reads downstream object paths rather than raw sequencing directories. We therefore recommend putting the ``clustering`` or ``reclustering`` output object in the second column of ``sample.txt``.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Analysis mode
     - Input
     - Output
   * - single_analysis (standard ``zarr`` mode)
     - ``sample.txt`` should contain at least ``sample_id input_path``; ``input_path`` is usually ``results/{sample}/clustering/{sample}.zarr`` or ``results/{sample}/reclustering/{sample}.zarr``
     - ``results/{sample}/reannotation/{sample}.zarr`` and ``results/{sample}/reannotation/celltype_annotations.csv``
   * - single_analysis (``visium_HD``)
     - ``sample.txt`` should contain at least ``sample_id input_path bin``; ``input_path`` is usually ``results/{sample}_{bin}um/clustering/{sample}.zarr``
     - ``results/{sample}/reannotation/{sample}.zarr`` and ``results/{sample}/reannotation/celltype_annotations.csv``
   * - single_analysis (``slide_seq``)
     - ``sample.txt`` should contain at least ``sample_id input_path``; ``input_path`` is usually ``results/{sample}/clustering/{sample}.h5ad``
     - ``results/{sample}/reannotation/{sample}.h5ad`` and ``results/{sample}/reannotation/celltype_annotations.csv``
   * - compare_analysis
     - ``sample.txt`` should contain at least ``sample_id input_path group``; in this mode, the workflow usually operates on an integrated object path
     - Aggregated output is written to ``results/merge_data/reannotation/concatenated_sdata`` together with the exported annotation table


Interpreting the results
------------------------

In this example, the reclustered tumor population is reannotated into four distinct malignant subpopulations based on their marker differences.

The workflow also exports UMAP plots, spatial mapping figures, and cell proportion plots after reannotation so that you can evaluate the revised labels from multiple perspectives.

A cell ID to ``celltype`` CSV file is also exported to support later visualization and annotation transfer.


.. figure:: /_static/images/umap_recelltype.png
   :width: 85%
   :align: center
   :alt: manual annotation celltype proportion

.. figure:: /_static/images/respatial_clusters.png
   :width: 85%
   :align: center
   :alt: manual annotation celltype proportion


.. figure:: /_static/images/recelltype_proportion.png
   :width: 85%
   :align: center
   :alt: manual annotation celltype proportion

If you are building atlas-style annotations, you may need to annotate each subcluster in detail and then merge the results.
Spatialsnake provides utility modules to make this process easier; see :doc:`../useful_tool/index`.

In the next step, we merge the annotated tumor subcluster labels back into the original larger dataset; see :doc:`../useful_tool/merge`.
