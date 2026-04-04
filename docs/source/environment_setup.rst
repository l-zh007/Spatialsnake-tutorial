How to install Spatialsnake?
============================

Create the environment
----------------------

.. code-block:: bash

   ## Create conda environment with the environment.yml file in github code page
   conda env create -f environment.yml -n spatialsnake_env     ## [or setting your own conda env name]
   conda activate spatialsnake_env
   pip install spatialsnake

If you have already downloaded the source code, you can also install it from the project directory:

.. code-block:: bash

   cd /path/to/spatialdata/spatialsnake
   pip install -e .

Check whether the installation was successful
---------------------------------------------

.. code-block:: bash

   spatialsnake --help
   spatialsnake --version

Configure the R environment
---------------------------

.. code-block:: bash

   spatialsnake install-packages



For a basic introduction to the command-line workflow, see :doc:`project_layout`
