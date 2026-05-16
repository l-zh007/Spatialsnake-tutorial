Preprocessing
=============

After ``Ingesting`` is complete, ``preprocess`` performs quality control, filtering, normalization, and preparation for dimensionality reduction.

Because spatial transcriptomics data are affected by technical noise and dropout, preprocessing is usually required to remove low-quality genes and spots or cells, followed by normalization steps such as library-size normalization and log transformation.
At this stage, you can also select highly variable genes to reduce noise, and in multi-sample settings you can correct batch effects to improve the reliability of downstream analysis.


Workflow overview
-----------------
1. Compute QC metrics and filter genes and spots or cells according to the selected thresholds.
2. Apply total-count normalization and log transformation.
3. Perform highly variable gene selection if enabled.
4. Run scaling and PCA, and optionally apply batch correction in multi-sample analyses.
5. Export the filtered object and save QC figures generated during preprocessing.

In short, this step prepares the spot-by-gene expression matrix for downstream analysis by improving data quality, standardizing values, and reducing technical noise.


step 1: sample.txt 配置文件
-----------------------

直接使用您integrate步骤使用的sample.txt配置文件即可,无需进行更改.

.. code-block:: text
  
   sample_id input_path
   sample_id data/sample_id

step 2: 参数选择与配置
---------------

此步骤我们包含了许多重要参数,请根据您的需求进行调整,以下是部分参数及其功能的展示:

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Parameter
     - Example
     - Description
   * - ``--min_cells`` / ``--min_genes``
     - ``3`` / ``200``
     - Control gene and spot/cell filtering thresholds
   * - ``--mt_threshold``
     - ``40``
     - Mitochondrial proportion threshold for filtering
   * - ``--batch_method``
     - ``harmony``
     - Batch correction method for integrated multi-sample analysis
   * - ``--n_top_genes``
     - ``3000``
     - Number of highly variable genes
   * - ``--n_comps``
     - ``50``
     - Number of PCA components
   * - ``--variable``
     - ``True``
     - Whether to run highly variable gene selection
   * - ``--NEIGHBORS``
     - ``10``
     - Neighbor graph parameter
   * - ``--sketch`` / ``--sample_rate``
     - ``True`` / ``0.30``
     - Sampling settings for very large datasets



配置建议:
~~~~~

1.对于所有情况: 我们建议您根据 ``integrate`` 步骤中的小提琴图输出进行 ``min_cell``，``min_gene``，``mt_threshold``的调整,根据您分析需求的不同可选择为 0-200 之间的值, mt_threshold 建议选择 30-50 之间的值.若您不进行设置,将自动选择默认值.
   
2.若您的分析对象为多样本整合数据,在注重上述参数的同时,建议您选择适合的 ``batch_method`` 进行批次效应的校正.harmony 是一个常用的方法,您也可以考虑其他方法如 bbknn.

3.若您的样本细胞/spot数量为几十万数量级 甚至百万,为了提升处理效率和降低内容占用,我们推荐您将 --sketch 设置为 True 同时选择合适的 --sample_rate. 此流程spatialsnake将会使用geosketch进行下采样分析
在后续的分析中,建议您在后续clustering步骤继续使用 --sketch 保持一致的下采样策略将聚类信息映射为所有spot/cell.

4.In multi-sample integration, different samples may require different thresholds such as ``min_cells``, ``min_genes``, or ``mt_threshold``.
You can add these sample-specific settings directly to ``sample.txt``, and the workflow will read them automatically and apply the corresponding filtering strategy.
同时请将--filter_list 设置为True。

sample.txt可改为

.. code-block:: text

   sample    input_path         group  min_cells min_genes mt_threshold
   Colon_Cancer_P2   data/Colon_Cancer_P2   Tumor  50  50  30
   Colon_Normal_P5  data/Colon_Normal_P5 Normal  50  50  30


参数配置方法:
~~~~~~~

1.The parameters listed above are commonly used settings that can be passed directly on the command line. 
If you are comfortable tuning spatial transcriptomics workflows, you can append them to the command as needed, for example ``--min_cells 5``.

2.Optional parameters through a configuration file.正如我们在教程Usage中所介绍的一样,我们可以通过修改yaml文件中的参数配置信息进行所有参数的自定义修改后再进行使用.用以下命令获取该步骤的yaml文件并修改.

.. code-block:: bash

   spatialsnake produce-file --option=preprocess


step 3: 命令运行
------------

通过之前教程的基本命令行介绍,详细您已经熟悉对于Spatialsnake的重要参数设置逻辑,这里我们只介绍预处理命令的运行,若您为多样本整合/其他平台数据,直接修改相关参数即可.
For the example dataset, we use ``--min_cells 100 --min_genes 100 --mt_threshold 30`` for single_analysis or visium_HD. This filters out spots or cells with fewer than 100 UMIs, fewer than 100 detected genes, or more than 30% mitochondrial signal.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --min_cells=100 --min_genes=100 --mt_threshold=30

