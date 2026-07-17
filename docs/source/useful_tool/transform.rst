Format Conversion Tool (``transform``)
======================================

``transform`` provides a lightweight interface for exporting a completed
Spatialsnake analysis to Scanpy (``.h5ad``) or Seurat (``.rds``), and for
importing a single ``.h5ad`` object into SpatialData (``.zarr``). The command
continues to run directly through the Python utility entry point; it does not
start a Snakemake workflow.

For the configuration reference, see :doc:`../config_reference/transform_yaml`.


Typical use cases
-----------------

1. Export one or more Spatialsnake ``zarr`` objects to one combined ``h5ad``
   file for Scanpy-compatible downstream analysis.
2. Export ``zarr`` or ``h5ad`` data to a Seurat ``.rds`` object using Schard.
3. Convert one legacy spatial or single-cell ``h5ad`` object to SpatialData.

The utility performs format conversion only. It does not normalize expression,
correct batch effects, register tissue sections, or make results from different
platforms biologically comparable.


Before you start
----------------

1. Install the required conversion packages with:

   .. code-block:: bash

      spatialsnake install-packages

   Seurat conversion requires the tested Schard ``1.1.0`` release. The command
   stops with an explicit version message if an older release is active.

2. In Spatialsnake output, ``adata.raw.X`` represents the original count
   matrix, whereas ``adata.X`` is normally log-normalized. With
   ``seurat_matrix=auto``, valid non-negative integer ``raw.X`` is therefore
   exported to the Seurat ``counts`` layer. If ``raw`` is absent, integer ``X``
   is treated as counts and non-integer ``X`` is written to a data-only assay.

3. Scanpy ``normalize_total(target_sum=1e4)`` followed by ``log1p`` and Seurat
   ``LogNormalize(scale.factor=10000)`` apply equivalent per-cell library-size
   scaling and logarithmic transformation when they start from the same count
   matrix. The converter does not call ``NormalizeData`` when raw counts are
   exported; normalization may be performed once in Seurat if required.

4. ``save_image=true`` exports downsampled legacy images when supported. This
   is intended for convenient visualization and is not a lossless copy of the
   original image pyramid, cell boundaries, labels, or coordinate transforms.


General command template
------------------------

.. code-block:: bash

   spatialsnake useful_tool --option=transform <INPUT>... \
     --transform_from=<zarr|h5ad> \
     --transform_to=<h5ad|zarr|seurat> \
     --output_dir=results/useful_results

The supported directions are ``zarr -> h5ad``, ``zarr -> seurat``,
``h5ad -> zarr``, and ``h5ad -> seurat``. Seurat is an output format only.
The output basename is taken from the first input. Every run writes the
converted object and ``<basename>_transform_report.csv``; multiple inputs are
combined into that single named output.


Scenario 1: ``zarr -> h5ad``
----------------------------

Convert one spatial object for use in Scanpy:

.. code-block:: bash

   spatialsnake useful_tool --option=transform \
     results/S1/annotation/S1.zarr \
     --transform_from=zarr --transform_to=h5ad \
     --save_image=true --output_dir=results/useful_results

Multiple Zarr inputs or multiple regions are converted library by library and
combined on disk using an outer gene join. Missing genes are represented by
zeros, ``library_id`` identifies each library, and observation IDs are changed
only when a duplicate exists across libraries. ``X``, ``raw``, compatible
layers, observation metadata, spatial coordinates, and within-library ``obsp``
graphs are retained. Pairwise graphs are block diagonal, so conversion does not
introduce cross-library edges.

If a Zarr object contains more than one table, specify the intended table:

.. code-block:: bash

   ... --table_key=table

For example, a three-library object produced by an earlier sample merge can be
exported directly without splitting it again:

.. code-block:: bash

   spatialsnake useful_tool --option=transform \
     results/useful_results/group_Group1.zarr \
     --transform_from=zarr --transform_to=h5ad \
     --save_image=true --output_dir=results/useful_results

This command produces ``group_Group1.h5ad`` and
``group_Group1_transform_report.csv``. When library-specific gene-level QC
columns in ``var`` contain different values, the first non-missing value is
retained and a warning is recorded. Expression matrices and observation-level
metadata are unaffected; use the original per-library objects when
sample-specific gene-level QC statistics are required.


