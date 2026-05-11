Slide-seq Input Tutorial
========================

Required files
--------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - Filename / pattern
     - Required
     - Format
     - Description
   * - ``**.tissue.gef`` ``**.cellbin.gef`` ``**.adjusted.cellbin.gef``
     - At least one
     - gef
     - Cell-by-gene expression matrix, 不同bin_size 文件
   * - ``**/images/**.tif``
     - Required
     - TIFF/OME.TIFF/OME-XML
     - 包含TIFF图像信息。
   * - ``**/images/**.h5ad``
     - No
     - h5ad
     - 软件分析结果

对于Stereoseq，我们要求您使用的文件层级结构需符合华大基因公司开发的 SAW V8 输出文件层级结构

.. figure:: /_static/images/Colon_Cancer_P2pca_variance_ratio.png
   :width: 85%
   :align: center
   :alt: SAW V8 

得益于Spatialdata官方开源公开的社区交流,我们通过社区交流将Spatialdata中的stereoseq读取函数优化,支持Stereoseq V8的读取和分析，同时基于@brainfo的贡献增加了cellbin adjusted.cellbin数据的读取选择,改良了读取函数的使用逻辑适配于spatialsnake
感谢 @brainfo 贡献的解决方案 https://github.com/brainfo/spatialdata-io/blob/main/src/spatialdata_io/readers/stereoseq.py

现在所需要的层级例如:

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── {sample_id}/
   ├── sample.txt (key sample description file)
   └── results/ (stores analysis outputs)

   data/
   └── {sample_id}/
       ├── feature_expression   *required at least
       │   ├── {sample_id}.tissue.gef
       │   ├── {sample_id}.cellbin.gef
       │   ├── {sample_id}.adjusted.cellbin.gef
       └── image/   *required at least
       │    └── {sample_id}_HE_regist.tif
       └── analysis/    *optional when load_analysis=False
           ├── {sample_id}.bin20_1.0.h5ad  
           └── {sample_id}.bin50_1.0.h5ad

Where these files come from
---------------------------

- Official download: 华大基因官网所提供的resources公开演示数据集资源
- Experimental output: 通过华大基因STOmics Stereoseq 测序平台取得的样本数据
- 公共数据集合下载: 若您想下载公共数据集合 请安装上述所要求的文件和文件层级存放你想分析的样本

Demo 使用示例演示
---------------------------

``run_type: stereo_seq``. In this tutorial, we use a public Mouse Brain Demo Data and organize the downloaded files into the directory structure expected by Spatialsnake.
One convenient public source for the required processed files is:
https://www.stomics.tech/col1317

为了节省演示的时间,我们这里只下载了feature_expression所需的文件于image所需的tif图像文件

``Example setup:

.. code-block:: bash

   mkdir -p project_root/data/Mouse_Brain
   cd project_root/data/Mouse_Brain
   mkdir -p feature_expression image
   cd feature_expression
   curl -C - -O https://demo.stomicsdb.tech/C04042E2_Mouse_Whole_Brain_Stereo-seq_FF_V1.3_ssDNA/outs/C04042E2.adjusted.cellbin.gef
   curl -C - -O https://demo.stomicsdb.tech/C04042E2_Mouse_Whole_Brain_Stereo-seq_FF_V1.3_ssDNA/outs/C04042E2.cellbin.gef
   curl -C - -O https://demo.stomicsdb.tech/C04042E2_Mouse_Whole_Brain_Stereo-seq_FF_V1.3_ssDNA/outs/C04042E2.tissue.gef

   cd ../image
   curl -C - -O https://demo.stomicsdb.tech/C04042E2_Mouse_Whole_Brain_Stereo-seq_FF_V1.3_ssDNA/outs/C04042E2_ssDNA_regist.tif
   cd ../


After download, the sample directory should match the layout shown below.

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── Mouse_Brain/
   ├── sample.txt (key sample description file)
   └── results/ (stores analysis outputs)

   data/
   └── Mouse_Brain/
       ├── feature_expression   *required at least
       │   ├── C04042E2.tissue.gef
       │   ├── C04042E2.cellbin.gef
       │   ├── C04042E2.adjusted.cellbin.gef
       └── image/   *required at least
            └── C04042E2_ssDNA_regist.tif



Input validation logic
----------------------

对于一份标准的空间转录组分析流程,Spatialsnake仅支持一种数据格式的摄取，即选择一个bin_size 或者SAW细胞分割结果cellbin/adjusted.cellbin 文件进行摄取
这样处理既能深入探究该分辨率下的分析结果,同时也能节省分析内存。对于选取,正如visium HD 的bin选取,我们建议您选择一个bin_size,例如20,50等,或cellbin adjusted_cellbin
并将此字段填写入sample.txt文件中
同时我们也支持您将多个格式进行写入，若有需求，请以逗号分隔填写

我们以cellbin结果进行演示,请复制第一个示例手动写入sample.txt中

Example ``sample.txt``
----------------------

``single_analysis``:

.. code-block:: text

   sample_id input_path bin_size
   Mouse_Brain data/Mouse_Brain cellbin

``多个数据bin_size``:

.. code-block:: text

   sample_id input_path bin_size
   Mouse_Brain data/Mouse_Brain 20,50

Run the command
------------------------------

我们只提供最小的命令,请根据您的需求进行多余参数修改

.. code-block:: bash

   spatialsnake single_analysis sample.txt stereo-seq --option=integrate

Output structure after ingestion
--------------------------------

.. code-block:: text

   results/
   ├── Mouse_Brain/
      └── integrate/
          ├── Mouse_Brain.zarr
          ├── total.png
          ├── total_umi_by_sample.png
          ├── total_genes_by_sample.png
          ├── genes_by_sample.png
          └── scatter.png


Output summary
--------------

- Main output: ``results/<sample>/integrate/<sample>.zarr``
- Additional output for comparison analysis: ``results/merge_data/integrate/concatenated_sdata.zarr``
- Additional QC plots: the ingestion script writes five QC figures into the ``integrate`` directory. These files are generated during execution even though they are not explicitly listed in the Snakemake ``output`` declaration.

Suggested figure content
------------------------

您已经通过此教程将你的数据的摄取为一个zarr对象,后续core_analysis 请参考 :doc:`/core_analysis/index.rst`。我们推荐您先使用示例数据进行core_analysis的基本分析学习。若您想节约时间直接对当前的数据进行后续分析，我们也在每个步骤的开头进行了基本的说明。
您只需按照教程将样本名称与基本参数根据平台进行修改即可进行后续分析  :doc:`/core_analysis/preprocessing.rst`。
If you want to run multi-sample integration analysis, continue to :doc:`/integration_analysis/multi_sample_integration`.

