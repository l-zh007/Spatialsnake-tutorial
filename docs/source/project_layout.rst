How to use Spatialsnake?
================================================

How does the command line work?
--------------------------------------------------------------

The command-line interface provides several entry points: the main workflow, utility tools, configuration template generation, package installation, help, and version display.
``<>`` indicates required arguments, ``[]`` indicates optional arguments, and ``[options]`` indicates additional parameter settings. Arguments must follow the documented syntax, including prefixes such as ``--`` and ``=`` where required.

.. code-block:: bash

  spatialsnake <command> <INPUT> <TYPE> [--option=<analysis_option>] [options] # main workflow
  spatialsnake useful_tool [--option=<ways>] <INPUT> [options] # utility tools
  spatialsnake produce-file [--option=<analysis_option>] # generate configuration templates
  spatialsnake install-packages # install required R packages
  spatialsnake (-h | --help) # show help
  spatialsnake --version # show version

Separate arguments with spaces
------------------------------------------------------------

- ``<command>``: main workflow channel. Choose ``single_analysis`` or ``compare_analysis`` according to your analysis strategy.
- ``<INPUT>``: input sample file. In the main workflow, this is usually ``sample.txt``, which stores sample IDs and data paths. In ``useful_tool``, it is one or more object paths.
- ``<TYPE>``: data type. Supported values are ``visium``, ``visium_segment``, ``visium_HD``, ``xenium``, ``Merfish``, and ``stereo_seq``.
- ``--option=<analysis_option>``: analysis module selection. Main workflow options include ``integrate``, ``preprocess``, ``clustering``, ``reclustering``, ``annotation_help``, ``annotation``, ``advance_analysis``, and ``compare_stage``. Utility workflow options include ``splitting``, ``merge``, and ``transform``.


命令行参数设置方法(``[options]``)
------------------------------------------------

Spatial transcriptomics analysis involves many important parameters, and these settings directly affect result quality and reliability. When running Spatialsnake, you should adjust parameters according to your specific dataset and study design.
You can set supported parameters directly on the command line. In addition to the standard command structure, append arguments in the form ``--parameter_name=value``.
To see which parameters are available from the command line, run ``spatialsnake -h``.

Example1: running the following command will ``preprocess`` the ``single`` ``visium`` data in ``sample.txt`` in parameter of ``--min_cells=3`` and ``--min_genes=200``:

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=preprocess --min_cells=3 --min_genes=200 --mt_threshold=50

Example2: running the following command will ``transform`` the ``zarr`` file in ``results/S1/annotation/S1.zarr`` to ``h5ad`` format, and save the image in ``results/useful_results`` directory.

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotation/S1.zarr --transform_from=zarr --transform_to=h5ad --save_image=True --output_dir=results/useful_results

以上是基础的分析启动命令行使用教程，剩余的命令行使用与组合会在后续的分析教程中随同展现使用。

如何使用yaml文件进行更丰富的参数设置? (``configfile``)
----------------------------------------------------------------------------

Since the workflow contains many parameters, only the most important and commonly used ones are exposed directly on the command line. All other settings can be configured through a ``.yaml`` file.

How do you obtain a YAML template?

.. code-block:: bash

   spatialsnake produce-file --option=<analysis_option> #analysis_option can be preprocess, advance_analysis, splitting, merge, transform......

These commands generate the corresponding template files, such as ``preprocess.yaml``, which you can then edit.

Each YAML template includes default values and inline explanations for the parameters. This is intended to help you understand the purpose of each setting and become familiar with the analysis workflow more quickly.

.. code-block:: yaml

   option: "preprocess"           # analysis stage, consistent with --option
   channel: "compare_analysis"    # analysis mode single sample or multi-sample comparison
   run_type: "visium"             # spatial transcriptomics platform type
   sample_list: "sample.txt"      # path to the sample description file
   results_folder: "results"      # root output directory
   min_cells: 50                  # minimum cells per sample; samples below this threshold are filtered
   min_genes: 50                  # minimum genes per sample; samples below this threshold are filtered
   mt_threshold: 30.0             # mitochondrial gene threshold; cells above this proportion are filtered
   batch_method: "harmony"        # batch correction method, choose from harmony or combat

Apply the YAML file with ``--configfile``

.. code-block:: bash

   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile=preprocess.yaml
   spatialsnake compare_analysis sample.txt visium --option=preprocess --configfile=preprocess.yaml --mt_threshold=60

.. note::
   Parameters provided through ``--configfile`` have lower priority than parameters set directly on the command line.
   For example, in the second command, if ``preprocess.yaml`` also defines ``mt_threshold``, the final value used is ``60`` from the command line.
   For beginners, we recommend starting with direct command-line parameters.


Originally Step: Prepare the working directory first
--------------------------------------------------------------------------------------------------------

.. code-block:: text

   project_root/ (current working directory)
   ├── data/ (stores your raw data)
   ├── sample.txt (key sample description file)
   ├── results/ (stores analysis outputs; generated automatically)
   └── <analysis_option>.yaml (optional configuration file)

.. code-block:: bash

   mkdir -p project_root/data project_root/results
   touch project_root/sample.txt

Minimal examples of ``sample.txt``
--------------------------------------------------------------------

 ``sample.txt`` 是一份以空格分隔的样本信息表,为了让用户熟悉及其重要的运行输入文件与配置信息,Spatialsnake将 样本id 输入文件目录/路径 分组信息 bin分辨率选择 重要输入文件等top级参数信息在此文件进行配置
 样本信息表是第一类型命令中每个分析模块的必要输入,根据模块的不同我们将对其中的内容进行不同的使用,请根据具体需求进行配置。

例如对于single_analysis分析stereoseq数据命令,我们需要配置的sample.txt文件如下:

.. code-block:: text

   sample_id input_path bin_size
   Mouse_Brain data/Mouse_Brain cellbin

而对于downstream_analysis 中的cellchat模块visium数据分析,我们需要配置sample.txt文件格式如下:

.. code-block:: text

   sample_id   input_path  scale_factor_path
   SampleA_Rep1  results/SampleA_Rep1/annotation/SampleA_Rep1.h5ad  results/SampleA_Rep1/scale_factor.json


About Log file
----------------------------

每次运行完成Spatialsnake后，会在 ``project_root`` 目录下生成一个 ``Log/xxx.log`` 目录文件，记录分析过程中所使用的命令与参数。
同时记录真实执行构建的 snakemake 命令。log 文件以时间戳命名，您可以在 ``log/`` 目录下查看对应文件。


.. important::
   如果您对spatialsnake进行空间转录组分析还不熟悉或对scverce生态不熟悉,我们推荐先使用demo数据进行示例分析以了解基本的分析流程 :doc:`core_analysis/index`
   为了简化演示步骤,对于每个空间转录组分析功能的demo示例,我们使用两套数据 Mouse_Brain(visium multi-sample) 与 Colon_Cancer(visium_HD single-sample) 为基础进行所有的示例演示,具体对应使用数据请阅读相应模块教程.同时对于每个平台的单样本读取过程我们也提供了示例数据,但不进行后续的分析.
   如果您对空间转录组分析有一定的了解,或想对自己的数据进行分析, continue to :doc:`data_input/index`.