Run with a YAML file. 请不要忘记保存你编辑后的yaml文件. 同时无需手动设置参数,若设置则会覆盖yaml文件中的值.

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --configfile=preprocess.yaml


Demo for preprocess with visium_HD
----------------------------------

我们将使用上一步摄取的Colon_Cancer_P2_008um数据进行预处理演示.
sample.txt可沿用之前的分析流程以固定core_analysis分析同一样本。

.. code-block:: text
  
   sample_id input_path bin
   Colon_Cancer_P2 data/Colon_Cancer_P2 8

Run the command
~~~~~~~~~~~~~~~

依据上述的解释和integrate步骤的小提琴图输出,对于一份单样本数据我们选择 --min_cells 100 --min_genes 100 --mt_threshold 30 作为预处理参数。

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --min_cells=100 --min_genes=100 --mt_threshold=30

若您想进行yaml文件配置进行更丰富的参数设置
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
   # 获取yaml文件并编辑
   spatialsnake produce-file --option=preprocess

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=preprocess --configfile=preprocess.yaml


Result file structure
---------------------

This example shows single-sample preprocessing for ``visium_HD``. After the run completes, first confirm that ``filter_{sample}.zarr`` has been generated, then review the QC figures to determine whether the chosen thresholds are appropriate.

.. code-block:: text

   results/
   └── Colon_Cancer_P2_008um/
       └── preprocess/
           ├── filter_Colon_Cancer_P2.zarr # filtered zarr object
           ├── Colon_Cancer_P2filtered_Total_UMI.png # filtered UMI distribution
           ├── Colon_Cancer_P2filtered_Total_Genes.png # filtered gene-count distribution
           ├── Colon_Cancer_P2_Mitochondrial_Genes.png # mitochondrial signal distribution
           ├── Colon_Cancer_P2_scatter.png # scatter plot of filtered UMI versus gene counts
           ├── Colon_Cancer_P2pca_variance_ratio.png # PCA variance ratio plot
           └── Colon_Cancer_P2_highly_variable.png # highly variable gene selection plot

The file ``filter_{sample}.zarr`` is the core input for downstream clustering and annotation. The remaining figures are used to evaluate UMI distribution, gene complexity, mitochondrial proportion, outliers, and PCA variance explained. If highly variable gene selection or sketch-based sampling is disabled, the corresponding files will not be generated.

Key outputs
~~~~~~~~~~~

1. ``{sample}filtered_Total_UMI.png`` (total UMI distribution)

.. figure:: /_static/images/Colon_Cancer_P2filtered_Total_UMI.png
   :width: 85%
   :align: center
   :alt: preprocess umi plot

   Filtered UMI distribution. Low-quality cells have been removed.

2. ``{sample}filtered_Total_Genes.png`` (detected gene distribution)

.. figure:: /_static/images/Colon_Cancer_P2filtered_Total_Genes.png
   :width: 85%
   :align: center
   :alt: preprocess genes plot

   Distribution of detected genes after filtering.

3. ``{sample}pca_variance_ratio.png`` and the recommended number of PCs printed in the terminal

   - This plot helps determine how many dimensions should be retained for downstream analysis.
   - The point where the curve clearly flattens often provides a useful reference.
   - In practice, compare a few nearby values around the recommended point and choose the most stable setting.

.. figure:: /_static/images/Colon_Cancer_P2pca_variance_ratio.png
   :width: 85%
   :align: center
   :alt: preprocess pca variance ratio

   PCA variance ratio plot. Use this figure together with the recommended PC value shown in the terminal to choose a suitable ``pcs`` setting for clustering.


4. ``{sample}_Mitochondrial_Genes.png`` (mitochondrial signal distribution)

   - This plot shows whether mitochondrial-related signal remains elevated after filtering.
   - If some regions are still globally high, consider tightening the filtering strategy while preserving sufficient data.
   - Adjust thresholds gradually to avoid removing genuine biological signal.

5. ``{sample}_scatter.png`` (summary scatter plot)

   - This plot helps identify potential low-quality clusters of observations.
   - Pay particular attention to regions with low gene counts and high mitochondrial proportion.
   - Interpret it together with the previous plots for a more reliable conclusion.

6. ``{sample}_highly_variable.png`` (highly variable gene plot, optional)

   - This plot confirms that downstream clustering will focus on the most informative genes.
   - If the selection is too narrow, structural information may be lost; if it is too broad, additional noise may be introduced.
   - Start with the default setting and refine it only if clustering results suggest it is necessary.



Continue to :doc:`clustering`.