Scenario 2: ``h5ad -> zarr``
----------------------------

.. code-block:: bash

   spatialsnake useful_tool --option=transform \
     results/useful_results/S1.h5ad \
     --transform_from=h5ad --transform_to=zarr \
     --output_dir=results/useful_results

Exactly one input is accepted. A legacy spatial H5AD containing
``obsm['spatial']`` and ``uns['spatial']`` is reconstructed with a table,
coordinates, Shapes, and available downsampled images. A conventional
single-cell H5AD becomes a table-only SpatialData object. Existing observation
names and ``cell_id`` values are retained. Use the :doc:`merge` utility when
multiple SpatialData objects need to be combined. A table-only result contains
no image, Shapes, or Points element and therefore cannot be spatially rendered
until appropriate spatial elements and coordinate transformations are added.


Scenario 3: ``h5ad -> seurat`` (``.rds``)
-----------------------------------------

Automatic matrix and data-type selection is recommended:

.. code-block:: bash

   spatialsnake useful_tool --option=transform \
     results/useful_results/S1.h5ad \
     --transform_from=h5ad --transform_to=seurat \
     --type=auto --seurat_matrix=auto \
     --output_dir=results/useful_results

Multiple H5AD inputs are combined into one Seurat object and distinguished by
``library_id``. All inputs must resolve to the same matrix semantics: either
counts or normalized data. Mixing count-only and normalized-only inputs in one
assay is rejected rather than silently changing their meaning.

When raw or integer counts are selected, the resulting Seurat v5 assay contains
a ``counts`` layer only. When a non-integer, normalized ``X`` is selected, it
contains a ``data`` layer only. The converter deliberately avoids duplicating
counts into ``data``. Consequently, run ``NormalizeData()`` in Seurat before a
downstream method that requires normalized expression if the exported object
contains only ``counts``.

``type=auto`` selects spatial mode when valid spatial coordinates exist. Native
spatial Seurat conversion is used only when Visium-style library IDs, images,
and scale factors are complete. Xenium, Stereo-seq, MERSCOPE, image-free
Visium HD, and ordinary single-cell objects use Schard's generic conversion;
their spatial coordinates are retained as a dimensional reduction, but cell
boundaries are not represented as a Visium image. Setting ``--type=sc``
explicitly requests this generic single-cell representation even when spatial
coordinates are present.


Scenario 4: ``zarr -> seurat`` (``.rds``)
-----------------------------------------

.. code-block:: bash

   spatialsnake useful_tool --option=transform \
     results/S1/annotation/S1.zarr \
     --transform_from=zarr --transform_to=seurat \
     --type=auto --seurat_matrix=auto --save_image=true \
     --output_dir=results/useful_results

A multi-library object uses the same command. For example:

.. code-block:: bash

   spatialsnake useful_tool --option=transform \
     results/useful_results/group_Group1.zarr \
     --transform_from=zarr --transform_to=seurat \
     --type=auto --seurat_matrix=auto --save_image=true \
     --output_dir=results/useful_results

With complete Visium metadata, this produces one spatial Seurat object with a
separate Seurat image and ``library_id`` for each library. With
``seurat_matrix=auto`` and valid Spatialsnake ``raw.X``, the assay stores the
original integer counts.

The utility first creates a complete temporary H5AD, then generates a minimal
H5AD containing only the selected expression matrix, metadata, coordinates,
and required spatial information for Schard. Temporary files are removed after
the RDS has been validated. Set ``--keep_intermediate=true`` only when the full
H5AD should also be retained as a user-facing output. With the default
``false``, only the RDS and transformation report remain.


