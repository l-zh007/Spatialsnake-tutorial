Format Conversion Tool (``transform``)
======================================

``transform`` converts data among ``zarr``, ``h5ad``, and ``seurat`` (``.rds``) formats so that you can continue spatial transcriptomics analysis in different software ecosystems.

For the configuration reference, see :doc:`../config_reference/transform_yaml`.


Typical use cases
-----------------

1. You want to export a Spatialsnake ``zarr`` object to the Scanpy ecosystem as ``h5ad``.
2. You already have an ``h5ad`` object and want to convert it back to ``zarr`` for use in Spatialsnake.
3. You want to convert an object to Seurat ``.rds`` format.


Before you start
----------------

Make sure that:

1. 已经安装必要的软件包,通常已经执行命令 ``spatialsnake --install-packages``.
2. 此转换可能会因格式问题而缺失部分已经分析的数据,请根据你的操作目的进行核对,spatialsnake只保证基础的数据成功转换.
3. Sufficient disk space is available, because ``zarr -> seurat`` creates an intermediate ``h5ad`` file.


General command template
------------------------

.. code-block:: bash

   spatialsnake useful_tool --option=transform <INPUT> --transform_from=<src> --transform_to=<dst> --output_dir=results/useful_results


Scenario 1: ``zarr -> h5ad``
----------------------------

Convert a ``zarr`` object into ``h5ad`` so that it can be used in Scanpy.

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotation/S1.zarr --transform_from=zarr --transform_to=h5ad --save_image=True --output_dir=results/useful_results

Notes:

- ``--save_image=True`` attempts to preserve spatial image information.
- Multiple input ``zarr`` objects are supported and can be combined into one ``h5ad`` output.
- The default output filename uses the basename of the first input, for example ``S1.h5ad``.


Scenario 2: ``h5ad -> zarr``
----------------------------

Convert ``h5ad`` back into ``zarr`` so that the object can re-enter the Spatialsnake workflow.

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/useful_results/S1.h5ad --transform_from=h5ad --transform_to=zarr --output_dir=results/useful_results

Notes:

- The current implementation is best suited to a single ``h5ad`` input.
- If multiple ``h5ad`` files are provided, the current script writes out the last loaded object, so multi-input use is not recommended.


Scenario 3: ``h5ad -> seurat`` (``.rds``)
-----------------------------------------

Convert ``h5ad`` into a Seurat ``.rds`` object by calling an R script.

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/useful_results/S1.h5ad --transform_from=h5ad --transform_to=seurat --type=st --output_dir=results/useful_results

Available ``--type`` values:

- ``st``: spatial transcriptomics (default)
- ``sc``: single-cell


Scenario 4: ``zarr -> seurat`` (``.rds``)
-----------------------------------------

This mode first converts ``zarr`` into an intermediate ``h5ad`` file and then continues to ``.rds``.

.. code-block:: bash

   spatialsnake useful_tool --option=transform results/S1/annotation/S1.zarr --transform_from=zarr --transform_to=seurat --save_image=True --type=st --output_dir=results/useful_results

The output usually includes:

- ``S1.h5ad`` (intermediate file)
- ``S1.rds`` (final Seurat file)


Key parameters in practice
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 20 56

   * - Parameter
     - Typical values
     - Description
   * - ``--transform_from``
     - ``zarr`` / ``h5ad``
     - Specifies the input format
   * - ``--transform_to``
     - ``h5ad`` / ``zarr`` / ``seurat``
     - Specifies the output format
   * - ``--save_image``
     - ``True`` / ``False``
     - Whether to preserve image information when converting from ``zarr`` to ``h5ad`` or in the first step of ``zarr -> seurat``
   * - ``--type``
     - ``st`` / ``sc``
     - Data type used when converting to Seurat; default is ``st``
   * - ``--output_dir``
     - ``results/useful_results``
     - Output directory


How to validate the results
---------------------------

1. Check whether the target file (``.h5ad``, ``.zarr``, or ``.rds``) has been generated in the output directory.
2. If the target is Seurat, also confirm that the intermediate ``.h5ad`` file was created successfully.
3. Open the result with the appropriate downstream tool to make sure the object loads correctly.


Common errors and how to fix them
---------------------------------

1. The workflow exits immediately because input and output formats are identical

   - Cause: ``--transform_from`` and ``--transform_to`` were set to the same value.
   - Fix: change one of them so that the source and target formats differ.

2. ``Rscript`` fails during Seurat conversion

   - Cause: the R environment is missing or required packages are not installed.
   - Fix: first test ``Rscript --version`` on the command line, then install the required R packages.

3. The intermediate ``h5ad`` file is not generated during ``zarr -> seurat``

   - Cause: the first step from ``zarr`` to ``h5ad`` failed.
   - Fix: run ``zarr -> h5ad`` separately first and confirm that the object and image information can be converted successfully.


.. note::
   此模块我们运用了 Pavel Mazin 等人开发的开源实用软件包schard,显然对于格式转换这一功能存在许多实用的工具例如 ``SeuratDisk ``,但经过比较,我们发现schard的功能与执行步骤更适配于Spatialsnake的分析流程且转换更稳定.
   更多信息可查看: `schard <https://github.com/cellgeni/schard>`_