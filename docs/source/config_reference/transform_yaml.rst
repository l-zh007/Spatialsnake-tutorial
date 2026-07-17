transform.yaml Reference
========================

This file configures ``spatialsnake useful_tool --option=transform``. The
utility supports ``zarr -> h5ad``, ``zarr -> seurat``, ``h5ad -> zarr``, and
``h5ad -> seurat``. Input paths remain positional command-line arguments.

.. list-table::
   :header-rows: 1
   :widths: 28 20 52

   * - Parameter
     - Default
     - Description
   * - ``output_dir``
     - ``results/useful_results``
     - Directory for the converted object and transformation report.
   * - ``transform_from``
     - ``zarr``
     - Source format: ``zarr`` or ``h5ad``.
   * - ``transform_to``
     - ``h5ad``
     - Target format: ``h5ad``, ``zarr``, or ``seurat``.
   * - ``type``
     - ``auto``
     - Data interpretation for Seurat export: ``auto``, ``st``, or ``sc``.
   * - ``seurat_matrix``
     - ``auto``
     - Matrix source for Seurat: ``auto``, ``raw``, or ``X``. Auto prefers valid Spatialsnake ``raw.X`` counts.
   * - ``table_key``
     - empty
     - SpatialData table name. An empty value requires exactly one table.
   * - ``save_image``
     - ``true``
     - Export supported downsampled legacy images; this is not a lossless image or boundary export.
   * - ``memory_limit_gb``
     - ``0``
     - Seurat memory safety limit. Zero uses 80% of available cgroup/system memory.
   * - ``keep_intermediate``
     - ``false``
     - Retain the full H5AD intermediate generated during ``zarr -> seurat``.

Matrix semantics
----------------

Spatialsnake defines ``raw.X`` as original counts. With
``seurat_matrix: "auto"``, valid non-negative integer ``raw.X`` is written to
Seurat ``counts``. If raw is unavailable, integer ``X`` becomes counts and a
non-integer, normalized ``X`` becomes a data-only assay. The converter does not
renormalize either representation. A counts export creates a counts-only
Seurat v5 assay, whereas a normalized export creates a data-only assay. Run
``NormalizeData()`` after conversion only when a counts-only object requires a
normalized data layer for downstream analysis.

Platform behavior
-----------------

Native spatial Seurat output requires complete Visium-style coordinates,
library IDs, images, and scale factors. Other spatial platforms use generic
Schard conversion and retain coordinates as a reduction. ``h5ad -> zarr``
accepts one input only; multiple sample objects should be joined with the
:doc:`../useful_tool/merge` utility. Multiple Zarr or H5AD inputs exported to
H5AD/Seurat are combined into one output named after the first input and are
distinguished by ``library_id``.

Output behavior
---------------

Every successful run writes ``<basename>.h5ad``, ``<basename>.zarr``, or
``<basename>.rds`` together with ``<basename>_transform_report.csv``. During
``zarr -> seurat``, ``keep_intermediate: true`` additionally retains the full
H5AD; the default removes conversion intermediates after RDS validation.

Large-data recommendations
--------------------------

1. Keep the default on-disk library concatenation and sparse matrices.
2. For Visium HD, use ``save_image: false`` when images are not required.
3. Keep ``memory_limit_gb: 0`` for automatic protection, or set a value that is
   known to be available to the conversion process.
4. Inspect ``<basename>_transform_report.csv`` to confirm matrix source,
   Seurat layer, library count, conversion mode, and the memory estimate.
