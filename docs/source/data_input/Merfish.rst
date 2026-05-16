MERFISH Input Tutorial
======================

Required files
--------------

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - Filename / pattern
     - Required
     - Format
     - Description
   * - ``**/cell_by_gene.csv``
     - required
     - CSV
     -  Counts file.
   * - ``**/detected_transcripts.csv``
     - required
     - CSV
     - Transcript file.
   * - ``**/cell_boundaries.parquet``
     - required
     - Parquet
     - Cell polygon boundaries.
   * - ``**/cell_metadata.csv``
     - required
     - Parquet
     - Per-cell metadata file.
   * - ``**/images/micron_to_mosaic_pixel_transform.csv``  ``**/images/**_z*.tif`` ``**/images/manifest.json``
     - No
     - TIFF/OME.TIFF/OME-XML
     - 包含TIFF图像信息,因Merfish 版本不同而不同,请参考Merfish 文档，若无图像信息Spatialsnake默认将不会读取此文件。请确保你的数据至少为Merfish2 版本。

根据Vizgen公司旗下MERFISH平台输出文件层级结构,构建基本的文件层级结构,将你下载的文件存储到data目录下: ``region_0`` 可替换为自定义样本名称。

例如:

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── region_0/
   ├── sample.txt (key sample description file)
   └── results/ (stores analysis outputs)

   data/
   └── region_0/
       ├── cell_by_gene.csv
       ├── detected_transcripts.csv.gz
       ├── ......
       └── images/
           ├── morphology_mip.ome.tif
           ├── ......
           └── manifest.json

由于3D多切片技术与相关分析流程还在开发中,这里请选择其中一个Region 进行分析，若后续有权威的科研技术进展，我们将更新此教程。

Where these files come from
---------------------------

- Official download: standard Vizgen MERSCOPE/MERFISH output directory
- Experimental output: cell and transcript files exported by a laboratory MERFISH pipeline
- Placeholder usage: you can first write ``/path/to/merfish_sample`` and replace it later with the real directory


Demo 使用示例演示
------------------------

``run_type: Merfish``. In this tutorial, we assume a standard MERFISH output directory prepared from a public or in-house Vizgen-style dataset.
One public example release is available from the Vizgen Breast Cancer Tissue Microarray Region_R1:
`Vizgen MERFISH Breast Cancer Dataset <https://console.cloud.google.com/storage/browser/vz-merfish2-showcase/202409242358_240916JHHUBC0005XQ-V2V-HubcTMA-V2-BY_VMSC02511>`_

这里我们将使用上述的下载链接所包含的Region_R1 Breast Cancer Tissue Microarray数据进行Demo读取演示，由于存储的文件较大且包含多个文件以及公共数据集存储方式,请自行按照层级下载。
确保你已经通过先前的教程进行了基础工作目录的创建。

Example setup:

.. code-block:: bash

   mkdir -p project_root/data/Mouse_Brain
   cd project_root/data/Mouse_Brain

After download, the sample directory should match the layout shown below.

Example directory layout
------------------------

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── Breast_Cancer/
   ├── sample.txt (key sample description file)
   └── results/ (stores analysis outputs)

   data/
   └── Breast_Cancer/
       ├── cell_by_gene.csv
       ├── detected_transcripts.csv.gz
       ├── ......
       └── images/
           ├── morphology_mip.ome.tif
           ├── ......
           └── manifest.json

``single_analysis``:

.. code-block:: text

   sample_id input_path
   Mouse_Brain data/Mouse_Brain

   note::
      如果你想进行多样本分析,请再学习完成本页面的内容后参考:doc:`/integration_analysis/multi_sample_integration` 进行配置与相关命令的学习。相较于单样本分析,多样本分析需要多个
      个样本data与sample.txt配置,同理每个样本的data路径与sample_id需要与sample.txt中配置的路径与sample_id一致。

这里只给出运行数据读取模块的最小分析代码，相关更多参数设置请参考对应配置文件 `../config_reference/integrate.yaml`。

.. code-block:: bash

   spatialsnake single_analysis sample.txt Merfish --option=integrate


Output structure after ingestion
--------------------------------

.. code-block:: text

   project_root/
   ├── data/ (stores your raw data)
   │   └── Breast_Cancer/
   ├── sample.txt (key sample description file)
   ├──log/
   └── results/ (stores analysis outputs)

   results/
   └── Breast_Cancer/
      └── integrate/
          ├── Breast_Cancer.zarr
          ├── total.png
          ├── total_umi_by_sample.png
          ├── total_genes_by_sample.png
          ├── genes_by_sample.png
          └── scatter.png


- Main output: ``results/<sample>/integrate/<sample>.zarr``
- Additional output for comparison analysis: ``results/merge_data/integrate/concatenated_sdata.zarr``
- Additional QC plots: single-sample ingestion writes five QC figures into the ``integrate`` directory. These files are generated in practice even though they are not explicitly declared in the Snakemake ``output`` section.

您已经通过此教程将你的数据的摄取为一个zarr对象,后续core_analysis 请参考 :doc:`/core_analysis/index`。我们推荐您先使用示例数据进行core_analysis的基本分析学习。若您想节约时间直接对当前的数据进行后续分析，我们也在每个步骤的开头进行了基本的说明。
您只需按照教程将样本名称与基本参数根据平台进行修改即可进行后续分析  :doc:`/core_analysis/preprocess`。
If you want to run multi-sample integration analysis, continue to :doc:`/integration_analysis/multi_sample_integration`.
