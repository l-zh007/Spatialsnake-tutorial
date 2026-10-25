Installing Spatialsnake
=======================

.. important::
   These instructions assume Linux and Conda. Activate the environment before
   using ``python -m pip``; Git is required for source/GitHub installations.
   For Conda setup, see the
   `Miniconda instructions <https://www.anaconda.com/docs/getting-started/miniconda/install/overview>`_.

.. note::
   The updated commands and filenames in these demos require a source checkout
   containing these changes (Option 3). Published version 0.0.6 uses the legacy
   command and output names.

Option 1: Install Spatialsnake from PyPI (recommended)
------------------------------------------------------

.. code-block:: bash

   ## STEPS 1–2: ~25–30 min combined
   ## STEP 1: Create the tested base environment
   conda create -n spatialsnake_env --override-channels -c conda-forge -c bioconda \
     python=3.12.11 snakemake-minimal=9.8.1 r-base=4.4.0 -y
   conda activate spatialsnake_env

.. code-block:: bash

   ## STEP 2: Install the R dependency layer
   conda install --override-channels -c conda-forge -c bioconda \
     r-optparse r-dplyr r-ggplot2 r-readr r-ragg \
     r-seurat r-remotes r-biocmanager r-presto r-nmf r-ggpubr \
     bioconductor-annotationdbi bioconductor-complexheatmap \
     bioconductor-clusterprofiler bioconductor-edger \
     bioconductor-org.hs.eg.db bioconductor-org.mm.eg.db \
     bioconductor-rhdf5 bioconductor-biocneighbors -y

.. code-block:: bash

   ## STEP 3: Install the Spatialsnake base package (~15–20 min)
   python -m pip install spatialsnake
   spatialsnake --version

Optional analysis dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Steps 1–3 provide core analysis. For optional modules, choose one PyTorch
build in Step 4, install the extended Python packages, then complete Step 5.

.. code-block:: bash

   ## OPTIONAL STEP 4A: Choose this command for an NVIDIA GPU
   python -m pip install --index-url https://download.pytorch.org/whl/cu128 \
     "torch==2.8.0"

   ## OPTIONAL STEP 4B: Or choose this command for a CPU-only installation
   # python -m pip install --index-url https://download.pytorch.org/whl/cpu \
   #   "torch==2.8.0"

   ## STEP 4C: Install the extended Python dependencies (~10 min)
   python -m pip install "spatialsnake[extended]"

.. code-block:: bash

   ## STEP 5: Install the remaining built-in R/GitHub dependencies (~25–30 min)
   spatialsnake install-packages

Steps 1–3 provide core analysis. Steps 4–5 add optional analysis dependencies;
choose either Step 4A or Step 4B before Step 4C. Times are approximate for a fresh installation
without cached downloads and vary with network speed and hardware.
Rerun Step 5 if interrupted; installed packages are detected and skipped.

Optional installation check:

.. code-block:: bash

   python -m pip check
   spatialsnake --version


Option 2: Install Spatialsnake from Bioconda
--------------------------------------------

Bioconda is the package entry point. No PyPI installation of Spatialsnake is needed.

.. note::
   The streamlined installer below applies to the next Bioconda release
   containing these changes; the published 0.0.6 installer uses the previous
   automatic PyTorch selection.

.. code-block:: bash

   ## STEP 1: Install Spatialsnake and the Conda dependency layer (~30–45 min)
   conda create -n spatialsnake_env --override-channels -c conda-forge -c bioconda \
     spatialsnake python=3.12.11 r-base=4.4.3 snakemake-minimal=9.8.1 -y
   conda activate spatialsnake_env

   ## STEP 2: Complete the base dependencies (~20–25 min)
   spatialsnake install-packages

The base installer completes packages missing from the Bioconda recipe and
repairs the tested ``setuptools`` / SpatialData compatibility stack. For
advanced analyses, first choose one PyTorch build:

