Spatialsnake for multi-sample integration
=========================================

Before reading this section, make sure you have completed at least one tutorial in :doc:`../data_input/index` so that you already know how to prepare ``sample.txt`` and run Spatialsnake.
This tutorial is intended for studies with multiple spatial transcriptomics datasets from different experimental conditions, such as different tumor types or different normal tissue types.
The integrated object produced here can be used for the same downstream analyses as a single-sample object, although some result files and interpretations differ.


基本且通用的摄取步骤
---------------------

本页教程只提供基本的多样本摄取教程,对于详细core_analysis请跳转到对应教程页。该部分适用于所有平台格式的数据,请确保你已经阅读你想进行整合摄取的平台的对应教程,对摄取步骤有基本的了解,本教程将不会重复介绍

step 1 : 数据的下载与存储路径
   spatialsnake的多样本摄取步骤支持整合两组不同实验条件的样本,每个样本的data路径与sample_id需要与sample.txt中配置的路径与sample_id一致。
   同时我们支持每组样本存在若干的生物学重复，
   无论任何平台,正确的存放方式为:

.. code-block:: text
   # 其中样本的id可以自定义与分组无关
   project_root/
   ├── data/
   │   ├── Normal_1/
   │   ├── Normal_2/
   │   ├── Normal_3/
   │   ├── cancer_1/
   │   ├── cancer_2/
   │   └── cancer_3/
   ├── sample.txt
   └── results/

step 2 : 配置sample.txt文件

同理,我们也利用样本文件表进行 样本id 输入文件目录 分组信息的配置填写。

.. code-block:: text

   sample_id   input_path         group
   Normal_1   data/Normal_1     Group1
   Normal_2   data/Normal_2     Group1
   Normal_3   data/Normal_3     Group1
   cancer_1   data/ST8059051     Group2
   cancer_2   data/ST8059052     Group2
   cancer_3   data/ST8059053     Group2


step 2 : 命令执行

区别于single_analysis,多样本分析需要多个样本data与sample.txt配置,且存在部分不同的命令参数配置

例如visium平台 ``compare_analysis`` 整合命令:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=integrate

总结:

对于spatialsnake的多样本整合步骤的基本的运行差异就介绍完了,对于下游的某些分析,compare_analysis可以开启不一样的参数配置，例如batch_method等,以适配不同的实验分析需求。
但总的来说最重要的只要将sample.txt文件配置好,并执行compare_analysis命令,确定好分析平台字段,即可正常完成多样本整合分析。

以下我将使用visium平台数据进行详细演示,若您已使用自己的分析数据完成此部分可跳过,直接进行后续的core_analysis preprocess 步骤。

Demo 使用示例演示
---------------------

Multi-sample analysis typically combines several datasets. For a concise demonstration, we use multiple Visium mouse brain sections from a public dataset:

https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-11114

我们将使用demo数据进行 core_analysis 的最小化演示,包含数据读取、预处理、注释等步骤。通过此教程您可直观了解 多样本整合分析与单样本的基本差异，对于每个模块功能的细节 参数设置 分析功能实现,请详细
阅读每个模块的开头简易使用教程,更可使用我们的visium HD 示例数据进行全面的分析学习。

This tutorial uses five public samples:

- Group 1: ``ST8059048``, ``ST8059049``, ``ST8059050``
- Group 2: ``ST8059051``, ``ST8059052``

If you are using your own dataset rather than the example shown here, the main fields you need to replace are:

- the sample IDs in the download script and in ``sample.txt``
- the ``input_path`` values in ``sample.txt``
- the biological group labels in the ``group`` column
- the platform type in the command if your data are not ``visium``

Step 1: create a download script in the project root
----------------------------------------------------

First make sure the current working directory contains a ``data/`` folder, then create a script named ``download.sh``.
This script downloads one expression matrix and one spatial archive for each sample and expands them directly into sample-specific directories under ``data/``.
If you are working with another public dataset, keep the same folder logic but replace the sample IDs and download URLs.

.. code-block:: bash

   #!/usr/bin/env bash
   set -euo pipefail
   ids=(ST8059048 ST8059049 ST8059050 ST8059051 ST8059052)
   for id in "${ids[@]}"; do
   mkdir -p "data/${id}"
   cd "data/${id}"
   wget -c "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/114/E-MTAB-11114/Files/${id}_filtered_feature_bc_matrix.h5"
   wget -c "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/114/E-MTAB-11114/Files/${id}_spatial.tar.gz"
   tar -xvzf "${id}_spatial.tar.gz"
   cd - >/dev/null
   done


