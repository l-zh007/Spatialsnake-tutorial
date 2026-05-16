How to install Spatialsnake?
============================

.. important::
   请确保你的 linux 系统中包含基础的运行软件，例如 `conda <https://www.anaconda.com/docs/getting-started/miniconda/install/overview>`_ / `git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_，请自行安装 miniconda 或者 conda 中的其中一种，同时也可自行安装 Mamba 加速进行环境构建。

Option 1: Install Spatialsnake from pypi
----------------------------------------

.. code-block:: bash

   ## STEP 1: Create conda environment with conda
   conda config --add channels defaults && conda config --add channels bioconda && conda config --add channels conda-forge
   conda create -n spatialsnake_env python=3.12.11 snakemake-minimal=9.8.1 r-base=4.4.0 -y   # 创建和配置spatialsnake所需的底层环境

.. code-block:: bash

   ## STEP 2: Activate the conda environment and install R packages
   conda activate spatialsnake_env 
   conda install -c conda-forge r-optparse r-tidyverse r-future r-jsonlite r-rcolorbrewer r-patchwork r-cowplot r-pheatmap r-seurat r-remotes r-biocmanager r-presto r-nmf r-circlize
   conda install -c bioconda bioconductor-annotationdbi bioconductor-complexheatmap bioconductor-clusterprofiler bioconductor-edger bioconductor-org.hs.eg.db bioconductor-org.mm.eg.db bioconductor-rhdf5 bioconductor-biocneighbors
   conda install -c conda-forge bbknn cython

.. code-block:: bash

   ## STEP 3: install Spatialsnake from pypi
   pip install spatialsnake
   spatialsnake --version  # check the version of spatialsnake installed

   # if you want to use the extended features, install the following packages to use the whole spatialsnake package.[downstream_analysis and utility tools]
   pip install spatialsnake[extended]
   spatialsnake --install-packages


Option 2: Install Spatialsnake from conda
-----------------------------------------

.. code-block:: bash

   ## STEP 1: Create conda environment with conda
   conda config --add channels defaults && conda config --add channels bioconda && conda config --add channels conda-forge
   conda create -n spatialsnake_env python=3.12.11 snakemake-minimal=9.8.1 r-base=4.4.0 -y   # 创建和配置spatialsnake所需的底层环境
   conda activate spatialsnake_env 
   conda install spatialsnake -c bioconda -c conda-forge

   spatialsnake --version  # check the version of spatialsnake installed
   # if you want to use the extended features, install the following packages to use the whole spatialsnake package.[downstream_analysis and utility tools]
   pip install spatialsnake[extended]
   spatialsnake --install-packages


Option 3: Install Spatialsnake from source code
-----------------------------------------------

.. code-block:: bash

   ## STEP 1: Create conda environment with conda
   conda config --add channels defaults && conda config --add channels bioconda && conda config --add channels conda-forge
   conda create -n spatialsnake_env python=3.12.11 snakemake-minimal=9.8.1 r-base=4.4.0 -y   # Create a conda environment with the required packages

.. code-block:: bash

   ## STEP 2: Activate the conda environment and install R packages
   conda activate spatialsnake_env 
   conda install -c conda-forge r-optparse r-tidyverse r-future r-jsonlite r-rcolorbrewer r-patchwork r-cowplot r-pheatmap r-seurat r-remotes r-biocmanager r-presto r-nmf r-circlize
   conda install -c bioconda bioconductor-annotationdbi bioconductor-complexheatmap bioconductor-clusterprofiler bioconductor-edger bioconductor-org.hs.eg.db bioconductor-org.mm.eg.db bioconductor-rhdf5 bioconductor-biocneighbors
   conda install -c conda-forge bbknn cython

   # make sure your git is installed
   git clone https://github.com/zhenghlin/spatialsnake.git
   cd spatialsnake
   python -m pip install .
   python -m pip install ".[extended]"
   spatialsnake --version  # check the version of spatialsnake installed
   spatialsnake --install-packages # install the required R packages from github which are not available in the pypi or bioconda


.. note::

  如果您遇到了环境配置出错问题，请在github issue上留言，我们会尽快回复您。 环境中所用到的关键包版本信息可通过仓库中的requirements.txt/requirements-extended.txt文件查看。
  我们推荐您创建一个新conda环境来安装Spatialsnake，以避免与您的其他环境冲突。
  同时若您的硬件性能有限，建议使用最小化的spatialsnake版本，以减少安装大量依赖。

若您缺少只安装Spatialsnake的最小化版本,可使用的分析模块有:

- integrate
- preprocess
- clustering
- reclustering
- annotation_help
- annotation*mannul/cell2Location
- reclustering
- reannotation
- utility_tools*merge/split

若您同时使用包内置命令 ``spatialsnake --install-packages`` 安装扩展功能,则可增加使用的分析模块有:

- annotation*RCTD
- compare_stage
- utility_tools*transforms
- downstream_analysis-banksy
- downstream_analysis-cellchat

若您同时执行安装了 ``spatialsnake[extended]`` 版本,则可增加使用的分析模块有:

- downstream_analysis-*

For a basic introduction to the command-line workflow, see :doc:`usage`
