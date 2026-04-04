transform.yaml Reference
========================

This configuration file corresponds to ``spatialsnake useful_tool --option=transform`` and is used for conversion among ``zarr``, ``h5ad``, and Seurat-compatible formats.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Parameter
     - Default
     - Description
   * - ``output_dir``
     - ``results/useful_results``
     - Output directory for converted files
   * - ``save_image``
     - ``True``
     - Whether to export image data when converting from ``zarr`` to ``h5ad``
   * - ``transform_from``
     - ``h5ad``
     - Input format
   * - ``transform_to``
     - ``h5ad``
     - Output format, such as ``h5ad``, ``zarr``, or ``seurat``

Tuning suggestions
------------------

1. For cross-ecosystem interoperability, keeping ``save_image=True`` is usually helpful for reproducible spatial visualization.
2. Reserve sufficient disk space before converting large objects.
3. For data sharing, exporting ``h5ad`` or ``seurat`` is often the most convenient choice for downstream collaborators.
