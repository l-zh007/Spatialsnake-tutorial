Installing Spatialsnake
=======================

.. important::
   Make sure your Linux system already includes basic required software such as `conda <https://www.anaconda.com/docs/getting-started/miniconda/install/overview>`_ and `git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_. Install either Miniconda or Conda before proceeding. You may also install Mamba if you want faster environment solving.

Option 1: Install Spatialsnake from PyPI
----------------------------------------

.. code-block:: bash

   ## STEP 1: Create conda environment with conda
   conda config --add channels defaults && conda config --add channels bioconda && conda config --add channels conda-forge
   conda create -n spatialsnake_env python=3.12.11 snakemake-minimal=9.8.1 r-base=4.4.0 -y   # create the base environment required for Spatialsnake

.. code-block:: bash

   ## STEP 2: Activate the conda environment and install R packages
   conda activate spatialsnake_env 
   conda install -c conda-forge r-optparse r-tidyverse r-future r-jsonlite r-rcolorbrewer r-patchwork r-cowplot r-pheatmap r-seurat r-remotes r-biocmanager r-presto r-nmf r-circlize
   conda install -c bioconda bioconductor-annotationdbi bioconductor-complexheatmap bioconductor-clusterprofiler bioconductor-edger bioconductor-org.hs.eg.db bioconductor-org.mm.eg.db bioconductor-rhdf5 bioconductor-biocneighbors
   conda install -c conda-forge bbknn cython

.. code-block:: bash

   ## STEP 3: Install Spatialsnake from PyPI
   pip install spatialsnake
   spatialsnake --version  # check the version of spatialsnake installed

   # Install optional dependencies for downstream analyses and utility tools.
   pip install "spatialsnake[extended]"
   spatialsnake install-packages


Option 2: Install Spatialsnake from conda
-----------------------------------------

.. code-block:: bash

   ## STEP 1: Install Spatialsnake and conda-managed dependencies
   conda create -n spatialsnake_env -c conda-forge -c bioconda spatialsnake -y
   conda activate spatialsnake_env

   spatialsnake --version  # check the version of spatialsnake installed
   # Complete the minimal conda installation with pip-only core packages.
   spatialsnake install-packages

   # Optional: install downstream Python packages, pybanksy, and R/GitHub packages.
   spatialsnake install-packages --extended


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
   spatialsnake install-packages # Install required R packages that are not distributed through PyPI or Bioconda.


.. note::

  If you encounter installation or environment errors, please open an issue on GitHub and we will respond as soon as possible. Version information for key dependencies can be found in ``requirements.txt`` and ``requirements-extended.txt`` in the repository.
  We recommend installing Spatialsnake in a fresh conda environment to avoid conflicts with other existing environments.
  If your hardware resources are limited, we recommend starting with the minimal Spatialsnake installation to avoid pulling in a large number of optional dependencies.

With the minimal Spatialsnake installation, the following modules are available:

- integrate
- preprocess
- clustering
- reclustering
- annotation_help
- annotation (manual and cell2location branches)
- reannotation
- utility tools: merge and splitting

If you additionally run the built-in command ``spatialsnake install-packages --extended``
for downstream Python packages, conflict-managed Python packages, and R/GitHub
packages, the following modules become available:

- annotation (RCTD branch)
- compare_stage
- utility tool: transform
- downstream analysis: BANKSY
- downstream analysis: CellChat

If you install the ``spatialsnake[extended]`` package, the following additional modules become available:

- all optional downstream-analysis modules

For a basic introduction to the command-line workflow, see :doc:`usage`
