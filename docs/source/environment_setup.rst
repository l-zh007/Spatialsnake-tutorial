安装与环境配置
==============

本章提供一套稳妥的环境配置流程，适合首次上手用户直接复制执行。

系统准备
--------

建议环境：

- Linux
- Conda 或 Mamba
- 至少 16 CPU 线程和 64 GB 内存用于中等规模样本

创建环境
--------

.. code-block:: bash

   conda create -n spatialsnake python=3.10 -y
   conda activate spatialsnake
   pip install --upgrade pip
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

生成默认配置模板
----------------

可按阶段自动生成配置文件模板：

.. code-block:: bash

   spatialsnake produce-file --option=integrate
   spatialsnake produce-file --option=preprocess
   spatialsnake produce-file --option=clustering

.. note::

   初学者建议先使用命令行参数跑通，再逐步把参数迁移到 ``config.yaml`` 管理。