Step 2: make the script executable and run it
---------------------------------------------

.. code-block:: bash

   chmod +x download.sh
   ./download.sh

After the script finishes, the input directory should follow the structure below.
This is the folder layout that Spatialsnake expects when reading multi-sample Visium data.

Example input directory layout
------------------------------

.. code-block:: text

   project_root/
   ├── data/
   │   ├── ST8059048/
   │   │   ├── ST8059048_filtered_feature_bc_matrix.h5
   │   │   └── spatial/
   │   │       ├── tissue_positions_list.csv
   │   │       ├── scalefactors_json.json
   │   │       ├── tissue_lowres_image.png
   │   │       └── tissue_hires_image.png
   │   ├── ST8059049/
   │   │   ├── ST8059049_filtered_feature_bc_matrix.h5
   │   │   └── spatial/
   │   ├── ST8059050/
   │   │   ├── ST8059050_filtered_feature_bc_matrix.h5
   │   │   └── spatial/
   │   ├── ST8059051/
   │   │   ├── ST8059051_filtered_feature_bc_matrix.h5
   │   │   └── spatial/
   │   └── ST8059052/
   │       ├── ST8059052_filtered_feature_bc_matrix.h5
   │       └── spatial/
   ├── sample.txt
   └── results/

If you are using your own data, keep the same two-level organization:

- one folder per sample under ``data/``
- one expression matrix and one ``spatial/`` directory inside each sample folder

Step 3: prepare ``sample.txt`` with group information
-----------------------------------------------------

For multi-sample integration, ``sample.txt`` is similar to the single-sample version but must also include a group column.
The ``group`` field defines the biological condition used later in comparison-oriented analyses, so it should reflect your real experimental design rather than arbitrary batch labels.
If you are using another dataset, replace both the sample IDs and the paths, and rename ``Group1`` and ``Group2`` to meaningful condition names such as ``Control`` and ``Disease``.

.. code-block:: text

   sample_id   input_path         group
   ST8059048   data/ST8059048     Group1
   ST8059049   data/ST8059049     Group1
   ST8059050   data/ST8059050     Group1
   ST8059051   data/ST8059051     Group2
   ST8059052   data/ST8059052     Group2

Step 4: run integration and merge the samples
---------------------------------------------

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=integrate

At this stage, Spatialsnake reads all sample folders listed in ``sample.txt``, standardizes them into one common object representation, and writes the merged result for downstream preprocessing.
If your data come from another platform, replace ``visium`` with the corresponding ``run_type``.

The result structure is similar to the single-sample workflow:

.. code-block:: text

   results/
   └── merge_data/
       └── integrate/
           └── concatenated_sdata
               ...........



Step 5: preprocess the integrated object
----------------------------------------

Single-sample analyses often do not require explicit batch correction, but for multi-sample analysis it is usually worth considering:

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --min_genes=100 --min_cells=100 --batch_method=harmony

Step 6: continue with the steps
------------------------------------------

After preprocessing, the remaining steps follow the standard ``compare_analysis`` workflow.
The pipeline will generate joint visualizations and result tables across samples.
Because the data are integrated, manual annotation is usually performed on the shared cluster identities across all samples.

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=clustering --resolution=0.8 --pcs=20
   spatialsnake compare_analysis sample.txt visium --option=annotation_help --species=mouse

For this mouse brain example, we provide only a coarse broad-region annotation. The labels are for tutorial demonstration only and are not intended as a formal reproduction of the original study annotation.

.. code-block:: bash

   sample 0 1 2 3 4 5.........please input anno by order of cluster
   thalamus,cortex,cortex,amygdala,hypothalamus,hypothalamus,striatum,cortex,cortex,white matter,hypothalamus,thalamus,hippocampus,hippocampus,hippocampus,piriform_cortex,cortex,cortex,cortex,cortex,cortex,cortex,cortex,amygdala,thalamus,thalamus

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=annotation --anno_algorithm=manual --annotation-file=annotation.txt

For your own data, replace these example labels with the cell types or tissue regions inferred from your own clustering and marker results.


You have now generated an integrated spatial transcriptomics object. The remaining analysis steps are similar to the single-sample workflow, with a few multi-sample-specific details explained on each step page.

Continue to :doc:`../core_analysis/index`.

Example visualizations are discussed in the downstream tutorial pages.
