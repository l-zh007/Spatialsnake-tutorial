Module 5: Spatially Enhanced Clustering (banksy)
================================================

``banksy`` introduces spatial neighborhood weighting on top of expression features to improve clustering coherence with tissue architecture.
Here we use an annotated example dataset to demonstrate how BANKSY can reveal spatial domain structure more clearly.

For the configuration reference, see :doc:`../config_reference/advance_analysis_yaml`.

Workflow overview
-----------------

1. **Read the input and validate spatial coordinates**
   Load the input object (``.zarr`` or ``.h5ad``) and confirm that valid spatial coordinates are available. If the ``spatial`` layer is missing, the workflow attempts to reconstruct it from other coordinate fields.
2. **Build the BANKSY neighborhood graph and weighting matrix**
   Initialize the spatial neighborhood graph using the selected geometric neighbor number (``k_geom``) and weight-decay strategy, then compute neighborhood-aware features for each cell or spot.
3. **Run dimensionality reduction and spatially enhanced clustering**
   Apply PCA and UMAP to the weighted feature matrix, then perform Leiden clustering across the selected ``lambda_list`` values and resolution settings.
4. **Evaluate performance against known annotations**
   If the input already contains ``celltype`` labels, the workflow also runs a non-spatial baseline clustering and compares the two strategies using metrics such as ARI, AMI, and MCC.
5. **Export figures and summary tables**
   Write out the spatial clustering figures, metric comparison plots, ``banksy_results.csv``, and the final best-performing cluster labels.

Prepare the input files
-----------------------

Recommended ``sample.txt`` format:

.. code-block:: text

   sample_id   input_path
   Colon_Cancer_P2_008um results/Colon_Cancer_P2_008um/annotation/Colon_Cancer_P2.zarr

Input requirements:

1. The input object should contain spatial coordinates. If they are missing, the workflow attempts to reconstruct them from ``array_row`` and ``array_col``.
2. An annotated object containing ``celltype`` is recommended so that the workflow can compare the BANKSY results against known labels automatically.


Common parameters
-----------------

.. list-table::
   :header-rows: 1
   :widths: 24 24 52

   * - Parameter
     - Typical values
     - Description
   * - ``runpipe``
     - ``banksy``
     - Selects the BANKSY branch
   * - ``k_geom``
     - ``15``
     - Geometric neighbor number controlling the spatial smoothing range
   * - ``max_m``
     - ``1``
     - Neighborhood order; larger values emphasize more distant neighborhoods
   * - ``nbr_weight_decay``
     - ``scaled_gaussian``
     - Neighborhood weight-decay strategy
   * - ``n_comps``
     - ``[20]``
     - Number of principal components used for dimensionality reduction
   * - ``lambda_list``
     - ``[0.8]``
     - Spatial weighting coefficient; larger values place more emphasis on spatial structure
   * - ``RES``
     - ``[0.5]``
     - Leiden resolution values controlling cluster granularity


.. code-block:: bash

  k_geom: 15
  max_m: 1
  nbr_weight_decay: "scaled_gaussian"
  lambda_list: [0.8]

Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=banksy


Result file structure
---------------------

.. code-block:: text

   results/
   └── banksy/
       ├── {sample}_banksy.zarr/
       ├── banksy_results/
       │   ├── banksy_results.csv
       │   ├── BANKSY-Results*.png/pdf
       │   ├── BANKSY-Results-Nonspatial*.png/pdf
       │   ├── scatter.png
       │   └── bar.png
       └── *_cell_clusters.csv

How to interpret the results
----------------------------

1. BANKSY spatial clustering plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/BANKSY_scaled_gaussian_pc50_nc0.80_r0.50_full_figure.png
   :width: 85%
   :align: center
   :alt: banksy spatial clustering results

Interpretation:
This figure shows the clustering results after incorporating spatial neighborhood weighting. Each color corresponds to one spatial domain. The main purpose of this figure is to assess domain continuity, boundary sharpness, and agreement with histological structure.

2. Tissue scatter plot
~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/BANKSY-Nonspatial_nonspatial_pc50_nc0.00_r0.50_full_figure.png
   :width: 85%
   :align: center
   :alt: banksy tissue scatter

Interpretation:
This plot maps the existing ``celltype`` annotation back onto the tissue coordinates and provides a biological reference for direct comparison with the BANKSY clusters.

3. Non-spatial clustering comparison plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interpretation:
This figure shows the clustering obtained with spatial weight set to zero, that is, using expression alone. It helps illustrate how much spatial information improves boundary smoothness and noise reduction.

4. Metric comparison bar plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/bar.png
   :width: 85%
   :align: center
   :alt: banksy metrics comparison

Interpretation:
This bar plot compares the spatially enhanced and non-spatial clustering results using metrics such as ARI, AMI, and MCC. Higher values indicate better agreement between the inferred clusters and the reference cell types or expected tissue partitioning.

5. Cluster label summary table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interpretation:
This table stores the clustering labels produced under all tested parameter combinations, such as different ``lambda`` and ``resolution`` values. It is the main table for reproducibility and for comparing spatial domains at different granularities.
