How to install Spatialsnake?
==============

创建环境(待定)
--------

.. code-block:: bash
   ## Create conda environment with the environment.yml file in github code page
   conda env create -f environment.yml -n spatialsnake_env     ## [or setting your own conda env name]
   conda activate spatialsnake_env
   pip install spatialsnake

如果你已下载项目源码，也可以在源码目录安装：

.. code-block:: bash

   cd /path/to/spatialdata/spatialsnake
   pip install -e .

检查是否安装成功
----------------

.. code-block:: bash

   spatialsnake --help
   spatialsnake --version

R 环境配置
----------------

.. code-block:: bash

   spatialsnake --install_packages
