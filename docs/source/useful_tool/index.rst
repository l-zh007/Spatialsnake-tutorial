Utility Tools
=============

Spatial transcriptomics analysis often requires repeated data restructuring.
Samples may need to be separated before deconvolution, broad cell classes may be
split for subclustering and reannotation, and completed objects may need to be
converted for software outside the Spatialsnake workflow. Reimplementing these
operations for every project can introduce inconsistent identifiers, metadata
loss, or unnecessary duplication of spatial elements.

The ``spatialsnake useful_tool`` interface provides three reusable command-line
utilities for these tasks: ``splitting`` for observation or spatial subsetting,
``merge`` for sample concatenation or annotation overlay, and ``transform`` for
controlled format conversion. The utilities preserve the relevant object
relationships and expose explicit parameters for cases in which the default
behavior is not appropriate.

Configuration reference:

- For ``splitting``, see :doc:`../config_reference/splitting_yaml`
- For ``merge``, see :doc:`../config_reference/merge_yaml`
- For ``transform``, see :doc:`../config_reference/transform_yaml`

Typical use cases:

1. If you want to perform subcluster annotation for multiple major cell classes, you can first split the SpatialData object by ``celltype``. In this case, ``splitting`` is recommended because it provides several useful splitting modes and parameters.
2. If you need to split samples or select an ROI based on image coordinates or sample metadata, use ``splitting``.
3. If you want to interact with 10x Genomics tools such as Loupe or Xenium Explorer, you can import lasso-selected CSV files into the ``splitting`` module for ROI extraction. You can also use the CSV files generated after splitting for clearer visualization in those tools.
4. If you want to merge subcluster annotation fields back into the original large-category SpatialData object, we recommend providing the synchronized ``celltype_annotations.csv`` output together with the SpatialData object path.
5. Use ``merge_by=sample`` to concatenate independent SpatialData samples, or ``merge_by=annotation`` to write refined subset annotations back to their complete parent object. Subsets from one parent should not be treated as independent samples.
6. The ``transform`` module supports conversion among SpatialData Zarr, AnnData H5AD, and Seurat RDS outputs for analyses that require tools outside the Spatialsnake workflow.

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
