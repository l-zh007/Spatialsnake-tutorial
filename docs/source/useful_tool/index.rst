Utility Tools
=============

This section corresponds to the ``spatialsnake useful_tool`` command and is designed for data restructuring and format conversion outside the main workflow.

Configuration reference:

- For ``splitting``, see :doc:`../config_reference/splitting_yaml`
- For ``merge``, see :doc:`../config_reference/merge_yaml`
- For ``transform``, see :doc:`../config_reference/transform_yaml`

Typical use cases:

1. If you want to perform subcluster annotation for multiple major cell classes, you can first split the SpatialData object by ``celltype``. In this case, ``splitting`` is recommended because it provides several useful splitting modes and parameters.
2. If you need to split samples or select an ROI based on image coordinates or sample metadata, use ``splitting``.
3. If you want to interact with 10x Genomics tools such as Loupe or Xenium Explorer, you can import lasso-selected CSV files into the ``splitting`` module for ROI extraction. You can also use the CSV files generated after splitting for clearer visualization in those tools.
4. If you want to merge subcluster annotation fields back into the original large-category SpatialData object, we recommend providing the synchronized ``celltype_annotations.csv`` output together with the SpatialData object path.
5. You can also merge two subset or parallel SpatialData objects by sample columns or cluster columns, and export the result as a merged ``zarr`` object for downstream analysis.
6. Because the pipeline is implemented in Python, most tools are built around the Python ecosystem. However, many spatial transcriptomics methods are also available in the R ecosystem. The ``transform`` module therefore supports format conversion among ``zarr`` (SpatialData), ``h5ad`` (Scanpy), and ``rds`` (Seurat).

The conversion scripts support single-sample and integrated multi-sample data.
For Seurat export, ``transform`` selects only the requested expression matrix,
preserves sparse storage, estimates peak memory before starting R, and stops
when the configured safety limit would be exceeded. See :doc:`transform` for
the platform-specific fallback and large-data recommendations.

.. toctree::
   :maxdepth: 1

   splitting
   merge
   transform