.. code-block:: bash

   ## STEP 3A: NVIDIA GPU with a CUDA 12.8-compatible driver
   python -m pip install --index-url https://download.pytorch.org/whl/cu128 \
     "torch==2.8.0"

   ## STEP 3B: Or choose CPU-only instead
   # python -m pip install --index-url https://download.pytorch.org/whl/cpu \
   #   "torch==2.8.0"

   ## STEP 4: Complete the extended dependencies (~30–40 min, excluding Torch)
   spatialsnake install-packages --extended
   python -m pip check

.. note::

   ``install-packages --extended`` includes the complete base stage, so running
   ``install-packages`` first is optional. The default reuses the selected
   PyTorch 2.8.0 build; no ``--torch-backend`` argument is needed. Analysis uses
   ``device=auto``: available CUDA is used, otherwise CPU; ``device=cpu`` or
   ``device=cuda`` can be specified explicitly. Some R packages come from tested
   GitHub revisions. Rerun the installer after interruption to complete missing
   packages.

Times are approximate references from installation tests, including retries and
version corrections, not guaranteed clean-install timings. Network speed and
Conda solving can substantially change them. Torch was tested with cached
CUDA wheels (~1 min); a fresh CPU/CUDA download takes additional time depending
on bandwidth. The extended installer no longer explicitly installs Napari/Qt.


Option 3: Install Spatialsnake from source code
-----------------------------------------------

Use this option to install the code directly from GitHub.

.. code-block:: bash

   conda create -n spatialsnake_env --override-channels -c conda-forge -c bioconda \
     python=3.12.11 r-base=4.4.0 snakemake-minimal=9.8.1 -y
   conda activate spatialsnake_env

Install the R dependency layer from Option 1, Step 2 in this environment before
continuing:

.. code-block:: bash

   git clone https://github.com/l-zh007/spatialsnake.git
   cd spatialsnake
   python -m pip install .
   spatialsnake --version

For advanced analyses:

.. code-block:: bash

   ## Select either the cu128 or cpu index, as shown in PyPI Step 4
   python -m pip install --index-url https://download.pytorch.org/whl/cu128 \
     "torch==2.8.0"
   python -m pip install ".[extended]"
   spatialsnake install-packages

.. note::

   The source route uses the same PyPI split: ``.[extended]`` installs the
   extended Python dependencies, and ``install-packages`` completes BANKSY and
   the R/GitHub dependencies. The ``--extended`` installer flag is reserved for
   the Bioconda route. If installation fails, please open an issue on GitHub.

For a basic introduction to the command-line workflow, see :doc:`usage`

Installation scope
------------------

PyPI base
~~~~~~~~~

Steps 1–3 install the R layer and ``spatialsnake`` base dependencies.
This provides data ingestion and sample assembly, preprocessing, clustering/reclustering, manual
annotation, and basic object utilities without the torch/scvi stack.
The Step 2 R layer also supports GO/KEGG enrichment and plotting for
``annotation_help``; no additional GitHub plotting package is required.
Step 5 completes the R/GitHub dependencies used by the additional modules.

PyPI extended and built-in packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 4 first installs the user-selected CPU or cu128 PyTorch build, then adds
cell2location, scvi-tools, CellCharter, Squidpy, CellPhoneDB, LIANA, pySCENIC
and napari-spatialdata. Step 5 adds BANKSY/pybanksy and the remaining R/GitHub
packages used by RCTD and CellChat.

Bioconda base
~~~~~~~~~~~~~

Bioconda followed by ``install-packages`` covers data ingestion and sample assembly,
preprocessing, clustering/reclustering, annotation help,
manual annotation, common enrichment and utility functions.

Bioconda extended
~~~~~~~~~~~~~~~~~

``install-packages --extended`` includes the complete Bioconda base stage and
reuses the manually selected CPU or cu128 PyTorch build and adds cell2location, scvi-tools,
CellCharter, Squidpy, CellPhoneDB, LIANA, pySCENIC, BANKSY, RCTD and CellChat.

Validation includes dependency checks, SpatialData object I/O and small-data
CLI analyses for the extended modules. It does not establish convergence or
biological validity for a full dataset or validate every platform and parameter.