Key parameters in practice
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 22 53

   * - Parameter
     - Values / default
     - Description
   * - ``--transform_from``
     - ``zarr``
     - Source format: ``zarr`` or ``h5ad``.
   * - ``--transform_to``
     - ``h5ad``
     - Target format: ``h5ad``, ``zarr``, or ``seurat``.
   * - ``--type``
     - ``auto``
     - ``auto``, ``st``, or ``sc`` for Seurat export. ``auto`` is recommended.
   * - ``--seurat_matrix``
     - ``auto``
     - ``auto`` prefers valid ``raw.X``; ``raw`` requires it; ``X`` explicitly uses ``adata.X``.
   * - ``--table_key``
     - empty
     - SpatialData table to export. An empty value is allowed only for an unambiguous single-table object.
   * - ``--save_image``
     - ``true``
     - Include downsampled legacy image metadata where possible; each complete Visium library becomes a separate Seurat image.
   * - ``--memory_limit_gb``
     - ``0``
     - Explicit Seurat conversion limit. Zero uses 80% of currently available cgroup/system memory.
   * - ``--keep_intermediate``
     - ``false``
     - Retain the complete H5AD made during ``zarr -> seurat``.
   * - ``--output_dir``
     - ``results/useful_results``
     - Destination for the converted object and report.


Memory protection for large data
--------------------------------

The converter preserves sparse matrices and combines libraries on disk. Before
starting Schard, it estimates a conservative peak requirement as approximately
``5 × selected matrix storage + images + 1 GiB``. By default, no more than 80%
of currently available memory is considered safe. If the estimate exceeds the
limit, the program stops before R starts. For large Visium HD data, first try
``--save_image=false``; if the object remains too large, convert samples
separately or run on a machine with more memory. The tool never silently drops
libraries or changes the requested merge mode.


How to validate the results
---------------------------

Each run produces the converted object and
``<basename>_transform_report.csv``. The report records the input libraries,
observations, genes, selected matrix source, target Seurat layer, conversion
mode, image information, memory estimate, and warnings. The utility also
reopens the H5AD, Zarr, or RDS before reporting success and verifies observation
counts, unique IDs, coordinates, and matrix alignment where applicable.

For H5AD output, a minimal Python check is:

.. code-block:: python

   import scanpy as sc

   adata = sc.read_h5ad("results/useful_results/group_Group1.h5ad")
   print(adata.shape)
   print(adata.obs["library_id"].value_counts())
   print(adata.obsm["spatial"].shape)
   print(adata.raw is not None)

For Seurat output, inspect the assay layers, libraries, and images before
continuing the analysis:

.. code-block:: r

   library(Seurat)
   object <- readRDS("results/useful_results/group_Group1.rds")
   Layers(object[[DefaultAssay(object)]], search = NA)
   table(object$library_id)
   Images(object)

   # Run this only when the object has a counts layer but no normalized data.
   object <- NormalizeData(object)


Common errors and how to fix them
---------------------------------

1. ``table_key`` is ambiguous

   - The Zarr contains multiple tables. Set ``--table_key`` to the table that
     carries the expression matrix to export.

2. ``raw.X`` is missing or is not an integer count matrix

   - Use ``--seurat_matrix=X`` only if exporting ``X`` is intentional. A
     non-integer ``X`` becomes a data-only assay and must not be interpreted as
     counts.

3. Estimated memory exceeds the safety limit

   - Disable image export, process samples separately, or increase available
     memory. Increase ``memory_limit_gb`` only when the stated memory is
     genuinely available.

4. Spatial data use the generic Seurat fallback

   - Native spatial conversion requires complete Visium-style image metadata.
     Other platforms still retain expression, observation metadata, and
     coordinates, but do not gain an artificial Visium image representation.

5. Schard version validation fails

   - Run ``spatialsnake install-packages`` to install the tested Schard 1.1.0
     release. Confirm the active R library with
     ``Rscript -e 'packageVersion("schard")'``.

6. Gene-level metadata conflict warnings appear during a multi-library export

   - Columns such as per-library mean or total counts may differ between
     inputs. The combined file retains the first non-missing value and reports
     the conflict. This does not alter ``X`` or ``raw.X``.

7. Raster or image-format compatibility warnings appear

   - Older SpatialData image metadata may be upgraded while producing legacy
     H5AD images. If the output passes the automatic reopen checks and the
     report contains all expected libraries and images, these warnings are
     informational rather than evidence of a failed conversion.


.. note::
   Schard is used only for the one-way H5AD-to-Seurat step. SpatialData-to-H5AD
   and H5AD-to-SpatialData conversion use the Spatialsnake/scverse conversion
   utilities. See `Schard <https://github.com/cellgeni/schard>`_ for the
   underlying Seurat reader implementation.
