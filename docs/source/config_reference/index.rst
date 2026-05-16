Configuration Reference and Practical Tips
==========================================

Practical tips:

Scenario 1: use Snakemake reproducibility to retune parameters and rerun a module
   For example, if the ``resolution`` and ``pcs`` values used in ``--option=clustering`` do not produce a satisfactory clustering result, you can adjust them and rerun the step.

   1. Tune ``resolution`` and ``pcs`` based on the UMAP result, for example by trying different resolution values such as 0.5, 0.7, or 0.9.
   2. 利用snakemake自带参数,请在原先的运行命令中加入 ``-r`` 参数即可自动删除分析结果,再次运行无 ``-r``的命令即可以新参数重新运行.

Scenario 2: run downstream modules independently, using either single-cell or spatial transcriptomics data as input
   In many studies, spatial transcriptomics data are accompanied by high-quality single-cell sequencing data generated under comparable experimental conditions. In that case, some downstream modules, such as ligand-receptor analysis or transcription factor analysis, can also use transcriptomics data in ``anndata``/``h5ad`` format as input, providing indirect support for the interpretation of spatial transcriptomics results.

Scenario 3: atlas-style analysis with repeated splitting, reclustering, and subcluster annotation across multiple cell types
   For example, when using ``--option=reclustering``, you may want to refine several cell types in parallel.

   1. Add the split ``zarr`` files for different cell types to ``sample.txt`` and assign distinct names.
   2. Use Snakemake parallelization to process different cell types simultaneously and improve efficiency. Note that this approach does not support per-sample parameter tuning. If one result is unsatisfactory, rerun that dataset separately with adjusted parameters.

Scenario 4: use ``useful_tool`` for ROI selection and sample splitting
   Typical use cases for ``--option=splitting`` include:

   1. Multiple samples are present on the same slide and need to be separated before analysis.
   2. After major-cell-type annotation, you want to focus on tumor infiltration regions or peri-tumor microenvironments.
   3. You want to define irregular ROIs using Loupe or Xenium Explorer.
   4. You want to define approximate rectangular ROIs using image coordinates.

Scenario 5: interact with the R/Seurat ecosystem through ``transform``

   1. Some spatial transcriptomics tools are available only in R, so you can use ``--option=transform`` to convert the data into a Seurat object for downstream analysis.
   2. Likewise, you can convert the data into standard ``anndata`` format when needed.

Scenario 6: resume after an interrupted run

   1. Use ``--unlock`` to unlock the workflow and rerun the interrupted module.

Scenario 7: add analysis stages midway by following the expected file structure

   1. In ``core_analysis``, the stages before annotation require sample names, raw files, and related metadata to ensure stable execution. If you want to run only one of these steps with your own data, place ``{sample}.zarr`` under ``results/{sample}/{option}/`` and Spatialsnake will use the information in ``sample.txt`` to continue from the expected input state.
   2. For downstream modules or utility modules, raw files are not required. You only need to provide the correct input files as described in the corresponding tutorial.

Parameter reference:

.. toctree::
   :maxdepth: 1
   :titlesonly:

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
